# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.jsparser import JsParser
from resources.lib.packer import cPacker
from resources.lib.parser import Parser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'speedvid', 'Speedvid')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url.replace('sn', 'embed'))
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Host', 'www.speedvid.net')
        html_content = request.request()

        # suppression commentaires
        html_content = re.sub(r'<!--.*?-->', '', html_content)

        parser = Parser()

        # fh = open('c:\\test0.txt', "w")
        # fh.write(html_content)
        # fh.close()

        # decodage de la page html
        sHtmlContent3 = html_content
        code = ''
        maxboucle = 10
        while maxboucle > 0:
            VSlog('loop : ' + str(maxboucle))
            sHtmlContent3 = checkCpacker(sHtmlContent3)
            sHtmlContent3 = checkAADecoder(sHtmlContent3)

            maxboucle = maxboucle - 1

        html_content = sHtmlContent3

        VSlog('fini')

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        realurl = ''

        red = re.findall('location.href *= *[\'"]([^\'"]+)', html_content)
        if red:
            realurl = red[0]
        else:
            VSlog("2")
            red = re.findall(
                'location\\.assign *\\( *"([^"]+)" \\)',
                html_content)
            if red:
                realurl = red[0]

        if 'speedvid' not in realurl:
            realurl = self.__getHost() + realurl

        if not realurl.startswith('http'):
            realurl = 'http:' + realurl

        if not realurl:
            VSlog("mauvaise redirection")
            return False, False

        VSlog('Real url>> ' + realurl)

        request = RequestHandler(realurl)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', self._url)

        html_content = request.request()

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        api_call = ''

        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\)\\))<'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            for packed in results[1]:
                html_content = cPacker().unpack(packed)
                html_content = html_content.replace('\\', '')
                if "jwplayer('vplayer').setup" in html_content:
                    sPattern2 = "{file:.([^']+.mp4)"
                    aResult2 = parser.parse(html_content, sPattern2)
                    if aResult2[0] is True:
                        api_call = aResult2[1][0]
                        break

        else:
            pattern = "file\\s*:\\s*\'([^\']+.mp4)"
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

        VSlog('API_CALL: ' + api_call)

        if api_call:
            # + #'|Host=' + api_call.replace('http://','').rsplit('/', 2)[0]
            api_call = api_call + '|User-Agent=' + UA

            return True, api_call

        return False, False
# *********************************************************************************************************************


def checkCpacker(strToPack):
    pattern = '>([^>]+\\(p,a,c,k,e(?:.|\\s)+?\\)\\)\\s*)<'
    results = re.search(pattern, strToPack, re.DOTALL | re.UNICODE)
    if results:
        # VSlog('Cpacker encryption')
        str2 = results.group(1)

        if not str2.endswith(';'):
            str2 = str2 + ';'

        # if not str2.startswith('eval'):
           # str2 = 'eval(function' + str2[4:]

        # Me demandez pas pourquoi mais si je l'affiche pas en log, ca freeze ?
        # VSlog(str2)

        try:
            tmp = cPacker().unpack(str2)
            # tmp = tmp.replace("\\'", "'")
        except BaseException:
            tmp = ''

        # VSlog(tmp)

        return strToPack[:(results.start() + 1)] + tmp + \
            strToPack[(results.end() - 1):]

    return strToPack


# def checkJJDecoder(str):

#     pattern = '([a-z]=.+?\(\)\)\(\);)'
#     results = re.search(pattern, str, re.DOTALL | re.UNICODE)
#     if (results):
#         VSlog('JJ encryption')
#         tmp = JJDecoder(results.group(0)).decode()

#         return str[:results.start()] + tmp + str[results.end():]

#     return str


def checkAADecoder(stringToDecode):
    results = re.search(
        '([>;]\\s*)(ﾟωﾟ.+?\\(\'_\'\\);)',
        str,
        re.DOTALL | re.UNICODE)
    if results:
        VSlog('AA encryption')

        # tmp = results.group(1) + AADecoder(results.group(2)).decode()

        JP = JsParser()
        liste_var = []

        try:
            js_code = results.group(2)

            try:
                js_code = unicode(js_code, "utf-8")
            except Exception:
                js_code = str(js_code)

            tmp = JP.ProcessJS(js_code, liste_var)
            tmp = JP.LastEval.decode('string-escape').decode('string-escape')

            return stringToDecode[:results.start()] + \
                tmp + stringToDecode[results.end():]
        except Exception:
            return ''
    return stringToDecode
