# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

import re

from resources.hosters.hoster import iHoster
from resources.lib.util import urlEncode


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'playreplay', 'PlayReplay')

    def __getIdFromUrl(self, url):
        pattern = 'http:..playreplay.net\\/framevideo\\/(.+?)\\?'
        results = re.findall(pattern, url)
        if results:
            return results[0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        vUrl = False
        s_id = self.__getIdFromUrl(self._url)

        query_args = {'r': '["tVL0gjqo5",["preview/flv_image",{"uid":"' +
                      s_id + '"}],' + '["preview/flv_link",{"uid":"' + s_id + '"}]]'}

        data = urlEncode(query_args)
        headers = {'User-Agent': 'Mozilla 5.10'}
        url = 'http://api.letitbit.net'
        request = urllib2.Request(url, data, headers)

        try:
            reponse = urllib2.urlopen(request)
        except UrlError as e:
            print(e.read())
            print(e.reason)

        html = reponse.read()

        html_content = html.replace('\\', '')

        link = re.findall('"link":"(.+?)"', html_content)
        if link:
            vUrl = link[0]

        # print(vUrl)

        if vUrl:
            api_call = vUrl
            return True, api_call

        return False, False
