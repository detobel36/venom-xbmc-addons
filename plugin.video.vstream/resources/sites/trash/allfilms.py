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
return False


SITE_IDENTIFIER = 'allfilms'
SITE_NAME = 'All Films'
SITE_DESC = 'Films'

URL_MAIN = 'https://wvvw.allfilms.co/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche-', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-1.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'recherche-Action-1.html'])
    liste.append(['Animation', URL_MAIN + 'recherche-Animation-1.html'])
    liste.append(['Aventure', URL_MAIN + 'recherche-aventure-1.html'])
    liste.append(['Biopic', URL_MAIN + 'recherche-Biopic-1.html'])
    liste.append(['Comédie', URL_MAIN + 'recherche-Comedie-1.html'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                 'recherche-Comedie-dramatique-1.html'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 'recherche-Comedie-musicale.html'])
    liste.append(['Divers', URL_MAIN + 'recherche-Divers-1.html'])
    liste.append(['Documentaire', URL_MAIN + 'recherche-Documentaire-1.html'])
    liste.append(['Drame', URL_MAIN + 'recherche-Drame-1.html'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 'recherche-Epouvante-horreur-1.html'])
    liste.append(['Famille', URL_MAIN + 'recherche-Famille-1.html'])
    liste.append(['Fantastique', URL_MAIN + 'recherche-Fantastique-1.html'])
    liste.append(['Guerre', URL_MAIN + 'recherche-Guerre-1.html'])
    liste.append(['Opéra', URL_MAIN + 'recherche-Opera-1.html'])
    liste.append(['Policier', URL_MAIN + 'recherche-Policier-1.html'])
    liste.append(['Romance', URL_MAIN + 'recherche-romance-1.html'])
    liste.append(['Science Fiction', URL_MAIN +
                 'recherche-science-fiction-1.html'])
    liste.append(['Thriller', URL_MAIN + 'recherche-thriller-1.html'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
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

    from itertools import chain
    generator = chain([1922,
                       1929,
                       1934,
                       1936,
                       1939,
                       1942,
                       1943,
                       1944,
                       1945,
                       1947,
                       1950,
                       1952],
                      range(1953,
                            1956),
                      [1957],
                      range(1960,
                            2021))

    for i in reversed(list(generator)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'recherche-' + Year + '-1.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch.replace(' ', '-') + '.html'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="movie-card".+?src="([^"]+)".+?title">([^<]+).+?href="([^"]+)">([^<]+).+?label>([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0].replace(' ', '%20')
            if sThumb.startswith('poster'):
                sThumb = URL_MAIN + sThumb
            title = aEntry[1]
            sUrl2 = aEntry[2]
            sQual = aEntry[3].upper()
            sLang = aEntry[4].upper()

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
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

        if aResult:
            sPattern = '-(\\d+).html'
            aResult = oParser.parse(sUrl, sPattern)
            if aResult[0]:
                number = int(aResult[1][0]) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', re.sub(
                    '-(\\d+).html', '-' + str(number) + '.html', sUrl))

                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    '[COLOR teal]Page ' +
                    str(number) +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    sPattern = 'class="lectt " src=["\']([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    # fh = open('c:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
