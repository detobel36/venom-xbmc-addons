# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'wstream', 'WStream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        # VSlog(self._url)

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()

        # Dean Edwards Packer
        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            sUnpacked = cPacker().unpack(results[1][0])
            html_content = sUnpacked

        pattern = '{file:"(.+?)",label:"(.+?)"}'
        results = parser.parse(html_content, pattern)
        # print(results)

        if results[0] is True:
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in results[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # tableau
            api_call = dialog().VSselectqual(qua, url)
        # print(api_call)

        if api_call:
            return True, api_call

        return False, False
