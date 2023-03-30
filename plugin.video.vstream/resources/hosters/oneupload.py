# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'oneupload', 'oneupload')

    def _getMediaLinkForGuest(self):
        api_call = ''

        oParser = Parser()
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<source src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            # + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=https://vidfast.co'
            return True, api_call

        return False, False
