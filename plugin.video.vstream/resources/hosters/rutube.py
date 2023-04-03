# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import dialog
from resources.lib.util import QuotePlus


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rutube', 'RuTube')

    def setUrl(self, url):
        self._url = url
        self._url = self._url.replace('http://', '')
        self._url = self._url.replace('https://', '')
        self._url = self._url.replace('rutube.ru/video/embed/', '')
        self._url = self._url.replace('video.rutube.ru/', '')
        self._url = self._url.replace('rutube.ru/video/', '')
        self._url = self._url.replace('rutube.ru/play/embed/', '')
        self._url = 'http://rutube.ru/play/embed/' + str(self._url)

    def __getIdFromUrl(self, url):
        # au cas ou test \/play\/embed\/(\w+)(?:\?|\\?)
        pattern = "\\/play\\/embed\\/(\\w+)"
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def __getRestFromUrl(self, url):
        # pattern = "\?([\w]=[\w-]+)"
        pattern = "\\?([^ ]+)"
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        stream_url = False

        parser = Parser()

        sID = self.__getIdFromUrl(self._url)
        sRestUrl = self.__getRestFromUrl(self._url)

        api = 'http://rutube.ru/api/play/options/' + sID + \
            '/?format=json&no_404=true&referer=' + QuotePlus(self._url)
        api = api + '&' + sRestUrl

        request = RequestHandler(api)
        html_content = request.request()

        pattern = '"m3u8": *"([^"]+)"'
        results = parser.parse(html_content, pattern)

        if not results:
            pattern = '"default": *"([^"]+)"'
            results = parser.parse(html_content, pattern)

        if results[0] is True:
            url2 = results[1][0]
        else:
            return False, False

        request = RequestHandler(url2)
        html_content = request.request()

        pattern = '(http.+?\\?i=)([0-9x_]+)'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            url = []
            qua = []

            for entry in results[1]:
                url.append(entry[0] + entry[1])
                qua.append(entry[1])

            # tableau
            stream_url = dialog().VSselectqual(qua, url)

        if stream_url:
            return True, stream_url
        else:
            return False, False

        return False, False
