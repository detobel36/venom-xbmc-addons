# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.gui.hoster import HosterGui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'allow_redirects', 'redirection')

    def _getMediaLinkForGuest(self):
        oRequestHandler = RequestHandler(self._url)
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()

        if sHosterUrl and sHosterUrl != self._url:
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setUrl(sHosterUrl)
                api_call = oHoster.getMediaLink()

                if api_call[0] is True:
                    return True, api_call[1]

        return False, False
