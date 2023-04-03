# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://www.video.tt/embed/xxx
# http://thevideo.me/embed-xxx-xxx.html

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import json
import ssl

from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"


# Meme code que vidup
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevideo_me', 'TheVideo')

    def __getIdFromUrl(self, url):
        """ URL trouvées:
            https://thevideo.me/1a2b3c4e5d6f
            https://thevideo.me/embed-1a2b3c4e5d6f.html
            http(s)://thevideo.me/embed-1a2b3c4e5d6f-816x459.html
        """
        pattern = '\\/(?:embed-)?(\\w+)(?:-\\d+x\\d+)?(?:\\.html)?$'
        results = Parser().parse(url, pattern)
        if results[0] is True:
            return results[1][0]
        return ''

    def setUrl(self, url):
        s_id = self.__getIdFromUrl(url)
        # anciens lien
        if 'video.' in url:
            self._url = 'http://thevideo.me/embed-' + s_id + '.html'
        else:
            self._url = "https://vev.io/embed/" + s_id

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False
        results = False

        request_headers = {"User-Agent": UA}

        # thevideo.me doesn't exist so take redirection
        req = urllib2.Request(self._url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, context=gcontext)
        # html_content = response.read()
        self._url = response.geturl()
        response.close()

        Json_url = 'https://vev.io/api/serve/video/' + \
            self.__getIdFromUrl(self._url)

        req = urllib2.Request(Json_url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, data={}, context=gcontext)
        html_content = response.read()
        results = json.loads(html_content)
        response.close()

        # VSlog(results['qualities'])

        if results:
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in results['qualities']:
                url.append(results['qualities'][i])
                qua.append(str(i))

            # dialog qualite
            api_call = dialog().VSselectqual(qua, url)

        # xbmc.sleep(5000)

        if api_call:
            return True, api_call

        return False, False
