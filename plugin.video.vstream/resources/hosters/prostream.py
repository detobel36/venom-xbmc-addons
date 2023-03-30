# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'prostream', 'Prostream')

    def _getMediaLinkForGuest(self, autoPlay=False):
        api_call = ''

        oParser = Parser()
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<script type=\'text/javascript\'>(.+?)<\\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            html = cPacker().unpack(aResult[1][0])
            sPattern = 'sources:\\["([^"]+)"\\]'
            aResult = oParser.parse(html, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
