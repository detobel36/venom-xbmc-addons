# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://mixloads.com/embed-xxx.html sur topreplay
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
import xbmcgui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mixloads', 'Mixloads')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        parser = Parser()

        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '{file:"([^"]+)",label:"([^"]+)"}'
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
                if ret > -1:
                    api_call = url[ret]

        if api_call:
            return True, api_call

        return False, False
