# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'vfilms'
SITE_NAME = 'VFilms'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'index.php?story=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)
# URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')  # Pas dispo sur cette
# source

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'nouveaux-films', 'showMovies')
MOVIE_BOX = (URL_MAIN + 'box-office001', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')


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
        'Films (Nouveautés)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_BOX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BOX[1],
        'Films (Populaires)',
        'star.png',
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
        'Films (Nouveautés)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_BOX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BOX[1],
        'Films (Populaires)',
        'star.png',
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
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = 'Film Par Genre'
    sEnd = 'Film Par Annee'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li><a href="([^<]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            title = aEntry[1]
            sUrl = URL_MAIN[:-1] + aEntry[0]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1994, 2023)):
        sYear = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'xfsearch/year/' + sYear + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch + '&do=search&subaction=search'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'item">.+?href="([^"]+)" title="([^"]+).+?src="([^"]+)'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            title = aEntry[1]
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[2])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            if 'series-streaming/' in sUrl:
                gui.addTV(SITE_IDENTIFIER, 'showSaisons', title,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

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
    sPattern = '<span>[\\d]+</span> <a href="([^"]+).+?">(\\d+)</a></div'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'full-text clearfix">([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = '<a href="([^"]+)"><div class="thumb"><div class="th-in"><div class="th-img img-resp-v"><img class=" ls-is-cached lazyloaded" src="([^"]+)" alt="\\d+ Season"><figcaption>(Saison \\d+)<\\/figcaption>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = sMovieTitle + aEntry[2]
            sDisplayTitle = title  # + ' [' + sQual + ']'

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sQual', sQual)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # le </ en fin de regex est utile
    sPattern = 'href="([^"]+)"><div class="fsa-ep">.+?</span>([^<]+)</'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' Episode ' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

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

    oParser = Parser()
    sPattern = 'data-playerlink="([^"]+).+?<span class="serv">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            sHost = aEntry[1]
            if "VO" in sHost:
                sDisplayTitle = ('%s (%s)') % (sMovieTitle, sHost)
            else:
                sDisplayTitle = sMovieTitle
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
