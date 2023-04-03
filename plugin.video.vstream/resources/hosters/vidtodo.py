# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://vidtodo.com/embed-xxx.html
# http://vidtodo.com/xxx
# http://vidtodo.com/xxx.html
# com, me

import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:69.0) Gecko/20100101 Firefox/69.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidtodo', 'VidToDo')

    def setUrl(self, url):
        self._url = str(url)
        if 'embed-' in self._url:
            self._url = self._url.replace('embed-', '')
        if not self._url.startswith('https'):
            self._url = self._url.replace('http', 'https')

        if not self._url.endswith('.html'):
            self._url = self._url + '.html'

    def extractSmil(self, smil):
        request = RequestHandler(smil)
        request.addParameters('referer', self._url)
        html_content = request.request()
        Base = re.search('<meta base="(.+?)"', html_content)
        Src = re.search('<video src="(.+?)"', html_content)
        return Base.group(1) + Src.group(1)

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        parser = Parser()
        request = RequestHandler(self._url)
        request.addHeaderEntry('Referer', self._url)
        request.addParameters('User-Agent', UA)
        html_content = request.request()

        pattern = 'sources:* \\[(?:{file:)*"([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        else:
            pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])

                pattern = '{file: *"([^"]+smil)"}'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    api_call = self.extractSmil(results[1][0])
                else:
                    pattern = 'src:"([^"]+.mp4)"'
                    results = parser.parse(html_content, pattern)
                    if results[0] is True:
                        api_call = results[1][0]  # .decode('rot13')

        if api_call:
            return True, api_call

        return False, False
