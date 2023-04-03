# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.pstream.net/e/xxxxx
import base64
import json

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import isMatrix
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import urlEncode

try:
    # python2
    from urlparse import urlparse
except BaseException:
    # python3
    from urllib.parse import urlparse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

headers = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'pstream', 'Pstream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        request = RequestHandler(self._url)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        html_content = request.request()

        parser = Parser()
        pattern = '<script src="(.+?)"'
        results = parser.parse(html_content, pattern)[1][1]

        request = RequestHandler(results)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        html_content = request.request()

        pattern = 'atob.+?\\}\\("(.+?)"'
        code = parser.parse(html_content, pattern)

        for i in code[1]:
            try:
                if isMatrix():
                    code = base64.b64decode(i).decode('ascii')
                else:
                    code = base64.b64decode(i)
                break
            except BaseException:
                pass

        jsonCall = json.loads(code[code.rfind("{"):])

        for a in jsonCall:
            try:
                if isMatrix():
                    d = base64.b64decode(
                        jsonCall[a].split('/')[4].split('.')[0]).decode('ascii')
                else:
                    d = base64.b64decode(
                        jsonCall[a].split('/')[4].split('.')[0])
                api_call = jsonCall[a]
                break
            except BaseException:
                pass

        if api_call:
            return True, api_call + '|' + urlEncode(headers)

        return False, False
