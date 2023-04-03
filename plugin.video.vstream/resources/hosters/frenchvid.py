# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# french-stream /18117-la-frontire-verte-saison-1.html
# liens FVS io
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frenchvid', 'Frenchvid')

    def _getMediaLinkForGuest(self, auto_play=False):
        # Get Redirection
        if 'fembed' in self._url:
            request = RequestHandler(self._url)
            request.addHeaderEntry('User-Agent', UA)
            request.request()
            self._url = request.getRealUrl()

        if 'french-vid' in self._url:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'fembed' in self._url or "femax20" in self._url:
            baseUrl = 'https://www.diasfem.com/api/source/'
        elif 'fem.tohds' in self._url:
            baseUrl = 'https://feurl.com/api/source/'
        else:
            baseUrl = 'https://' + self._url.split('/')[2] + '/api/source/'

        if 'fem.tohds' in self._url:
            request_handler = RequestHandler(self._url)
            html_content = request_handler.request()

            pattern = '<iframe src="([^"]+)"'
            parser = Parser()
            results = parser.parse(html_content, pattern)

            url = baseUrl + results[1][0].rsplit('/', 1)[1]
            postdata = 'r=""' + '&d=' + self._url.split('/')[2]
        else:
            url = baseUrl + self._url.rsplit('/', 1)[1]
            postdata = "r=''" + "&d=" + self._url.split('/')[2]

        request = RequestHandler(url)
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', self._url)
        request.addParametersLine(postdata)
        page = request.request(json_decode=True)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])

            api_call = dialog().VSselectqual(qua, url)

            request = RequestHandler(api_call)
            request.addHeaderEntry('Host', 'fvs.io')
            request.addHeaderEntry('User-Agent', UA)
            request.request()
            api_call = request.getRealUrl()

            if api_call:
                return True, api_call + '|User-Agent=' + UA

        request_handler = RequestHandler(self._url)
        html_content = request_handler.request()
        pattern = 'var video_source = "([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results:
            return True, results[1][0] + '|User-Agent=' + UA

        return False, False
