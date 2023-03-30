# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filepup', 'FilePup')

    def _getMediaLinkForGuest(self, autoPlay=False):
        oRequestHandler = RequestHandler(self._url)
        # oRequestHandler.addParameters('login', '1')
        sHtmlContent = oRequestHandler.request()

        oParser = Parser()
        sPattern = 'type: "video\\/mp4", *src: "([^<>"{}]+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            return True, aResult[1][0]

        return False, False
