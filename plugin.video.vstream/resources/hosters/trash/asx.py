from resources.hosters.hoster import iHoster
from resources.lib.handler.hosterHandler import cHosterHandler


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'asx', 'Stream File')

    def getPattern(self):
        return 'mms://(.*?)"'

    def _getMediaLinkForGuest(self, auto_play=False):
        oHosterHandler = cHosterHandler()
        results = oHosterHandler.getUrl(self)
        if results[0] is True:
            return True, 'mms://' + results[1]
        return False, ''
