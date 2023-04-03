# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Meme code que thevideo
# https://vidup.me/embed-xxx-703x405.html
# https://vidup.me/embed/xxx-703x405.html
# https://vidup.me/xxx-703x405.html
# https://vidup.io/embed/xxx
# https://vidup.io/xxx

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import json
import ssl

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vidup', 'VidUp')

    def __getIdFromUrl(self, url):
        pattern = 'https*:\\/\\/vidup.+?\\/(?:embed-)?(?:embed/)?([0-9a-zA-Z]+)'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request_headers = {"User-Agent": UA}
        req = urllib2.Request(self._url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, context=gcontext)
        self._url = response.geturl()

        response.close()

        Json_url = "https://vidup.io/api/serve/video/" + \
            self.__getIdFromUrl(self._url)

        req = urllib2.Request(Json_url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, data={}, context=gcontext)
        html_content = response.read()
        results = json.loads(html_content)

        response.close()

        if results:
            url = []
            qua = []

            for i in results['qualities']:
                url.append(results['qualities'][i])
                qua.append(str(i))

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
