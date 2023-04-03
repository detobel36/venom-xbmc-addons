# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidfast', 'Vidfast')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '{file:"([^"]+)"}'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0].replace(
                ',', '').replace(
                'master.m3u8', 'index-v1-a1.m3u8')

        if api_call:
            return True, api_call + '|User-Agent=' + UA + \
                '&Referer=' + self._url + '&Origin=https://vidfast.co'

        return False, False
