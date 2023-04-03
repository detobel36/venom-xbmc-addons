# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'estream', 'Estream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        # type1
        parser = Parser()
        pattern = '<source *src="([^"]+)" *type=\'video/.+?\''
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        # type2?
        pattern = '<script type=\'text/javascript\'>(.+?)</script>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            stri = cPacker().unpack(results[1][0])
            pattern = 'file:"([^"]+)",label:"([0-9]+)"}'
            results = parser.parse(stri, pattern)
            if results[0] is True:
                url = []
                qua = []

                for entry in results[1]:
                    url.append(entry[0])
                    qua.append(entry[1][:3] + '*' + entry[1][3:])

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
