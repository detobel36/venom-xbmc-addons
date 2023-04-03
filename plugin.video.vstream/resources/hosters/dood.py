# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre pseudo
# Ne pas passer par la version de téléchargement.
# Tous les liens ne sont pas téléchargeables.
import random
import base64
import time

try:  # Python 2
    import urllib2 as urllib
except ImportError:  # Python 3
    import urllib.request as urllib

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


def compute(s):
    a = s.replace("/", "1")
    a = base64.b64decode(a)
    a = a.replace("/", "Z")
    a = base64.b64decode(a)
    a = a.replace("@", "a")
    a = base64.b64decode(a)
    return a


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        self._url = str(url).replace(
            '/d/', '/e/').replace('doodstream.com', 'dood.la')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        headers = {'User-Agent': UA}

        req = urllib.Request(self._url, None, headers)
        with urllib.urlopen(req) as response:
            html_content = response.read()
            urlDownload = response.geturl()

        try:
            html_content = html_content.decode('utf8')
        except BaseException:
            pass

        parser = Parser()

        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        fin_url = ''.join(random.choice(possible) for _ in range(10))

        pattern = 'return a\\+"(\\?token=[^"]+)"'
        results = parser.parse(html_content, pattern)

        if not results[0]:
            return False, False

        d = results[1][0]

        fin_url = fin_url + d + str(int(1000 * time.time()))

        pattern = "\\$\\.get\\('(\\/pass_md5[^']+)"
        results = parser.parse(html_content, pattern)
        url2 = 'https://' + urlDownload.split('/')[2] + results[1][0]

        headers.update({'Referer': urlDownload})

        req = urllib.Request(url2, None, headers)
        with urllib.urlopen(req) as response:
            html_content = response.read()

        try:
            html_content = html_content.decode('utf8')
        except BaseException:
            pass

        api_call = html_content + fin_url

        if api_call:
            api_call = api_call + '|Referer=' + urlDownload
            return True, api_call

        return False, False
