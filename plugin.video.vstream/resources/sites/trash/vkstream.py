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
return False  # 0212020 Site HS depuis plus de 1 moi

SITE_IDENTIFIER = 'vkstream'
SITE_NAME = 'Vkstream'
SITE_DESC = 'Series en streaming, streaming HD, streaming VF, séries, récent'

# URL_MAIN = 'https://wvv.vkstream.org/' # sous cloudfare
# ajout 09/10/2020 nom : VoirSeries ,clone sans CF avec  même code html
URL_MAIN = 'https://wvw.voirseries1.co/'

SERIE_SERIES = (URL_MAIN + 'series/page/1', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_VIEWS = (URL_MAIN + 'top-series/page/1', 'showSeries')
SERIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'search?search=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'series/genre/action_1'])
    liste.append(['Animation', URL_MAIN + 'series/genre/animation_1'])
    liste.append(['Aventure', URL_MAIN + 'series/genre/aventure_1'])
    liste.append(['Biopic', URL_MAIN + 'series/genre/biopic_1'])
    liste.append(['Comédie', URL_MAIN + 'series/genre/comaedie_1'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 'series/genre/comaedie-musicale_1'])
    liste.append(['Documentaire', URL_MAIN + 'series/genre/documentaire_1'])
    liste.append(['Drame', URL_MAIN + 'series/genre/drame_1'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 'series/genre/epouvante-horreur_1'])
    liste.append(['Famille', URL_MAIN + 'series/genre/famille_1'])
    liste.append(['Fantastique', URL_MAIN + 'series/genre/fantastique_1'])
    liste.append(['Guerre', URL_MAIN + '/series/genre/guerre_1'])
    liste.append(['Policier', URL_MAIN + 'series/genre/policier_1'])
    liste.append(['Romance', URL_MAIN + 'series/genre/romance_1'])
    liste.append(['Science Fiction', URL_MAIN +
                 'series/genre/science-fiction_1'])
    liste.append(['Thriller', URL_MAIN + 'series/genre/thriller_1'])
    liste.append(['Western', URL_MAIN + 'series/genre/western_1'])
    liste.append(['Divers', URL_MAIN + 'series/genre/divers_1'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    for i in reversed(range(1997, 2021)):  # avant 1997 peu de results
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/annee/' + Year + '_1')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="item_larg">\\s*<a href="([^"]+)".+?"([^"]+)">.+?<img src="([^"]+)"'
    parser = Parser()
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

            url2 = entry[0]
            title = entry[1]
            thumb = entry[2]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('([0-9]+)$', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Page ' +
                str(number) +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'href="([^"]+)"\\s*rel="next"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return False


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # description
    pattern = 'colo_cont">.+?>([^<]*)</p>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        desc = results[1][0]
        desc = ('[COLOR coral]%s[/COLOR] %s') % (' SYNOPSIS : \r\n\r\n', desc)
    else:
        desc = ''

    pattern = 'class="item">.+?href="([^"]+)".+?<h2>([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url2 = entry[0]
            title = movie_title + ' ' + entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
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

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '"" href="([^"]*)".+?ep_ar.+?span>([^<]*)<'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            url = entry[0]
            title = movie_title + ' E' + entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'seriesHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'href=\'([^"]*)\'.+?alt="([^"]*)".+?icon.([^"]*).png'
    # g1 url g2 host g3 vostfr vf

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:

            if (str(entry[0]).find('streaming-video.html') >= 0):  # Fake
                continue

            url = URL_MAIN[:-1] + entry[0]
            hoster = re.sub('\\.\\w+', '', entry[1]).capitalize()
            lang = str(entry[2]).upper()
            display_title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, hoster)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'hostersLink',
                display_title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def hostersLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    request_handler.request()
    hoster_url = request_handler.getRealUrl()

    hoster = HosterGui().checkHoster(hoster_url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
