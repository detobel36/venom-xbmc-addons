import re
import time

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidto', 'VidTo')

    def setUrl(self, url):
        self._url = url.replace('http://vidto.me/', '')
        self._url = self._url.replace('embed-', '')
        self._url = re.sub(r'\-.*\.html', '', self._url)
        self._url = 'http://vidto.me/' + str(self._url)

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '<input type="hidden" name="([^"]+)" value="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            time.sleep(7)
            request = RequestHandler(self._url)
            request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
            for entry in results[1]:
                request.addParameters(entry[0], entry[1])

            request.addParameters('referer', self._url)
            html_content = request.request()
            html_content = html_content.replace('file:""', '')

            pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])
                pattern = ',file:"([^"]+)"}'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    return True, results[1][0]
            else:
                pattern = '{file:"([^"]+)",label:"(\\d+p)"}'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    url = []
                    qua = []
                for i in results[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                if len(url) == 1:
                    return True, url[0]

                elif len(url) > 1:
                    # 240p de nos jours serieux dialog choix inutile max vue
                    # 360p pour le moment
                    return True, url[0]

        return False, False
