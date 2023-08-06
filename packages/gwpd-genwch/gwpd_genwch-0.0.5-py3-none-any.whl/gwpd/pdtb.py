import gwcomm as comm


class pdtb():
    """Pandas table

    Arguments:
        model {string} -- Model

    Keyword Arguments:
        path {string} -- Model config path (default: {None})
        owner {string} -- Record owner (default: {None})
        security {int} -- Security type (default: {0})
            0 -- None
            1 -- Public
            2 -- Protected
            3 -- Private
            9 -- Auth

    Functions:
        save -- Save dataframe

    Method:
        secpath -- Security path
    """
    secpath = {0: "", 1: "public", 2: "protected", 3: "private", 9: "auth"}
    _df = None

    def _join_path(self, *args):
        """Join path

        Arguments:
            args {tuple} -- Path

        Returns:
            string -- concate path
        """
        import os
        path = args[0]
        for i in range(len(args)-1):
            if args[i+1] != "":
                path = os.path.join(path, args[i+1])
        return path

    def _load_conf(self, file):
        """Load config file

        Arguments:
            file {string} -- config file

        Returns:
            dict -- config content
        """
        import json
        with open(file, 'r') as f:
            conf = json.load(f)
        return conf

    def _get_cols(self, tag=None):
        """Get columns

        Keyword Arguments:
            tag {string} -- Column flag (default: {None})

        Returns:
            list -- column list
        """
        cols = self._conf.get("cols", []) if self._conf.get(
            "sink", {}) == {} else self._conf.get("sink", {}).get("cols", [])
        if tag == None:
            rtn = [c.get("name") for c in cols]
        else:
            rtn = [c.get("name")
                   for c in cols if c.get(tag, False)]
        return rtn

    def save(self):
        """Save dataframe

        Returns:
            bool -- True - success, False - fail
            pd.DataFrame -- Full dataframe
        """
        import pandas as pd
        path = self._conf.get("path")
        if isinstance(self._df, pd.DataFrame):
            df = self._df
        else:
            cols = self._get_cols()
            cols += [c.get("name") for c in [m for m in self._meta]]
            df = pd.DataFrame(columns=cols)
        df.to_parquet(path=path, compression='gzip')
        self._lg.info("df saved")
        return True, df

    def _load(self):
        """Load dataframe

        Returns:
            pd.DataFrame -- Full dataframe
        """
        import pandas as pd
        import os
        path = self._conf.get("path")
        if os.path.isfile(path):
            df = pd.read_parquet(path=path)
        else:
            _, df = self.save()
        self._lg.info(f"df loaded - {self._name}")
        return df

    def __remove_col(self, data, tag="iskey"):
        """Remove columns

        Arguments:
            data {dict} -- data

        Keyword Arguments:
            tag {string} -- tag (default: {"iskey"})

        Returns:
            dict -- data
        """
        cols = self._get_cols(tag)
        rtn = {k: v for k, v in data.items() if k not in cols}
        return rtn

    def __split_data_key(self, data):
        """Split data into data and key for update

        Arguments:
            data {dict} -- data

        Returns:
            dict -- data
            dict -- key
        """
        key = {k: v for k, v in data.items() if k in self._get_cols(tag="iskey")}
        data = self.__remove_col(data, tag="iskey")
        data = self.__remove_col(data, tag="ignupd")
        return data, key

    def _cols(self):
        return self._conf.get("sink", self._conf).get("cols", [])

    def __add_meta(self, data, isupd=False):
        """Add metadata to data

        Arguments:
            data {dict} -- data

        Keyword Arguments:
            isupd {bool} -- is update? (default: {False})

        Returns:
            dict -- data
        """
        conf = [{k: v for k, v in m.items()}
                for m in self._meta
                if m.get("ignupd", False) == False or isupd == False]
        if conf == []:
            return data
        for k, v in self.__default_col(data=data, conf=conf, gen=True).items():
            data[k] = v
        return data

    def __default_col(self, data, conf=None, gen=False):
        """Set default value to columns

        Arguments:
            data {dict} -- data

        Keyword Arguments:
            conf {string} -- column config (default: {None})
            gen {bool} -- apply auto gen (default: {False})

        Returns:
            dict -- data
        """
        def genrun(conf):
            pfx = conf.get("pfx", "")
            ln = conf.get("len", 1)
            try:
                tdt = self.get(applyacl=False)
                cur = len(tdt)+1
            except:
                cur = 1
            run = str(cur).zfill(ln)
            return f"{pfx}{run}"

        def genuuid():
            import uuid
            return uuid.uuid4()

        from datetime import datetime
        conf = self._conf.get("cols", []) if conf == None else conf
        now = datetime.now()
        rtn = {}
        for c in conf:
            v = data.get(c.get("name"), None)
            if v == None:
                if c.get("genuuid", False):
                    v = genuuid()
                elif c.get("genrun", False):
                    v = genrun(c.get("genrun_dtl", {}))
                elif c.get("gendtm", False):
                    v = now
                elif c.get("isowner", False):
                    v = self._owner
                else:
                    v = c.get("default", 0 if c.get(
                        "type", "str") == "int" else "")
            if c.get("type", "str") == "int":
                v = int(v)
            elif c.get("type", "str") == "uuid":
                v = str(v)
            elif c.get("type", "str") == "str":
                v = str(v)
            rtn[c.get("name")] = v
        return rtn

    def __valid(self, data, chktag=["required"]):
        """Validate columns value

        Arguments:
            data {dict} -- data

        Keyword Arguments:
            chktag {list} -- check tag (default: {["required"]})
        """
        def __chkcol(cols, tag):
            for c in self._get_cols(tag=tag):
                if c not in cols:
                    self._lg.warning(f"Missing {tag} - {c}")
                    return False
            return True
        cols = [k for k, v in data.items()]
        rtn = True
        for c in chktag:
            rtn = rtn and __chkcol(cols, c)
        return rtn

    def _concat_dict(self, fdt, ldt):
        """Concat dict

        Arguments:
            fdt {dict} -- 1st dict
            ldt {dict} -- 2nd dict

        Returns:
            dict -- data
        """
        for k, v in ldt.items():
            if k not in [k for k, v in fdt.items()]:
                fdt[k] = v
        return fdt

    def _get_df(self, df=None):
        """get default df

        Keyword Arguments:
            df {pd.DataFrame} -- dataframe (default: {None})
            applyacl {bool} -- apply acl (default: {True})

        Returns:
            pd.DataFrame -- dataframe
        """
        import pandas as pd
        if not(isinstance(df, pd.DataFrame)):
            df = self._df
        return df

    def _apply_acl(self, df=None):
        df = self._get_df(df)
        filter = {"creby": self._owner}
        return self.filter(df=df, filter=filter)

    def filter(self, df, filter):
        """Filter dataframe

        Keyword Arguments:
            filter {dict} -- filter (default: {{}})
            df {pd.DataFrame} -- dataframe (default: {None})

        Returns:
            pd.DataFrame -- dataframe
        """
        df = self._get_df(df=df)
        try:
            for k, v in filter.items():
                df = df[df[k] == v]
        except:
            pass
        return df

    def _isexists(self, data, df=None, applyacl=None):
        """check data is exists

        Arguments:
            data {dict} -- data

        Keyword Arguments:
            df {pd.DataFrame} -- dataframe (default: {None})

        Returns:
            bool -- is exists
        """
        applyacl = self._req_security(act=0, applyacl=applyacl)
        df = self._get_df(df=df)
        if applyacl:
            df = self._apply_acl(df=df)
        key = {c: data.get(c, None) for c in self._get_cols(tag="iskey")}
        df = self.filter(filter=key, df=df)
        if df.empty:
            return False
        return True

    def _req_security(self, act, applyacl=None):
        """Require security

        Arguments:
            act {int} -- 0 - read, 1 - update

        Returns:
            bool -- True - require, False - ignore
        """
        if applyacl != None:
            return applyacl
        sec = self._security
        if sec == 2:
            if act == 1:
                return True
        elif sec == 3:
            return True
        return False

    def insert(self, data):
        """Insert records

        Arguments:
            data {dict} -- data

        Returns:
            bool -- True - success, False - fail
            pd.DataFrame -- data
        """
        df = self._get_df()
        data = self.__default_col(data=data, gen=True)
        data = self.__add_meta(data=data, isupd=False)
        rtn = self.__valid(data, chktag=["required"])
        if not(rtn):
            return False, None
        if self._isexists(data=data, df=df, applyacl=False):
            self._lg.error("record exists")
            return False, None
        self._lg.debug(f"insert - {self._name} - {data}")
        df.loc[-1] = data
        df.index = df.index + 1
        df = df.sort_index()
        self._df = df
        return True, df

    def update(self, data):
        """Update

        Arguments:
            data {dict} -- data

        Returns:
            bool -- True - success, False - fail
        """
        import pandas as pd
        df = self._get_df()
        data = self.__default_col(data=data, gen=False)
        data = self.__add_meta(data=data, isupd=True)
        rtn = self.__valid(data, chktag=["required"])
        if not(rtn):
            return False, None
        if not(self._isexists(data=data, df=df, applyacl=False)):
            self._lg.error("record not exists")
            return False, None
        if self._req_security(act=1, applyacl=None):
            df = self._apply_acl(df=df)
            if not(self._isexists(data=data, df=df)):
                self._lg.error("apply sec - record not exists")
                return False, None
        data, key = self.__split_data_key(data)
        df_filt = self.filter(filter=key, df=df)
        idx = df_filt.index.tolist()
        self._lg.debug(data)
        df.update(pd.DataFrame(data, index=idx))
        return True, df

    def upsert(self, data):
        df = self._get_df()
        if self._isexists(data=data, df=df):
            rtn, df = self.update(data)
        else:
            rtn, df = self.insert(data)
        return rtn, df

    def get(self, df=None, filter={}, key=None, applyacl=None, allcols=False):
        """Get data in list of dict

        Keyword Arguments:
            filter {dict} -- filter (default: {{}})

        Returns:
            list -- list of data in {dict}
        """
        applyacl = self._req_security(act=0, applyacl=applyacl)
        df = self._get_df(df=df)
        if key != None and filter == {}:
            filter = {c: key for c in self._get_cols("iskey")}
        if filter != {}:
            df = self.filter(df=df, filter=filter)
        if applyacl:
            df = self._apply_acl(df=df)
        if not(allcols):
            df = df[[c.get("name") for c in self._cols()]]
        return df.to_dict("records")

    def get_first(self, filter={}, key=None, applyacl=None, allcols=False):
        """Get 1st data in dict

        Keyword Arguments:
            filter {dict} -- filter (default: {{}})

        Returns:
            dict -- data in {dict}
        """
        df = self.get(filter=filter, key=key,
                      applyacl=applyacl, allcols=allcols)
        if df == []:
            return {}
        return df[0]

    def __init__(self, model, path=None, owner=None, security=0):
        self._lg = comm.logger(f"pdtb({model})")
        path = "./conf/data" if path == None else path
        conffile = self._join_path(path, self.secpath[security], model+".json")
        self._conf = self._load_conf(file=conffile)
        self._name = self._conf.get("name")
        self._lg.info(f"init - {self._name}")
        self._security = security
        self._owner = owner
        self.acl = self._conf.get("acl", 0)
        self._meta = [{"name": "creby", "type": "str",
                       "isowner": True, "ignupd": True},
                      {"name": "credtm", "type": "datetime",
                       "gendtm": True, "ignupd": True},
                      {"name": "updby", "type": "str",
                       "isowner": True},
                      {"name": "upddtm", "type": "datetime",
                       "gendtm": True}]
        if self._owner == None:
            self.acl = 0
            self._meta = []
        df = self._load()
        import pandas as pd
        if not(isinstance(df, pd.DataFrame)):
            raise
        self._df = df
