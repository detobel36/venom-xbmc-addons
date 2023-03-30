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
    output_parameter_handler.addParameter('siteUrl', SPORT_LIVE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_LIVE[1],
        'Sports (En direct)',
        'replay.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = URL_MAIN + input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix():
        sHtmlContent = sHtmlContent.replace('Ã®', 'î').replace('Ã©', 'é')

    # récupérer les drapeaux pour en faire des thumb
    sPattern = "\\.flag\\.([^{]+){.+?url\\(([^)]+)\\)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    flags = dict(aResult[1])

    sPattern = "colspan=\"7\".+?<b>([^<]+)<\\/b>.+?location\\.href = '([^']+).+?text-align.+?>(.+?)<\\/td>.+?<span class=\"flag ([^\"]+).+?text-align.+?>([^<]+).+?text-align: left.+?>([^<]+).+?<span class=\"t\">([^<]+)<\\/span>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[1]
            sDate = aEntry[2].replace('<br />', ' ')
            flag = aEntry[3]
            sdesc1 = aEntry[4]
            sdesc2 = aEntry[5]
            sTime = aEntry[6]

            sThumb = flags.get(flag)
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
            title += '(' + aEntry[0] + ')'
            sDisplayTitle = title
            desc = sDisplayTitle

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHoster',
                title,
                sThumb,
                sDisplayTitle,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if not sUrl.startswith('http'):
        sUrl = URL_MAIN + sUrl
    title = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')
    sThumb = input_parameter_handler.getValue('sThumb')
    sCat = 6
    sMeta = 0

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Double Iframe a passer.
    sPattern = "document\\.getElementById\\('video'\\)\\.src='([^']+)'.+?>([^<]+)<"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[1]:  # Pas de flux
        gui.setEndOfDirectory()
        return

    for entry in aResult[1]:
        output_parameter_handler = OutputParameterHandler()
        iframeURL1 = entry[0]
        canal = entry[1]
        sMovieTitle = title
        if canal not in sMovieTitle:
            sMovieTitle += ' [' + canal + ']'

        output_parameter_handler.addParameter('sMovieTitle', title)
        output_parameter_handler.addParameter('thumbnail', sThumb)
        output_parameter_handler.addParameter('desc', desc)

        oGuiElement = GuiElement()
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setDescription(desc)
        oGuiElement.setFileName(sMovieTitle)
        oGuiElement.setSiteName(resources.sites.freebox.SITE_IDENTIFIER)
        oGuiElement.setFunction('play__')
        oGuiElement.setIcon('tv.png')
        oGuiElement.setMeta(sMeta)
        oGuiElement.setThumbnail(sThumb)
        oGuiElement.setDirectTvFanart()
        oGuiElement.setCat(sCat)
        oGuiElement.setMeta(sMeta)

        if 'dailymotion' in iframeURL1:
            output_parameter_handler.addParameter(
                'sHosterIdentifier', 'dailymotion')
            output_parameter_handler.addParameter('sMediaUrl', iframeURL1)
            output_parameter_handler.addParameter(
                'siteUrl', sHosterUrl)  # variable manquante
            output_parameter_handler.addParameter('sFileName', sMovieTitle)
            oGuiElement.setFunction('play')
            oGuiElement.setSiteName('HosterGui')
            # addHost absent ???? del 20/08/2021
            gui.addHost(oGuiElement, output_parameter_handler)
            Gui.CONTENT = 'movies'
            gui.setEndOfDirectory()
            return

        oRequestHandler = RequestHandler(iframeURL1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
        sHtmlContent = oRequestHandler.request()

        sHosterUrl = ''
        oParser = Parser()
        sPattern = '<iframe.+?src="([^"]+)'
        aResult2 = oParser.parse(sHtmlContent, sPattern)

        if not aResult2[0]:
            sPattern = "playStream\\('iframe','([^']+)'\\)"
            aResult2 = oParser.parse(sHtmlContent, sPattern)

        if aResult2[0]:
            iframeURL1 = aResult2[1][0]

            if 'cloudstream' in iframeURL1:
                sHosterUrl = getHosterWigistream(iframeURL1, sUrl)

            if not sHosterUrl:
                oRequestHandler = RequestHandler(iframeURL1)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()

                oParser = Parser()
                sPattern = '<iframe.+?src="([^"]+)'
                aResult2 = oParser.parse(sHtmlContent, sPattern)

                if aResult2[0]:
                    urlHoster = aResult2[1][0]
                    if 'primetubsub' in urlHoster or 'sportcast' in urlHoster:
                        sHosterUrl = getHosterPrimetubsub(
                            urlHoster, iframeURL1)
                    else:
                        sHosterUrl = getHosterWigistream(urlHoster, iframeURL1)

        if sHosterUrl:
            output_parameter_handler.addParameter('siteUrl', sHosterUrl)
            gui.addFolder(oGuiElement, output_parameter_handler)

    Gui.CONTENT = 'files'
    gui.setEndOfDirectory()


def getHosterWigistream(url, referer):
    url = url.strip()
    if not url.startswith('http'):
        url = 'http:' + url
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sUnpack = cPacker().unpack(sstr)
        sPattern = 'src="(.+?)"'
        aResult = re.findall(sPattern, sUnpack)
        if aResult:
            return aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    else:
        sPattern = "source:'(.+?)'"
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            return aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False


def getHosterPrimetubsub(url, referer):
    oParser = Parser()

    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return

    referer = url
    url = aResult[1][0]

    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()
    sPattern = "(src|[^/]source):'([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return

    referer = url
    url = aResult[1][0][1]

    return url + '|User-Agent=' + UA + '&Referer=' + Quote(referer)
