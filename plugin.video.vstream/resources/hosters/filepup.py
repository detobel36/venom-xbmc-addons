# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filepup', 'FilePup')

    def _getMediaLinkForGuest(self, auto_play=False):
        request_handler = RequestHandler(self._url)
        # request_handler.addParameters('login', '1')
        html_content = request_handler.request()

        parser = Parser()
        pattern = 'type: "video\\/mp4", *src: "([^<>"{}]+?)"'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            return True, results[1][0]

        return False, False
