# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'facebook', 'Facebook')

    def _getMediaLinkForGuest(self, auto_play=False):
        qua = []
        url = []
        api_call = ''

        request = RequestHandler(self._url)
        html_content = request.request()
        pattern = '((?:h|s)d)_src:"([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            for entry in results[1]:
                qua.append(str(entry[0]))
                url.append(str(entry[1]))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
