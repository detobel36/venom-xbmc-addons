# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'dpstream'
SITE_NAME = 'DpStream'
SITE_DESC = 'Series et Films en VF ou VOSTFR '

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VIEWS = (URL_MAIN + 'films-box-office', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showMovies')
SERIE_GENRES = (True, 'showSeriesGenres')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')

# recherche utilisé quand on n'utilise pas le globale
MY_SEARCH_MOVIES = (key_search_movies, 'showSearchMovie')
MY_SEARCH_SERIES = (key_search_series, 'showSearchSerie')

FUNCTION_SEARCH = 'showMovies'

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
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
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films ',
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
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = MY_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = MY_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
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
        'soap',
        'science-fiction-fantastique',
        'talk',
        'telefilm',
        'thriller',
        'politics',
        'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'categories/' + igenre])

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


def showSeriesGenres():
    gui = Gui()

    liste = []
    listegenre = [
        'action',
        'action-adventure',
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
        'news',
        'reality',
        'romance',
        'science-fiction',
        'soap',
        'science-fiction-fantastique',
        'talk',
        'thriller',
        'politics',
        'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN +
                     'categories/' + igenre + '/series'])

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


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        bvalid, sToken, sCookie = getTokens()
        if bvalid:
            oUtil = cUtil()
            sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
            sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
            sSearchText = oUtil.CleanName(sSearchText)

            pData = '_token=' + sToken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
            oRequestHandler = RequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Cookie', sCookie)
            oRequestHandler.addParametersLine(pData)
            sHtmlContent = oRequestHandler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # ref thumb title year
    sPattern = 'class="item mb-4">.+?ref="([^"]*).+?src="([^"]*).+?pt-2">([^<]*).+?muted">([^<]*).*?type">([^<]*)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[1])
            # .split(' en streaming')[0].split('streaming | ')[1]
            title = aEntry[2].strip()
            sYear = aEntry[3]
            sType = aEntry[4].lower()

            if bSearchMovie:
                if sType == 'serie':
                    continue
            if bSearchSerie:
                if sType == 'film':
                    continue

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue  # Filtre de recherche

            sDisplayTitle = title + '(' + sYear + ')'

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if sSearch and not bSearchMovie and not bSearchSerie:
                sDisplayTitle = sDisplayTitle + ' [' + aEntry[4] + ']'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if sSearch:
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showSelectType',
                    sDisplayTitle,
                    sThumb,
                    '',
                    output_parameter_handler,
                    input_parameter_handler)
            elif SERIE_NEWS[0] not in sUrl:
                output_parameter_handler.addParameter('sYear', sYear)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                sDisplayTitle = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
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
    sPattern = '>([^<]+)</a></li><li class="page-item"><a class="page-link" href="([^"]+)">(?!\\d)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSelectType(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = Parser()
    sPattern = 'mb-3 d-block">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'no description'

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('sYear', sYear)

    # (a modifier car ce n'est plus le cas)
    # dans le cas d'une recherche on ne sait pas si c'est un film ou une serie
    # class="description">.*?<br>([^<]+)

    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    if '<meta name=description content="serie' in sHtmlContent:
        gui.addTV(
            SITE_IDENTIFIER,
            'showSaisons',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)
    else:
        gui.addMovie(
            SITE_IDENTIFIER,
            'showLinks',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'mb-3 d-block">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'no description'
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = 'class="seasonbar.+?href="([^"]+).+?arrow-right.+?>(\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            saison = aEntry[1]

            title = ("%s %s") % (sMovieTitle, ' Saison ' + saison)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
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
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    iSaison = ''
    sPattern = 'saison.(.+?)'
    aResult = oParser.parse(sUrl, sPattern)
    if aResult[0]:
        iSaison = ' Saison ' + aResult[1][0]

    sPattern = 'class="seasonbar".+?href="([^"]+).+?rrow-right"><.span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            nEpisode = aEntry[1]

            title = sMovieTitle + iSaison + ' episode' + nEpisode

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
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

    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if '<meta name=description content="serie' in sHtmlContent and 'episode' not in sUrl:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('desc', desc)
        gui.addTV(
            SITE_IDENTIFIER,
            'showSaisons',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

        gui.setEndOfDirectory()
        return

    sPattern = 'mb-3 d-block">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'no description'
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # p-1 movie p-2 serie
    sPattern = 'data-url="([^"]+).+?class="p-.+?alt="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sKey = aEntry[0]
            sHost = re.sub('www.', '', aEntry[1])
            sHost = re.sub('embed.mystream.to', 'mystream', sHost)
            sHost = re.sub('\\.\\w+', '', sHost).capitalize()
            sLang = aEntry[2].upper()
            sUrl2 = URL_MAIN + 'll/captcha?hash=' + sKey

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addMovie(
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
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.*?src=([^\\s]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getTokens():
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'name=_token.+?value="([^"]+).+?<div class="typeahead'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?dpstream_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; dpstream_session=' + site_session + ';'
    return True, token, cook
