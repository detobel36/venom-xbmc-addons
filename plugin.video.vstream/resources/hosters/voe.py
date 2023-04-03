# coding: utf-8

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self):
        request = RequestHandler(self._url)
        html_content = request.request()

        api_call = ''

        parser = Parser()
        pattern = '"hls":\\s*"([^"]+)"'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
