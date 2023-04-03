# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
    'Chrome/83.0.4103.116 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ninjastream', 'NinjaStream')

    # facultatif mais a laisser pour compatibilitee
    # Extraction du lien et decodage si besoin
    def _getMediaLinkForGuest(self, auto_play=False):
        request_handler = RequestHandler(
            "https://ninjastream.to/api/video/get")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Referer', self._url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        request_handler.addHeaderEntry(
            'Origin', 'https://{0}'.format(self._url.split('/')[2]))
        request_handler.addJSONEntry('id', self._url.split('/')[4])
        html_content = request_handler.request(json_decode=True)

        api_call = html_content['result']['playlist']

        if api_call:
            # Rajout d'un header ?
            # api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) ' + \
            #    'Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False
