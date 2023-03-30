# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'yourvid', 'Yourvid')

    # Extraction du lien et decodage si besoin
    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = Parser()
        sPattern = 'sources:\\s*\\["([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
