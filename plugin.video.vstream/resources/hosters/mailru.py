# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mailru', 'MailRu')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {"User-Agent": UA}

        req1 = urllib2.Request(self._url, None, headers)
        resp1 = urllib2.urlopen(req1)
        html_content = resp1.read()
        resp1.close()

        pattern = '{"metadataUrl":"([^"]+)",'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        vurl = 'http://my.mail.ru/' + results[1][0]

        req = urllib2.Request(vurl, None, headers)

        try:
            response = urllib2.urlopen(req)
        except UrlError as e:
            print(e.read())
            print(e.reason)

        data = response.read()
        head = response.headers
        response.close()

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            parser = Parser()
            pattern = '(?:^|,) *([^;,]+?)=([^;,\\/]+?);'
            results = parser.parse(str(head['Set-Cookie']), pattern)
            # print(results)
            if results[0] is True:
                for cook in results[1]:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'

        pattern = '{"url":"([^"]+)",.+?"key":"(\\d+p)"}'
        results = parser.parse(data, pattern)
        if results[0] is True:
            # initialisation des tableaux
            url = []
            qua = []
            # Remplissage des tableaux
            for i in results[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # Affichage du tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, 'http:' + api_call + '|User-Agent=' + UA + '&Cookie=' + cookies

        return False, False
