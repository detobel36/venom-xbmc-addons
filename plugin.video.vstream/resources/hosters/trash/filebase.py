from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filebase', 'FileBase.to')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '<form action="#" method="post">.*?id="uid" value="([^"]+)" />'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            sUid = results[1][0]

            request = RequestHandler(self._url)
            request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
            request.addParameters('dl_free12', 'DivX Stream')
            request.addParameters('uid', sUid)
            html_content = request.request()

            pattern = '<input type="hidden" id="uid" name="uid" value="([^"]+)" />'
            parser = Parser()
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                sUid = results[1][0]

                request = RequestHandler(self._url)
                request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
                request.addParameters('captcha', 'ok')
                request.addParameters('filetype', 'divx')
                request.addParameters('submit', 'Download')
                request.addParameters('uid', sUid)
                html_content = request.request()

                pattern = '<param value="([^"]+)" name="src" />'
                parser = Parser()
                results = parser.parse(html_content, pattern)

                if results[0] is True:
                    sMediaFile = results[1][0]
                    return True, sMediaFile

        return False, results
