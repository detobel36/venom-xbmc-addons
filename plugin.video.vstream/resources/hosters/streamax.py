# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamax', 'Streamax')

    def __getIdFromUrl(self, url):
        pattern = 'id=([a-zA-Z0-9]+)'
        parser = Parser()
        results = parser.parse(url, pattern)

        if results[0] is True:
            return results[1][0]
        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        parser = Parser()

        urlId = self.__getIdFromUrl(self._url)

        url = 'https://streamax.club/hls/' + urlId + '/' + urlId + '.playlist.m3u8'

        url = []
        qua = []

        request = RequestHandler(url)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry(
            'Referer',
            'https://streamax.club/public/dist/index.html?id=' +
            urlId)
        html_content = request.request()

        pattern = 'RESOLUTION=(\\d+x\\d+)(.+?.m3u8)'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            for entry in results[1]:
                url.append('https://streamax.club' + entry[1])
                qua.append(entry[0])

            if url:
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
