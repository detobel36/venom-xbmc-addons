# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import Unquote
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import re
return False  # Sous Cloudflare 14/10/2021


SITE_IDENTIFIER = 'enstream'
SITE_NAME = 'Enstream'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = "https://www.enstream.club/"

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (True, 'showAlpha')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
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

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Ordre alphabétique)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Comédie Dramatique', 'comedie-dramatique'],
             ['Comédie Musicale', 'comedie-musical'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'],
             ['Historique', 'historique'], ['Judiciaire', 'judiciaire'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

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


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1942, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'Annee/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0-9', ''], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F'], ['G', 'G'],
             ['H', 'H'], ['I', 'I'], ['J', 'J'], ['K', 'K'], ['L', 'L'], ['M', 'M'], ['N', 'N'], ['O', 'O'],
             ['P', 'P'], ['Q', 'Q'], ['R', 'R'], ['S', 'S'], ['T', 'T'], ['U', 'U'], ['V', 'V'], ['W', 'W'],
             ['X', 'X'], ['Y', 'Y'], ['Z', 'Z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'ABC/' + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    if search:
        url = URL_MAIN + 'search.php'
        request_handler = RequestHandler(url)
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addParameters('q', Unquote(search))
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)

    request_handler.addHeaderEntry('Referer', URL_MAIN)
    html_content = request_handler.request()

    if search:
        pattern = '<a href="([^"]+).+?url\\((.+?)\\).+?<div class="title"> (.+?) </div>'
    elif 'Annee/' in url or '/ABC' in url:
        pattern = '<div class="table-movies-content.+?href="([^"]+).+?url\\((.+?)\\).+?<.i>.([^<]+)'
    elif 'genre/' in url:
        pattern = 'film-uno.+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+)'
    else:
        pattern = 'class="film-uno".+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+).+?min.+?·([^<]+).+?short-story">([^<]*)'

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

            url = entry[0]
            thumb = entry[1]
            title = entry[2]
            desc = ''
            if len(entry) > 3:
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    qual = entry[3].split('·')[1].replace('Â', '').strip()
                    lang = entry[3].split('·')[2].strip()
                else:
                    qual = entry[3].split('·')[1].strip()
                    lang = entry[3].split('·')[2].strip()

                desc = entry[4]

                display_title = ('%s [%s] (%s)') % (title, qual, lang)
                output_parameter_handler.addParameter('qual', qual)

            else:
                display_title = title

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHoster',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)
        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            # sNumPage = re.search('(page|genre).*?[-=\/]([0-9]+)',
            # next_page).group(2)  # ou replace'.html',''; '([0-9]+)$'
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class=\'Paginaactual\'.+?a href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search(
            '(page|genre).*?[-=\\/]([0-9]+)',
            next_page).group(2)
        paging = number_next + '/' + number_max
        return next_page, paging

    pattern = '<span>\\d+</span>.+?href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search(
            '(page|genre).*?[-=\\/]([0-9]+)',
            next_page).group(2)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHoster(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-url="([^"]+)".+?data-code="([^"]+)".+?mobile">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sDataUrl = entry[0]
            sDataCode = entry[1]
            host = entry[2].capitalize()

            # filtrage des hosters
            hoster = HosterGui().checkHoster(host)
            if not hoster:
                continue

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)
            lien = URL_MAIN + 'video/' + sDataCode + '/recaptcha/' + sDataUrl

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', lien)
            output_parameter_handler.addParameter('referer', url)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersLinks',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    pattern = "class=.download.+?href='/([^']*).+?mobile.>([^<]+)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            lien = URL_MAIN + entry[0]
            host = entry[1].capitalize()
            hoster = HosterGui().checkHoster(host)
            if not hoster:
                continue

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', lien)
            output_parameter_handler.addParameter('referer', url)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersLinks',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHostersLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', referer)

    request_handler.request()
    hoster_url = request_handler.getRealUrl()
    hoster = HosterGui().checkHoster(hoster_url)

    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
