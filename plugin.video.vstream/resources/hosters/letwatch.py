# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letwatch', 'LetWatch')

    def __getUrlFromJavascriptCode(self, html_content):
        # parser = Parser()
        # pattern = "(eval\(function.*?)(.+?)</script>"
        # results = parser.parse(html_content, pattern)

        results = re.search(
            '(eval\\(function.*?)\\s*</script>', html_content, re.DOTALL)

        if results.group(1):
            sJavascript = results.group(1)

            # sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sUnpacked = cPacker().unpack(sJavascript)

            return sUnpacked

        return False

    def _getMediaLinkForGuest(self, auto_play=False):
        request = RequestHandler(self._url)
        html_content = request.request()

        sUnpacked = self.__getUrlFromJavascriptCode(html_content)

        # jwplayer("vplayer").setup({sources:[
        # {file:"http://94.242.57.154/l7z7fz25dmnhgn4vfkbbeauaqogvhaabb62mkm4zvaxq3iodhdvlahybe6sa/v.flv",label:"SD"}],
        # image:"http://94.242.57.154/i/03/00249/d8g74g00wtuv.jpg",skin:"",duration:"5314",width:680,height:390,
        # primary:"flash",startparam:"start",plugins:{"http://letwatch.us/player6/lightsout.js

        pattern = 'sources:\\[{file:"(.+?)"'

        parser = Parser()
        results = parser.parse(sUnpacked, pattern)

        if results[0] is True:
            api_call = results[1][0]
            return True, api_call

        return False, False
