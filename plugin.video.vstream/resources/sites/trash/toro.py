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
return False  # désactivée le 03122020 site HS depuis plus de 1 mois


SITE_IDENTIFIER = 'toro'
SITE_NAME = 'Toro'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = 'https://www.torostreaming.com/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-en-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'genre/', 'showGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming/', 'showMovies')
SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
SERIE_LAST = (URL_MAIN + 'dernieres-saisons/', 'showMovies')


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
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

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
        'Films & Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films & Séries (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LAST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LAST[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Films & Séries (Genres)',
        'genres.png',
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
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)</a>([^<]+)<'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1] + entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = []
    liste.append(['09', URL_MAIN + 'lettre/09/'])
    liste.append(['A', URL_MAIN + 'lettre/a/'])
    liste.append(['B', URL_MAIN + 'lettre/b/'])
    liste.append(['C', URL_MAIN + 'lettre/c/'])
    liste.append(['D', URL_MAIN + 'lettre/d/'])
    liste.append(['E', URL_MAIN + 'lettre/e/'])
    liste.append(['F', URL_MAIN + 'lettre/f/'])
    liste.append(['G', URL_MAIN + 'lettre/g/'])
    liste.append(['H', URL_MAIN + 'lettre/h/'])
    liste.append(['I', URL_MAIN + 'lettre/i/'])
    liste.append(['J', URL_MAIN + 'lettre/j/'])
    liste.append(['K', URL_MAIN + 'lettre/k/'])
    liste.append(['L', URL_MAIN + 'lettre/l/'])
    liste.append(['M', URL_MAIN + 'lettre/m/'])
    liste.append(['N', URL_MAIN + 'lettre/n/'])
    liste.append(['O', URL_MAIN + 'lettre/o/'])
    liste.append(['P', URL_MAIN + 'lettre/p/'])
    liste.append(['Q', URL_MAIN + 'lettre/q/'])
    liste.append(['R', URL_MAIN + 'lettre/r/'])
    liste.append(['S', URL_MAIN + 'lettre/s/'])
    liste.append(['T', URL_MAIN + 'lettre/t/'])
    liste.append(['U', URL_MAIN + 'lettre/u/'])
    liste.append(['V', URL_MAIN + 'lettre/v/'])
    liste.append(['W', URL_MAIN + 'lettre/w/'])
    liste.append(['X', URL_MAIN + 'lettre/x/'])
    liste.append(['Y', URL_MAIN + 'lettre/y/'])
    liste.append(['Z', URL_MAIN + 'lettre/z/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'ShowList',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+).jpg".+?<strong>([^<]+)<.+?<td>([^<]+)'
    # pattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+).jpg".class.+?<strong>([^<]+)<.+?<td>([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            thumb = entry[1] + '.jpg'
            if thumb.startswith('/'):
                thumb = 'https:' + thumb  # pas d'image de qualité d'mage trouvé
            title = entry[2]
            year = entry[3]

            display_title = title + ' (' + year + ')'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if 'series-/' in url or '/serie-' in url or '/serie/' in url:
                gui.addTV(SITE_IDENTIFIER, 'showSXE', display_title,
                          '', thumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            pattern = 'next page-numbers".+?page\\/(\\d{1,3})'
            results = parser.parse(html_content, pattern)
            page = ''
            if results[0]:
                page = results[1][0]
            gui.addNext(
                SITE_IDENTIFIER,
                'ShowList',
                '[COLOR teal]Page ' +
                page +
                ' >>>[/COLOR]',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # pattern = 'class="TPost C">.+?href="([^"]+)".+?img src="([^"]+)".+?title">([^<]+).+?year">([^<]+)'
    pattern = 'class="TPost C">.+?href="([^"]+)".+?img src="([^"]+).jpg".+?title">([^<]+).+?year">([^<]+)'
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
            # thumb = re.sub('/w\d+', '/w342', entry[1])  # meilleur
            # resolution pour les thumbs venant de tmdb
            thumb = entry[1] + '.jpg'
            if thumb.startswith('/'):
                thumb = 'https:' + thumb
            title = entry[2]
            year = entry[3]
            # VSlog(url2)
            display_title = title + ' (' + year + ')'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if '/series/' in url2 or '/serie-' in url2 or '/serie/' in url2:  # a revoir les cas
                gui.addTV(SITE_IDENTIFIER, 'showSXE', display_title,
                          '', thumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
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
                number = re.search('page/([0-9]+)/', next_page).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    '[COLOR teal]Page ' +
                    number +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'next page-numbers" href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    # récupération du synopsis
    desc = ''
    pattern = 'class="Description"><p>(.+?)</p>'
    aResultDesc = parser.parse(html_content, pattern)
    if aResultDesc[0]:
        desc = aResultDesc[1][0]

    pattern = 'class="Title AA-Season.+?tab="(\\d)|class="Num">(\\d{1,2}).+?href="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                sSaison = 'Saison ' + entry[0]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    sSaison +
                    '[/COLOR]')
            else:
                url = entry[2]
                Ep = entry[1]
                title = movie_title + ' Episode' + Ep

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('year', year)
                output_parameter_handler.addParameter('desc', desc)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-tplayernv.+?span>([^<]+)'
    aResult0 = re.findall(pattern, html_content)
    pattern = 'id="Opt\\d.+?src=.+?trembed=(\\d).+?trid=(\\d{5})'
    aResult1 = re.findall(pattern, html_content)

    # récupération du synopsis
    desc = ''
    pattern = 'class="Description"><p>(.+?)</p>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = results[1][0]

    nbElement = len(aResult0)
    for i in range(nbElement):
        # print (aResult0[i] + ' ' + aResult1[i][0]+ ' ' + aResult1[i][1])
        host = aResult0[i]
        sCode = aResult1[i][0]
        sCode1 = aResult1[i][1]
        title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)
        url = URL_MAIN + '?trembed=' + sCode + '&trid=' + sCode1 + '&trtype=1'

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('year', year)

        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            thumb,
            desc,
            output_parameter_handler)

    pattern = 'trdownload=(\\d+).+?trid=(\\d+).+?alt.+?noscript>([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            host = entry[2]
            sCode = entry[0]
            sCode1 = entry[1]
            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)
            url = URL_MAIN + '?trdownload=' + sCode + '&trid=' + sCode1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('year', year)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-tplayernv.+?span>([^<]+)'
    aResult0 = re.findall(pattern, html_content)
    pattern = 'id="Opt\\d.+?src=.+?trembed=(\\d).+?trid=(\\d{5,6})'
    aResult1 = re.findall(pattern, html_content)

    nbElement = len(aResult0)
    for i in range(nbElement):
        # print (aResult0[i] + ' ' + aResult1[i][0]+ ' ' + aResult1[i][1])
        host = aResult0[i]
        sCode = aResult1[i][0]
        sCode1 = aResult1[i][1]
        title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

        url = URL_MAIN + '?trembed=' + sCode + '&trid=' + sCode1 + '&trtype=2'

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('year', year)

        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            thumb,
            desc,
            output_parameter_handler)

    pattern = 'trdownload=(\\d+).+?trid=(\\d+).+?alt.+?noscript>([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            host = entry[2]
            sCode = entry[0]
            sCode1 = entry[1]
            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)
            url = URL_MAIN + '?trdownload=' + sCode + '&trid=' + sCode1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('year', year)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    request_handler = RequestHandler(url)

    request_handler.request()
    html_content = request_handler.request()
    urlreal = request_handler.getRealUrl()

    if 'trembed=' not in urlreal:
        hoster_url = urlreal  # liens de téléchargements
    else:
        pattern = 'src="([^"]+)"'
        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0]:
            hoster_url = results[1][0]  # link stream

    hoster = HosterGui().checkHoster(hoster_url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
