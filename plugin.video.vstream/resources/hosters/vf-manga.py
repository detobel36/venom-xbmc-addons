# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# import base64
import codecs

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vf-manga', 'vf-manga')

    def _getMediaLinkForGuest(self):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()
        pattern = 'unescape\\("(.+?)"'
        results = parser.parse(html_content, pattern)

        if (results[0]):
            s = results[1][0].replace('%', '')
            chain = codecs.decode(s, "hex")

            pattern = '<script type="text\\/javascript">(eval\\(function\\(p,a,c,k,e,d.+?)<\\/script>'
            results = parser.parse(chain, pattern)
            if not results[0]:
                return False, False

            html_content = cPacker().unpack(results[1][0])

            pattern = '<iframe src=.+?"([^"]+)'
            results = parser.parse(html_content, pattern)

            if results[0]:
                api_call = results[1][0].replace('\\', '')

                if not api_call.startswith('http'):
                    api_call = 'https://vf-manga.cc/player/' + api_call

                request = RequestHandler(api_call)
                request.addHeaderEntry('Referer', self._url)
                html_content = request.request()
                api_call = request.getRealUrl()

        if api_call:
            return False, api_call  # redirection

        return False, False
