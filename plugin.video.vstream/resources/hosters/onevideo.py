# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import Unquote


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'onevideo', 'Onevideo')

    def __getIdFromUrl(self):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def __getKey(self):
        oRequestHandler = RequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'key: "(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            aResult = aResult[1][0].replace('.', '%2E')
            return aResult
        return ''

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('http://www.onevideo.to/', '')
        self._url = self._url.replace('embed.php?id=', '')
        self._url = 'http://www.onevideo.to/embed.php?id=' + str(self._url)

    def _getMediaLinkForGuest(self):
        # api_call = ('http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s') %
        #    (self.__getKey(), self.__getIdFromUrl())
        api_call = ('http://www.onevideo.to/api/player.api.php?user=undefined&codes=1&file=%s' +
                    '&pass=undefined&key=%s') % (self.__getIdFromUrl(), self.__getKey())

        oRequest = RequestHandler(api_call)
        sHtmlContent = oRequest.request()

        sPattern = 'url=(.+?)&title'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            stream_url = Unquote(aResult[1][0])
            return True, stream_url
        else:
            return False, False

        return False, False
