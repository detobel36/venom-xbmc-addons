# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import VSlog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler


class cHosterHandler:

    def getUrl(self, hoster):
        url = hoster.getUrl()
        VSlog("hosterhandler " + url)
        request = RequestHandler(url)
        content = request.request()

        aMediaLink = Parser().parse(content, hoster.getPattern())
        if aMediaLink[0]:
            return True, aMediaLink[1][0]
        return False, ''

    def getHoster(self, sHosterFileName):
        exec("from resources.hosters." + sHosterFileName + " import cHoster")

        return cHoster()
