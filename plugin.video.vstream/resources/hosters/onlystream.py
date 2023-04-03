# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'onlystream', 'OnlyStream')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        parser = Parser()
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            api_call = results[1][0][0]

        else:
            pattern = '(\\s*eval\\s*\\(\\s*function\\(p,a,c,k,e(?:.|\\s)+?)<\\/script>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])

                pattern = '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    url = []
                    qua = []
                    for i in results[1]:
                        url.append(str(i[0]))
                        if len(i) > 1:
                            q = str(i[1])
                            qua.append(q)
                        else:
                            q = "Inconnu"
                            qua.append(q)

                    api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
