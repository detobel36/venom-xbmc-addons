from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'bronline', 'BR-Online.de')

    def _getMediaLinkForGuest(self, auto_play=False):
        return True, self._url
