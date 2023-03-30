# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmcgui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self, autoPlay=False):
        url = []
        qua = []

        oRequest = RequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '"url.+?":"(.+?)\\.(\\d+).mp4'

        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:

            for aEntry in aResult[1]:
                url.append(aEntry[0])
                qua.append(str(aEntry[1]))

            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality', qua)
            # sUrl = url[ret] + '.' + qua[ret] + '.mp4'
            api_call = ('%s.%s.mp4') % (url[ret], qua[ret])

            if api_call:
                return True, api_call

        return False, False
