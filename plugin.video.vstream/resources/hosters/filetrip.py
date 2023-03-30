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

    def _getMediaLinkForGuest(self, autoPlay=False):
        # lien deja decode
        if self._url[-4] == '.':
            return True, self._url

        # Sinon on decode
        self._url = self.reformat(self._url)

        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = "file': '(.+?)',"
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            return True, aResult[1][0]

        return False, False
