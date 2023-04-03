# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'supervideo', 'SuperVideo')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        if self._url.startswith('/'):
            self._url = 'https:' + self._url

        request = RequestHandler(self._url)
        html_content = request.request()
        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])
            pattern = 'file:"([^<>"]+?\\.mp4).+?label:"([^"]+)"'
            results = parser.parse(html_content, pattern)

        if results[0] is True:
            url = []
            qua = []
            for i in results[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # Choix des qualités
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
