# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://streamz.cc/xxx
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


def getheader(url, c):
    request_handler = RequestHandler(url)
    request_handler.disableRedirect()
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Cookie', c)
    html_content = request_handler.request()
    return request_handler.getResponseHeader()['Location']


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamz', 'Streamz')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        parser = Parser()

        request = RequestHandler(self._url)
        request.addHeaderEntry('User-Agent', UA)
        html_content = request.request()

        urlDownload = request.getRealUrl()
        host = 'https://' + urlDownload.split('/')[2]

        cookie = request.GetCookies()

        # By-pass fake video
        # Get url
        urlJS = host + '/js/count.js'
        request = RequestHandler(urlJS)
        request.addHeaderEntry('User-Agent', UA)
        JScode = request.request()

        JScode = JScode.replace(' ', '')

        r = "if\\(\\$\\.adblock!=null\\){\\$\\.get\\('([^']+)',{([^}]+)}"
        results = parser.parse(JScode, r)

        if not results[0]:
            return False, False

        data = results[1][0][1].split(':')
        Fakeurl = results[1][0][0] + '?' + \
            data[0] + '=' + data[1].replace("'", "")

        # Request URL
        request = RequestHandler(Fakeurl)
        request.addHeaderEntry('User-Agent', UA)
        try:
            tmp = request.request()
        except BaseException:
            pass
        pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for i in results[1]:
                decoded = cPacker().unpack(i)

                if "videojs" in decoded:
                    decoded = decoded.replace('\\', '')

                    r = re.search("src:'([^']+)'", decoded, re.DOTALL)
                    if r:
                        url = r.group(1)

            VSlog(url)
            url = url.replace("getlink-", "getmp4-")

            api_call = getheader(url, cookie)

        VSlog(api_call)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
