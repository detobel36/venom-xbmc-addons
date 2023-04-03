# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmcgui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self, auto_play=False):
        url = []
        qua = []

        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = '"url.+?":"(.+?)\\.(\\d+).mp4'

        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:

            for entry in results[1]:
                url.append(entry[0])
                qua.append(str(entry[1]))

            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality', qua)
            # url = url[ret] + '.' + qua[ret] + '.mp4'
            api_call = ('%s.%s.mp4') % (url[ret], qua[ret])

            if api_call:
                return True, api_call

        return False, False
