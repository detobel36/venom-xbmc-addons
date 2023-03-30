# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'downace', 'Downace')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = Parser()
        # sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        # aResult = oParser.parse(sHtmlContent,sPattern)
        # if aResult[0] is True:
        #    sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = 'controls preload="none" src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            # pas de choix qualité trouvé pour le moment
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
