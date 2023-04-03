# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import RequestHandler
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        html_content = GetHtml(url)
        pattern = '<form action="(.+?)" method="post"'
        result = re.findall(pattern, html_content)
        url = 'https://multiup.org' + ''.join(result[0])

        NewUrl = url.replace('http://www.multiup.org/fr/download',
                             'http://www.multiup.eu/fr/mirror') .replace('http://www.multiup.eu/fr/download',
                                                                         'http://www.multiup.eu/fr/mirror') .replace('http://www.multiup.org/download',
                                                                                                                     'http://www.multiup.eu/fr/mirror')

        html_content = GetHtml(NewUrl)

        pattern = 'nameHost="([^"]+)".+?link="([^"]+)".+?class="([^"]+)"'
        r = re.findall(pattern, html_content, re.DOTALL)

        if not r:
            return False

        for item in r:

            if 'bounce-to-right' in str(item[2]
                                        ) and 'download-fast' not in item[1]:
                self.list.append(item[1])

        return self.list


class cJheberg:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):

        if url.endswith('/'):
            url = url[:-1]

        idFile = url.rsplit('/', 1)[-1]
        NewUrl = 'https://api.jheberg.net/file/' + idFile
        html_content = GetHtml(NewUrl)

        pattern = '"hosterId":([^"]+),"hosterName":"([^"]+)",".+?status":"([^"]+)"'
        r = re.findall(pattern, html_content, re.DOTALL)
        if not r:
            return False

        for item in r:
            if 'ERROR' not in item[2]:
                urllink = 'https://download.jheberg.net/redirect/' + \
                    idFile + '-' + item[0]
                try:
                    url = GetHtml(urllink)
                    self.list.append(url)
                except BaseException:
                    pass

        return self.list


# modif cloudflare
def GetHtml(url, postdata=None):

    if 'download.jheberg.net/redirect' in url:
        request = RequestHandler(url)
        html_content = request.request()
        url = request.getRealUrl()
        return url
    else:
        html_content = ''
        request = RequestHandler(url)
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)

        if postdata is not None:
            request.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            request.addHeaderEntry(
                'Content-Type',
                'application/x-www-form-urlencoded; charset=UTF-8')
            request.addHeaderEntry(
                'Referer', 'https://download.jheberg.net/redirect/xxxxxx/yyyyyy/')

        elif 'download.jheberg.net' in url:
            request.addHeaderEntry('Host', 'download.jheberg.net')
            request.addHeaderEntry('Referer', url)

        request.addParametersLine(postdata)

        html_content = request.request()

        return html_content
