# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = '_4kstreamz'
SITE_NAME = '4kstreamz'
SITE_DESC = 'Films et Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'list-films.html', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1921, 2022)):
        sYear = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'filmspar?annee=' + sYear)  # / inutile
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<h4 class="head nop">Genre'
    sEnd = '<div class="menu_first">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'a href="([^"]+)" class="an">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1].capitalize()
            triAlpha.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        for title, sUrl in triAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '-').replace('%20', '-') + '.html'
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'list-films.html' in sUrl or '/films/page' in sUrl:
        sPattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+).+?class="qualitos">' + \
            '([^<]+).+?class="synopsis nop">([^<]+)'
    else:
        sPattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sThumb = aEntry[1]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            title = aEntry[2].strip()
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            sQual = ''
            desc = ''
            if 'list-films.html' in sUrl or '/films/page' in sUrl:
                sQual = aEntry[3]
                desc = aEntry[4]

            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sQual', sQual)

            if '/series' not in sUrl2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    if 'suivanthds' in sHtmlContent:  # genre
        sPattern = '>([^<]+)</a><a class="suivanthds.+?href="([^"]+)'
    elif 'CurrentPage' in sHtmlContent:  # film année serie
        sPattern = "CurrentPage.+?href='([^']+).+?>([^<]+)</a></div"
    else:  # film année à partir de la page 8
        sPattern = "</a><span>.+?<a href='([^']+).+?</span>.+?>([^<]+)</a></div></div>\\s*</div>\\s*</div>"

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        if 'suivanthds' in sHtmlContent:  # genre
            sNumberMax = aResult[1][0][0]
            sNextPage = aResult[1][0][1]
        # elif 'CurrentPage':  # film année serie
            # sNextPage = aResult[1][0][0]
            # sNumberMax = aResult[1][0][1]
        else:  # film année à partir de la page 8
            sNextPage = aResult[1][0][0]
            sNumberMax = aResult[1][0][1]

        sNumberNext = re.search(
            'page-([0-9]+)|([0-9]+)$',
            sNextPage).group(0)  # page-XX.html ou  annee-aaaa/XX
        sNumberNext = sNumberNext.replace('page-', '')
        sNextPage = URL_MAIN[:-1] + sNextPage
        sPaging = sNumberNext + '/' + sNumberMax

        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'itemprop="description">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    start = sHtmlContent.find('<div class="contentomovies">')
    sHtmlContent = sHtmlContent[start:]
    sPattern = '<a href="([^"]+).+?class="nop">Saison([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            saison = aEntry[1].replace(' ', '')

            title = ("%s %s %s") % (sMovieTitle, 'saison', saison)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sYear', sYear)
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
    sYear = input_parameter_handler.getValue('sYear')

    iSaison = ''
    sPattern = 'saison.(.+?)'
    aResult = oParser.parse(sUrl, sPattern)
    if aResult[0]:
        iSaison = ' Saison ' + aResult[1][0].replace(' ', '')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="contentomovies">'
    sEnd = '<div class="keywords"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+).+?class="titverle">.+?class="nop">.+?pisode([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            nEpisode = aEntry[1].replace(' ', '')
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            title = sMovieTitle + iSaison + ' episode' + nEpisode

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    oHosterGui = HosterGui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'itemprop="description">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = '<img src=".(vf|vostfr).png|data-url="([^"]+).+?data-code="([^"]+).+?<span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sLang = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sLang = aEntry[0].upper()

            if aEntry[1]:
                dataUrl = aEntry[1]
                dataCode = aEntry[2]
                if "/thumbnail/" in dataCode:
                    continue
                sHost = aEntry[3].capitalize()
                if not oHosterGui.checkHoster(sHost):
                    continue

                sUrl2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + '&CData=' + dataCode
                sDisplayTitle = (
                    '%s (%s) [COLOR coral]%s[/COLOR]') % (title, sLang, sHost)
                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sHost', sHost)
                output_parameter_handler.addParameter('sLang', sLang)
                output_parameter_handler.addParameter('referer', sUrl)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
                    sThumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    sPattern = "<img src=\".(vf|vostfr).png|class=.Playersbelba.+?PPl=(.+?)CData=([^']+).+?<.span>.+?<span>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sLang = aEntry[0].upper()

            if aEntry[1]:
                dataUrl = aEntry[1]
                dataCode = aEntry[2]
                sHost = aEntry[3].capitalize()
                if not oHosterGui.checkHoster(sHost):
                    continue

                sUrl2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + 'CData=' + dataCode

                sDisplayTitle = (
                    '%s (%s) [COLOR coral]%s[/COLOR]') % (title, sLang, sHost)

                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sHost', sHost)
                output_parameter_handler.addParameter('sLang', sLang)
                output_parameter_handler.addParameter('referer', sUrl)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
                    sThumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oHosterGui = HosterGui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')

    oRequest = RequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.request()
    urlReal = oRequest.getRealUrl()
    if URL_MAIN in urlReal:
        oRequest = RequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', referer)
        oRequest.request()
        sHtmlContent = oRequest.request()

        oParser = Parser()
        sPattern = 'class="DownloadSection.+?href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                oHosterGui.showHoster(
                    gui,
                    oHoster,
                    sHosterUrl,
                    sThumb,
                    input_parameter_handler=input_parameter_handler)

    else:
        sHosterUrl = urlReal
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            oHosterGui.showHoster(
                gui,
                oHoster,
                sHosterUrl,
                sThumb,
                input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
