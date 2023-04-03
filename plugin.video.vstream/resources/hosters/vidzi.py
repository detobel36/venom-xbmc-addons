# -*- coding: utf-8 -*-
# https://vidzi.tv/xxx.html
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidzi', 'Vidzi')

    def setUrl(self, url):
        self._url = url.replace('http://vidzi.tv/', '')
        self._url = self._url.replace('https://vidzi.tv/', '')
        self._url = self._url.replace('embed-', '')
        self._url = re.sub(r'\-.*\.html', r'', self._url)
        self._url = self._url.replace('.html', '')
        self._url = 'https://vidzi.tv/' + str(self._url) + '.html'

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        request = RequestHandler(self._url)
        html_content = request.request()
        parser = Parser()

        # lien direct
        pattern = ',{file: *"([^"]+)"}\\]'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        # 2 test Dean Edwards Packer
        else:
            pattern = "<script type='text/javascript'>(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                sUnpacked = cPacker().unpack(results[1][0])
                pattern = 'file:"([^"]+\\.mp4)'
                results = parser.parse(sUnpacked, pattern)
                if results[0] is True:
                    api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
