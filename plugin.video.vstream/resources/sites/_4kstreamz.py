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

SITE_IDENTIFIER = '_4kstreamz'
SITE_NAME = '4kstreamz'
SITE_DESC = 'Films et Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'list-films.html', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')


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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
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


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1921, 2022)):
        year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'filmspar?annee=' + year)  # / inutile
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '<h4 class="head nop">Genre'
    end = '<div class="menu_first">'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'a href="([^"]+)" class="an">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '-').replace('%20', '-') + '.html'
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if 'list-films.html' in url or '/films/page' in url:
        pattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+).+?class="qualitos">' + \
            '([^<]+).+?class="synopsis nop">([^<]+)'
    else:
        pattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+)'

    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2

            thumb = entry[1]
            if 'http' not in thumb:
                thumb = URL_MAIN[:-1] + thumb

            title = entry[2].strip()
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            qual = ''
            desc = ''
            if 'list-films.html' in url or '/films/page' in url:
                qual = entry[3]
                desc = entry[4]

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)

            if '/series' not in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page is not False:
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
    if 'suivanthds' in html_content:  # genre
        pattern = '>([^<]+)</a><a class="suivanthds.+?href="([^"]+)'
    elif 'CurrentPage' in html_content:  # film année serie
        pattern = "CurrentPage.+?href='([^']+).+?>([^<]+)</a></div"
    else:  # film année à partir de la page 8
        pattern = "</a><span>.+?<a href='([^']+).+?</span>.+?>([^<]+)</a></div></div>\\s*</div>\\s*</div>"

    results = parser.parse(html_content, pattern)
    if results[0]:
        if 'suivanthds' in html_content:  # genre
            number_max = results[1][0][0]
            next_page = results[1][0][1]
        # elif 'CurrentPage':  # film année serie
            # next_page = results[1][0][0]
            # number_max = results[1][0][1]
        else:  # film année à partir de la page 8
            next_page = results[1][0][0]
            number_max = results[1][0][1]

        number_next = re.search(
            'page-([0-9]+)|([0-9]+)$',
            next_page).group(0)  # page-XX.html ou  annee-aaaa/XX
        number_next = number_next.replace('page-', '')
        next_page = URL_MAIN[:-1] + next_page
        paging = number_next + '/' + number_max

        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'itemprop="description">([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    start = html_content.find('<div class="contentomovies">')
    html_content = html_content[start:]
    pattern = '<a href="([^"]+).+?class="nop">Saison([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):
            url2 = entry[0]
            saison = entry[1].replace(' ', '')

            title = ("%s %s %s") % (movie_title, 'saison', saison)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('year', year)
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
    year = input_parameter_handler.getValue('year')

    iSaison = ''
    pattern = 'saison.(.+?)'
    results = parser.parse(url, pattern)
    if results[0]:
        iSaison = ' Saison ' + results[1][0].replace(' ', '')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<div class="contentomovies">'
    end = '<div class="keywords"'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+).+?class="titverle">.+?class="nop">.+?pisode([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            nEpisode = entry[1].replace(' ', '')
            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2

            title = movie_title + iSaison + ' episode' + nEpisode

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    oHosterGui = HosterGui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'itemprop="description">([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = '<img src=".(vf|vostfr).png|data-url="([^"]+).+?data-code="([^"]+).+?<span>([^<]+)'
    results = parser.parse(html_content, pattern)
    lang = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if entry[0]:
                lang = entry[0].upper()

            if entry[1]:
                dataUrl = entry[1]
                dataCode = entry[2]
                if "/thumbnail/" in dataCode:
                    continue
                host = entry[3].capitalize()
                if not oHosterGui.checkHoster(host):
                    continue

                url2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + '&CData=' + dataCode
                display_title = (
                    '%s (%s) [COLOR coral]%s[/COLOR]') % (title, lang, host)
                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('host', host)
                output_parameter_handler.addParameter('lang', lang)
                output_parameter_handler.addParameter('referer', url)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    pattern = "<img src=\".(vf|vostfr).png|class=.Playersbelba.+?PPl=(.+?)CData=([^']+).+?<.span>.+?<span>([^<]+)"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if entry[0]:
                lang = entry[0].upper()

            if entry[1]:
                dataUrl = entry[1]
                dataCode = entry[2]
                host = entry[3].capitalize()
                if not oHosterGui.checkHoster(host):
                    continue

                url2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + 'CData=' + dataCode

                display_title = (
                    '%s (%s) [COLOR coral]%s[/COLOR]') % (title, lang, host)

                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('host', host)
                output_parameter_handler.addParameter('lang', lang)
                output_parameter_handler.addParameter('referer', url)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oHosterGui = HosterGui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')

    request = RequestHandler(url)
    request.addHeaderEntry('Referer', referer)
    request.request()
    urlReal = request.getRealUrl()
    if URL_MAIN in urlReal:
        request = RequestHandler(url)
        request.addHeaderEntry('Referer', referer)
        request.request()
        html_content = request.request()

        parser = Parser()
        pattern = 'class="DownloadSection.+?href="([^"]+)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            hoster_url = results[1][0]
            hoster = oHosterGui.checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                oHosterGui.showHoster(
                    gui,
                    hoster,
                    hoster_url,
                    thumb,
                    input_parameter_handler=input_parameter_handler)

    else:
        hoster_url = urlReal
        hoster = oHosterGui.checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            oHosterGui.showHoster(
                gui,
                hoster,
                hoster_url,
                thumb,
                input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
