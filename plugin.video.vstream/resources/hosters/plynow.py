# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://uqload.com/embed-xxx.html

import re
try:
    import urllib.parse as urllib
except BaseException:
    import urllib

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'plynow', 'Plynow')

    def _getMediaLinkForGuest(self, auto_play=False):
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request()

        # On récupere l'array
        pattern = '<script>\\s*\\(function\\(\\).+?=(.+?)var player'
        results = parser.parse(html_content, pattern)
        if results:
            for entry in results[1]:
                uHv4sb = entry

        # uHv4sb = re.search('<script>\s*\(function\(\).+?=(.+?);','f', re.DOTALL).group(1)

        # On récupere chaque element de l'array et ont le mets dans un tuple
        # que Python gere
        b = re.findall('"(.+?)"', str(uHv4sb))
        x = []

        for a in b:
            # Unquote decode les elements qui sont en unicode.
            x.append(urllib.unquote(a.replace('\\x', '%')))

        # On inverse le resultat et l'assemble en un string.
        result = ''.join(x)[::-1]
        hoster_url = re.findall('src="([^"]+)', result)
        hoster_url = str(hoster_url).replace(
            '[', '').replace(
            ']', '').replace(
            "'", '')
        api_call = hoster_url

        if api_call:
            return True, api_call  # + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
