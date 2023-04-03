# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
# Ne marche pas, ne marchera que sous kodi V17
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.gui.gui import Gui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

# import ssl,urllib2
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rapidvideo', 'RapidVideo')

    def _getMediaLinkForGuest(self, auto_play=False):
        # VSlog(self._url)
        api_call = False

        request = RequestHandler(self._url)
        # request.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) ' + \
        #   'Gecko/20100101 Firefox/49.0')
        # request.addHeaderEntry('Upgrade-Insecure-Requests','1')
        # request.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        # request.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        html_content = request.request()

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        parser = Parser()
        pattern = '"file":"([^"]+)","label":"([0-9]+)p"'
        results = parser.parse(html_content, pattern)

        if (results[0]):
            url = []
            qua = []

            for entry in results[1]:
                url.append(entry[0])
                qua.append(entry[1])

            # tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
