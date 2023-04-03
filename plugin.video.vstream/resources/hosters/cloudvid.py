# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://cloudvid.co/embed-xxxx.html
# https://clipwatching.com/embed-xxx.html

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cloudvid', 'Cloudvid')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        if not self._url.endswith('.html'):
            self._url = self._url + '.html'

    def _getMediaLinkForGuest(self, auto_play=False, api_call=None):
        request = RequestHandler(self._url)
        html_content = request.request()

        if 'File was deleted' in html_content:
            return False, False

        parser = Parser()
        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            sHtmlContent2 = cPacker().unpack(results[1][0])

            pattern = '{file:"([^"]+)",label:"([^"]+)"}'
            results = parser.parse(sHtmlContent2, pattern)
            if results[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in results[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url)

            if not api_call:
                pattern = 'src:"([^"]+)"'
                results = parser.parse(sHtmlContent2, pattern)
                if results[0]:
                    api_call = results[1][0].replace(
                        ',', '').replace('.urlset', '')

        if not api_call:
            pattern = 'sources: *\\[{src: "([^"]+)", *type: "video/mp4"'
            results = parser.parse(html_content, pattern)
            if results[0]:
                api_call = results[1][0]

        if not api_call:
            pattern = 'source src="([^"]+)" type='
            results = parser.parse(html_content, pattern)
            if results[0]:
                api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
