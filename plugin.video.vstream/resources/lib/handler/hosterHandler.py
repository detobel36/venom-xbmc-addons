# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import VSlog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler


class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        VSlog("hosterhandler " + sUrl)
        oRequest = RequestHandler(sUrl)
        sContent = oRequest.request()

        aMediaLink = Parser().parse(sContent, oHoster.getPattern())
        if (aMediaLink[0]):
            return True, aMediaLink[1][0]
        return False, ''

    def getHoster(self, sHosterFileName):
        exec("from resources.hosters." + sHosterFileName + " import cHoster")

        return cHoster()
