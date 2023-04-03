# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'prostream', 'Prostream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '<script type=\'text/javascript\'>(.+?)<\\/script>'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            html = cPacker().unpack(results[1][0])
            pattern = 'sources:\\["([^"]+)"\\]'
            results = parser.parse(html, pattern)
            if results[0] is True:
                api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
