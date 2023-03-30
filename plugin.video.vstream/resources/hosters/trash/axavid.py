# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'axavid', 'Axavid')

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'file: "([^"]+)"'

        oParser = Parser()
        sHtmlContent = sHtmlContent.replace('|', '/')
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
