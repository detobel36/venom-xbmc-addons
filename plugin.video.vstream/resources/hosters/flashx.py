# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError
    from urllib2 import HTTPError as HttpError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
    from urllib.error import HTTPError as HttpError

import re

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser

# Remarque : meme code que vodlocker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def ASCIIDecode(string):
    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c = string[i]
        if string[i:(i + 2)] == '\\x':
            c = chr(int(string[(i + 2):(i + 4)], 16))
            i += 3
        if string[i:(i + 2)] == '\\u':
            cc = int(string[(i + 2):(i + 6)], 16)
            if cc > 256:
                # ok c'est de l'unicode, pas du ascii
                return ''
            c = chr(cc)
            i += 5
        ret = ret + c
        i = i + 1

    return ret


def getHtml(url, headers):
    request = urllib2.Request(url, None, headers)
    reponse = urllib2.urlopen(request)
    sCode = reponse.read()
    reponse.close()

    return sCode


def unlockUrl(url2=None):
    headers9 = {
        'User-Agent': UA,
        'Referer': 'https://www.flashx.co/dl?playthis'
    }

    url1 = 'https://www.flashx.co/js/code.js'
    if url2:
        url1 = url2

    if not url1.startswith('http'):
        url1 = 'https:' + url1

    VSlog('Test unlock url :' + url1)

    request = RequestHandler(url1)
    request.addParameters('User-Agent', UA)
    # request.addParameters('Accept', '*/*')
    # request.addParameters('Accept-Encoding', 'gzip, deflate, br')
    # request.addParameters('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addParameters('Referer', 'https://www.flashx.co/dl?playthis')
    code = request.request()

    url = ''
    if not code:
        url = request.getRealUrl()
        VSlog('Redirection :' + url)
    else:
        # VSlog(code)
        results = re.search(
            "!= null\\){\\s*\\$.get\\('([^']+)', *{(.+?)}",
            code,
            re.DOTALL)
        if results:
            dat = results.group(2)
            dat = dat.replace("'", '')
            dat = dat.replace(" ", '')

            dat2 = dict(x.split(':') for x in dat.split(','))

            dat3 = results.group(1) + '?'
            for i, j in dat2.items():
                dat3 = dat3 + str(i) + '=' + str(j) + '&'

            url = dat3[:-1]

    # url = 'https://www.flashx.tv/flashx.php?fxfx=6'

    if url:
        VSlog('Good Url :' + url1)
        VSlog(url)
        getHtml(url, headers9)
        return True

    VSlog('Bad Url :' + url1)

    return False


