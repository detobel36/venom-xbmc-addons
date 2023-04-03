# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Vidcloud / vcstream.to
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidcloud', 'VidCloud')

    def __getIdFromUrl(self, url):
        # https://vcstream.to/embed/5bcf5b4c39aff/The.Spy.Who.Dumped.Me.mp4
        pattern = 'vcstream.to/embed/([^<]+)/'
        parser = Parser()
        results = parser.parse(url, pattern)
        if results[0]:
            return results[1][0]
        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        s_id = self.__getIdFromUrl(self._url)
        url = 'https://vcstream.to/player?fid=%s&page=embed' % s_id

        pattern = 'file.+?\\"([^<]+)\\"\\}'
        request = RequestHandler(url)
        html_content = request.request()

        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0]:
            api_call = results[1][0].replace('\\\\', '').replace(':\\"', '')

        if api_call:
            return True, api_call

        return False, False
