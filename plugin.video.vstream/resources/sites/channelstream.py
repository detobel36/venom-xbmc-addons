# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re
import time
import resources.sites.freebox

from resources.lib.packer import cPacker
from resources.lib.comaddon import isMatrix, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import Quote

from datetime import datetime, timedelta

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_SPORTS = (True, 'load')
SPORT_LIVE = ('/programme.php', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_LIVE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_LIVE[1],
        'Sports (En direct)',
        'replay.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = URL_MAIN + input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    if isMatrix():
        html_content = html_content.replace('Ã®', 'î').replace('Ã©', 'é')

    # récupérer les drapeaux pour en faire des thumb
    pattern = "\\.flag\\.([^{]+){.+?url\\(([^)]+)\\)"
    results = parser.parse(html_content, pattern)
    flags = dict(results[1])

    pattern = "colspan=\"7\".+?<b>([^<]+)<\\/b>.+?location\\.href = '([^']+).+?text-align.+?>(.+?)<\\/td>.+?<span class=\"flag ([^\"]+).+?text-align.+?>([^<]+).+?text-align: left.+?>([^<]+).+?<span class=\"t\">([^<]+)<\\/span>"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[1]
            sDate = entry[2].replace('<br />', ' ')
            flag = entry[3]
            sdesc1 = entry[4]
            sdesc2 = entry[5]
            sTime = entry[6]

            thumb = flags.get(flag)
            title = ''
            if sDate:
                try:
                    sDate += ' ' + sTime
                    d = datetime(*
                                 (time.strptime(sDate, '%Y-%m-%d %H:%M')[0:6]))
                    d += timedelta(hours=6)
                    sDate = d.strftime("%d/%m/%y %H:%M")
                except Exception as e:
                    pass
                title = sDate + ' - '

            if sdesc1:
                title += sdesc1 + ' - ' + sdesc2 + ' - '
            title += '(' + entry[0] + ')'
            display_title = title
            desc = display_title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHoster',
                title,
                thumb,
                display_title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if not url.startswith('http'):
        url = URL_MAIN + url
    title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')
    thumb = input_parameter_handler.getValue('thumb')
    cat = 6
    sMeta = 0

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Double Iframe a passer.
    pattern = "document\\.getElementById\\('video'\\)\\.src='([^']+)'.+?>([^<]+)<"
    results = parser.parse(html_content, pattern)

    if not results[1]:  # Pas de flux
        gui.setEndOfDirectory()
        return

    for entry in results[1]:
        output_parameter_handler = OutputParameterHandler()
        iframeURL1 = entry[0]
        canal = entry[1]
        movie_title = title
        if canal not in movie_title:
            movie_title += ' [' + canal + ']'

        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('thumbnail', thumb)
        output_parameter_handler.addParameter('desc', desc)

        gui_element = GuiElement()
        gui_element.setTitle(movie_title)
        gui_element.setDescription(desc)
        gui_element.setFileName(movie_title)
        gui_element.setSiteName(resources.sites.freebox.SITE_IDENTIFIER)
        gui_element.setFunction('play__')
        gui_element.setIcon('tv.png')
        gui_element.setMeta(sMeta)
        gui_element.setThumbnail(thumb)
        gui_element.setDirectTvFanart()
        gui_element.setCat(cat)
        gui_element.setMeta(sMeta)

        if 'dailymotion' in iframeURL1:
            output_parameter_handler.addParameter(
                'hoster_identifier', 'dailymotion')
            output_parameter_handler.addParameter('media_url', iframeURL1)
            output_parameter_handler.addParameter(
                'site_url', hoster_url)  # variable manquante
            output_parameter_handler.addParameter('file_name', movie_title)
            gui_element.setFunction('play')
            gui_element.setSiteName('HosterGui')
            # addHost absent ???? del 20/08/2021
            gui.addHost(gui_element, output_parameter_handler)
            Gui.CONTENT = 'movies'
            gui.setEndOfDirectory()
            return

        request_handler = RequestHandler(iframeURL1)
        request_handler.addHeaderEntry('User-Agent', UA)
        # request_handler.addHeaderEntry('Referer', siterefer) # a verifier
        html_content = request_handler.request()

        hoster_url = ''
        parser = Parser()
        pattern = '<iframe.+?src="([^"]+)'
        aResult2 = parser.parse(html_content, pattern)

        if not aResult2[0]:
            pattern = "playStream\\('iframe','([^']+)'\\)"
            aResult2 = parser.parse(html_content, pattern)

        if aResult2[0]:
            iframeURL1 = aResult2[1][0]

            if 'cloudstream' in iframeURL1:
                hoster_url = getHosterWigistream(iframeURL1, url)

            if not hoster_url:
                request_handler = RequestHandler(iframeURL1)
                request_handler.addHeaderEntry('User-Agent', UA)
                html_content = request_handler.request()

                parser = Parser()
                pattern = '<iframe.+?src="([^"]+)'
                aResult2 = parser.parse(html_content, pattern)

                if aResult2[0]:
                    urlHoster = aResult2[1][0]
                    if 'primetubsub' in urlHoster or 'sportcast' in urlHoster:
                        hoster_url = getHosterPrimetubsub(
                            urlHoster, iframeURL1)
                    else:
                        hoster_url = getHosterWigistream(urlHoster, iframeURL1)

        if hoster_url:
            output_parameter_handler.addParameter('site_url', hoster_url)
            gui.addFolder(gui_element, output_parameter_handler)

    Gui.CONTENT = 'files'
    gui.setEndOfDirectory()


def getHosterWigistream(url, referer):
    url = url.strip()
    if not url.startswith('http'):
        url = 'http:' + url
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    results = re.findall(pattern, html_content)

    if results:
        sstr = results[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sUnpack = cPacker().unpack(sstr)
        pattern = 'src="(.+?)"'
        results = re.findall(pattern, sUnpack)
        if results:
            return results[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    else:
        pattern = "source:'(.+?)'"
        results = re.findall(pattern, html_content)
        if results:
            return results[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False


def getHosterPrimetubsub(url, referer):
    parser = Parser()

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()
    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        return

    referer = url
    url = results[1][0]

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()
    pattern = "(src|[^/]source):'([^']+)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        return

    referer = url
    url = results[1][0][1]

    return url + '|User-Agent=' + UA + '&Referer=' + Quote(referer)
