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

SITE_IDENTIFIER = 'videobuzzy_com'
SITE_NAME = 'Videobuzzy'
SITE_DESC = 'Sélection des vidéos les plus populaires de Videobuzzy'

URL_MAIN = 'https://www.videobuzzy.com/'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenres')

# URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler.addParameter('site_url', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos du net',
        'buzz.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos du net (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_MAIN + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Galerie', URL_MAIN + 'galerie.htm'])
    liste.append(['Football', URL_MAIN + 'football.htm'])
    liste.append(['Humour', URL_MAIN + 'humour.htm'])
    liste.append(['Animaux', URL_MAIN + 'animaux.htm'])
    liste.append(['Insolite', URL_MAIN + 'insolite.htm'])
    liste.append(['Télévision', URL_MAIN + 'television.htm'])
    liste.append(['Musique', URL_MAIN + 'musique.htm'])
    liste.append(['Sport', URL_MAIN + 'sport.htm'])
    liste.append(['Cinéma', URL_MAIN + 'cinema.htm'])
    # liste.append(['Bref.', URL_MAIN + 'BREF-tous-les-episodes-de-la-serie-de-canal-+-4902.news'])
    liste.append(['Top Vidéo', URL_MAIN + 'top-video.php'])

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
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "class='titre_news_index' href='(.+?)' title='(.+?)'.+?class=\"thumbnail\" src='(.+?)'.+?class='corps_news_p2'>(.+?)</span>"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            thumb = entry[2]
            desc = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/page-([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<span class="current">.+?</span><a href="(.+?)" title=\'.+?\'>.+?</a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return URL_MAIN + results[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'file: "(.+?)", label: "(.+?)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]
            title = movie_title + ' | ' + entry[1]
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
