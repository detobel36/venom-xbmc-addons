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

SITE_IDENTIFIER = 'vf_film'
SITE_NAME = 'VF Film'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'tous-les-films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-meilleurs-films-en-streaming/', 'showMovies')
MOVIE_NOTES = (
    URL_MAIN +
    'films-les-plus-populaires-en-streaming/',
    'showMovies')
MOVIE_GENRES = (True, 'showGenres')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
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
    if (sSearchText):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()
    oUtil = cUtil()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'option class="level-0" value="\\d+">(.+?)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry
            if 'Uncategorized' in title:
                continue

            sUrl = URL_MAIN + 'genre/' + \
                oUtil.CleanName(title).replace(' ', '-')

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
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '/lettre/' in sUrl:
        sPattern = '</span></td>.+?href="([^"]+).+?src="([^"]+).+?strong>([^<]+).+?<td>([^<]+)'
    else:
        sPattern = 'TPost C.+?href="([^"]+).+?src="([^"]+).+?Title">([^<]+).+?Description"><p>([^<]+)'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+/', '/w342/', 'https:' + aEntry[1])
            title = aEntry[2]
            if '/lettre/' in sUrl:
                desc = ''
                sYear = aEntry[3]
            else:
                desc = aEntry[3]
                sYear = ''

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            sDisplayTitle = title

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHoster',
                sDisplayTitle,
                '',
                sThumb,
                desc,
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
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '>([^<]+)</a> <a class="next page-numbers" href="([^"]+)">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHoster(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    # hoster
    sPattern = 'tplayernv.+?<span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        hosters = aResult[1]
        numHoster = 0
        # url
        sPattern = 'class="TPlayerTb.+?src=(?:"|&quot;)(.+?)(?:"|&quot;)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                oHoster = HosterGui().checkHoster(hosters[numHoster])
                numHoster += 1
                if not oHoster:
                    continue

                oRequestHandler = RequestHandler(aEntry)
                sHtmlContent = oRequestHandler.request()
                sPattern = '<iframe.+?src="([^"]+)'
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    oHoster = HosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
