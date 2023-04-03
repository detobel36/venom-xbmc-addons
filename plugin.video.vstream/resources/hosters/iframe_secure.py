# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster
from resources.lib.gui.hoster import HosterGui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'iframe_secure', 'Iframe-Secure')

    def setUrl(self, url):
        self._url = url.replace('http://www.iframe-secure.com/embed/', '')
        self._url = self._url.replace('//iframe-secure.com/embed/', '')
        self._url = 'http://www.iframe-secure.com/embed/iframe.php?u=%s' % self._url

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        results = re.findall(pattern, html_content)

        if results:
            sUnpacked = cPacker().unpack(results[0])
            html_content = sUnpacked

            if html_content:

                parser = Parser()
                pattern = "replace\\(.*'(.+?)'"
                results = parser.parse(html_content, pattern)

                if results[0] is True:
                    hoster_url = results[1][0]

                    if not hoster_url.startswith('http'):
                        hoster_url = 'http:%s' % hoster_url

                    hoster_url = hoster_url.replace('\\', '')
                    hoster = HosterGui().checkHoster(hoster_url)
                    hoster.setUrl(hoster_url)
                    api_call = hoster.getMediaLink(auto_play)

                    if api_call[0] is True:
                        return True, api_call[1]

        return False, False
