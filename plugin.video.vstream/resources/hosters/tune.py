# -*- coding: utf-8 -*-
import json

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tune', 'Tune')

    def __getIdFromUrl(self, url):  # correction ancienne url >> embed depreciated
        pattern = '(?:play/|video/|embed\\?videoid=|vid=)([0-9]+)'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = ''
        url = []
        qua = []
        s_id = self.__getIdFromUrl(self._url)

        url = 'https://api.tune.pk/v3/videos/' + s_id

        request = RequestHandler(url)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('X-KEY', '777750fea4d3bd585bf47dc1873619fc')
        request.addHeaderEntry('X-REQ-APP', 'web')  # pour les mp4
        request.addHeaderEntry('Referer', self._url)  # au cas ou
        sHtmlContent1 = request.request()

        if sHtmlContent1:
            sHtmlContent1 = cUtil().removeHtmlTags(sHtmlContent1)
            html_content = cUtil().unescape(sHtmlContent1)

            content = json.loads(html_content)

            content = content["data"]["videos"]["files"]

            if content:
                for x in content:
                    if 'Auto' in str(content[x]['label']):
                        continue
                    url2 = str(
                        content[x]['file']).replace(
                        'index', str(
                            content[x]['label']))

                    url.append(url2)
                    qua.append(repr(content[x]['label']))

                api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA

            return False, False
