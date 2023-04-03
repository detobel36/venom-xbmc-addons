# coding: utf-8
import re

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'verystream', 'VeryStream')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        api_call = ''

        pattern = 'id="videolink">([^<>]+)<\\/p>'
        results = re.findall(pattern, html_content)

        if results:

            api_call = 'https://verystream.com/gettoken/' + \
                results[0] + '?mime=true'

        if api_call:
            return True, api_call

        return False, False
