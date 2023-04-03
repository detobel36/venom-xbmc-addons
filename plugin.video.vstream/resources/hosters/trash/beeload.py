# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.packer import cPacker
# from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'beeload', 'Beeload')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        api_call = ''

        parser = Parser()

        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        results = re.findall(pattern, html_content)

        if (results):
            sUnpacked = cPacker().unpack(results[0])
            html_content = sUnpacked

            pattern = "'([^<>']+?\\.mp4)"
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
