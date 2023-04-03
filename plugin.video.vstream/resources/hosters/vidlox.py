# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, isKrypton


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidlox', 'Vidlox')
        if not isKrypton():
            self._defaultDisplayName = '(Windows\\Android Nécessite Kodi17)' + ' Vidlox'

    def setUrl(self, url):
        url = url.replace('embed-dlox.me/', 'embed-')
        self._url = str(url)

    def _getMediaLinkForGuest(self, auto_play=False):
        parser = Parser()
        request = RequestHandler(self._url)
        request.addHeaderEntry(
            'Referer', "https://vidlox.me/8m8p7kane4r1.html")
        html_content = request.request()

        # accelère le traitement
        html_content = parser.abParse(html_content, 'var player', 'vvplay')

        pattern = '([^"]+\\.mp4)'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            # initialisation des tableaux
            url = []
            qua = ["HD", "SD"]  # sd en 2eme pos generalement quand sd
            api_call = ''

            # Remplissage des tableaux
            for i in results[1]:
                url.append(str(i))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
