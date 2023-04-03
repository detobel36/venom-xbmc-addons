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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Populaires)',
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


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = 'menu-item-object-category menu-item-[0-9]+"><a href="([^"]+)">(.+?)<'
    results = parser.parse(html_content, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        triAlpha = []
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[1] in (
                'Liste De Films De Noël',
                'Films De Noël',
                'Top Films Streaming',
                'Top Films',
                'Prochainement',
                'Uncategorized',
                'Genres',
                    'Tendance'):
                continue

            url = entry[0]
            title = entry[1].capitalize()
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
        search_text = util.CleanName(
            search.replace(URL_SEARCH_MOVIES[0], ''))
        url = URL_SEARCH_MOVIES[0] + search_text.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'class="ml-item"> <a href="([^"]+).+?img src="([^"]*).+?alt="([^"]+).+?(?:|jtip-quality">([^<]+).+?)desc"><p>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            thumb = re.sub('/w\\d+/', '/w342/', entry[1])
            title = entry[2].replace(
                'en streaming', '').replace(
                'en steaming', '')
            qual = entry[3] if not search else ''
            desc = entry[4]

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

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

    pattern = 'link rel="next" href="([^\"]+).+?>([^<]+)</a></li></ul></nav'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_next = next_page.split('/')[-1]
        number_max = results[1][0][1].split('/')[-1]
        paging = number_next + '/' + number_max
        return next_page, str(paging)

    pattern = "active'><a class=''>[0-9]+</a></li><li><a rel='nofollow' class='page larger' href='([^']+).+?([^']+)'>Last<"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_next = next_page.split('/')[-1]
        number_max = results[1][0][1].split('/')[-1]
        paging = number_next + '/' + number_max
        return next_page, str(paging)

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'id="tab\\d".+?data-(|litespeed-)src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            hoster_url = entry[1]
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
