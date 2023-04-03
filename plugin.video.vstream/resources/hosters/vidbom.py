# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbom', 'Vidbom')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = 'sources: *\\[{file:"([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]
        else:
            pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\)\\)\\))'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])
                pattern = '{file:"([^"]+.mp4)"'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
