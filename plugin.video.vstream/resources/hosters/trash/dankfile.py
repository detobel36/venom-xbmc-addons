from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dankfile', 'DankFile.com')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        return self.__getUrlFromJavascriptCode(html_content)

    def __getUrlFromJavascriptCode(self, html_content):
        pattern = "<script type='text/javascript'>eval.*?return p}\\((.*?)</script>"
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            sJavascript = results[1][0]

            sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            pattern = ".addVariable\\('file','([^']+)'"
            parser = Parser()
            aResultLink = parser.parse(sUnpacked, pattern)

            if aResultLink[0] is True:
                results = []
                results.append(True)
                results.append(aResultLink[1][0])
                return results

        return False, ''
