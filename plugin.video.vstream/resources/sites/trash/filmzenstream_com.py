# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import Unquote
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # 25/12/2020


SITE_IDENTIFIER = 'filmzenstream_com'
SITE_NAME = 'Filmzenstream'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = 'https://filmzenstream.xyz/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'Categorie/action/'])
    liste.append(['Animation', URL_MAIN + 'Categorie/animation/'])
    liste.append(['Aventure', URL_MAIN + 'Categorie/aventure/'])
    liste.append(['Biographie', URL_MAIN + 'Categorie/biography/'])
    liste.append(['Comédie', URL_MAIN + 'Categorie/comedie/'])
    liste.append(['Crime', URL_MAIN + 'Categorie/crime/'])
    liste.append(['Drame', URL_MAIN + 'Categorie/drame/'])
    liste.append(['Documentaire', URL_MAIN + 'Categorie/documentaire/'])
    liste.append(['Famille', URL_MAIN + 'Categorie/famille/'])
    liste.append(['Fantaisie', URL_MAIN + 'Categorie/fantaisie/'])
    # liste.append(['Guerre', URL_MAIN + 'Categorie/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'Categorie/history/'])
    liste.append(['Horreur', URL_MAIN + 'Categorie/horreur/'])
    liste.append(['Musical', URL_MAIN + 'Categorie/musique/'])
    liste.append(['Mystère', URL_MAIN + 'Categorie/mystere/'])
    liste.append(['Romance', URL_MAIN + 'Categorie/romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'Categorie/science-fiction/'])
    liste.append(['Sport', URL_MAIN + 'Categorie/sport/'])
    liste.append(['Thriller', URL_MAIN + 'Categorie/thriller/'])
    liste.append(['War', URL_MAIN + 'Categorie/war/'])

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
            'siteUrl', URL_MAIN + 'Categorie/' + Year + '-films/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sSearch = Unquote(sSearch)
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'href="([^"]+)" title="([^"]+)".+?src="([^"]+)'
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

            sUrl2 = aEntry[0]
            title = aEntry[1]
            sThumb = aEntry[2]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            title = title.replace(' VF Streaming', '')

            sYear = None
            if len(title) > 4 and title[-4:].isdigit():
                sYear = title[-4:]
                title = title[0:len(title) - 4] + '(' + sYear + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            if sYear:
                output_parameter_handler.addParameter('sYear', sYear)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^"]+?)" class="next">'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe[^<>]+?(?:data-)*data-src="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            if 'belike' in aEntry:
                if aEntry.startswith('/'):
                    oRequestHandler = RequestHandler('https:' + aEntry)
                else:
                    oRequestHandler = RequestHandler(aEntry)

                oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()

            # pour récuperer le lien Downpit
            elif 'downpit' in aEntry:
                oRequestHandler = RequestHandler(aEntry)
                sHtmlContent = oRequestHandler.request()
                sPattern = '<iframe.+?src="([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:
                        sHosterUrl = aEntry

            else:
                sHosterUrl = aEntry
                # Vire les bandes annonces
                if 'youtube.com' in aEntry:
                    continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
