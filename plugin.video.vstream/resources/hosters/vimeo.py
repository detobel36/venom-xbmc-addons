# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def __getIdFromUrl(self, url):
        pattern = 'vimeo\\.com\\/(?:video\\/)?([0-9]+)'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        s_id = self.__getIdFromUrl(self._url)
        web_url = 'https://player.vimeo.com/video/' + s_id

        request = RequestHandler(web_url)
        html_content = request.request()
        pattern = ',"url":"(.+?)",.+?"quality":"(.+?)",'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in results[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # tableaux
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

            return False, False
