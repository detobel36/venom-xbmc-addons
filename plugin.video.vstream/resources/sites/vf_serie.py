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

SITE_IDENTIFIER = 'vf_serie'
SITE_NAME = 'VF Série'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showSeries'
URL_SEARCH = (URL_MAIN + '?s=', FUNCTION_SEARCH)
URL_SEARCH_SERIES = (URL_SEARCH[0], FUNCTION_SEARCH)

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming-gratuit/', 'showSeries')
SERIE_VIEWS = (URL_MAIN + 'les-meilleurs-series-tv/', 'showSeries')
SERIE_NOTES = (URL_MAIN + 'series-tv-les-plus-populaires/', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showAlpha')


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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NOTES[1],
        'Séries (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()
    util = cUtil()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = 'option class="level-0" value="\\d+">(.+?)</option>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry
            if 'Non' in title or 'Nom' in title:  # "Non classé" et "Nom de la catégorie"
                continue

            url = URL_MAIN + 'category/' + \
                util.CleanName(title).replace(' ', '-')

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0-9', '0-9'], ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'],
             ['H', 'h'], ['I', 'i'], ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'],
             ['P', 'p'], ['Q', 'q'], ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'],
             ['X', 'x'], ['Y', 'y'], ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'lettre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if '/lettre/' in url:
        pattern = '</span></td>.+?href="([^"]+).+?src="([^"]+).+?strong>([^<]+)'
    else:
        pattern = 'TPost C.+?href="([^"]+).+?src="([^"]+).+?Title">([^<]+).+?Description"><p>([^<]+)'

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
            thumb = re.sub('/w\\d+/', '/w342/', 'https:' + entry[1])
            if thumb.startswith('/'):
                thumb = 'https' + thumb
            title = entry[2]

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            if '/lettre/' in url:
                desc = ''
            else:
                desc = entry[3]

            display_title = title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
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
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>([^<]+)</a><a class="next page-numbers" href="([^"]+)">Next'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    desc = ''
    try:
        pattern = 'Description"><p>([^<]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'data-tab=.+?pan>([^<]+)|Num">([^<]+).+?src="([^"]+).+?href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)
    sSaison = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if entry[0]:
                sSaison = entry[0]
                title = movie_title + ' Saison ' + sSaison
                display_title = title

                sUrlSaison = url + "?sNumSaison=" + sSaison
                output_parameter_handler.addParameter('site_url', sUrlSaison)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showSxE',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    url, sNumSaison = url.split('?sNumSaison=')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    desc = ''
    try:
        pattern = 'Description"><p>([^<]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'data-tab=.+?pan>([^<]+)|Num">([^<]+).+?src="([^"]+).+?href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)
    sSaison = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if entry[0]:
                sSaison = entry[0]
            else:
                if sSaison != sNumSaison:
                    continue
                sEpisode = entry[1]
                sThumbEp = re.sub('/w\\d+/', '/w342/', 'https:' + entry[2])
                url = entry[3]
                sTitleEp = entry[4]

                title = movie_title + ' Episode ' + sEpisode
                display_title = title

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showHoster',
                    display_title,
                    '',
                    sThumbEp,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'class="TPlayerTb.+?src="([^"]+)"'

    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:

            request_handler = RequestHandler(entry)
            html_content = request_handler.request()
            pattern = '<iframe.+?src="([^"]+)'
            results = parser.parse(html_content, pattern)

            if results[0]:
                hoster_url = results[1][0]
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
