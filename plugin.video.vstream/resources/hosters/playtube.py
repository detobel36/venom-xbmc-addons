# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://playtube.ws/embed-xxxxx.html
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'playtube', 'Playtube')

    def _getMediaLinkForGuest(self, auto_play=False):
        request_handler = RequestHandler(self._url)
        html_content = request_handler.request()

        sPattern2 = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?\\)\\)\\))'
        results = re.findall(sPattern2, html_content)
        list_url = []
        list_qua = []
        if results:
            str2 = results[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)
            parser = Parser()
            pattern = '(https.+?.m3u8)'
            results = re.findall(pattern, strs)
            if results:
                urlhost = results[0]
                request_handler = RequestHandler(urlhost)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', self._url)
                sHtmlContent2 = request_handler.request()
                parser = Parser()
                pattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\\d+x\\d+).*?(https.*?m3u8)'
                results = parser.parse(sHtmlContent2, pattern)
                if results[0] is True:
                    for entry in results[1]:
                        list_url.append(entry[1])
                        list_qua.append(entry[0])

                    api_call = dialog().VSselectqual(list_qua, list_url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
