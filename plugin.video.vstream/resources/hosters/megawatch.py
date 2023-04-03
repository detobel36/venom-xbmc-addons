# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megawatch', 'Megawatch')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()
        if 'File was deleted' in html_content:
            return False, False

        parser = Parser()
        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])

        pattern = '{file:"(http.+?mp4)"}'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            # pas de choix qualité trouvé pour le moment
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
