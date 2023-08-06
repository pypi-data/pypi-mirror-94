import gwcomm as comm


class scrape():

    def __init__(self, name=None, url=None, conf=None, *args, **kwargs):
        self._lg = comm.logger(f"scrape({name})")
        self._fullconf = conf
        self._cont = ""
        if name == None:
            return
        self._para = kwargs
        self._para["page"] = self._para.get("page", 1)
        self._conf = comm.conv_conf(conf.get(name, {}), self._para)
        self._url = self._conf.get("url", None) if url == None else url
        if self._url != None and self._url != "":
            self._lg.info(f"init - url: {self._url}")
            self._cont = self.content(url=self._url)

    def content(self, url=None):
        """Get html content

        Keyword Arguments:
            url {string} -- uri (default: {None})

        Returns:
            string -- html content
        """
        import requests
        url = self._url if url == None else url
        res = requests.get(url)
        if res.status_code == 200:
            from bs4 import BeautifulSoup
            return BeautifulSoup(res.content, features="html.parser")
        return ""

    def __extract(self, cont, conf):
        """Extract elements from content

        Arguments:
            cont {string} -- html content
            conf {dict} -- config

        Returns:
            list -- list of elements
        """
        for c in conf.get("steps", []):
            if cont != None and cont != "":
                try:
                    cont = cont.find(c.get("tag"), c.get("attr", None))
                except:
                    self._lg.debug("find_all - \ncont: {}\ntag: {}\nattr: {}".format(cont, c.get("tag"), c.get(
                        "attr", None)))
                    cont = None
        if cont == None:
            return None
        try:
            cont = cont.find_all(conf.get("tag"), conf.get(
                "attr", None))
        except:
            self._lg.debug("find_all - \ncont: {}\ntag: {}\nattr: {}".format(cont, conf.get("tag"), conf.get(
                "attr", None)))
            cont = ""
        try:
            cont = self.__getpos(
                lst=cont, pos=conf.get("pos", None), rtnlst=True)
        except:
            self._lg.debug(
                "getpos - \ncont: {}\npos: {}".format(cont, conf.get("pos", None)))
            cont = ""
        return cont

    def __getpos(self, lst, pos, rtnlst=False):
        """Get object of list with pos, return the latest object if pos > len(lst)

        Arguments:
            lst {list} -- List of object
            pos {int} -- Position

        Keyword Arguments:
            rtnlst {bool} -- Force to return value in list (default: {False})

        Returns:
            list / string -- Value of list
        """
        rtn = lst
        if pos == None:
            if not(rtnlst):
                if len(rtn) == 0:
                    rtn = ""
                else:
                    rtn = rtn[len(rtn)-1]
        elif len(lst) >= 1:
            pos = min(len(lst)-1, pos)
            rtn = rtn[pos]
            if rtnlst:
                rtn = [rtn]
        return rtn

    def __process(self, val, conf):
        """Process value

        Arguments:
            val {string} -- Value
            conf {dict} -- Config

        Returns:
            string -- Value
        """
        import re
        method = conf.get("method", None)
        if method != None:
            val = val.get(method, "")
        elif val != "":
            if conf.get("isscript", False):
                val = val.string
            else:
                val = val.text
            # self._lg.debug(f"val: {val}")
        for c in conf.get("process", []):
            for k, v in c.items():
                if k == "replace":
                    val = re.sub(v.get("fm", ""), v.get("to", ""), val)
                elif k == "split":
                    sp = val.split(v.get("delim", " "))
                    # self._lg.debug(f"val: {val}, sp: {sp}")
                    val = self.__getpos(lst=sp, pos=v.get(
                        "pos", None), rtnlst=v.get("islist", False))
                elif k == "isstrip" and v == True and isinstance(val, str):
                    val = val.strip()
        return val

    def __validate(self, val, conf):
        """Validate value

        Arguments:
            val {list} -- Value
            conf {dict} -- Config

        Returns:
            list -- list of value
        """
        for cfg in [v for v in conf if v.get("validate", []) != []]:
            vcfg = cfg.get("validate", {})
            if vcfg.get("isnumeric", False):
                val = [i for i in val if i.get(
                    cfg.get("name"), "").isnumeric()]
            elif vcfg.get("ignval", None) != None:
                val = [i for i in val if i.get(
                    cfg.get("name"), "") != vcfg.get("ignval", None)]
        return val

    def items(self, cont=None, conf=None):
        """Extract items from html content

        Keyword Arguments:
            cont {string} -- html content (default: {None})
            conf {dict} -- Config (default: {None})

        Returns:
            list -- list of items
        """
        conf = self._conf if conf == None else conf
        cont = self._cont if cont == None else cont
        cfg = conf.get("items", {})
        cont = self.__extract(cont, cfg)
        if cont == "" or cont == None:
            return []
        self._items = [self.info(value=i, conf=conf) for i in cont]
        self._items = self.__validate(
            val=self._items, conf=conf.get("info", []))
        return self._items

    def info(self, value, conf=None):
        """Extract info from items

        Arguments:
            value {string} -- Value

        Keyword Arguments:
            conf {dict} -- Config (default: {None})

        Returns:
            string -- Value
        """
        conf = self._conf if conf == None else conf
        cfg = conf.get("info", [])
        rtn = {}
        for c in cfg:
            val = self.__extract(cont=value, conf=c.get("get", {}))
            val = self.__getpos(lst=val, pos=c.get("pos", None))
            rtn[c.get("name")] = self.__process(val=val, conf=c)
        return rtn
