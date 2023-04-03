# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'turbovid', 'Turbovid.net')

    def __getIdFromUrl(self, url):
        pattern = "http://turbovid.net/([^<]+)"
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def setUrl(self, url):
        if 'embed' not in url:
            self._url = str(self.__getIdFromUrl(url))
            self._url = 'http://turbovid.net/embed-' + str(self._url) + '.html'
        else:
            self._url = url

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()
        if not html_content:
            return False, False

        pattern = 'var/type/(.+?)/.+?/provider/mp4/([^<]+)/flash/'

        parser = Parser()
        html_content = html_content.replace('|', '/')
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = (
                'http://178.33.122.207:%s/%s/v.mp4') % (results[1][0][0], results[1][0][1])
            return True, api_call

        return False, False
