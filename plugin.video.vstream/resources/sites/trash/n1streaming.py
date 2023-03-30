# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# site HS desactivée le 15/10/2020 (les dernieres corrections sont
# adaptées au site 01 streaming qui n'est pas un clone)
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


SITE_IDENTIFIER = 'n1streaming'
SITE_NAME = 'N1 Streaming'
SITE_DESC = 'Films & Séries'

URL_MAIN = 'https://www.01streaming.net/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')

MOVIE_GENRES = (True, 'showMoviesGenres')
SERIE_GENRES = (True, 'showSeriesGenres')
MOVIE_ANNEES = (True, 'showMovieYears')


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
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries',
        'series.png',
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
    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films & Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    for i in reversed(
        range(
            2000,
            2021)):  # a revérifier pas grand chose (4-5 films par pages)32 - 90
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'release/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesGenres():
    showGenres('?type=movies')


def showSeriesGenres():
    showGenres('?type=series')


def showGenres(sType):

    gui = Gui()
    liste = []
    listegenre = [
        'action',
        'action-adventure',
        'afro',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'histoire',
        'horreur',
        'kids',
        'musique',
        'mystere',
        'reality',
        'romance',
        'science-fiction',
        'science-fiction-fantastique',
        'telefilm',
        'thriller',
        'vieux',
        'war-politics',
        'western']

    url1g = URL_MAIN + 'genre/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre + '/' + sType])

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


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<h2 class="entry-title">([^<>]+).+?src="([^"]+).+?<a href="([^"]+)"'

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

            sThumb = aEntry[1]
            sUrl2 = aEntry[2]
            title = aEntry[0]

            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            s = title
            if ('/release/' in sUrl or sSearch):
                if '/serie' in sUrl2:
                    s = s + ' [Serie] '
                else:
                    s = s + ' [Film] '

            sDisplayTitle = s

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl2:
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
                    'showHosters',
                    sDisplayTitle,
                    'films.png',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            snumberNext = 'Next '
            try:
                snumberNext = 'Page ' + \
                    re.search('/page/([0-9]+)', sNextPage).group(1)
            except BaseException:
                pass
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal] ' +
                snumberNext +
                ' >>>[/COLOR]',
                output_parameter_handler)
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href="([^"]+)">SUIVANT</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        if aResult[1][0].startswith('/'):
            return URL_MAIN[:-1] + aResult[1][0]
        else:
            return aResult[1][0]

    return False


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    desc = ''
    sPattern = 'class="description.+?<p>(.+?)<.p><.div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = aResult[1][0]
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', desc)

    sPattern = 'choose-season.+?ref="([^"]+).+?inline">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            saison = aEntry[1]

            title = ("%s %s") % (sMovieTitle, ' Saison ' + saison)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h2 class="entry-title">([^><]+).+?<a href="([^"]+)" class="lnk-blk">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl2 = aEntry[1]
            title = aEntry[0]

            sDisplayTitle = title

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
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

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    sPattern = '<iframe (?:data-)*src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
