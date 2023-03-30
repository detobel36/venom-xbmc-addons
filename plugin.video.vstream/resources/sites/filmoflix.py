# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # CF depuis le 26/11/2020
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'filmoflix'
SITE_NAME = 'Filmoflix'
SITE_DESC = ' films et series'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'filmsenstreaming/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'seriesenstreaming/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VF = (URL_MAIN + 'seriesenstreaming/series-vf/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'seriesenstreaming/series-vostfr/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisé quand on n'utilise pas le globale
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Series',
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
        'Série (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFR[1],
        'Série (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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
        'Recherche Séries',
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
        'Série(Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFR[1],
        'Série(VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_movies + sSearchText
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


def showMovieGenres():
    showGenres(URL_MAIN + 'filmsenstreaming/', '')


def showSerieGenres():
    showGenres(URL_MAIN + 'seriesenstreaming/', '-s')


def showGenres(urltype, s):
    gui = Gui()

    liste = []
    listegenre = [
        'action',
        'animation',
        'aventure',
        'biopic',
        'comedie',
        'drame',
        'documentaire',
        'epouvante-horreur',
        'espionnage',
        'famille',
        'fantastique',
        'guerre',
        'historique',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    # https://www.filmoflix.net/filmsenstreaming/action/
    # https://www.filmoflix.net/seriesenstreaming/action-s/

    for igenre in listegenre:
        liste.append([igenre.capitalize(), urltype + igenre + s + '/'])

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

        pdata = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + sSearch
        oRequest = RequestHandler(URL_SEARCH[0])
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # ref thumb title years
    sPattern = 'class="th-item".+?.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]*).+?Date.+?<.span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            title = aEntry[2]
            sYear = aEntry[3].strip()

            if bSearchMovie:
                if '/serie' in sUrl2:
                    continue
            if bSearchSerie:
                if '/serie' not in sUrl2:
                    continue

            sDisplayTitle = title
            if sSearch and not bSearchMovie and not bSearchSerie:
                if '/serie' in sUrl2:
                    sDisplayTitle = sDisplayTitle + ' {Série}'
                else:
                    sDisplayTitle = sDisplayTitle + ' {Film}'

            sDisplayTitle = sDisplayTitle + ' (' + sYear + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/series' not in sUrl2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovieLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

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

    sPattern = 'navigation.+?<span>\\d+</span> <a href="([^"]+).+?>([^<]+)</a></div>'
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
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'property="og:description".+?content="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'FilmoFlix'
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResult[1][0])

    sPattern = 'th-item">.+?href="([^"]*).+?src="([^"]*).+?title.+?>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            sSaison = aEntry[2]  # SAISON 2

            title = ("%s %s") % (sMovieTitle, sSaison)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', title)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

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

    sStart = 'class="saisontab'
    sEnd = 'class="clearfix'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+).+?fsa-ep">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sEpisode = aEntry[1].replace('é', 'e').strip()  # épisode 2
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2
            title = sMovieTitle + ' ' + sEpisode

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSerieLinks',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showSerieLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    sPattern = "class=\"lien.+?playEpisode.+?\'([^\']*).+?'([^\']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            videoId = aEntry[0]
            xfield = aEntry[1]
            hosterName = xfield.replace(
                '_',
                ' ').capitalize().replace(
                'vf',
                '(VF)').replace(
                'vostfr',
                '(VOSTFR)')

            postdata = 'id=' + videoId + '&xfield=' + xfield + '&action=playEpisode'
            sUrl2 = URL_MAIN + 'engine/inc/serial/app/ajax/Season.php'

            sDisplayTitle = (
                '%s [COLOR coral]%s[/COLOR]') % (title, hosterName)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('cook', cook)
            output_parameter_handler.addParameter('postdata', postdata)

            gui.addLink(
                SITE_IDENTIFIER,
                'showSerieHosters',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSerieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    # cook = input_parameter_handler.getValue('cook')
    postdata = input_parameter_handler.getValue('postdata')

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    # oRequest.addHeaderEntry('Cookie', cook) # pas besoin ici mais besoin
    # pour les films
    oRequest.addParametersLine(postdata)
    sHtmlContent = oRequest.request()

    oParser = Parser()
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


def showMovieLinks(input_parameter_handler=False):

    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    oParser = Parser()
    sPattern = 'text clearfix">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'FilmoFlix'
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResult[1][0])

    sPattern = "lien fx-row.+?\"getxfield.+?(\\d+).+?\'([^\']*).+?'([^\']*).+?images.([^\\.]+).+?pl-5\">([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            videoId = aEntry[0]
            xfield = aEntry[1]
            token = aEntry[2]
            # images :aEntry[3] (VF).png
            sQual = aEntry[4]
            hosterName = xfield.replace(
                '_',
                ' ').capitalize().replace(
                'vf',
                '(VF)').replace(
                'vostfr',
                '(VOSTFR)')

            sUrl2 = URL_MAIN + 'engine/ajax/getxfield.php?id=' + \
                videoId + '&xfield=' + xfield + '&token=' + token

            sDisplayTitle = (
                '%s [%s] [COLOR coral]%s[/COLOR]') % (title, sQual, hosterName)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('cook', cook)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showMovieHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    cook = input_parameter_handler.getValue('cook')

    oRequest = RequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', referer)
    if cook:
        oRequest.addHeaderEntry('Cookie', cook)
    sHtmlContent = oRequest.request()

    oParser = Parser()
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
