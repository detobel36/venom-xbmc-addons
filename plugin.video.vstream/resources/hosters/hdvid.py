# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import Parser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hdvid', 'HdVid')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()
        parser = Parser()

        api_call = False

        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\)\\)\\s*)<\\/script>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])
            pattern = 'file:"([^"]+)",label:"[0-9]+"}'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

        else:
            pattern = 'file:"([^"]+)",label:"[0-9]+"}'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0] + '|User-Agent=' + \
                    UA  # + '&Referer=' + self._url

        if api_call:
            return True, api_call

        return False, False