def loadLinks(htmlcode):
    VSlog('Scan des liens')

    host = 'https://www.flashx.tv'
    pattern = '[\\("\'](https*:)*(\\/[^,"\'\\)\\s]+)[\\)\'"]'
    results = re.findall(pattern, htmlcode, re.DOTALL)

    # VSlog(str(results))
    for http, urlspam in results:
        url = urlspam

        if http:
            url = http + url

        url = url.replace('/\\/', '//')
        url = url.replace('\\/', '/')

        # filtrage mauvaise url
        if (url.count('/') < 2) or ('<' in url) or ('>' in url) or (len(url) < 15):
            continue
        if '[' in url or ']' in url:
            continue
        if '.jpg' in url or '.png' in url:
            continue

        # VSlog('test : ' + url)

        if '\\x' in url or '\\u' in url:
            url = ASCIIDecode(url)
            if not url:
                continue

        if url.startswith('//'):
            url = 'http:' + url

        if url.startswith('/'):
            url = host + url

        # Url ou il ne faut pas aller
        if 'dok3v' in url:
            continue

        # pour test
        if ('.js' not in url) or ('.cgi' not in url):
            continue
        # if 'flashx' in url:
            # continue

        headers8 = {'User-Agent': UA,
                    'Referer': 'https://www.flashx.tv/dl?playthis'
                    }

        try:
            request = urllib2.Request(url, None, headers8)
            reponse = urllib2.urlopen(request)
            sCode = reponse.read()
            reponse.close()
            # VSlog('Worked ' + url)
        except HttpError as e:
            if not e.geturl() == url:
                try:
                    headers9 = {
                        'User-Agent': UA,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br'}
                    request = urllib2.Request(
                        e.geturl().replace(
                            'https', 'http'), None, headers9)
                    reponse = urllib2.urlopen(request)
                    sCode = reponse.read()
                    reponse.close()
                    # VSlog('Worked ' + url)
                except HttpError as e:
                    VSlog(str(e.code))
                    # VSlog(e.read())
                    VSlog('Redirection Blocked ' + url + ' Red ' + e.geturl())
            else:
                # VSlog('Blocked ' + url)
                VSlog(str(e.code))
                VSlog('>>' + e.geturl())
                VSlog(e.read())

    VSlog('fin des unlock')


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'flashx', 'FlashX')

    def getRedirectHtml(self, web_url, s_id, NoEmbed=False):
        headers = {
            # 'Host': 'www.flashx.tv',
            'User-Agent': UA,
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'http://embed.flashx.tv/embed.php?c=' + s_id,
            'Accept-Encoding': 'identity'
        }

        MaxRedirection = 3
        while MaxRedirection > 0:

            # generation headers
            # headers2 = headers
            # headers2['Host'] = self.getHost(web_url)

            VSlog(str(MaxRedirection) + ' Test sur : ' + web_url)
            request = urllib2.Request(web_url, None, headers)

            redirection_target = web_url

            try:
                # ok ca a enfin marche
                reponse = urllib2.urlopen(request)
                html_content = reponse.read()
                reponse.close()

                if reponse.geturl() != web_url and reponse.geturl() != '':
                    redirection_target = reponse.geturl()
                else:
                    break
            except UrlError as e:
                if (e.code == 301) or (e.code == 302):
                    redirection_target = e.headers['Location']
                else:
                    # VSlog(str(e.code))
                    # VSlog(str(e.read()))
                    return False

            web_url = redirection_target

            if 'embed' in redirection_target and NoEmbed:
                # rattage, on a pris la mauvaise url
                VSlog('2')
                return False

            MaxRedirection = MaxRedirection - 1

        return html_content

    def __getIdFromUrl(self, url):
        pattern = "https*:\\/\\/((?:www.|play.)?flashx.+?)\\/(?:playvid-)?(?:embed-)?(?:embed.+?=)?" + \
            "(-*[0-9a-zA-Z]+)?(?:.html)?"
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0][1]

        return ''

    def getHost(self, url):
        parser = Parser()
        pattern = 'https*:\\/\\/(.+?)\\/'
        results = parser.parse(url, pattern)
        if results[0]:
            return results[1][0]
        return ''

    def setUrl(self, url):
        self._url = 'http://' + \
            self.getHost(url) + '/embed.php?c=' + self.__getIdFromUrl(url)

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        parser = Parser()

        # on recupere le host actuel
        HOST = self.getHost(self._url)

        # on recupere l'ID
        s_id = self.__getIdFromUrl(self._url)
        if s_id == '':
            VSlog("Id prb")
            return False, False

        # on ne garde que les chiffres
        # s_id = re.sub(r'-.+', '', s_id)

        # on cherche la vraie url
        html_content = self.getRedirectHtml(self._url, s_id)

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        pattern = 'href=["\'](https*:\\/\\/www\\.flashx[^"\']+)'
        AllUrl = re.findall(pattern, html_content, re.DOTALL)
        # VSlog(str(AllUrl))

        # Disabled for the moment
        # if False:
        #     if AllUrl:
        #         # Need to find which one is the good link
        #         # Use the len don't work
        #         for i in AllUrl:
        #             if i[0] == '':
        #                 web_url = i[1]
        #     else:
        #         return False,False
        # else:
        # web_url = AllUrl[0]

        web_url = AllUrl[0]

        # Requests to unlock video
        # unlock fake video
        loadLinks(html_content)
        # unlock bubble
        unlock = False
        url2 = re.findall(
            '["\']([^"\']+?\\.js\\?cache.+?)["\']',
            html_content,
            re.DOTALL)
        if not url2:
            VSlog('No special unlock url find')
        for i in url2:
            unlock = unlockUrl(i)
            if unlock:
                break

        if not unlock:
            VSlog('No special unlock url working')
            return False, False

        # get the page
        html_content = self.getRedirectHtml(web_url, s_id, True)

        if html_content is False:
            VSlog('Passage en mode barbare')
            # ok ca a rate on passe toutes les url de AllUrl
            for i in AllUrl:
                if not i == web_url:
                    html_content = self.getRedirectHtml(i, s_id, True)
                    if html_content:
                        break

        if not html_content:
            return False, False

        if 'reload the page!' in html_content:
            # VSlog("page bloquée")

            # On recupere la bonne url
            sGoodUrl = web_url

            # on recupere la page de refresh
            pattern = 'reload the page! <a href="([^"]+)">!! <b>'
            results = re.findall(pattern, html_content)
            if not results:
                return False, False
            sRefresh = results[0]

            # on recupere le script de debloquage
            pattern = "<script type='text/javascript' src='([^']+)'><\\/script>"
            results = re.findall(pattern, html_content)
            if not results:
                return False, False

            deblockurl = results[0]
            if deblockurl.startswith('//'):
                deblockurl = 'http:' + deblockurl

            # on debloque la page
            html_content = self.getRedirectHtml(deblockurl, s_id)

            # lien speciaux ?
            if sRefresh.startswith('./'):
                sRefresh = 'http://' + self.getHost(sGoodUrl) + sRefresh[1:]

            # on rafraichit la page
            html_content = self.getRedirectHtml(sRefresh, s_id)

            # et on re-recupere la page
            html_content = self.getRedirectHtml(sGoodUrl, s_id)

        # if (False):

        #     # A t on le lien code directement?
        #     pattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        #     results = re.findall(pattern, html_content)

        #     if (results):
        #         # VSlog("lien code")

        #         AllPacked = re.findall('(eval\(function\(p,a,c,k.*?)\s+<\/script>', html_content, re.DOTALL)
        #         if AllPacked:
        #             for i in AllPacked:
        #                 sUnpacked = cPacker().unpack(i)
        #                 html_content = sUnpacked
        #                 if "file" in html_content:
        #                     break
        #         else:
        #             return False, False

        # decodage classique
        pattern = '{file:"([^",]+)",label:"([^"<>,]+)"}'
        pattern = '{src: *\'([^"\',]+)\'.+?label: *\'([^"<>,\']+)\''
        results = parser.parse(html_content, pattern)

        # VSlog(str(results))

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
            return True, api_call

        return False, False
