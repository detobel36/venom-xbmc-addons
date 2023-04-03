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

SITE_IDENTIFIER = 'voirseries_best'
SITE_NAME = 'VoirSeries'
SITE_DESC = 'Séries en streaming VF et VOSTFR '

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_NEWS = (URL_MAIN + 'series/', 'showSeries')
SERIE_NEWS_SAISONS = (URL_MAIN, 'showSaisonsEpisodesNews')
tagnewsepidodes = '#tagnewsepidodes'
SERIE_NEWS_EPISODES = (URL_MAIN + tagnewsepidodes, 'showSaisonsEpisodesNews')
SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showAlpha')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_SERIES = (True, 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS_SAISONS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_SAISONS[1],
        'Séries (Dernières saisons)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS_EPISODES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_EPISODES[1],
        'Séries (Derniers épisodes)',
        'news.png',
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
        'Séries (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Adventure', 'adventure'],
             ['Arts-Martiaux', 'arts-martiaux'], ['Biopic', 'biopic'], ['Biographie', 'biographie'],
             ['Biography', 'biography'], ['Comédie', 'comedie'], ['Comédie dramatique', 'comedie-dramatique'],
             ['Comédie musicale', 'comedie-musicale'], ['Crime', 'crime'], ['Documentaire', 'documentaire'],
             ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Horreur', 'horreur'], ['Policier', 'policier'],
             ['Romance', 'romance'], ['Thriller', 'thriller'], ['Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genres/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'],
             ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'], ['H', 'h'], ['I', 'i'],
             ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'], ['Q', 'q'], ['R', 'r'],
             ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'], ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'liste/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = 'Année</div>'
    end = 'class="Genres Séries">'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href=([^ ]+) rel=nofollow><i class=material-icons>date_range</i><br>([0-9]{4})'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:
            url = entry[0]
            Year = entry[1]
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                Year,
                'annees.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSaisonsEpisodesNews():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    start = 'Derniers épisodes Séries-TV ajoutés'
    end = 'more_horiz'
    html_content = parser.abParse(html_content, start, end)

    if url == SERIE_NEWS_EPISODES[0]:  # ne pas réduire les regex
        pattern = '<li>\\s*<a href=([^ ]+) title=".+?>([^<]+)<span> <i class="langue ([^"]+)'
    else:
        pattern = '<li>\\s*<a href=([^ ]+) title="([^"]+)">[^<]+<span class'

    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            thumb = ''
            url2 = entry[0]
            title = entry[1].replace('  - S', '').title()
            if url == SERIE_NEWS_EPISODES[0]:
                lang = entry[2]
                if 'vf' in lang:
                    thumb = URL_MAIN + 'storage/icon/vf.png'
                if 'vostfr' in lang:
                    thumb = URL_MAIN + 'storage/icon/vostfr.png'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if url == SERIE_NEWS_EPISODES[0]:
                gui.addTV(SITE_IDENTIFIER, 'showHosters', title,
                          '', thumb, '', output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                          '', thumb, '', output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+').replace('%20', '+') + '&submit='
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class=shortstory>.+?href=([^ ]+).+?data-src=([^ ]+).+?>([^<]+)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            thumb = entry[1]
            title = entry[2]

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            if search:
                gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                          '', thumb, '', output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showSaisons', title,
                          '', thumb, '', output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

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
    pattern = '>(\\d+)</a> <a class="next page-numbers" href=([^ ]+) >Suivant'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging
    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    pattern = 'fsynopsis>\\s*<p>([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', results[1][0])

    pattern = 'class="shortstory">.+?href="([^"]+).+?data-src="([^"]+).+?<figcaption>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            thumb = entry[1]
            title = movie_title + ' ' + entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if not thumb:
        pattern = 'fstory-poster.+?data-src=([^ ]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            thumb = results[1][0]

    if not desc:
        pattern = 'fsynopsis>\\s*<p>([^<]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = (
                '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', results[1][0])

    pattern = 'class=saision_LI2>\\s*<a href=([^ ]+).+?span>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = movie_title + ' ' + entry[1]

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


def showLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()

    if 'storage/icon/' in thumb:
        pattern = 'poster image">\\s*<img src="([^"]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            thumb = results[1][0]

    if not desc:
        pattern = 'fsynopsis>\\s*<p>([^<]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = (
                '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', results[1][0])

    pattern = '<div data-url=([^ ]+).+?id=player_v_DIV_5.*?(?:class="download-server"|)>([^<]+).+?langue ([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]

            if HosterGui().checkHoster(url2) is False:
                continue

            sHostName = entry[1]
            lang = entry[2].upper()
            if 'HD VIP' in sHostName or 'STREAMANGO' in sHostName or 'OPENLOAD' in sHostName or 'VERYSTREAM' in sHostName:
                continue

            sHostName = sHostName.capitalize()
            display_title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, sHostName)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('host', sHostName)
            output_parameter_handler.addParameter('lang', lang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-url=([^ ]+).+?langue ([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]
            if hoster_url.startswith('/'):
                hoster_url = 'https:' + hoster_url
            lang = entry[1].upper()

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title + ' (' + lang + ')')
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
