# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import base64

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streammoe', 'Stream.moe')

    def _getMediaLinkForGuest(self, autoPlay=False):
        api_call = False

        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = Parser()
        sPattern = "var contents = atob\\('([^']+)'\\);"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            chain = base64.decodestring(aResult[1][0])

            sPattern = '<source src="([^"]+)"'
            aResult = oParser.parse(chain, sPattern)
            if (aResult[0]):
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
