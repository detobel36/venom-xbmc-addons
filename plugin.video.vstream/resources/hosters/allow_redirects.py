# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.gui.hoster import HosterGui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'allow_redirects', 'redirection')

    def _getMediaLinkForGuest(self, auto_play=False):
        request_handler = RequestHandler(self._url)
        request_handler.request()
        hoster_url = request_handler.getRealUrl()

        if hoster_url and hoster_url != self._url:
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setUrl(hoster_url)
                api_call = hoster.getMediaLink()

                if api_call[0] is True:
                    return True, api_call[1]

        return False, False
