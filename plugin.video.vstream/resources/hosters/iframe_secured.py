# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# stream elite
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.gui.hoster import HosterGui

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'iframe_secured', 'Iframe-Secured')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        # http://iframe-secured.com/embed/evovinec
        # http://iframe-secured.com/embed/iframe.php?u=evovinec
        self._url = url.replace('http://iframe-secured.com/embed/', '')
        self._url = self._url.replace('//iframe-secured.com/embed/', '')
        self._url = 'http://iframe-secured.com/embed/iframe.php?u=%s' % self._url

    def _getMediaLinkForGuest(self, auto_play=False):
        parser = Parser()
        request = RequestHandler(self._url)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry(
            'Referer', self._url.replace(
                'iframe.php?u=', ''))
        html_content = request.request()

        pattern = '<input  id=".+?name="([^"]+)" type="hidden" value="([^"]+)"/><input  id="challenge" ' + \
            'name="([^"]+)" type="hidden" value="([^"]+)"/>'

        results = parser.parse(html_content, pattern)
        if results[0] is True:
            postdata = results[1][0][0] + '=' + results[1][0][1] + \
                '&' + results[1][0][2] + '=' + results[1][0][3]

            request = RequestHandler(self._url)
            request.setRequestType(1)
            request.addHeaderEntry('User-Agent', UA)
            request.addHeaderEntry('Referer', self._url)
            request.addParametersLine(postdata)

            html_content = request.request()

            pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
            results = re.findall(pattern, html_content)

            if results:
                sUnpacked = cPacker().unpack(results[0])
                html_content = sUnpacked
                if html_content:
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
