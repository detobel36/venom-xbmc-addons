# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamtape', 'Streamtape')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern1 = 'ById\\(\'ideoo.+?=\\s*["\']([^"\']+)[\'"].+?["\']([^"\']+)\'\\)'

        aResult = oParser.parse(sHtmlContent, sPattern1)

        if aResult[0] is True:
            url = aResult[1][0][1]
            api_call = 'https://streamtape.com/get_video' + url[url.find('?'):] + "&stream=1"

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
