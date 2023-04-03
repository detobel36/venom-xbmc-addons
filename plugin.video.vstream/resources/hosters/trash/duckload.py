from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import Parser
from resources.lib.gui.gui import Gui
from resources.hosters.hoster import iHoster
import time
import random


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'duckload', 'Duckload.com')

    def setUrl(self, url):
        self._url = url.replace('/divx/', '/play/').replace('.html', '')

    def getMediaLink(self, auto_play=False):
        premium_handler = cPremiumHandler(self.getPluginIdentifier())
        if premium_handler.isPremiumModeAvailable():
            username = premium_handler.getUsername()
            password = premium_handler.getPassword()
            return self._getMediaLinkByPremiumUser(username, password)

        return self._getMediaLinkForGuest(auto_play)

    def _getMediaLinkByPremiumUser(self, username, password):
        request_handler = RequestHandler('http://www.duckload.com/api/public/login&user=' + username + '&pw=' +
                                         password + '&fmt=json&source=WEB')
        request_handler.request()

        response_cookie = request_handler.getResponseHeader().getheader("Set-Cookie")

        request_handler = RequestHandler(self._url)
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addParameters('stream', '')
        request_handler.addHeaderEntry('Cookie', response_cookie)
        html_content = request_handler.request()

        pattern = '<param name="src" value="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            return True, results[1][0]

        return False, results

    def _getMediaLinkForGuest(self, auto_play=False):
        seconds_for_wait = 10

        request = RequestHandler(self._url)
        html_content = request.request()

        php_session_id = self.__getPhpSessionId(request.getResponseHeader())

        post_name = ''
        post_value = ''
        post_button_name = ""
        pattern = '<form onsubmit="return checkTimer.*?<input type="hidden" name="([^"]+)" ' + \
            'value="([^"]+)".*?<button name="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            for entry in results[1]:
                post_name = entry[0]
                post_value = entry[1]
                post_button_name = entry[2]

        pattern = 'var tick.*?=(.*?);'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            ticket_value = str(results[1][0]).replace(' ', '')
            seconds_for_wait = int(ticket_value) + 2

            gui = Gui()
            gui.showNofication(seconds_for_wait, 3)
            time.sleep(seconds_for_wait)

            rnd_x = random.randint(1, 99999999 - 10000000) + 10000000
        rnd_y = random.randint(1, 999999999 - 100001000) + 100000000
        ts1 = float(time.time())
        ts2 = float(time.time())
        ts3 = float(time.time())
        ts4 = float(time.time())
        ts5 = float(time.time())

        cookie_value = php_session_id + '; '
        cookie_value = cookie_value + '__utma=' + \
            str(rnd_y) + '.' + str(rnd_x) + '.' + str(ts1) + '.' + str(ts2) + '.' + str(ts3) + '; '
        cookie_value = cookie_value + '__utmb=' + \
            str(rnd_y) + '.1.10.' + str(ts3) + '; '
        cookie_value = cookie_value + '__utmc=' + str(rnd_y) + "; "
        cookie_value = cookie_value + '__utmz=' + str(rnd_y) + '.' + str(ts4) + \
            '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '

        request = RequestHandler(self._url)
        request.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request.addHeaderEntry('Cookie', cookie_value)
        request.addParameters(post_name, post_value)
        request.addParameters(post_button_name, '')

        html_content = request.request()

        pattern = '<param name="src" value="([^"]+)"'
        results = Parser().parse(html_content, pattern)

        if results[0] is True:
            return True, results[1][0]

        return False, results

    def __getPhpSessionId(self, header):
        return header.getheader("Set-Cookie").split(";")[0]
