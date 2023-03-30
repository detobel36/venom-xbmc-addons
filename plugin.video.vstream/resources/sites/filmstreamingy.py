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

SITE_IDENTIFIER = 'filmstreamingy'
SITE_NAME = 'FilmStreamingY'
SITE_DESC = 'stream HD, streaming Sans pub, streaming vf'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'dernier/film-en-streaming', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'dernier/genres/top-films-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'menu-item-object-category menu-item-[0-9]+"><a href="([^"]+)">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        triAlpha = []
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[1] in (
                'Liste De Films De Noël',
                'Films De Noël',
                'Top Films Streaming',
                'Top Films',
                'Prochainement',
                'Uncategorized',
                'Genres',
                    'Tendance'):
                continue

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
    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(
            sSearch.replace(URL_SEARCH_MOVIES[0], ''))
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'class="ml-item"> <a href="([^"]+).+?img src="([^"]*).+?alt="([^"]+).+?(?:|jtip-quality">([^<]+).+?)desc"><p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[1])
            title = aEntry[2].replace(
                'en streaming', '').replace(
                'en steaming', '')
            sQual = aEntry[3] if not sSearch else ''
            desc = aEntry[4]

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
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

    sPattern = 'link rel="next" href="([^\"]+).+?>([^<]+)</a></li></ul></nav'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberNext = sNextPage.split('/')[-1]
        sNumberMax = aResult[1][0][1].split('/')[-1]
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, str(sPaging)

    sPattern = "active'><a class=''>[0-9]+</a></li><li><a rel='nofollow' class='page larger' href='([^']+).+?([^']+)'>Last<"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberNext = sNextPage.split('/')[-1]
        sNumberMax = aResult[1][0][1].split('/')[-1]
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, str(sPaging)

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="tab\\d".+?data-(|litespeed-)src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry[1]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
