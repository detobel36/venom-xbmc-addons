# -*- coding: utf8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://thevideo.cc/embed-xxx.html
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui


# UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevid', 'Thevid')

    def __getIdFromhtml(self, html):
        pattern = "var thief='([^']+)';"
        parser = Parser()
        results = parser.parse(html, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()
        parser = Parser()

        api_call = ''

        s_id = self.__getIdFromhtml(html_content)
        if s_id == '':
            return False, False

        request = RequestHandler('https://thevideo.cc/vsign/player/' + s_id)
        sHtmlContent2 = request.request()
        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?\\)\\))"
        results = parser.parse(sHtmlContent2, pattern)
        if results[0] is True:
            sUnpacked = cPacker().unpack(results[1][0])
            pattern = 'vt=([^"]+)";'
            results = parser.parse(sUnpacked, pattern)
            if results[0] is True:
                sVt = results[1][0]

        pattern = '"file":"([^"]+)","label":"([^"]+)"'
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
            return True, api_call + '?direct=false&ua=1&vt=' + sVt

        return False, False
