# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://userload.co/embed/xxxx
import re

import requests

from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'userload', 'Userload')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        keymorocco = ''
        keymycountry = ''
        morocco = ''
        mycountry = ''

        urlapi = "https://userload.co/api/assets/userload/js/videojs.js"

        # A voir quel encodage il faut pour Kodi 18.
        sHtmlContent1 = requests.get(urlapi).content.decode('utf-8')

        parser = Parser()
        pattern = '(ﾟωﾟ.+?\\(\'_\'\\);)'
        results = parser.parse(sHtmlContent1, pattern)

        if results[0] is True:
            sdecode = AADecoder(results[1][0]).decode()

            pattern = 'morocco=".([^\\W]+).+?"&mycountry=".([^\\W]+)'
            aResult_2 = parser.parse(sdecode, pattern)

            if aResult_2[0] is True:
                keymorocco = aResult_2[1][0][0]
                keymycountry = aResult_2[1][0][1]

        referer = self._url.split('|Referer=')[1]
        url = self._url.split('|Referer=')[:-1][0]

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Referer', referer)
        sHtmlContent1 = request_handler.request()

        sPattern2 = '<script type="text/javascript">(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
        results = re.findall(sPattern2, sHtmlContent1)

        if results:
            str2 = results[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)

            parser = Parser()
            pattern = 'var\\s(.+?)="([^"]*)'
            results = parser.parse(strs, pattern)

            if results[0] is True:
                for r in results[1]:
                    if r[0] == keymorocco:
                        morocco = r[1]
                    if r[0] == keymycountry:
                        mycountry = r[1]

        if morocco and mycountry:
            url2 = 'https://userload.co/api/request/'
            pdata = 'morocco=' + morocco + '&mycountry=' + mycountry
            request = RequestHandler(url2)
            request.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request.addHeaderEntry(
                'Content-Type',
                'application/x-www-form-urlencoded')
            request.addHeaderEntry('Content-Length', len(str(pdata)))
            request.addHeaderEntry('Referer', url)
            request.addParametersLine(pdata)
            api_call = request.request()

            if 'mp4' in api_call and 'uloadcdn.com' in api_call:
                return True, api_call.strip()

        return False, False
