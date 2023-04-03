# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'psyplay'
SITE_NAME = 'Psy Play'
SITE_DESC = 'stream HD, streaming Sans pub, streaming vf'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming-10', 'showMovies')
MOVIE_SANTA = (URL_MAIN + 'liste-de-films-de-noel', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'top-films-streaming-10', 'showMovies')
MOVIE_IMDB = (URL_MAIN + 'top-imdb', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = ('http://', 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SANTA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SANTA[1],
        'Films de Noël',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_IMDB[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_IMDB[1],
        'Films (Top IMDB)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SANTA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SANTA[1],
        'Films de Noël',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_IMDB[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_IMDB[1],
        'Films (Top IMDB)',
        'star.png',
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
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_MOVIES[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = 'category menu-item.+?href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if ('liste-de-films-de-noel' in entry[0]
                    ) or ('top-films-streaming-10' in entry[0]):
                continue

            url = entry[0]
            title = entry[1].capitalize().replace('Co-', 'Comédie-')
            triAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        for title, url in triAlpha:
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
    if search:
        util = cUtil()
        url = search
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = util.CleanName(search_text)
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'ml-item">.+?href="([^"]+).+?(?:|quality">([^<]*).+?)src="([^"]+).+?alt="([^"]+).+?(?:|tag">([^<]*).+?)desc">(.*?)</'
    parser = Parser()
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
            qual = entry[1]
            thumb = re.sub('/w\\d+/', '/w342/', entry[2])
            title = entry[3].replace(
                ' en streaming',
                '').replace(
                ' en Streaming',
                '').replace(
                ' Streaming',
                '') .replace(
                ' streaming',
                '').replace(
                    ' Straming',
                    '').replace(
                        'Version Francais',
                'VF')
            if '/series' in url2:
                title = re.sub('Episode \\d+', '', title)

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue  # Filtre de recherche

            year = entry[4]
            desc = entry[5].replace('<p>', '')

            display_title = ('%s [%s] (%s)') % (title, qual, year)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            if '/series' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
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
    pattern = "<a class=''>.+?href='([^']+).+?/(\\d+)'>Last"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    pattern = "<a class=''>.+?href='([^']+).+?>(\\d+)</a></li>"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    # Uniquement saison a chaque fois
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    start = '<i class="fa fa-server mr5">'
    end = '<noscript>'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            title = movie_title + entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
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
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'iframe src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
