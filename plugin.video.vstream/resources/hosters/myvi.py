# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.myvi.tv/embed/xxxxxxxxx
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.util import Unquote

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'myvi', 'Myvi')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request().replace('\\u0026', '&')
        cookies = request.GetCookies()  # + ";"

        pattern = 'CreatePlayer.+?v=(.+?)&tp'

        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = Unquote(results[1][0])
        if api_call:
            return True, api_call + '|User-Agent=' + UA + \
                '&Referer=' + self._url + '&Cookie=' + cookies

        return False, False
