from datetime import datetime
from requests.models import Response

import mechanicalsoup


class LazyBrowser(mechanicalsoup.StatefulBrowser):
    __slots__ = ['tabs']
    def __init__(self):
        self.tabs = {}
        super().__init__(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')

    def open(self, url, *args, timeout=60, **kwargs) -> Response:
        """translate=True necessary when url hostname is www.jw.org and ip request from AWS servers"""
        if url in self.tabs:
            try:
                header_expires = self.tabs[url].headers.get('Expires')
                dt_expires = datetime.strptime(header_expires, "%a, %d %b %Y %H:%M:%S %Z")
            except:
                return self.tabs[url]
            if header_expires and dt_expires > datetime.now():
                return self.tabs[url]


        if len(self.tabs) >= 10:
            old_tab = list(self.tabs)[0]
            self.tabs.pop(old_tab)
        kwargs = dict(timeout=timeout) | kwargs
        res = super().open(url, *args, **kwargs)
        self.tabs |= {url: res}
        return res


browser = LazyBrowser()
