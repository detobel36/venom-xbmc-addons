# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

try:
    import json
except BaseException:
    import simplejson as json

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'soundcloud', 'Soundcloud')

    def _getMediaLinkForGuest(self, auto_play=False):
        url2 = ''
        VSlog(self._url)

        request = RequestHandler(self._url)
        request.addHeaderEntry('User-Agent', UA)
        html_content = request.request()

        parser = Parser()

        # Magic number
        pattern = 'soundcloud:\\/\\/sounds:([0-9]+)">'
        results = parser.parse(html_content, pattern)
        if results[0]:
            n = results[1][0]
        else:
            VSlog('err magic number')
            return False

        # First need client id
        pattern = '<script crossorigin src="([^"]+)"></script>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for i in results[1]:
                # Bon evidement la jai pris "48-" mais ca change surement
                if '48-' in i:
                    url2 = i
                    break
        else:
            VSlog('err id1')
            return False

        if not url2:
            VSlog('err url2')
            return False

        request = RequestHandler(url2)
        request.addHeaderEntry('User-Agent', UA)
        html_content = request.request()

        pattern = 'client_id:"([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            s_id = results[1][0]
        else:
            VSlog('err id2')
            return False

        # Need track
        TrackUrl = 'https://api-v2.soundcloud.com/tracks?ids=' + n + '&client_id=' + s_id
        VSlog('TrackUrl : ' + TrackUrl)
        request = RequestHandler(TrackUrl)
        request.addHeaderEntry('User-Agent', UA)
        html_content = request.request()
        pattern = 'soundcloud:tracks:([^"]+\\/)stream'
        results = parser.parse(html_content, pattern)
        if results[0]:
            sTrack = results[1][0]
        else:
            VSlog('err tracks')
            return False

        jsonurl = 'https://api-v2.soundcloud.com/media/soundcloud:tracks:' + \
            sTrack + 'stream/hls?client_id=' + s_id
        VSlog('jsonurl : ' + jsonurl)

        request = RequestHandler(jsonurl)
        request.addHeaderEntry('User-Agent', UA)
        html_content = request.request()

        # fh = open('c:\\test.txt', 'w')
        # fh.write(html_content)
        # fh.close()

        json_string = json.loads(html_content)
        api_call = json_string['url']

        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False
