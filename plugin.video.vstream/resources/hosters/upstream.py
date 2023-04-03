# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upstream', 'Upstream')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        request = RequestHandler(self._url)
        request.addHeaderEntry("User-Agent", UA)
        html_content = request.request()

        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        aResult_1 = re.findall(pattern, html_content)

        if aResult_1:
            sUnpacked = cPacker().unpack(aResult_1[0])
            html_content = sUnpacked

        pattern = 'sources: *\\[\\{file:"([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0]
        elif len(aResult_1) > 1:
            sUnpacked = cPacker().unpack(aResult_1[1])
            html_content = sUnpacked
            pattern = 'sources: *\\[\\{file:"([^"]+)"'
            parser = Parser()
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

        if api_call:
            return True, api_call + '|Referer=' + self._url

        return False, False
