# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.comaddon import Progress
import base64
import re
return False  # 11/02/22 - Plus de liens


SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Films toon'
SITE_DESC = 'Films en streaming'

URL_MAIN = "https://filmstoon.in/"

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'movies/page/1/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

# on rajoute le tag page/1/ sur les premieres pages, utilisé par la
# fonction nextpage pas de liens next
SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/page/1/', 'showMovies')
SERIE_NEWS_EPISODE = (URL_MAIN + 'episode/page/1/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

# variables globales
key_search_movies = '#searchsomemovies#'
key_search_series = '#searchsomeseries#'
URL_SEARCH_MOVIES = (key_search_movies, 'showSearch')
URL_SEARCH_SERIES = (key_search_series, 'showSearch')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_MOVIES[1],
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

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS_EPISODE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_EPISODE[1],
        'Episodes (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl += sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    # https://filmstoon.in/genre/action/

    liste = []
    listegenre = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'Documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'horreur',
        'musique',
        'romance',
        'thriller',
        'science-fiction']

    url1g = URL_MAIN + 'genre/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre + '/page/1/'])

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
    # https://filmstoon.in/release-year/2020/
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1935, 2023)):
        sYear = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'release-year/' + sYear + '/page/1/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False

    if sSearch:
        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True

        elif key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch)
        sUrl = URL_SEARCH[0] + sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url image alt year desc
    sPattern = 'class="ml-item".+?href="([^"]+).+?src="([^"]+).+?alt="([^"]+).+?(?:|tag">([^<]*).+?)desc">(.*?)</p'
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

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[1])
            title = aEntry[2]
            if 'episode' in sUrl or '/series/' in sUrl:
                title = title.replace(
                    '- Season',
                    ' ').replace(
                    '-Season',
                    ' ').replace(
                    'Season',
                    '').replace(
                    '- Saison',
                    '')
                title = re.sub('\\d+', '', title)
            sYear = aEntry[3]
            desc = aEntry[4].replace('<p>', '')

            if bSearchMovie:
                if 'series' in sUrl2:
                    continue
            if bSearchSerie:
                if 'series' not in sUrl2:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearch, title):
                    continue

            if desc:
                desc = (
                    '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', desc)

            sDisplayTitle = title
            if sSearch or 'genre/' in sUrl or 'release-year/' in sUrl:
                if 'series' in sUrl2:
                    sDisplayTitle = sDisplayTitle + ' [Série]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [Film]'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)

            if 'series' not in sUrl2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalid, sNextPage, sNumPage = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalid):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(shtml, surl):
    # pas de lien next page on crée l'url et on verifie l'index de la derniere
    # page
    sMax = ''
    iMax = 0
    sPattern = 'page/(\\d+)/'
    oParser = Parser()
    aResult = oParser.parse(shtml, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sCurrentMax = aEntry
            iCurrentMax = int(sCurrentMax)
            if iCurrentMax > iMax:
                iMax = iCurrentMax
                sMax = sCurrentMax

    sPattern = 'page.(\\d+)'
    oParser = Parser()
    aResult = oParser.parse(surl, sPattern)
    if aResult[0]:
        sCurrent = aResult[1][0]
        iCurrent = int(sCurrent)
        iNext = iCurrent + 1
        sNext = str(iNext)
        pCurrent = 'page/' + sCurrent
        pNext = 'page/' + sNext
        sUrlNext = surl.replace(pCurrent, pNext)

    else:
        return False, False, False

    if iMax != 0 and iMax >= iNext:
        return True, sUrlNext, sNext + '/' + sMax

    elif iNext == 0:  # c'est un bug de programmation
        return False, False, False

    return False, False, False


def showSaison():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    # permet de couper une partie précise du code html pour récupérer plus
    # simplement les episodes.
    sStart = 'class="les-title"'
    sEnd = '<div class="mvi-content"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<strong>Season.+?(\\d+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sNumSaison = aEntry[0]
            sSaison = 'Saison ' + aEntry[0]
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            sDisplayTitle = sMovieTitle + ' ' + sSaison
            title = sMovieTitle

            output_parameter_handler.addParameter('siteUrl', sUrlSaison)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showSXE',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    # permet de couper une partie précise du code html pour récupéré plus
    # simplement les episodes.
    sStart = '<strong>Season ' + sNumSaison
    sEnd = '<div class="tvseason">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="([^"]+).+?Episode.+?(\\d+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            Ep = aEntry[1]
            Saison = 'Saison ' + sNumSaison
            title = sMovieTitle + ' ' + Saison + ' Episode' + Ep

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
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

    # 1 seul host constaté 10112020 : uqload

    # sHosterUrl = ''
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    sPattern = '<div class="movieplay"><iframe src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        if 'embedo' in aResult[1][0]:

            # url1 https://embedo.to/e/QW9RSEhEeEZFUTJXVXo0dzBhdzhVZz09
            # url2 https://embedo.to/s/cTJtdlNDY2J5aGM9
            # url3 https://embedo.to/r/cTJtdlNDY2J5aGM9

            url1 = aResult[1][0]
            oRequestHandler = RequestHandler(url1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'window.park = "([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                redirect = base64.b64decode(aResult[1][0])
                sPattern = '"page_url":"([^"]+)'
                aResult = oParser.parse(redirect, sPattern)

                if aResult[0]:

                    url2 = aResult[1][0]
                    url3 = url2.replace('\\', '').replace('/s/', '/r/')

                    oRequestHandler = RequestHandler(url3)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('connection', 'keep-alive')
                    sHtmlContent = oRequestHandler.request()
                    getReal = oRequestHandler.getRealUrl()

                    if 'http' in getReal:
                        sHosterUrl = getReal
                        oHoster = HosterGui().checkHoster(sHosterUrl)
                        sDisplayTitle = sMovieTitle
                        if (oHoster):
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
