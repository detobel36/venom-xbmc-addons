# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Wholecloud-Movshare
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'wholecloud', 'Wholecloud')

    def __getIdFromUrl(self):
        pattern = 'v=([^<]+)'
        parser = Parser()
        results = parser.parse(self._url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        s_id = self.__getIdFromUrl()

        request = RequestHandler(self._url)
        html_content = request.request()

        r = re.search('var fkzd="([^"]+)"', html_content)
        if r:
            url = 'http://www.wholecloud.net/api/player.api.php?key=' + \
                r.group(1) + '&file=' + s_id
            request = RequestHandler(url)
            html_content = request.request()
            r2 = re.search('^url=([^&]+)&', html_content)
            if r2:
                api_call = r2.group(1)

        if api_call:
            return True, api_call

        return False, False
