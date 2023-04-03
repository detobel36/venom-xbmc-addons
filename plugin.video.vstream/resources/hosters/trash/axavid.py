# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'axavid', 'Axavid')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = 'file: "([^"]+)"'

        parser = Parser()
        html_content = html_content.replace('|', '/')
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0]
            return True, api_call

        return False, False
