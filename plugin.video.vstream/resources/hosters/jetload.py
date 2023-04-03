# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 2 methode play
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'jetload', 'Jetload')

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR skyblue]' + self._defaultDisplayName + \
            '[/COLOR]' + ' ' + '(Il faut pairer son ip au site https://jlpair.net/ tous les 3h)'

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('/e/', '/api/fetch/')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        # type 1

        pattern = '{"src":"([^"]+)","type":"video/mp4"}'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        # type 2

        # sPattern1 = 'src: *"(.+?.mp4)",'
        # aResult1 = parser.parse(html_content, sPattern1)
        # if (aResult1[0] == True):
            # return True, aResult1[1][0]

        # #type ?
        # sPattern1 = '<input type="hidden" id="file_name" value="([^"]+)">'
        # aResult1 = parser.parse(html_content, sPattern1)
        # if (aResult1[0] == True):
            # FN = aResult1[1][0]

        # pattern = '<input type="hidden" id="srv_id" value="([^"]+)">'
        # results = parser.parse(html_content, pattern)
        # if results[0] is True:
            # SRV = results[1][0]

            # pdata = 'file_name=' + FN + '.mp4&srv=' + SRV

            # request = RequestHandler('https://jetload.net/api/download')
            # request.setRequestType(1)
            # #request.addHeaderEntry('User-Agent', UA)
            # request.addHeaderEntry('Referer', self._url)
            # request.addHeaderEntry('Accept', 'application/json, text/plain, */*')
            # request.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            # request.addParametersLine(pdata)

            # api_call = request.request()

        # #type ?
        # else:
            # pattern = '<input type="hidden" id="srv" value="([^"]+)">'
            # results = parser.parse(html_content, pattern)
            # if (aResult1[0] == True):
            # Host = results[1][0]
            # api_call = Host + '/v2/schema/' + FN + '/master.m3u8'

        if api_call:
            return True, api_call

        return False, False
