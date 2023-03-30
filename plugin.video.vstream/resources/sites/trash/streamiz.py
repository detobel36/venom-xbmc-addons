# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 37 https://streamiz-filmze.org/ 24122020
# url instable et de plus en plus souvent  redirection vers streamcomplet3
# (clone qui le remplace)
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


SITE_IDENTIFIER = 'streamiz'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Films en streaming.'

URL_MAIN = 'https://streamiz-filmze.org/v7/'


MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/box-office/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/vostfr/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
        sUrl = sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    liste = []
    listegenre = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'drame',
        'guerre',
        'historique',
        'horreur',
        'musical',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western',
        'documentaire',
        'spectacle']

    # href="/films/action/
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'films/' + igenre + '/'])

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


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:

        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        pData = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + sSearch
        sUrl = URL_MAIN + 'index.php?do=search'
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParametersLine(pData)
        sHtmlContent = oRequestHandler.request()

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # on ne récupère pas les films aléatoire
    end = sHtmlContent.find('<b>Film aléatoire</b>')
    sHtmlContent = sHtmlContent[:end]

    oParser = Parser()
    sPattern = 'images radius-3">.+?src="([^"]*)" alt="([^"]*).+?(?:|rip"><.+?>([^<]*).+?)link"><a href="([^"]*)'
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

            sThumb = aEntry[0]
            title = aEntry[1]
            sLang = aEntry[2]
            sUrl2 = aEntry[3]

            sDisplayTitle = ('%s (%s)') % (title, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</div></div><div class="col-lg-1 col-sm-2 col-xs-2 pages-next"><a href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'Synopsis.+?info-text">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'streamiz-filmze.org'
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = '<iframe.+?src="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry

            oHoster = HosterGui().checkHoster(sUrl)
            if (oHoster):
                hostName = oHoster.getDisplayName()
            else:
                hostName = getHostName(sUrl)

            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (title, hostName)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
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

    sHosterUrl = sUrl
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


def getHostName(url):

    try:
        if 'www' not in url:
            sHost = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        sHost = url

    return sHost.capitalize()
