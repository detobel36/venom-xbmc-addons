# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidwatch', 'VidWatch')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = 'file:"([^"]+.mp4)",label:"([0-9]+)"}'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0][0]

        if api_call:
            return True, api_call

        return False, False
