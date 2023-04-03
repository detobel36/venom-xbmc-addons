# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import base64

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.hunter import hunter
from resources.lib.comaddon import VSlog, isMatrix

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upvideo', 'UpVideo')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False
        parser = Parser()
        pattern = 'return decodeURIComponent\\(escape\\(r\\)\\)}\\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\\))]+)\\)'

        request = RequestHandler(self._url)
        request.addHeaderEntry('Cookie', 'popads2=opened')
        html_content = request.request()

        results = parser.parse(html_content, pattern)

        # Get decode page
        # request = RequestHandler("https://upvideo.to/assets/js/tabber.js")
        # request.addHeaderEntry('Referer', self._url)
        # sHtmlContent2 = request.request()
        # aResult2 = parser.parse(sHtmlContent2, pattern)

        # if (aResult2[0] == True):
        #     j = aResult2[1][0]
        #     decoder = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))
        #     VSlog("Decoder ok")

        if results[0] is True:
            l = results[1]
            for j in l:
                data = hunter(
                    j[0], int(
                        j[1]), j[2], int(
                        j[3]), int(
                        j[4]), int(
                        j[5]))
                if "fcbbbdddebad" in data:
                    r = re.search('var fcbbbdddebad *= *"([^"]+)" *;', data)
                    if not r:
                        VSlog('er2')
                    v2 = r.group(1).split('aHR0')[1].split('YTk0NT')[0]

                    if isMatrix():
                        api_call = "htt" + (base64.b64decode(v2).decode())
                    else:
                        api_call = "htt" + base64.b64decode(v2)

        if api_call:
            return True, api_call

        return False, False
