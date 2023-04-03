from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidload', 'VidLoad')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = 'var token="([^"]+)".+?var crsf="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            entry = results[1][0]

            request = RequestHandler('https://www.vidload.net/vid/')
            request.addParameters('gone', entry[0])
            request.addParameters('oujda', entry[1])
            request.addParameters('referer', self._url)
            request.setRequestType(RequestHandler.REQUEST_TYPE_POST)

            resolvedUrl = request.request()
            if resolvedUrl:
                resolvedUrl = resolvedUrl.replace('\r\n', '')
                return True, resolvedUrl

        return False, False
