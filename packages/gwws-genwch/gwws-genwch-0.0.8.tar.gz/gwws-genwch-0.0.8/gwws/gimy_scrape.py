from .scrape import *


class gimy_scrape(scrape):
    def get(self, type, lst=None, conf=None):
        """Get Gimy objects

        Arguments:1
            type {string} -- cats / subcats / medias / streams / links

        Keyword Arguments:
            lst {list} -- Filter list (default: {None})
            conf {dict} -- Config (default: {None})

        Returns:
            list -- List of dict
        """
        conf = self._fullconf if conf == None else conf
        # self._lg.debug(f"conf: {conf}")
        if type == "cats":
            return self.__get_cats(conf=conf)
        elif type == "subcats":
            try:
                if lst[0].get("cat_id", None) == None:
                    lst = None
            except:
                lst = None
            lst = self.get(type="cats", conf=conf) if lst == None else lst
            return self.__get_subcats(lst=lst, conf=conf)
        elif type == "medias":
            try:
                if lst[0].get("scat_id", None) == None:
                    lst = None
            except:
                lst = None
            lst = self.get(type="subcats", conf=conf) if lst == None else lst
            return self.__get_medias(lst=lst, conf=conf)
        elif type == "streams":
            try:
                if lst[0].get("scat_id", None) != None:
                    lst = self.get(type="medias", lst=lst,
                                   conf=conf) if lst == None else lst
                else:
                    if lst[0].get("media_id", None) == None:
                        lst = None
            except:
                lst = None
            lst = self.get(type="medias", conf=conf) if lst == None else lst
            # medias = self.__get_medias(lst=lst, conf=conf)
            return self.__get_streams(lst=lst, conf=conf)
        elif type == "links":
            try:
                if lst[0].get("media_id", None) == None:
                    lst = None
                elif lst[0].get("st", None) == None:
                    lst = None
                elif lst[0].get("ep", None) == None:
                    lst = None
            except:
                lst = None
            lst = self.get(type="streams", conf=conf) if lst == None else lst
            return self.__get_links(lst=lst, conf=conf)
        return []

    def __get_cats(self, conf=None):
        import copy
        conf = self._fullconf if conf == None else conf
        cfg = copy.deepcopy(conf)
        cat_ws = scrape(name="cat", conf=cfg)
        cats = cat_ws.items()
        del cat_ws
        return cats

    def __get_subcats(self, lst, conf=None):
        import copy
        conf = self._fullconf if conf == None else conf
        subcats = []
        for c in lst:
            cfg = copy.deepcopy(conf)
            cat_id = c.get("cat_id", "")
            subcat_ws = scrape(name="subcat", conf=cfg, cat_id=cat_id)
            t = []
            for i in subcat_ws.items():
                i["cat_id"] = cat_id
                t.append(i)
            subcats += t
            del subcat_ws
        return subcats

    def __get_medias(self, lst, conf=None):
        import copy
        conf = self._fullconf if conf == None else conf
        pages = conf.get("media", {}).get("pages", 1)
        medias = []
        for c in lst:
            scat_id = c.get("scat_id", "")
            for page in range(pages):
                cfg = copy.deepcopy(conf)
                media_ws = scrape(
                    name="media", conf=cfg, scat_id=scat_id, page=page+1)
                medias += media_ws.items()
                del media_ws
        return medias

    def split_data(self, lst, cols, keys, grp):
        """Split streams data into st / ep

        Arguments:
            lst {list} -- Source
            cols {list} -- Column list
            keys {list} -- Key list
            grp {string} -- Group

        Returns:
            list -- List of value
        """
        grp_dt = lst.get(grp, [])
        if grp_dt == []:
            grp_dt = [{k: lst.get(k) for k in cols}]
        else:
            t = []
            for i in grp_dt:
                for k in keys:
                    i[k] = lst.get(k)
                t.append(i)
            grp_dt = t
        return grp_dt

    def __get_streams(self, lst, conf=None):
        import copy
        conf = self._fullconf if conf == None else conf
        streams = []
        for c in lst:
            cfg = copy.deepcopy(conf)
            media_id = c.get("media_id", "")
            stream_ws = scrape(
                name="stream", conf=cfg, media_id=media_id)
            stream = {"media_id": media_id}
            for c in conf.get("stream", {}).get("confs", []):
                cfg = conf.get(c, {})
                t = stream_ws.items(conf=cfg)
                if len(t) == 1:
                    for i in t:
                        for k, v in i.items():
                            stream[k] = v
                elif len(t) == 0:
                    stream = {}
                    break
                else:
                    stream[c] = t
            if stream != {}:
                streams.append(stream)
            del stream_ws
        return streams

    def __get_links(self, lst, conf=None):
        import copy
        conf = self._fullconf if conf == None else conf
        links = []
        for c in lst:
            media_id = c.get("media_id")
            for e in c.get("stream_ep", []):
                st = e.get("st")
                ep = e.get("ep")
                cfg = copy.deepcopy(conf)
                link_ws = scrape(
                    name="link", conf=cfg, media_id=media_id, st=st, ep=ep)
                link = {"media_id": media_id, "st": st, "ep": ep}
                for t in link_ws.items():
                    if len(t) == 1:
                        for k, v in t.items():
                            link[k] = v
                    links.append(link)
                    break
        return links
