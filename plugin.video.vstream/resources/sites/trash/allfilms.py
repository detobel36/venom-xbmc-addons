# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


SITE_IDENTIFIER = 'allfilms'
SITE_NAME = 'All Films'
SITE_DESC = 'Films'

URL_MAIN = 'https://wvvw.allfilms.co/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche-', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-1.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'recherche-Action-1.html'])
    liste.append(['Animation', URL_MAIN + 'recherche-Animation-1.html'])
    liste.append(['Aventure', URL_MAIN + 'recherche-aventure-1.html'])
    liste.append(['Biopic', URL_MAIN + 'recherche-Biopic-1.html'])
    liste.append(['Comédie', URL_MAIN + 'recherche-Comedie-1.html'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                 'recherche-Comedie-dramatique-1.html'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 'recherche-Comedie-musicale.html'])
    liste.append(['Divers', URL_MAIN + 'recherche-Divers-1.html'])
    liste.append(['Documentaire', URL_MAIN + 'recherche-Documentaire-1.html'])
    liste.append(['Drame', URL_MAIN + 'recherche-Drame-1.html'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 'recherche-Epouvante-horreur-1.html'])
    liste.append(['Famille', URL_MAIN + 'recherche-Famille-1.html'])
    liste.append(['Fantastique', URL_MAIN + 'recherche-Fantastique-1.html'])
    liste.append(['Guerre', URL_MAIN + 'recherche-Guerre-1.html'])
    liste.append(['Opéra', URL_MAIN + 'recherche-Opera-1.html'])
    liste.append(['Policier', URL_MAIN + 'recherche-Policier-1.html'])
    liste.append(['Romance', URL_MAIN + 'recherche-romance-1.html'])
    liste.append(['Science Fiction', URL_MAIN +
                 'recherche-science-fiction-1.html'])
    liste.append(['Thriller', URL_MAIN + 'recherche-thriller-1.html'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
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

    from itertools import chain
    generator = chain([1922,
                       1929,
                       1934,
                       1936,
                       1939,
                       1942,
                       1943,
                       1944,
                       1945,
                       1947,
                       1950,
                       1952],
                      range(1953,
                            1956),
                      [1957],
                      range(1960,
                            2021))

    for i in reversed(list(generator)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'recherche-' + Year + '-1.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search.replace(' ', '-') + '.html'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="movie-card".+?src="([^"]+)".+?title">([^<]+).+?href="([^"]+)">([^<]+).+?label>([^<]+)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0].replace(' ', '%20')
            if thumb.startswith('poster'):
                thumb = URL_MAIN + thumb
            title = entry[1]
            url2 = entry[2]
            qual = entry[3].upper()
            lang = entry[4].upper()

            display_title = ('%s [%s] (%s)') % (title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        if results:
            pattern = '-(\\d+).html'
            results = parser.parse(url, pattern)
            if results[0]:
                number = int(results[1][0]) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', re.sub(
                    '-(\\d+).html', '-' + str(number) + '.html', url))

                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    '[COLOR teal]Page ' +
                    str(number) +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    pattern = 'class="lectt " src=["\']([^"]+)'

    results = parser.parse(html_content, pattern)

    # fh = open('c:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
