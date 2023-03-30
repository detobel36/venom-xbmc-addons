# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'vimeo\\.com\\/(?:video\\/)?([0-9]+)'
        oParser = Parser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self, autoPlay=False):
        sId = self.__getIdFromUrl(self._url)
        web_url = 'https://player.vimeo.com/video/' + sId

        oRequest = RequestHandler(web_url)
        sHtmlContent = oRequest.request()
        sPattern = ',"url":"(.+?)",.+?"quality":"(.+?)",'
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # tableaux
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

            return False, False
