# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # ne propose que Netu en hoster 31/01/21


SITE_IDENTIFIER = 'streaming_planet'
SITE_NAME = 'Streaming-planet'
SITE_DESC = 'Film streaming vf - streaming complet'

URL_MAIN = 'https://streaming-planet.ws/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'index.php?do=lastnews', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&titleonly=3&story=',
    'showSearch')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH[1],
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


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sSearch = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sSearch)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Animation', URL_MAIN + 'animation/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Biographie', URL_MAIN + 'biographie/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Crime', URL_MAIN + 'crime/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Familial', URL_MAIN + 'familial/'])
    liste.append(['Fantasy', URL_MAIN + 'fantasy/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Histoire', URL_MAIN + 'histoire/'])
    liste.append(['Horreur', URL_MAIN + 'horreur/'])
    liste.append(['Mélodrame', URL_MAIN + 'melodrame/'])
    liste.append(['Musique', URL_MAIN + 'musique/'])
    liste.append(['Mystère', URL_MAIN + 'mystery/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Sports', URL_MAIN + 'sports/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
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
    for i in reversed(range(2017, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'nouveau-' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'movie-item">\\s*<a href="([^"]+)">\\s*<h3>([^<]*)</h3.+?style=.+?>([^<]*).+?;">([^<]*).+?;">([^<]*).+?src="([^"]*)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            title = aEntry[1]
            sQual = aEntry[2]
            sYear = aEntry[3]
            sLang = aEntry[4]
            sThumb = aEntry[5]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN + sThumb
            sDisplayTitle = ('%s [%s] (%s) (%s)') % (
                title, sQual, sLang, sYear)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a></div>.+?<a href="([^"]+)"><i class="fa fa-angle-right" aria-hidden="true"></i></a>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe.+?data-src="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if 'youtube' in sHosterUrl:
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
