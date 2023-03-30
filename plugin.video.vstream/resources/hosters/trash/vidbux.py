from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbux', 'VidBux.com')

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<input name="([^"]+)".*?value=([^>]+)>'
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            oRequest = RequestHandler(self._url)
            oRequest.setRequestType(RequestHandler.REQUEST_TYPE_POST)

            for aEntry in aResult[1]:
                oRequest.addParameters(
                    str(aEntry[0]), str(aEntry[1]).replace('"', ''))

            sHtmlContent = oRequest.request()
            return self.__getUrlFromJavascriptCode(sHtmlContent)

        return self.__getUrlFromJavascriptCode(sHtmlContent)

    def __getUrlFromJavascriptCode(self, sHtmlContent):
        sPattern = "<script type='text/javascript'>eval.*?return p}\\((.*?)</script>"
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sJavascript = aResult[1][0]

            sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sPattern = ".addVariable\\('file','([^']+)'"
            oParser = Parser()
            aResultLink = oParser.parse(sUnpacked, sPattern)

            if aResultLink[0] is True:
                aResult = []
                aResult.append(True)
                aResult.append(aResultLink[1][0])
                return aResult

        return False, ''
