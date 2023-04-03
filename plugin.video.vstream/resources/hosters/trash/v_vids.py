# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'v_vids', 'V-Vids')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = "file: '(.+?)'"

        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            return True, results[1][0]
        else:
            return False, False

        return False, False
