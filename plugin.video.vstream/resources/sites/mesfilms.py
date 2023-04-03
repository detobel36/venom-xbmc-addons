# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import SiteManager
from resources.lib.parser import Parser
from resources.lib.util import QuotePlus, cUtil

SITE_IDENTIFIER = 'mesfilms'
SITE_NAME = 'Mes Films'
SITE_DESC = 'Mes Films - Films en streaming HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'

URL_SEARCH = (URL_MAIN + '?s=', 'showSearchResult')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/?get=movies', 'showMovies')
MOVIE_CLASS = (URL_MAIN + 'films-classiques/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
# MOVIE_LIST = (True, 'showList')


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

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_CLASS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_CLASS[1],
        'Films (Classiques)',
        'star.png',
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

    # ne fonctionne plus sur le site
    # output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + QuotePlus(search_text)
        showSearchResult(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Action & aventure', 'action-adventure'], ['Animation', 'animation'],
             ['Aventure', 'aventure'], ['Comédie', 'comedie'], ['Crime', 'crime'], ['Documentaire', 'documentaire'],
             ['Drame', 'drame'], ['Etranger', 'etranger'], ['Familial', 'familial'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['News', 'news'], ['Policier', 'policier'], ['Reality', 'reality'],
             ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Science Fiction & Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Talk', 'talk'],
             ['Téléfilm', 'telefilm'], ['Thriller', 'thriller'], ['War & Politics', 'war-politics'],
             ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()

    liste = [['09', '09'], ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'],
             ['H', 'h'], ['I', 'i'], ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'],
             ['Q', 'q'], ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'],
             ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + '?letter=true&s=title-' + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1963, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'annee/' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchResult(search=''):
    gui = Gui()
    parser = Parser()
    url = search

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = util.CleanName(search_text)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'animation-2".+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?(?:|year">([^<]*)<.+?)<p>(.*?)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            thumb = re.sub(
                '/w\\d+/',
                '/w342/',
                entry[1],
                1)  # meilleure qualité
            title = entry[2].replace(': Season', ' Saison')
            year = entry[3]
            if year != '':  # on ne récupere que l'année
                year = re.search('(\\d{4})', year).group(1)
            desc = entry[4]

            # on ne recherche que des films même si séries et animés disponible
            if '/film/' not in url:
                continue

            # Filtrer les résultats
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            # permet à addMovie d'afficher l'année en Meta
            output_parameter_handler.addParameter('year', year)

            gui.addMovie(SITE_IDENTIFIER, 'showLinks', title, '',
                         thumb, desc, output_parameter_handler)


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'poster">\n*<[^<>]+src="([^"]+)" alt="([^"]+).+?(?:|quality">([^<]+).+?)href="([^"]+).+?<span>([^<]+).+?(texto">(.*?)<|<\\/article)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            thumb = re.sub(
                '/w\\d+/',
                '/w342/',
                entry[0],
                1)  # ameliore la qualité
            title = entry[1]
            qual = entry[2]
            url2 = entry[3]
            year = entry[4]
            desc = ''  # cas ou la sdesc n'est pas presente
            if entry[6]:
                desc = entry[6]
            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class="pagination"><span>Page.+?de ([^<]+).+?href="([^"]+)"><i id=.nextpagination'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showLinks(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    try:
        pattern = 'og:description" content="(.+?)" /><meta'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = "type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+)</span>\\s*<span class='server'>([^<]+)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            _type = entry[0]
            sPost = entry[1]
            sNume = entry[2]
            qual = entry[3]
            host = re.sub('\\.\\w+', '', entry[4]).capitalize()
            if 'Youtube' in host:
                continue

            title = (
                '%s [%s] [COLOR coral]%s[/COLOR]') % (movie_title, qual, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('_type', _type)
            output_parameter_handler.addParameter('sPost', sPost)
            output_parameter_handler.addParameter('sNume', sNume)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    _type = input_parameter_handler.getValue('_type')
    sPost = input_parameter_handler.getValue('sPost')
    sNume = input_parameter_handler.getValue('sNume')

    # trouve la vraie url
    request_handler = RequestHandler(URL_MAIN)
    request_handler.request()
    url2 = request_handler.getRealUrl() + 'wp-admin/admin-ajax.php'

    request_handler = RequestHandler(url2)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    request_handler.addParameters('action', 'doo_player_ajax')
    request_handler.addParameters('type', _type)
    request_handler.addParameters('post', sPost)
    request_handler.addParameters('nume', sNume)
    html_content = request_handler.request()
    pattern = "(http[^'\"]+)"
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
