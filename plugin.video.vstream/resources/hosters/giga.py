# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 2 hoster giga & 2gigalink
# from resources.lib.handler.requestHandler import RequestHandler

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import ssl

from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'giga', 'Giga')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        myContext = ssl._create_unverified_context()

        req = urllib2.Request(self._url)
        handle = urllib2.urlopen(req, context=myContext)
        html_content = handle.read()
        handle.close()

        parser = Parser()
        pattern = "var mp4v = '(.+?)'"
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            return True, results[1][0]
        else:
            # streamgk
            pattern = '<a id="downloadb" class="btn btn-default.+?href="([^"]+)"'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                return True, results[1][0]

        return False, False
