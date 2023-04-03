# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'downace', 'Downace')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        # pattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        # results = parser.parse(html_content,pattern)
        # if results[0] is True:
        #    html_content = cPacker().unpack(results[1][0])

        pattern = 'controls preload="none" src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            # pas de choix qualité trouvé pour le moment
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
