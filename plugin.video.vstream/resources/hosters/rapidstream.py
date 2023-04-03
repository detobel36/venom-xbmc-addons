# -*- coding: utf-8 -*-
# https://rapidstream.co/embed-zxxx-635x445.html tfarjo twd

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rapidstream', 'Rapidstream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request()
        pattern = '"(http[^"]+(?:.m3u8|.mp4))"'

        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][1]

        if api_call:
            return True, api_call

        return False, False
