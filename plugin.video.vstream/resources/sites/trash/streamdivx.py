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

"""
Pour rappel.
Problème avec les DNS en ipv6 il faut utiliser les suivantes
CloudFlare DNS:
Préféré : 2606:4700:4700::1111
Auxiliaire : 2606:4700:4700::1001
Ou:
Google DNS:
Préféré : 2001:4860:4860::8888
Auxiliaire : 2001:4860:4860::8844
"""


# from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamdivx'
SITE_NAME = 'StreamDivx'
SITE_DESC = 'Regarder, Voir Films En Streaming VF 100% Gratuit.'

# ou 'https://www.voustreaming.com/' < recherche hs
URL_MAIN = 'https://wvvw.streamdivx.net/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'tags/', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        search_text = search_text.replace(' ', '+')
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Musicale', 'comedie-musicale'], ['Drame', 'drame'], ['Documentaire', 'documentaire'],
             ['Epouvante Horreur', 'epouvante-horreur'], ['Erotique', 'erotique'], ['Espionnage', 'espionnage'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Judiciaire', 'judiciaire'], ['Musical', 'musical'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1985, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'tags/' + Year + '/')
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
        url = search
        request = RequestHandler(url)
        html_content = request.request()
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        if '<h2 class="side-title nop">film du moment</h2>' in html_content:
            start = '<div class="films-group small'
            end = '<div class="side-title">films par Genres'
            html_content = parser.abParse(html_content, start, end)
        else:
            html_content = html_content

    pattern = 'class="film-uno *">.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+).+?class="quality ">([^<]+).+?class="nop short-story *">(.+?)</p>'
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
            title = entry[2]  # .decode("unicode_escape").encode("latin-1")
            qual = entry[3]
            desc = entry[4]
            display_title = ('%s [%s]') % (title, qual)

            # Nettoie le titre, la premiere phrase est souvent doublée
            desc = desc.replace('SYNOPSIS ET DÉTAILS', '').lstrip()
            if len(desc) > 180:
                idx = desc.find(desc[:15], 30, 180)
                if idx > 0:
                    desc = desc[idx:]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)
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
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a href="([^"]+)">Last page</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    # sPost = input_parameter_handler.getValue('sPost')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe src="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            if hoster_url.startswith('/'):
                hoster_url = 'http:' + hoster_url
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
