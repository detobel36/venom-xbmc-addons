# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# from resources.lib.handler.requestHandler import RequestHandler

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import re

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'googledrive', 'GoogleDrive')

    def __getIdFromUrl(self, url):
        pattern = 'google.+?([a-zA-Z0-9-_]{20,40})'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        url = []
        qua = []
        api_call = ''

        # reformatage du lien
        s_id = self.__getIdFromUrl(self._url)
        url = 'https://drive.google.com/file/d/' + s_id + '/view'

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html_content = response.read()

        Headers = response.headers
        response.close()

        # listage des cookies
        c = Headers['Set-Cookie']
        c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\\/]+?);', c)
        if c2:
            cookies = ''
            for cook in c2:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'

        pattern = '\\["fmt_stream_map","([^"]+)"]'

        parser = Parser()
        results = parser.parse(html_content, pattern)
        if not results[0]:
            if '"errorcode","150"]' in html_content:
                dialog().VSinfo("Nombre de lectures max dépassé")
            return False, False

        sListUrl = results[1][0]

        if sListUrl:
            aResult2 = parser.parse(
                html_content, '([0-9]+)\\/([0-9]+x[0-9]+)\\/')

        # liste les qualitee
            r = parser.parse(sListUrl, '([0-9]+)\\|([^,]+)')
            for item in r[1]:
                url.append(item[1].decode('unicode-escape'))
                for i in aResult2[1]:
                    if item[0] == i[0]:
                        qua.append(i[1])

        # Affichage du tableau
        api_call = dialog().VSselectqual(qua, url)
        api_call = api_call + '|User-Agent=' + UA + '&Cookie=' + cookies

        if api_call:
            return True, api_call

        return False, False
