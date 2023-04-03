# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://player.vimple.ru/iframe/XXXXXXXXXXXXXXXXXXXXX

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimple', 'Vimple')

    def _getMediaLinkForGuest(self, auto_play=False):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        req = urllib2.Request(self._url, None, headers)
        response = urllib2.urlopen(req)
        html_content = response.read()
        head = response.headers
        response.close()

        parser = Parser()

        cookies = ''
        if 'Set-Cookie' in head:
            pattern = '(?:^|,) *([^;,]+?)=([^;,\\/]+?);'
            results = parser.parse(str(head['Set-Cookie']), pattern)
            if results[0] is True:
                for cook in results[1]:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
        # Get link
        pattern = '"video":\\[{"default":true,"url":"([^"]+?)"}]'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            url = results[1][0]
            url = url.replace('\\/', '/')

            api_call = url + '|Cookie=' + cookies

            return True, api_call

        return False, False
