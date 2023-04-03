# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidia', 'Vidia')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()
        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])
            pattern = '{file:"([^"]+)"}'
            results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0].replace(
                ',', '').replace(
                'master.m3u8', 'index-v1-a1.m3u8')

        if api_call:
            return True, api_call

        return False, False
