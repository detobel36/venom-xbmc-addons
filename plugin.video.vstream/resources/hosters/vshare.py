# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# test sur http://vshare.eu/embed-wuqinr62cpn6-703x405.html
#          http://vshare.eu/embed-cxmr4o8l2waa-703x405.html
#          http://vshare.eu/embed-cxmr4o8l2waa703x405.html erreur code streambb
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vshare', 'Vshare')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = re.sub('-*\\d{3,4}x\\d{3,4}', '', self._url)
        self._url = self._url.replace('https', 'http')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        if '<div id="deleted">' in html_content:
            return False, False

        parser = Parser()
        pattern = '<source src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]
        else:
            pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])
                pattern = '{file:"(http.+?vid.mp4)"'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
