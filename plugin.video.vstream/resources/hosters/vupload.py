# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vupload', 'Vupload')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close

        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'

        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            html_content = cPacker().unpack(results[1][0])

        pattern = '{src:\\s*"([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
