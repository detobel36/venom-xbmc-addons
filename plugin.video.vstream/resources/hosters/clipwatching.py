# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clipwatching', 'ClipWatching')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False, api_call=None):
        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        # accelère le traitement
        html_content = parser.abParse(
            html_content, 'var holaplayer', 'vvplay')
        # Traitement pour les liens m3u8
        html_content = html_content.replace(
            ',', '').replace(
            'master.m3u8', 'index-v1-a1.m3u8')
        pattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        results = parser.parse(html_content, pattern)

        if results[0]:
            # initialisation des tableaux
            url = []
            qua = []
            n = 1

            # Remplissage des tableaux
            for i in results[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1

            # dialogue Lien si plus d'une url
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
