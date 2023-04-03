# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vid_ag', 'Vid.ag')

    def getUrl(self, url):
        r = re.search(
            '\\/\\/((?:www\\.)?vid\\.ag)\\/(?:embed-)?([0-9A-Za-z]+)', url)
        if r:
            return 'http://%s/embed-%s.html' % (r.groups()[0], r.groups()[1])
        else:
            return False

    def _getMediaLinkForGuest(self, auto_play=False):
        web_url = self.getUrl(self._url)
        request = RequestHandler(web_url)
        html_content = request.request()

        parser = Parser()

        # Dean Edwards Packer
        pattern = "(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?)<\\/script>"
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            sUnpacked = cPacker().unpack(results[1][0])
            html_content = sUnpacked

        pattern = 'file\\s*:\\s*"([^"]+)'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]
            return True, api_call
        else:
            return False, False

        return False, False
