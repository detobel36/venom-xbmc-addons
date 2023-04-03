# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
# meme code frenchvid etc.. fvsio


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clickopen', 'ClickOpen')

    def _getMediaLinkForGuest(self, auto_play=False):
        url = 'https://clickopen.win/api/source/' + self._url.rsplit('/', 1)[1]

        postdata = 'r=&d=clickopen.win'

        request = RequestHandler(url)
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        # request.addHeaderEntry('Accept', '*/*')
        # request.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        # request.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # request.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        request.addHeaderEntry('Referer', self._url)
        request.addParametersLine(postdata)
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
