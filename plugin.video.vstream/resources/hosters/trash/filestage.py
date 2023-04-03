from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filestage', 'FileStage.to')

    def getPattern(self):
        return 's1.addVariable\\("file".*?"([^"]+)"'

    def _getMediaLinkForGuest(self, auto_play=False):
        oHosterHandler = cHosterHandler()
        results = oHosterHandler.getUrl(self)
        if results[0] is True:
            return True, cUtil().urlDecode(results[1])

        return False, ''
