# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
import re

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'netu', 'Netu')

    def setUrl(self, url):
        self._url = url.replace('https', 'http')
        self._url = self._url.replace('http://netu.tv/', 'http://hqq.tv/')
        self._url = self._url.replace('http://waaw.tv/', 'http://hqq.tv/')
        self._url = self._url.replace('http://vizplay.icu/', 'http://hqq.tv/')
        self._url = self._url.replace(
            'http://hqq.tv/player/hash.php?hash=',
            'http://hqq.tv/player/embed_player.php?vid=')
        self._url = self._url.replace(
            'http://hqq.tv/watch_video.php?v=',
            'http://hqq.tv/player/embed_player.php?vid=')

    def __getIdFromUrl(self):
        pattern = 'https*:\\/\\/hqq\\.(?:tv|player|watch)\\/player\\/embed_player\\.php\\?vid=([0-9A-Za-z]+)'
        parser = Parser()
        results = parser.parse(self._url, pattern)

        if results[0] is True:
            return results[1][0]
        return ''

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        ids = self.__getIdFromUrl()

        hqqUrl = 'http://hqq.tv/player/embed_player.php?vid=' + ids + '&autoplay=no'

        request_handler = RequestHandler(hqqUrl)
        request_handler.addHeaderEntry('User-Agent', UA)
        html = request_handler.request()

        vid = re.search("videokeyorig *= *\'(.+?)\'", html, re.DOTALL).group(1)

        url = "time=1&ver=0&secure=0&adb=0%2F&v={}&token=&gt=&embed_from=0&wasmcheck=1".format(
            vid)

        request_handler = RequestHandler(
            'https://hqq.tv/player/get_md5.php?' + url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Accept', '*/*')
        request_handler.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request_handler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        request_handler.addHeaderEntry('Referer', hqqUrl)

        request_handler.request()
        api_call = request_handler.getRealUrl()

        if api_call:
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
