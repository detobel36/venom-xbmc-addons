# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'directmoviedl', 'DirectMovieDl')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        if 'movie.directmoviedl' in self._url:
            request = RequestHandler(self._url)
            html_content = request.request()
            parser = Parser()
            pattern = '="([^"]+)" type="video/mp4'
            results = parser.parse(html_content, pattern)
            api_call = results[1][0]
        else:
            request = RequestHandler(self._url)
            html_content = request.request()
            parser = Parser()
            pattern = 'src="(http.+?)"'
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                for entry in results[1]:
                    hoster = entry
                    request = RequestHandler(hoster)
                    sHtmlContent1 = request.request()
                    sPattern1 = '="([^"]+)" type="video/mp4'
                    aResult1 = parser.parse(sHtmlContent1, sPattern1)
                    api_call = aResult1[1][0]

        if api_call:
            return True, api_call

        return False, False
