# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filetrip', 'Filetrip')

    def reformat(self, url):
        url = url.replace('http://filetrip.net/', '')
        url = url.replace('embed?', '')
        url = 'http://filetrip.net/embed?' + str(url)
        return url

    def _getMediaLinkForGuest(self, auto_play=False):
        # lien deja decode
        if self._url[-4] == '.':
            return True, self._url

        # Sinon on decode
        self._url = self.reformat(self._url)

        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = "file': '(.+?)',"
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            return True, results[1][0]

        return False, False
