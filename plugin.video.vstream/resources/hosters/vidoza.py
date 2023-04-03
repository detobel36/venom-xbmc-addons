# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://vidoza.net/embed-xxx.html

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidoza', 'Vidoza')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        if 'File was deleted' in html_content:
            return False, False

        pattern = 'src: *"([^"]+)".+?label:"([^"]+)"'
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

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
