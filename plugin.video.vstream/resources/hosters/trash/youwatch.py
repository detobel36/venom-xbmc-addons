# -*- coding: utf8 -*-
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youwatch', 'Youwatch')

    def __getIdFromUrl(self, url):
        pattern = "http://youwatch.org/([^<]+)"
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def setUrl(self, url):
        if 'embed' not in url:
            self._url = str(self.__getIdFromUrl(url))
            self._url = 'http://youwatch.org/embed-' + str(self._url) + '.html'
            if not re.match('[0-9]+x[0-9]+.html', self._url, re.IGNORECASE):
                self._url = self._url.replace('.html', '-640x360.html')
        else:
            self._url = url

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()

        pattern = '<iframe[^<>]+?src="(.+?)" [^<>]+?> *<\\/iframe>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            request_handler = RequestHandler(results[1][0])
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', results[1][0])
            html_content = request_handler.request()

        pattern = '\\[{file:"(.+?)",label:"(.+?)"}\\]'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            return True, results[1][0][0] + '|Referer=' + self._url

        return False, False
