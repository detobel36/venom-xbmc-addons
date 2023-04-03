# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://gounlimited.to/embed-xxx.html
# top_replay robin des droits
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'gounlimited', 'Gounlimited')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        if not self._url.endswith('.mp4'):
            parser = Parser()
            request = RequestHandler(self._url)
            html_content = request.request()

            pattern = '(\\s*eval\\s*\\(\\s*function\\(p,a,c,k,e(?:.|\\s)+?)<\\/script>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                html_content = cPacker().unpack(results[1][0])

                pattern = '{src:"([^"]+)"'
                results = parser.parse(html_content, pattern)

                # fh = open('c:\\test.txt', 'w')
                # fh.write(html_content)
                # fh.close()

                if results[0] is True:
                    api_call = results[1][0]
        else:
            api_call = self._url

        if api_call.endswith('.mp4'):
            return True, api_call
        else:
            return True, api_call + '|User-Agent=' + UA

        return False, False
