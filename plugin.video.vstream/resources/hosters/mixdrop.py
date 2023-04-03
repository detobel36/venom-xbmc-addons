# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'mixdrop', 'Mixdrop')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace("/f/", "/e/")

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        parser = Parser()

        request = RequestHandler(self._url)
        request.addHeaderEntry('Cookie', 'hds2=1')
        html_content = request.request()

        pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])

            pattern = 'wurl="([^"]+)"'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

            if api_call.startswith('//'):
                api_call = 'https:' + results[1][0]

            if api_call:
                return True, api_call

        return False, False
