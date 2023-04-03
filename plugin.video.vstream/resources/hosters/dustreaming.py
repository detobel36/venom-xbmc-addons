# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dustreaming', 'Dustreaming')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''

        url = self._url.replace('/v/', '/api/source/')
        request = RequestHandler(url)
        request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request.addHeaderEntry('Referer', self._url)
        request.addParameters('r', '')
        request.addParameters('d', 'dustreaming.fr')
        html_content = request.request()

        page = json.loads(html_content)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])

            if url:
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
