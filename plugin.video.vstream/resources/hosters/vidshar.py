# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://vidshar.net/embed-phcw5702mptz.html

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidshar', 'Vidshar')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request()

        sPattern1 = 'sources.+?src.+?"(.+?)"'

        results = parser.parse(html_content, sPattern1)
        if results[0] is True:
            api_call = results[1][0]

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
