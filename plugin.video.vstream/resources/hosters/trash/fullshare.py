import time
import random

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.gui.gui import Gui
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fullshare', 'FullShare.net')

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        header = request.getResponseHeader()
        php_session_id = self.__getPhpSessionId(header)

        pattern = 'var time_wait = ([^;]+);'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            sSecondsForWait = int(results[1][0]) + 2

            pattern = '<input type="hidden" name="code" value="([^"]+)"'
            parser = Parser()
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                sCode = results[1][0]

                gui = Gui()
                gui.showNofication(sSecondsForWait, 3)
                time.sleep(sSecondsForWait)

                rndX = random.randint(1, 99999999 - 10000000) + 10000000
                rndY = random.randint(1, 999999999 - 100001000) + 100000000
                ts1 = float(time.time())
                ts2 = float(time.time())
                ts3 = float(time.time())
                ts4 = float(time.time())
                ts5 = float(time.time())

                sCookieValue = '__utma=' + \
                    str(rndY) + '.' + str(rndX) + '.' + str(ts1) + '.' + str(ts2) + '.' + str(ts3) + '; '
                sCookieValue = sCookieValue + '__utmz=' + str(rndY) + '.' + str(ts4) + \
                    '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
                sCookieValue = sCookieValue + php_session_id + '; '
                sCookieValue = sCookieValue + '__utmc=' + str(rndY) + "; "
                sCookieValue = sCookieValue + '__utmb=' + \
                    str(rndY) + '.7.10.' + str(ts5) + "; ADBLOCK=1"

                request = RequestHandler(self._url)
                request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
                request.addHeaderEntry('Cookie', sCookieValue)
                request.addParameters('code', sCode)
                html_content = request.request()

                pattern = '<param name="src" value="([^"]+)"'
                parser = Parser()
                results = parser.parse(html_content, pattern)

                if results[0] is True:
                    return True, results[1][0]

        return False, results

    def __getPhpSessionId(self, header):
        sReponseCookie = header.getheader("Set-Cookie")
        aResponseCookies = sReponseCookie.split(";")
        return aResponseCookies[0]
