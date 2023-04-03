# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://video.sibnet.ru/shell.php?videoid=xxxxxx

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sibnet', 'Sibnet')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False
        urlmain = 'https://video.sibnet.ru'
        request_handler = RequestHandler(self._url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', urlmain + '/')
        html_content = request_handler.request()

        parser = Parser()
        pattern = 'src:.+?"([^"]+)'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = urlmain + results[1][0] + '|Referer=' + self._url

        if api_call:
            return True, api_call

        return False, False
