# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
    'Chrome/83.0.4103.116 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamlare', 'Streamlare')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request_handler = RequestHandler(
            "https://sltube.org/api/video/stream/get")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Referer', self._url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addParameters('id', self._url.split('/')[4])
        html_content = request_handler.request()

        parser = Parser()
        pattern = 'label":"([^"]+).*?file":"([^"]+)'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            url = []
            qua = []
            for entry in results[1]:
                qua.append(entry[0])
                url.append(entry[1])

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
