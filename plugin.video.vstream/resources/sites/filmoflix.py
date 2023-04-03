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
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Series',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Série (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFR[0])
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
    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
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
    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Série(Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFR[1],
        'Série(VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = key_search_series + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = key_search_movies + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = search_text
        showMovies(url)
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    bSearchMovie = False
    bSearchSerie = False

    if search:
        search = search.replace(' ', '+').replace('%20', '+')
        if key_search_movies in search:
            search = search.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in search:
            search = search.replace(key_search_series, '')
            bSearchSerie = True

        pdata = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + search
        request = RequestHandler(URL_SEARCH[0])
        request.setRequestType(1)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(pdata)
        html_content = request.request()

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # ref thumb title years
    pattern = 'class="th-item".+?.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]*).+?Date.+?<.span>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            thumb = entry[1]
            if 'http' not in thumb:
                thumb = URL_MAIN[:-1] + thumb
            title = entry[2]
            year = entry[3].strip()

            if bSearchMovie:
                if '/serie' in url2:
                    continue
            if bSearchSerie:
                if '/serie' not in url2:
                    continue

            display_title = title
            if search and not bSearchMovie and not bSearchSerie:
                if '/serie' in url2:
                    display_title = display_title + ' {Série}'
                else:
                    display_title = display_title + ' {Film}'

            display_title = display_title + ' (' + year + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if '/series' not in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovieLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    else:
        gui.addText(SITE_IDENTIFIER)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()

    pattern = 'navigation.+?<span>\\d+</span> <a href="([^"]+).+?>([^<]+)</a></div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'property="og:description".+?content="([^"]+)'
    results = parser.parse(html_content, pattern)
    desc = 'FilmoFlix'
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', results[1][0])

    pattern = 'th-item">.+?href="([^"]*).+?src="([^"]*).+?title.+?>([^<]*)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):

            url2 = entry[0]
            thumb = entry[1]
            if 'http' not in thumb:
                thumb = URL_MAIN[:-1] + thumb
            sSaison = entry[2]  # SAISON 2

            title = ("%s %s") % (movie_title, sSaison)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', title)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    start = 'class="saisontab'
    end = 'class="clearfix'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+).+?fsa-ep">([^<]*)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            sEpisode = entry[1].replace('é', 'e').strip()  # épisode 2
            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2
            title = movie_title + ' ' + sEpisode

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSerieLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showSerieLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    cook = request_handler.GetCookies()

    pattern = "class=\"lien.+?playEpisode.+?\'([^\']*).+?'([^\']*)"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            videoId = entry[0]
            xfield = entry[1]
            hosterName = xfield.replace(
                '_',
                ' ').capitalize().replace(
                'vf',
                '(VF)').replace(
                'vostfr',
                '(VOSTFR)')

            postdata = 'id=' + videoId + '&xfield=' + xfield + '&action=playEpisode'
            url2 = URL_MAIN + 'engine/inc/serial/app/ajax/Season.php'

            display_title = (
                '%s [COLOR coral]%s[/COLOR]') % (title, hosterName)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('cook', cook)
            output_parameter_handler.addParameter('postdata', postdata)

            gui.addLink(
                SITE_IDENTIFIER,
                'showSerieHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSerieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    # cook = input_parameter_handler.getValue('cook')
    postdata = input_parameter_handler.getValue('postdata')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    # request.addHeaderEntry('Cookie', cook) # pas besoin ici mais besoin
    # pour les films
    request.addParametersLine(postdata)
    html_content = request.request()

    parser = Parser()
    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        hoster_url = results[1][0]
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showMovieLinks(input_parameter_handler=False):

    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    cook = request_handler.GetCookies()

    parser = Parser()
    pattern = 'text clearfix">([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'FilmoFlix'
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', results[1][0])

    pattern = "lien fx-row.+?\"getxfield.+?(\\d+).+?\'([^\']*).+?'([^\']*).+?images.([^\\.]+).+?pl-5\">([^<]+)"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            videoId = entry[0]
            xfield = entry[1]
            token = entry[2]
            # images :entry[3] (VF).png
            qual = entry[4]
            hosterName = xfield.replace(
                '_',
                ' ').capitalize().replace(
                'vf',
                '(VF)').replace(
                'vostfr',
                '(VOSTFR)')

            url2 = URL_MAIN + 'engine/ajax/getxfield.php?id=' + \
                videoId + '&xfield=' + xfield + '&token=' + token

            display_title = (
                '%s [%s] [COLOR coral]%s[/COLOR]') % (title, qual, hosterName)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('cook', cook)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showMovieHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    cook = input_parameter_handler.getValue('cook')

    request = RequestHandler(url)
    request.addHeaderEntry('Referer', referer)
    if cook:
        request.addHeaderEntry('Cookie', cook)
    html_content = request.request()

    parser = Parser()
    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        hoster_url = results[1][0]
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
