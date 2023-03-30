from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidload', 'VidLoad')

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'var token="([^"]+)".+?var crsf="([^"]+)"'
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            aEntry = aResult[1][0]

            oRequest = RequestHandler('https://www.vidload.net/vid/')
            oRequest.addParameters('gone', aEntry[0])
            oRequest.addParameters('oujda', aEntry[1])
            oRequest.addParameters('referer', self._url)
            oRequest.setRequestType(RequestHandler.REQUEST_TYPE_POST)

            resolvedUrl = oRequest.request()
            if resolvedUrl:
                resolvedUrl = resolvedUrl.replace('\r\n', '')
                return True, resolvedUrl

        return False, False
