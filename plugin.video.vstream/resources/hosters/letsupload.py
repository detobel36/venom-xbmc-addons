# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://letsupload.co/plugins/mediaplayer/site/_embed.php?u=1r0c1&w=770&h=320
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letsupload', 'Letsupload')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = 'file: *"([^"]+)",*'

        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
