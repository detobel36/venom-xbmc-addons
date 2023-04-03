# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://xdrive.cc/embed/xxxxxx/blabla.mp4 >fstreamvk

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'xdrive', 'Xdrive')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = '<source src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
