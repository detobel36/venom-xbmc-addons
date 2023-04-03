# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import Parser
from resources.lib.comaddon import xbmcgui, dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'raptu', 'Rapidvideo')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        url = self._url

        parser = Parser()
        request = RequestHandler(url)
        html_content = request.request()

        if 'rapidvideo' in url:  # qual site film illimite
            pattern = '<a href="([^"]+&q=\\d+p)"'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                url = []
                qua = []
                for i in results[1]:
                    url.append(str(i))
                    qua.append(str(i.rsplit('&q=', 1)[1]))

                if len(url) == 1:
                    pattern = '<source src="([^"]+)" type="video/.+?"'
                    results = parser.parse(html_content, pattern)
                    if results[0] is True:
                        api_call = results[1][0]

                elif len(url) > 1:
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality', qua)
                    if (ret > -1):
                        request = RequestHandler(url[ret])
                        html_content = request.request()
                        pattern = '<source src="([^"]+)" type="video/.+?"'
                        results = parser.parse(html_content, pattern)
                        if results[0] is True:
                            api_call = results[1][0]

            else:
                request = RequestHandler(url)
                html_content = request.request()
                pattern = '<source src="([^"]+)" type="video/.+?" label="([^"]+)"'
                results = parser.parse(html_content, pattern)

                url = []
                qua = []
                api_call = False

                for entry in results[1]:
                    url.append(entry[0])
                    qua.append(entry[1])

                # Affichage du tableau
                api_call = dialog().VSselectqual(qua, url)

        else:
            pattern = '{"file":"([^"]+)","label":"([^"]+)"'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                url = []
                qua = []
                for i in results[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                if len(url) == 1:
                    api_call = url[0]

                elif len(url) > 1:
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality', qua)
                    if (ret > -1):
                        api_call = url[ret]

        if api_call:
            return True, api_call

        return False, False
