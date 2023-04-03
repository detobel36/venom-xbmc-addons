# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'flix555', 'Flix555')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '(\\s*eval\\s*\\(\\s*function\\(p,a,c,k,e(?:.|\\s)+?)<\\/script>'
        results = parser.parse(html_content, pattern)

        # Attention sous titre present aussi

        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])

            pattern = '{sources:\\[{file:"([^"]+)",label:"([^"]+)"'
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                api_call = results[1][0][0]

        if api_call:
            return True, api_call

        return False, False
