from .pdtb import *


class pdvw(pdtb):
    """Pandas view

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
    """

    def __join_df(self, filter={}, dfs=[], applyacl=True):
        """Join multi df

        Returns:
            pd.DataFrame -- dataframe
        """
        import pandas as pd
        if self._src == []:
            return None
        df = None
        if filter != {}:
            dfs = []
        if len(dfs) != len(self._src):
            dfs = []
        srclst = self._src
        for i in range(len(self._src)):
            s = self._src[i]
            o = s.get("obj")
            name = s.get("name")
            j = [c.get("name") for c in s.get("join")]
            if dfs != []:
                tdf = dfs[i]
            else:
                tdf = o._get_df()
                self._lg.debug(f"filter: {filter}")
                tdf = o.filter(df=tdf, filter=filter)

            if applyacl:
                tdf = o._apply_acl(df=tdf)

            if isinstance(df, pd.DataFrame):
                tdf = tdf[[c.get("name") for c in o._cols()]]
                df = pd.merge(df, tdf, on=j, how="left")
            else:
                df = tdf
        return df

    def save(self):
        rtn = True
        for s in self._src:
            o = s.get("obj")
            r, _ = o.save()
            rtn = rtn and r
            if not(rtn):
                return rtn
        return True, self._get_df()

    def _load(self):
        """Load - redirect to join dataframe

        Returns:
            pd.DataFrame -- dataframe
        """
        rtn = self.__join_df()
        return rtn

    def get(self, df=None, filter={}, key=None, applyacl=None, allcols=False):
        """Get data in list of dict

        Keyword Arguments:
            filter {dict} -- filter (default: {{}})

        Returns:
            list -- list of data in {dict}
        """
        import pandas as pd
        applyacl = self._req_security(act=0, applyacl=applyacl)
        if key != None and filter == {}:
            filter = {c: key for c in self._get_cols("iskey")}
        # self._lg.debug(f"filter: {filter}")
        if isinstance(df, pd.DataFrame):
            df = df
        else:
            df = self.__join_df(filter=filter, applyacl=applyacl)
        df = self.filter(df=df, filter=filter)
        if not(allcols):
            df = df[[c.get("name") for c in self._cols()]]
        return df.to_dict("records")

    def upsert(self, data):
        df = self.__join_df()
        if self._isexists(data=data, df=df, applyacl=False):
            rtn, df = self.update(data)
        else:
            rtn, df = self.insert(data)
        return rtn, df

    def update(self, data):
        rtn = True
        xdata = {}
        for s in self._src:
            o = s.get("obj")
            name = s.get("name")
            for c in s.get("join", []):
                v_dt = data.get(c.get("name"), None)
                v = xdata.get(c.get("name"), None)
                if v_dt == None:
                    if v != None:
                        data[c.get("name")] = v
            tmp = o.get_first(
                filter=data, applyacl=False, allcols=True)
            self._lg.debug(f"update - {name} - {tmp} = {data}")
            rtn = rtn and o.update(data=data)
            xdata = self._concat_dict(xdata, o.get_first(
                filter=data, applyacl=False, allcols=True))
            if not(rtn):
                return rtn, None
        self._df = self.__join_df()
        return True, self._df

    def insert(self, data):
        rtn = True
        xdata = {}
        for s in self._src:
            o = s.get("obj")
            name = s.get("name")
            for c in s.get("join", []):
                if data.get(c.get("name"), None) == None:
                    v = xdata.get(c.get("name"), None)
                    if v != None:
                        data[c.get("name")] = v
            self._lg.debug(f"insert - {name} - {xdata} = {data}")
            rtn = rtn and o.insert(data=data)
            xdata = self._concat_dict(xdata, o.get_first(
                filter=data, applyacl=False, allcols=True))
            if not(rtn):
                return rtn, None
        self._df = self.__join_df()
        return True, self._df

    def __init__(self, model, path=None, owner=None, security=0):
        try:
            super().__init__(model=model, path=path, owner=owner, security=security)
        except:
            pass
        self._lg = comm.logger(f"pdvw({model})")
        self._lg.info("init")
        self._src = []
        for s in self._conf.get("source", []):
            spath = path if s.get("security", None) == None else None
            mod = s.get("conf")
            sec = s.get("security")
            obj = pdtb(model=mod, path=spath, owner=owner,
                       security=sec)
            if obj.acl != None and self.acl == None:
                self.acl = obj.acl
            elif obj.acl != None and self.acl != None:
                self.acl = max(obj.acl, self.acl)
            else:
                self.acl = 0
            self._src.append({"obj": obj, "name": s.get(
                "name"), "join": s.get("join", [])})
        if self._src == []:
            raise
        try:
            df = self._load()
        except Exception as e:
            self._lg.error(f"{e}")
            df = None
            pass
        import pandas as pd
        if not(isinstance(df, pd.DataFrame)):
            raise
        self._df = df
