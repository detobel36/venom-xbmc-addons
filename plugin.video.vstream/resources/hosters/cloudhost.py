# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# ==>otakufr

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cloudhost', 'Cloudhost')

    def _getMediaLinkForGuest(self, auto_play=False, api_call=None):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '<source src="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0]:
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
