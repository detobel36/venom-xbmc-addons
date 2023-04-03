# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megaup', 'Megaup')

    def _getMediaLinkForGuest(self, auto_play=False):
        request_handler = RequestHandler(self._url)
        request_handler.addHeaderEntry('User-Agent', UA)
        html_content = request_handler.request()
        cookies = request_handler.GetCookies() + ";"

        data = re.search('Mhoa_URL\\((.+?)\\);', html_content).group(1)
        data = re.findall("'(.+?)'", data)

        part1 = data[0]
        part2 = data[1]
        file = data[2]
        size = data[3]

        cidken = ''
        d1p1 = part1[0:len(part1) // 4]
        cidken += d1p1[::-1]
        d1p2 = part1[len(part1) // 4 * 2:len(part1) // 4 * 3]
        cidken += d1p2[::-1]
        d2p1 = part2[3:(len(part2) + 3) // 2]
        cidken += d2p1[::-1]

        time.sleep(6)

        request_handler = RequestHandler(
            "https://download.megaup.net/?idurl=" +
            cidken +
            "&idfilename=" +
            file +
            "&idfilesize=" +
            size)
        request_handler.addHeaderEntry('User-Agent', UA)
        html_content = request_handler.request()

        la = re.search(
            'window\\.location\\.replace\\("(.+?)"',
            html_content).group(1)

        request_handler = RequestHandler(la)
        request_handler.disableRedirect()
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            "Referer", "https://download.megaup.net/")
        request_handler.addHeaderEntry("Cookie", cookies)
        request_handler.request()
        api_call = request_handler.getResponseHeader()['Location']

        if api_call:
            return True, api_call + "|User-Agent=" + UA

        return False, False
