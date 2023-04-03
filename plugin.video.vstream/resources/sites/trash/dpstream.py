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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
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

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
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
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
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
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = MY_SEARCH_SERIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = MY_SEARCH_MOVIES[0] + search_text
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
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

        bvalid, sToken, sCookie = getTokens()
        if bvalid:
            util = cUtil()
            search_text = search.replace(URL_SEARCH_MOVIES[0], '')
            search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
            search_text = util.CleanName(search_text)

            pData = '_token=' + sToken + '&search=' + search
            url = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
            request_handler = RequestHandler(url)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', URL_MAIN)
            request_handler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            request_handler.addHeaderEntry('Cookie', sCookie)
            request_handler.addParametersLine(pData)
            html_content = request_handler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # ref thumb title year
    pattern = 'class="item mb-4">.+?ref="([^"]*).+?src="([^"]*).+?pt-2">([^<]*).+?muted">([^<]*).*?type">([^<]*)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            thumb = re.sub('/w\\d+/', '/w342/', entry[1])
            # .split(' en streaming')[0].split('streaming | ')[1]
            title = entry[2].strip()
            year = entry[3]
            _type = entry[4].lower()

            if bSearchMovie:
                if _type == 'serie':
                    continue
            if bSearchSerie:
                if _type == 'film':
                    continue

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue  # Filtre de recherche

            display_title = title + '(' + year + ')'

            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2

            if search and not bSearchMovie and not bSearchSerie:
                display_title = display_title + ' [' + entry[4] + ']'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if search:
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showSelectType',
                    display_title,
                    thumb,
                    '',
                    output_parameter_handler,
                    input_parameter_handler)
            elif SERIE_NEWS[0] not in url:
                output_parameter_handler.addParameter('year', year)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                display_title = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '>([^<]+)</a></li><li class="page-item"><a class="page-link" href="([^"]+)">(?!\\d)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSelectType(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    html_content = request.request()

    parser = Parser()
    pattern = 'mb-3 d-block">([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'no description'

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', movie_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('year', year)

    # (a modifier car ce n'est plus le cas)
    # dans le cas d'une recherche on ne sait pas si c'est un film ou une serie
    # class="description">.*?<br>([^<]+)

    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    if '<meta name=description content="serie' in html_content:
        gui.addTV(
            SITE_IDENTIFIER,
            'showSaisons',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)
    else:
        gui.addMovie(
            SITE_IDENTIFIER,
            'showLinks',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'mb-3 d-block">([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'no description'
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = 'class="seasonbar.+?href="([^"]+).+?arrow-right.+?>(\\d+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            saison = entry[1]

            title = ("%s %s") % (movie_title, ' Saison ' + saison)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

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

    iSaison = ''
    pattern = 'saison.(.+?)'
    results = parser.parse(url, pattern)
    if results[0]:
        iSaison = ' Saison ' + results[1][0]

    pattern = 'class="seasonbar".+?href="([^"]+).+?rrow-right"><.span>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            nEpisode = entry[1]

            title = movie_title + iSaison + ' episode' + nEpisode

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()

    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    html_content = request.request()

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if '<meta name=description content="serie' in html_content and 'episode' not in url:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('desc', desc)
        gui.addTV(
            SITE_IDENTIFIER,
            'showSaisons',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)

        gui.setEndOfDirectory()
        return

    pattern = 'mb-3 d-block">([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'no description'
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    # p-1 movie p-2 serie
    pattern = 'data-url="([^"]+).+?class="p-.+?alt="([^"]+).+?alt="([^"]+)'
    results = parser.parse(html_content, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            key = entry[0]
            host = re.sub('www.', '', entry[1])
            host = re.sub('embed.mystream.to', 'mystream', host)
            host = re.sub('\\.\\w+', '', host).capitalize()
            lang = entry[2].upper()
            url2 = URL_MAIN + 'll/captcha?hash=' + key

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('lang', lang)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe.*?src=([^\\s]+)'
    results = re.findall(pattern, html_content)
    if results:
        hoster_url = results[0]
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getTokens():
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = request_handler.getResponseHeader()
    pattern = 'name=_token.+?value="([^"]+).+?<div class="typeahead'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        token = results[1][0]

    pattern = 'XSRF-TOKEN=([^;]+).+?dpstream_session=([^;]+)'
    results = parser.parse(sHeader, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        XSRF_TOKEN = results[1][0][0]
        site_session = results[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; dpstream_session=' + site_session + ';'
    return True, token, cook
