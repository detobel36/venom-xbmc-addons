from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.gui.gui import Gui
from resources.hosters.hoster import iHoster
import time
import random


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sharehoster', 'ShareHoster.com')

    def _getMediaLinkForGuest(self, auto_play=False):
        aSplit = self._url.split('/')
        s_id = aSplit[-1]

        url = 'http://www.sharehoster.com/flowplayer/config.php?movie=' + s_id

        request = RequestHandler(url)
        html_content = request.request()

        pattern = "playlist': \\[.*?},.*?'url': '(.*?)'"
        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            file_name = results[1][0]
            return True, file_name

        return False, ''
