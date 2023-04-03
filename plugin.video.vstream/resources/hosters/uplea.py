# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import xbmc

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'uplea', 'Uplea', 'violet')

    def getMediaLink(self, auto_play=False):
        if 'site=cDownload&function' not in sys.argv[2]:
            if not auto_play:
                oDialog = dialog().VSok("ATTENTION, Pas de streaming sans premium\n" +
                                        "Pour voir le film passer par l'option 'Télécharger et Lire' du menu contextuel.")
            return False, False
        return self._getMediaLinkForGuest(auto_play)

    def _getMediaLinkForGuest(self, auto_play=False):
        # http:///dl/12345XXYEEEEREERERE

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        headers = {'User-Agent': UA,
                   'Host': 'uplea.com',
                   # 'Referer': self._url ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
                   # 'Content-Type': 'application/x-www-form-urlencoded'
                   }

        req = urllib2.Request(self._url, None, headers)
        response = urllib2.urlopen(req)
        html_content = response.read()
        head = response.headers
        response.close()

        parser = Parser()

        # get step
        urlstep = ''
        pattern = '<a href="(\\/step\\/[^<>"]+)">'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            urlstep = results[1][0]

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            cookies = head['Set-Cookie']
            pattern = '(__cfduid=[0-9a-z]+;).+?(PHPSESSID=[0-9a-z]+)'
            results = parser.parse(str(cookies), pattern)
            if results[0] is True:
                cookies = str(results[1][0][0]) + str(results[1][0][1])

        url = 'http://uplea.com' + urlstep

        headers['Cookie'] = cookies
        headers['Referer'] = self._url

        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        html_content = response.read()
        head = response.headers
        response.close()

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        # waiting time
        waitingtime = 20
        pattern = "ulCounter\\({'timer':([0-9]+)}\\);"
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            waitingtime = int(results[1][0]) + 2

        pattern = '<a class="button-download" href="([^<>"]+?)">'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            dialog.VSinfo('Waiting time', self._displayName, waitingtime)
            xbmc.sleep(waitingtime * 1000)

            # print(results[1][0])

            return True, results[1][0] + '|User-Agent=' + \
                UA  # + '&Referer=' + self._url

        return False, False
