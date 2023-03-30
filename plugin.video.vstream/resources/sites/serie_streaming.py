# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'serie_streaming'
SITE_NAME = 'Série Streaming'
SITE_DESC = 'Serie Streaming - voir votre series streaming Gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + 'search.php?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showSeries')
SERIE_GENRES = (True, 'showGenres')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showSeries(URL_SEARCH[0] + sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'allowGenrebydefault">'
    sEnd = 'Dernières Episodes récents'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+).+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    triAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1]
            triAlpha.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, sUrl in triAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
        reqType = RequestHandler.REQUEST_TYPE_POST
        sPattern = 'href="([^"]+).+?image: url\\((.+?)"title">([^<]+)'
        idxUrl = 0
        idxThumb = 1
        idxTitle = 2
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        reqType = RequestHandler.REQUEST_TYPE_GET
        sPattern = 'item">.+?href="([^"]+)" title="([^"]+).+?-src="([^"]+)'
        idxUrl = 0
        idxTitle = 1
        idxThumb = 2

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.setRequestType(reqType)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[idxUrl]
            title = aEntry[idxTitle].strip()
            sThumb = 'https:' + \
                aEntry[idxThumb].replace('posters//tv', 'posters/tv')

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()

    sPattern = "<a>\\d+</a></li><li><a href='([^']+).+?>([0-9]+)</a></li></ul>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page-([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    sPattern = "<span>\\d+</span><li><a href='([^']+).+?>([0-9]+)</a></li></ul>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('[-|/]([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'dci-desc">(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0].split('streaming')[1]
    except BaseException:
        pass

    # pour ne pas prendre les propositions de la source
    sStart = 'dcr-rating">'
    sEnd = 'regarder aussi'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'item">.+?href="([^"]+)" title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            sUrl = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'title"><a href="([^"]+)" title=.+?(episode [0-9]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' ' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # streaming
    sPattern = 'data-hex="([^"]+).+?data-code="([^"]+).+?mobile">([^<]+).+?language ([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sDataHex = aEntry[0]
            sDataCode = aEntry[1]
            sHost = aEntry[2].capitalize()
            sLang = aEntry[3].upper()

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)
            lien = URL_MAIN + 'iframeCode=' + sDataCode + '/' + sDataHex

            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', lien)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHost)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    # download
    sPattern = 'tele"><a href=\'([^\']+).+?mobile">([^<]+).+?language ([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sDataCode = aEntry[0]
            sHost = aEntry[1].capitalize()
            sLang = aEntry[2].upper()

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)
            lien = URL_MAIN[:-1] + sDataCode

            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', lien)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHost)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', referer)

    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = HosterGui().checkHoster(sHosterUrl)

    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
