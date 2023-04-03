# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import re
import base64

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
# from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ddlfr', 'ddlfr')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        request = RequestHandler(self._url)
        request.addHeaderEntry('Referer', self._url)
        html_content = request.request()
        # VSlog(html_content)
        parser = Parser()
        pattern = 'JuicyCodes\\.Run\\("(.+?)"\\);'
        results = parser.parse(html_content, pattern)
        # VSlog(results)
        if results[0] is True:

            media = results[1][0].replace('+', '')
            media = base64.b64decode(media)

            # cPacker decode
            media = cPacker().unpack(media)
            # VSlog(media)
            if media:

                pattern = '{"file":"(.+?)","label":"(.+?)"'
                results = parser.parse(media, pattern)
                # VSlog(results)

                # initialisation des tableaux
                if results[0] is True:
                    url = []
                    qua = []
                # Remplissage des tableaux
                    for i in results[1]:
                        url.append(str(i[0] + '|Referer=' + self._url))
                        qua.append(str(i[1]))
                # Si une seule url
                    api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
