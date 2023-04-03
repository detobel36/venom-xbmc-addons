# -*- coding: utf-8 -*-
# https://upvid.co/embed-xxx.html
# https://upvid.co/xxx.html

import base64
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
from resources.lib.comaddon import isMatrix, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upvid', 'UpVid')

    def setUrl(self, url):
        self._url = str(url)
        # lien embed obligatoire
        if 'embed-' not in self._url:
            self._url = self._url.rsplit(
                '/', 1)[0] + '/embed-' + self._url.rsplit('/', 1)[1]

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()
        url = self._url

        sPattern1 = '<iframe id="iframe" src="([^"]+)"'
        sPattern2 = '<input type="hidden" id="link" value="([^"]+)'

        referer = self._url

        # Max 3 fois
        for i in range(0, 3):

            request = RequestHandler(url)
            request.addHeaderEntry('User-Agent', UA)
            request.addHeaderEntry('Referer', referer)
            html_content = request.request()
            html_content = html_content.replace('\n', '')

            referer = url

            # ok c'est fini, on a la bonne page
            if 'ﾟωﾟﾉ' in html_content:
                break

            results = parser.parse(html_content, sPattern1)

            if results[0] is True:
                url = results[1][0]
            else:
                results = parser.parse(html_content, sPattern2)
                if results[0] is True:
                    url = results[1][0]

        results = re.search(
            'id="code".+?value="(.+?)"',
            html_content,
            re.DOTALL)

        if results:

            sFunc = base64.b64decode(results.group(1))

            results = re.search(
                '(ﾟωﾟ.+?\\(\'_\'\\);)',
                html_content,
                re.DOTALL | re.UNICODE)
            if results:
                html_content = AADecoder(results.group(1)).decode()
                if html_content:
                    results = re.search(
                        "func.innerHTML.+?\\('(.+?)',", html_content, re.DOTALL)
                    if results:
                        chars = results.group(1)
                        final = sDecode(chars, sFunc)
                        pattern = "source\\.setAttribute\\('src', '([^']+)'\\)"
                        results = parser.parse(final, pattern)
                        if results[0] is True:
                            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False


def sDecode(r, o):
    t = []
    e = []
    n = 0
    a = ""
    for f in range(256):
        e.append(f)

    for f in range(256):
        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if f not in e:
            f = 0
        t = e[f]
        e[f] = e[n]
        e[n] = t

        if isMatrix():
            a += chr(o[h] ^ e[(e[f] + e[n]) % 256])
        else:
            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
    return a
