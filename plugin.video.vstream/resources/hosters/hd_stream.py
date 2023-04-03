# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom
# Hoster pour les liens https://hd-stream.xyz/embed/
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'hd_stream', 'HDStream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request_handler = RequestHandler(self._url)
        html_content = request_handler.request()

        parser = Parser()
        pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
        results = parser.parse(html_content, pattern)

        if results[0] is True:

            html_content = cPacker().unpack(results[1][0])
            pattern = 'file":"([^"]+)".+?"label":"([^"]+)"'
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                url = []
                qua = []

                for entry in results[1]:
                    url.append(entry[0])
                    qua.append(entry[1])

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
