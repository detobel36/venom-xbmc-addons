# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'o1streaming'
SITE_NAME = '01 Streaming'
SITE_DESC = 'Films & Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming/', 'showMovies')
MOVIE_GENRES = ('?type=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')
SERIE_GENRES = ('?type=series', 'showGenres')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
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
        'films.png',
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
        'Films & Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    oRequestHandler = RequestHandler(URL_MAIN + 'accueil/')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="btn sm" href="([^"]+)">([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            Year = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                Year,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    siteUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(URL_MAIN + 'accueil/')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)<'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0] + siteUrl
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sUrl = sSearch
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'entry-header"> *<h2 class="entry-title">([^<]+).+?src="([^"]+).+?class="year">([^<]+).+?href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[1]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb
            sYear = aEntry[2]
            sUrl2 = aEntry[3]
            title = aEntry[0]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche
            sDisplayTitle = title
            if '/release/' in sUrl or sSearch:
                if '/serie' in sUrl2:
                    sDisplayTitle += ' {Série}'
                else:
                    sDisplayTitle += ' {Film}'

            if sYear:
                sDisplayTitle += ' (%s)' % sYear

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/serie' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    'series.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    'films.png',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
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
    sPattern = '>([^<]+)</a><a href="([^"]+)"\\s*>SUIVANT</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        if sNextPage.startswith('/'):
            return URL_MAIN[:-1] + sNextPage, sPaging
        else:
            return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'description"><p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = 'choose-season"><a href="([^"]+).+?inline">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sMovieTitle = sMovieTitle + ' Saison ' + aEntry[1]

            # output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'wp-admin/admin-ajax.php')
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                sMovieTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = 'h2 class="entry-title">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            title = aEntry[0]
            sUrl = aEntry[1]
            # if sUrl.startswith('/'):
            # sUrl = URL_MAIN + sUrl

            # title = re.sub('- Saison \d+', '', title)  # double affichage
            # de la saison

            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
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
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    numUrl = 0

    # récupération du Synopsis
    if desc is False:
        try:
            sPattern = 'description"><p>(.+?)</p>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                desc = aResult[1][0]
        except BaseException:
            pass

    sPatternUrl = '<iframe (?:data-)*src="([^"]+)"'
    aResultUrl = oParser.parse(sHtmlContent, sPatternUrl)
    if aResultUrl[0]:
        sPatternHost = 'class="btn(| on)" href="([^"]+).+?class="server">([^<]+) <'
        aResultHost = oParser.parse(sHtmlContent, sPatternHost)
        if aResultHost[0]:
            output_parameter_handler = OutputParameterHandler()
            for aEntry in aResultHost[1]:

                sUrl2 = aResultUrl[1][numUrl]
                numUrl += 1
                sHost = aEntry[2]
                sLang = 'VF'
                if '-VOSTFR' in sHost:
                    sLang = 'VOSTFR'
                sHost = sHost.replace(
                    'VF',
                    '').replace(
                    'VOSTFR',
                    '').replace(
                    ' -',
                    '')

                oHoster = HosterGui().checkHoster(sHost)
                if oHoster:
                    sDisplayTitle = (
                        '%s [COLOR coral]%s[/COLOR] (%s)') % (sMovieTitle, sHost, sLang)
                    output_parameter_handler.addParameter('siteUrl', sUrl2)
                    output_parameter_handler.addParameter('sThumb', sThumb)
                    output_parameter_handler.addParameter('desc', desc)
                    output_parameter_handler.addParameter('sHost', sHost)
                    output_parameter_handler.addParameter('sLang', sLang)
                    output_parameter_handler.addParameter(
                        'sMovieTitle', sMovieTitle)
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
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'src="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
