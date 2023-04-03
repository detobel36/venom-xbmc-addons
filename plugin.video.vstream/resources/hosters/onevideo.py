# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.util import Unquote


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'onevideo', 'Onevideo')

    def __getIdFromUrl(self):
        pattern = "id=([^<]+)"
        parser = Parser()
        results = parser.parse(self._url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def __getKey(self):
        request_handler = RequestHandler(self._url)
        html_content = request_handler.request()
        pattern = 'key: "(.+?)";'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            results = results[1][0].replace('.', '%2E')
            return results
        return ''

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('http://www.onevideo.to/', '')
        self._url = self._url.replace('embed.php?id=', '')
        self._url = 'http://www.onevideo.to/embed.php?id=' + str(self._url)

    def _getMediaLinkForGuest(self, auto_play=False):
        # api_call = ('http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s') %
        #    (self.__getKey(), self.__getIdFromUrl())
        api_call = ('http://www.onevideo.to/api/player.api.php?user=undefined&codes=1&file=%s' +
                    '&pass=undefined&key=%s') % (self.__getIdFromUrl(), self.__getKey())

        request = RequestHandler(api_call)
        html_content = request.request()

        pattern = 'url=(.+?)&title'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            stream_url = Unquote(results[1][0])
            return True, stream_url
        else:
            return False, False

        return False, False
