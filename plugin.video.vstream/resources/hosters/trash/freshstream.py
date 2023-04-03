# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog  # , VSlog

# import re


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'freshstream', 'Freshstream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = "var vsuri = \'(.+?)\'"
        results = parser.parse(html_content, pattern)

        if (results[0]):
            request = RequestHandler(results[1][0])
            sHtmlContent1 = request.request()

            sPattern1 = '"([^"]+)":"([^"]+)"'
            aResult1 = parser.parse(sHtmlContent1, sPattern1)

        if (aResult1[0]):

            url = []
            qua = []
            api_call = False

            for entry in aResult1[1]:
                url.append(entry[1])
                qua.append(entry[0])

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
