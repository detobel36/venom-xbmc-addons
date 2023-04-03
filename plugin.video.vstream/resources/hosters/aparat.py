# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://aparat.cam/embed-xxxxx.html

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'aparat', 'Aparat')

    def _getMediaLinkForGuest(self, auto_play=False):
        VideoType = 2  # dl mp4 lien existant non utilisé ici
        VideoType = 1  # m3u8

        list_q = []
        list_url = []

        if VideoType == 1:
            request_handler = RequestHandler(self._url)
            html_content = request_handler.request()

            parser = Parser()
            pattern = 'src:\\s+"([^"]+)'
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                url2 = results[1][0]
                request_handler = RequestHandler(url2)
                sHtmlContent2 = request_handler.request()

                # prend tous les formats (peu créer problèmes CODECS avc1)
                # pattern = 'RESOLUTION=(\w+).+?(https.+?m3u8)'

                # limite les formats
                pattern = 'PROGRAM-ID.+?RESOLUTION=(\\w+).+?(https.+?m3u8)'
                results = parser.parse(sHtmlContent2, pattern)
                for entry in results[1]:
                    list_q.append(entry[0])
                    # parfois lien de meme qualité avec url différentes
                    list_url.append(entry[1])

            if list_url:
                api_call = dialog().VSselectqual(list_q, list_url)
                if api_call:
                    return True, api_call

        if VideoType == 2:
            request_handler = RequestHandler(self._url)
            html_content = request_handler.request()

            parser = Parser()
            pattern = 'file_code=(\\w+)&hash=([^&]+)'
            results = parser.parse(html_content, pattern)

            if results[0] is True:
                resultId = results[1][0][0]
                resultHash = results[1][0][1]
                url = 'https://aparat.cam/dl?op=download_orig&id=' + resultId + \
                      '&mode=0&hash=' + resultHash  # + '&embed=1&adb=0'
                data = 'op=download_orig&id=' + resultId + '&mode=n&hash=' + resultHash
                request_handler = RequestHandler(url)
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry('Referer', url)
                request_handler.addParametersLine(data)
                html_content = request_handler.request()

                pattern = 'href="([^"]+.mp4)'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    api_call = results[1][0]
                    if api_call:
                        return True, api_call

        return False, False
