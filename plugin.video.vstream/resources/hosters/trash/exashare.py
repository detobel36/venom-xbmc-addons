# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import urllib

try:  # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmc


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'exashare', 'Exashare')

    def _getMediaLinkForGuest(self, auto_play=False):
        api_call = False

        request = RequestHandler(self._url)
        html_content = request.request()
        parser = Parser()

        # methode1
        # lien indirect
        if 'You have requested the file:' in html_content:
            POST_Url = re.findall(
                'form method="POST" action=\'([^<>"]*)\'',
                html_content)[0]
            POST_Selected = re.findall(
                'form method="POST" action=(.*)</Form>',
                html_content,
                re.DOTALL)[0]
            POST_Data = {}
            POST_Data['op'] = re.findall(
                'input type="hidden" name="op" value="([^<>"]*)"',
                POST_Selected)[0]
            # POST_Data['usr_login'] = re.findall('input type="hidden" name="usr_login" value="([^<>"]*)"',
            #                           POST_Selected)[0]
            POST_Data['id'] = re.findall(
                'input type="hidden" name="id" value="([^<>"]*)"',
                POST_Selected)[0]
            POST_Data['fname'] = re.findall(
                'input type="hidden" name="fname" value="([^<>"]*)"',
                POST_Selected)[0]
            # POST_Data['referer']   = re.findall('input type="hidden" name="referer" value="([^<>"]*)"',
            #                           POST_Selected)[0]
            POST_Data['hash'] = re.findall(
                'input type="hidden" name="hash" value="([^<>"]*)"',
                POST_Selected)[0]
            POST_Data['imhuman'] = 'Proceed to video'

            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            headers = {
                'User-Agent': UA,
                'Host': 'www.exashare.com',
                'Referer': self._url,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded'}

            postdata = urllib.urlencode(POST_Data)

            req = urllib2.Request(POST_Url, postdata, headers)

            xbmc.sleep(10 * 1000)

            response = urllib2.urlopen(req)
            html_content = response.read()
            response.close()

            # fh = open('c:\\test.txt', "w")
            # fh.write(html_content)
            # fh.close()

        pattern = 'file: "([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            api_call = results[1][0]

        # methode2
        pattern = '<iframe[^<>]+?src="(.+?)"[^<>]+?><\\/iframe>'
        results = parser.parse(html_content, pattern)
        if results[0] is True:
            url = results[1][0]
            request = RequestHandler(url)
            request.addHeaderEntry('Referer', url)
            # request.addHeaderEntry('Host','dowed.info')
            html_content = request.request()

            pattern = 'file: *"([^"]+)"'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                api_call = results[1][0]

            # methode2-3
            pattern = '<iframe.+?src="([^"]+)".+?<\\/iframe>'
            results = parser.parse(html_content, pattern)
            if results[0] is True:
                vurl = results[1][0]
                request = RequestHandler(vurl)
                html_content = request.request()
                pattern = 'file: *"([^"]+)"'
                results = parser.parse(html_content, pattern)
                api_call = results[1][0]

        if api_call:
            return True, api_call

        return False, False
