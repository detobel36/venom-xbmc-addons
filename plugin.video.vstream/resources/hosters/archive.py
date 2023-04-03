# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'archive', 'Archive')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '<source src="([^"]+.mp4)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]
            if api_call.startswith('/'):
                api_call = 'https://archive.org' + results[1][0]

        if api_call:
            return True, api_call

        return False, False
