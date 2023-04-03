# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'azerfile', 'Azerfile')

    def setUrl(self, url):
        self._url = str(url)

        pattern = 'http://(?:www.|embed.|)azerfile.(?:com)/(?:video/|embed\\-|)?([0-9a-z]+)'

        parser = Parser()
        results = parser.parse(self._url, pattern)
        self._url = 'http://azerfile.com/' + str(results[1][0])

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        pattern = 'file=([^<]+)&image'

        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            file = results[1][0]

            liste = file.split('/')

            # api_call = ('http://azerfile.com:%s/d/%s/video.mp4') % (liste[-1], liste[-2])
            api_call = results[1][0]
            return True, api_call

        return False, False
