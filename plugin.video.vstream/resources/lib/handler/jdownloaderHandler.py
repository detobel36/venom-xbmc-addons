# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import Addon, dialog, VSlog


class cJDownloaderHandler:
    ADDON = Addon()
    DIALOG = dialog()

    def sendToJDownloader(self, url):
        if self.__checkConfig() is False:
            VSlog('Settings ueberpruefen (XBMC)')
            return False

        if self.__checkConnection() is False:
            VSlog('Verbindung fehlgeschlagen (JD aus?)')
            return False

        bDownload = self.__download(url)
        if bDownload is True:
            self.DIALOG.VSinfo('Link gesendet', 'JDownloader')

    def __checkConfig(self):
        bEnabled = self.ADDON.getSetting('jd_enabled')
        if bEnabled == 'true':
            return True
        return False

    def __getHost(self):
        return self.ADDON.getSetting('jd_host')

    def __getPort(self):
        return self.ADDON.getSetting('jd_port')

    def __getAutomaticStart(self):
        bAutomaticStart = self.ADDON.getSetting('jd_automatic_start')
        if bAutomaticStart == 'true':
            return True
        return False

    def __getLinkGrabber(self):
        bAutomaticStart = self.ADDON.getSetting('jd_grabber')
        if bAutomaticStart == 'true':
            return True
        return False

    def __download(self, sFileUrl):
        host = self.__getHost()
        sPort = self.__getPort()
        bAutomaticDownload = self.__getAutomaticStart()
        bLinkGrabber = self.__getLinkGrabber()

        sLinkForJd = self.__createJDUrl(
            sFileUrl, host, sPort, bAutomaticDownload, bLinkGrabber)
        VSlog("JD Link " + str(sLinkForJd))

        request_handler = RequestHandler(sLinkForJd)
        request_handler.request()
        return True

    def __createJDUrl(
            self,
            sFileUrl,
            host,
            sPort,
            bAutomaticDownload,
            bLinkGrabber):
        sGrabber = '0'
        if bLinkGrabber is True:
            sGrabber = '1'

        sAutomaticStart = '0'
        if bAutomaticDownload is True:
            sAutomaticStart = '1'

        url = 'http://' + str(host) + ':' + str(sPort) + '/action/add/links/grabber' + \
            str(sGrabber) + '/start' + str(sAutomaticStart) + '/' + sFileUrl
        return url

    def __checkConnection(self):
        VSlog("check JD Connection")
        host = self.__getHost()
        sPort = self.__getPort()

        sLinkForJd = 'http://' + str(host) + ':' + str(sPort)

        try:
            request_handler = RequestHandler(sLinkForJd)
            request_handler.request()
            return True
        except Exception as e:
            return False
        return False
