# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'allvid', 'Allvid')

    def _getMediaLinkForGuest(self, auto_play=False):
        # print self._url
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()

        # lien indirect
        pattern = '<iframe.+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            request = RequestHandler(results[1][0])
            html_content = request.request()

        # test pour voir si code
        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])

        pattern = 'file:"([^"]+\\.mp4)"(?:,label:"([^"]+)")*'
        results = parser.parse(html_content, pattern)

        if results[0] is True:

            # initialisation des tableaux
            url = []
            qua = []

            # Replissage des tableaux
            for i in results[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # Afichage du tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
