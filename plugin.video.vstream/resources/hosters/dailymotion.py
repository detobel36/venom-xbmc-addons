# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dailymotion', 'DailyMotion')

    def setUrl(self, url):
        self._url = str(url)
        if "metadata" not in self._url:
            if 'embed/video' in self._url:
                self._url = "https://www.dailymotion.com/player/metadata/video/" + \
                    self._url.split('/')[5]
            else:
                self._url = "https://www.dailymotion.com/player/metadata/video/" + \
                    self._url.split('/')[4]

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False
        url = []
        qua = []

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()

        pattern = '{"type":"application.+?mpegURL","url":"([^"]+)"}'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            request = RequestHandler(results[1][0])
            request.addHeaderEntry(
                'User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) ' +
                'Gecko/20100101 Firefox/70.0')
            request.addHeaderEntry(
                'Accept-Language',
                'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            html_content = request.request()

            pattern = 'NAME="([^"]+)"(,PROGRESSIVE-URI="([^"]+)"|http(.+?)\\#)'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                for entry in reversed(results[1]):
                    quality = entry[0].replace('@60', '')
                    if quality not in qua:
                        qua.append(quality)
                        link = entry[2] if entry[2] else 'http' + entry[3]
                        url.append(link)

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
