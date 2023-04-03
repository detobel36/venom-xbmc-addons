# coding: utf-8
import re
import xbmcgui

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'easyvid', 'EasyVid')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()
        if 'File was deleted' in html_content:
            return False, False

        api_call = ''

        parser = Parser()
        pattern = '{file: *"([^"]+(?<!smil))"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        else:
            pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
            results = re.findall(pattern, html_content)
            if (results):
                sUnpacked = cPacker().unpack(results[0])
                html_content = sUnpacked

                pattern = '{file:"(.+?)",label:"(.+?)"}'
                results = parser.parse(html_content, pattern)
                if results[0] is True:
                    # initialisation des tableaux
                    url = []
                    qua = []
                    # Remplissage des tableaux
                    for i in results[1]:
                        url.append(str(i[0]))
                        qua.append(str(i[1]))
                    # Si une seule url
                    if len(url) == 1:
                        api_call = url[0]
                    # si plus de une
                    elif len(url) > 1:
                        # Affichage du tableau
                        dialog2 = xbmcgui.Dialog()
                        ret = dialog2.select('Select Quality', qua)
                        if (ret > -1):
                            api_call = url[ret]

        if api_call:
            return True, api_call

        return False, False
