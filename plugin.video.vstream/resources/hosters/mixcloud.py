# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mixcloud', 'Mixcloud')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = 'https://audiocdn.+?mixcloud.com/previews/(.+?).mp3'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = 'https://audio4.mixcloud.com/secure/hls/' + \
                results[1][0] + '.m4a/index.m3u8'

        if api_call:
            return True, api_call

        return False, False
