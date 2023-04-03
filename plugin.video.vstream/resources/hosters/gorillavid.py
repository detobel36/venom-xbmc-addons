# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'gorillavid', 'Gorillavid')

    def __getIdFromUrl(self, url):
        pattern = 'http://gorillavid.in/embed.+?-([^<]+)-'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False
        parser = Parser()

        s_id = self.__getIdFromUrl(self._url)

        url = 'http://gorillavid.in/' + s_id
        request = RequestHandler(url)
        html_content = request.request()
        pattern = '<input type="hidden" name="([^"]+)" value="([^"]+)"'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
            for entry in results[1]:
                request.addParameters(entry[0], entry[1])
            request.addParameters('referer', url)
            html_content = request.request()
            r2 = re.search('file: "([^"]+)",', html_content)
            if r2:
                api_call = r2.group(1)

        if api_call:
            return True, api_call

        return False, False
