# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 45 07022021
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # voir https://01seriestreaming.com/


SITE_IDENTIFIER = 'hds_streamingvf'
SITE_NAME = 'Hds-Streamingvf'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = 'https://hds-streamingvf.org/'

# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_NEWS = (URL_MAIN + 'filmstreaming/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'seriestreaming/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'reseau/netflix/', 'showMovies')

key_serie = '?key_serie&s='
key_film = '?key_film&s='
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + key_film, 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + key_serie, 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films & Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films & Séries (Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_MOVIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_SERIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():

    gui = Gui()

    liste = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'histoire',
        'horreur',
        'kids',
        'musique',
        'mystere',
        'reality',
        'romance',
        'science-fiction',
        'science-fiction-fantastique',
        'soap',
        'telefilm/',
        'thriller',
        'war-politics',
        'western']

    output_parameter_handler = OutputParameterHandler()
    for igenre in liste:
        title = igenre.capitalize()
        url = URL_MAIN + 'genre/' + igenre + '/'
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    import datetime
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
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


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        url = search.replace(' ', '+').replace('%20 ', '+')
        pattern = 'class="result-item".+?href="([^"]+).+?src="([^"]+).+?alt="([^"]+).+?class="year">([^<]+).+?contenido"><p>([^<]*)'
    else:
        pattern = 'class="item.(?:movies|tvshows).+?src="([^"]+).+?alt="([^"]+).+?class="rating.+?<.span>([^<]*).+?href="([^"]+).+?<span>(\\d{4}).+?class="texto">([^<]*)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

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

            if search:
                url2 = entry[0]
                thumb = entry[1]
                title = entry[2]
                year = entry[3]
                desc = entry[4]

            else:
                thumb = entry[0]
                title = entry[1]
                sRate = entry[2]
                url2 = entry[3]
                year = entry[4]
                desc = 'IMDb :' + sRate + '\r\n' + entry[5]

            if key_serie in url:
                if '/series' not in url2:
                    continue
            if key_film in url:
                if '/series' in url2:
                    continue

            display_title = title
            if '/series' in url2:
                display_title = display_title + ' [Série]'
            else:
                display_title = display_title + ' [Film]'

            if year:
                display_title = ('%s (%s)') % (display_title, year)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if '/series' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
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
        next_page, sPagination = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                sPagination,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = "class=\"pagination\"><span>.+?de.(\\d+)</span>.+?class=\"current\".+?a href='([^']*)"
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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'property="og:description".+?content="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = "class='custom.+?href=(?:\"|'|)([^'\">]+).+?class='title'>([^<]+).+?src=(?:\"|'|)([^'\"]+)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        if 'la saison que vous voulez voir' not in html_content:
            # juste info si bug ou pas
            gui.addText(SITE_IDENTIFIER, 'Pas de video disponible')
        else:
            gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            sSaison = entry[1]
            thumb = entry[2]

            title = ("%s %s") % (movie_title, sSaison)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('year', year)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "class=.numerando.+?>([^<]+).+?ref='([^']+).>([^<]*)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sSaisonEpisode = entry[0]
            url2 = entry[1]
            sDesc2 = entry[2] + '\r\n' + desc
            title = movie_title + sSaisonEpisode

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('desc', sDesc2)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                sDesc2,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = "data-type='([^']*).*?post='([^']*).*?nume='([^']*).*?title'>([^<]*).+?flags.(.+?).png"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            datatype = entry[0]
            datapost = entry[1]
            datanum = entry[2]
            host = re.sub('\\.\\w+', '', entry[3])
            lang = str(entry[4]).upper()

            if 'lecteur hd' in host.lower():
                continue

            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            pdata = 'action=doo_player_ajax&post=' + datapost + \
                '&nume=' + datanum + '&type=' + datatype
            display_title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host.capitalize())

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('pdata', pdata)
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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParametersLine(pdata)
    html_content = request.request()
    pattern = '(http[^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            hoster_url = entry
            if 'userload' in hoster_url:
                hoster_url = hoster_url + "|Referer=" + URL_MAIN
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    gui.setEndOfDirectory()
