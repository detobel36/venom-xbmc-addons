# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'v_vids', 'V-Vids')

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = "file: '(.+?)'"

        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            return True, aResult[1][0]
        else:
            return False, False

        return False, False
