# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.handler.premiumHandler import cPremiumHandler

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'uploaded', 'Uploaded', 'violet')

    def getMediaLink(self, auto_play=False):
        self.premium_handler = cPremiumHandler(self.getPluginIdentifier())
        print(self.premium_handler.isPremiumModeAvailable())

        if (not self.premium_handler.isPremiumModeAvailable()):
            if not auto_play:
                oDialog = dialog().VSok('ATTENTION, Pas de streaming sans premium.')
            return False, False

        return self._getMediaLinkByPremiumUser(auto_play)

    def _getMediaLinkForGuest(self, auto_play=False):
        pass

    def _getMediaLinkByPremiumUser(self, auto_play=False):
        api_call = False

        if not self.premium_handler.Authentificate():
            return False, False

        url = self._url

        api_call = url + '|' + self.premium_handler.AddCookies()

        # print(api_call)

        if api_call:
            return True, api_call

        return False, False
