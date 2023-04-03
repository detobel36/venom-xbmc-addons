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
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_MOVIES[1],
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

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS_EPISODE[0])
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
    url = input_parameter_handler.getValue('site_url')
    search_text = gui.showKeyBoard()
    if (search_text):
        url += search_text
        showMovies(url)
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
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
        year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'release-year/' + year + '/page/1/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False

    if search:
        if key_search_movies in search:
            search = search.replace(key_search_movies, '')
            bSearchMovie = True

        elif key_search_series in search:
            search = search.replace(key_search_series, '')
            bSearchSerie = True

        util = cUtil()
        search = util.CleanName(search)
        url = URL_SEARCH[0] + search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # url image alt year desc
    pattern = 'class="ml-item".+?href="([^"]+).+?src="([^"]+).+?alt="([^"]+).+?(?:|tag">([^<]*).+?)desc">(.*?)</p'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            thumb = re.sub('/w\\d+/', '/w342/', entry[1])
            title = entry[2]
            if 'episode' in url or '/series/' in url:
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
            year = entry[3]
            desc = entry[4].replace('<p>', '')

            if bSearchMovie:
                if 'series' in url2:
                    continue
            if bSearchSerie:
                if 'series' not in url2:
                    continue

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search, title):
                    continue

            if desc:
                desc = (
                    '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', desc)

            display_title = title
            if search or 'genre/' in url or 'release-year/' in url:
                if 'series' in url2:
                    display_title = display_title + ' [Série]'
                else:
                    display_title = display_title + ' [Film]'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if 'series' not in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        bvalid, next_page, sNumPage = __checkForNextPage(html_content, url)
        if (bvalid):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
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
    pattern = 'page/(\\d+)/'
    parser = Parser()
    results = parser.parse(shtml, pattern)
    if results[0]:
        for entry in results[1]:
            sCurrentMax = entry
            iCurrentMax = int(sCurrentMax)
            if iCurrentMax > iMax:
                iMax = iCurrentMax
                sMax = sCurrentMax

    pattern = 'page.(\\d+)'
    parser = Parser()
    results = parser.parse(surl, pattern)
    if results[0]:
        sCurrent = results[1][0]
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
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    # permet de couper une partie précise du code html pour récupérer plus
    # simplement les episodes.
    start = 'class="les-title"'
    end = '<div class="mvi-content"'
    html_content = parser.abParse(html_content, start, end)
    pattern = '<strong>Season.+?(\\d+)'

    results = parser.parse(html_content, pattern)
    sSaison = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sNumSaison = entry[0]
            sSaison = 'Saison ' + entry[0]
            sUrlSaison = url + "?sNumSaison=" + sNumSaison
            display_title = movie_title + ' ' + sSaison
            title = movie_title

            output_parameter_handler.addParameter('site_url', sUrlSaison)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showSXE',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    url, sNumSaison = url.split('?sNumSaison=')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    # permet de couper une partie précise du code html pour récupéré plus
    # simplement les episodes.
    start = '<strong>Season ' + sNumSaison
    end = '<div class="tvseason">'
    html_content = parser.abParse(html_content, start, end)
    pattern = '<a href="([^"]+).+?Episode.+?(\\d+)'

    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            Ep = entry[1]
            Saison = 'Saison ' + sNumSaison
            title = movie_title + ' ' + Saison + ' Episode' + Ep

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
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

    # 1 seul host constaté 10112020 : uqload

    # hoster_url = ''
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    pattern = '<div class="movieplay"><iframe src="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        if 'embedo' in results[1][0]:

            # url1 https://embedo.to/e/QW9RSEhEeEZFUTJXVXo0dzBhdzhVZz09
            # url2 https://embedo.to/s/cTJtdlNDY2J5aGM9
            # url3 https://embedo.to/r/cTJtdlNDY2J5aGM9

            url1 = results[1][0]
            request_handler = RequestHandler(url1)
            request_handler.addHeaderEntry('Referer', url)
            html_content = request_handler.request()

            pattern = 'window.park = "([^"]+)'
            results = parser.parse(html_content, pattern)

            if results[0]:
                redirect = base64.b64decode(results[1][0])
                pattern = '"page_url":"([^"]+)'
                results = parser.parse(redirect, pattern)

                if results[0]:

                    url2 = results[1][0]
                    url3 = url2.replace('\\', '').replace('/s/', '/r/')

                    request_handler = RequestHandler(url3)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry('connection', 'keep-alive')
                    html_content = request_handler.request()
                    getReal = request_handler.getRealUrl()

                    if 'http' in getReal:
                        hoster_url = getReal
                        hoster = HosterGui().checkHoster(hoster_url)
                        display_title = movie_title
                        if (hoster):
                            hoster.setDisplayName(display_title)
                            hoster.setFileName(movie_title)
                            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
