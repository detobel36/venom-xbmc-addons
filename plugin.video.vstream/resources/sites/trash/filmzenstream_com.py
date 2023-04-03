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
import re
return False  # 25/12/2020


SITE_IDENTIFIER = 'filmzenstream_com'
SITE_NAME = 'Filmzenstream'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = 'https://filmzenstream.xyz/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'Categorie/action/'])
    liste.append(['Animation', URL_MAIN + 'Categorie/animation/'])
    liste.append(['Aventure', URL_MAIN + 'Categorie/aventure/'])
    liste.append(['Biographie', URL_MAIN + 'Categorie/biography/'])
    liste.append(['Comédie', URL_MAIN + 'Categorie/comedie/'])
    liste.append(['Crime', URL_MAIN + 'Categorie/crime/'])
    liste.append(['Drame', URL_MAIN + 'Categorie/drame/'])
    liste.append(['Documentaire', URL_MAIN + 'Categorie/documentaire/'])
    liste.append(['Famille', URL_MAIN + 'Categorie/famille/'])
    liste.append(['Fantaisie', URL_MAIN + 'Categorie/fantaisie/'])
    # liste.append(['Guerre', URL_MAIN + 'Categorie/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'Categorie/history/'])
    liste.append(['Horreur', URL_MAIN + 'Categorie/horreur/'])
    liste.append(['Musical', URL_MAIN + 'Categorie/musique/'])
    liste.append(['Mystère', URL_MAIN + 'Categorie/mystere/'])
    liste.append(['Romance', URL_MAIN + 'Categorie/romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'Categorie/science-fiction/'])
    liste.append(['Sport', URL_MAIN + 'Categorie/sport/'])
    liste.append(['Thriller', URL_MAIN + 'Categorie/thriller/'])
    liste.append(['War', URL_MAIN + 'Categorie/war/'])

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

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2017, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'Categorie/' + Year + '-films/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        search = Unquote(search)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'href="([^"]+)" title="([^"]+)".+?src="([^"]+)'
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
            title = entry[1]
            thumb = entry[2]
            if thumb.startswith('//'):
                thumb = 'http:' + thumb

            title = title.replace(' VF Streaming', '')

            year = None
            if len(title) > 4 and title[-4:].isdigit():
                year = title[-4:]
                title = title[0:len(title) - 4] + '(' + year + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            if year:
                output_parameter_handler.addParameter('year', year)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = 'href="([^"]+?)" class="next">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<iframe[^<>]+?(?:data-)*data-src="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            if 'belike' in entry:
                if entry.startswith('/'):
                    request_handler = RequestHandler('https:' + entry)
                else:
                    request_handler = RequestHandler(entry)

                request_handler.request()
                hoster_url = request_handler.getRealUrl()

            # pour récuperer le lien Downpit
            elif 'downpit' in entry:
                request_handler = RequestHandler(entry)
                html_content = request_handler.request()
                pattern = '<iframe.+?src="([^"]+)"'
                results = parser.parse(html_content, pattern)
                if results[0]:
                    for entry in results[1]:
                        hoster_url = entry

            else:
                hoster_url = entry
                # Vire les bandes annonces
                if 'youtube.com' in entry:
                    continue

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
