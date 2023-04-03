# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streampourvous'
SITE_NAME = 'StreampourVous'
SITE_DESC = 'films,'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film-streaming/', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'film-streaming/', 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/animation/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (URL_MAIN + 'serie-streaming/', 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche film',
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Animations)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche film',
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
        'Recherche série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Animations)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showNetwork():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    output_parameter_handler.addParameter('tmdb_id', 213)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_CANAL[0])
    output_parameter_handler.addParameter('tmdb_id', 285)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_AMAZON[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1024)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_DISNEY[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2739)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_APPLE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2552)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_YOUTUBE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (YouTube Originals)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<ul class="genres scrolling">'
    end = '><nav class="releases"><h2>Année de production</h2>'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+).+?<i>(\\d*)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()
            number = entry[2]  # + ' Films'
            if number < '2':
                number = number + ' Film'
            else:
                number = number + ' Films'
            display_title = ('%s (%s)') % (title, number)
            TriAlpha.append((display_title, url))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for display_title, url in TriAlpha:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                display_title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<h2>Année de production</h2><ul class="releases scrolling">'
    end = 'class="primary"><div class="columenu">'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showYearsSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1997, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'sortie/' + Year + '/?post_types=tvshows')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
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


def showMovies(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    parser = Parser()

    if search:
        url = search.replace(' ', '+')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = '<div class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?<p>(.+?)</p>'

    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        start = 'class="animation-2 items">'
        end = '<div class=\'resppages\'>'
        html_content = parser.abParse(html_content, start, end)
        pattern = 'class="item.+?"><div class="poster.+?src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)href="([^"]+).+?<span>([0-9]{4}).+?texto">(.*?)</div'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        utils = cUtil()
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            qual = ''
            year = ''
            desc = ''
            if search:
                url = entry[0]
                thumb = entry[1]
                title = entry[2]
                desc = entry[3]
            else:
                thumb = entry[0]
                title = re.sub('\\([0-9]{4}\\)', '', entry[1])
                if entry[2]:
                    qual = entry[2]  # parfois lang
                url = entry[3]
                year = entry[4]
                if entry[5]:
                    desc = entry[5].replace(
                        'Voir',
                        '').replace(
                        'Film complet streaming VF HD',
                        '') .replace(
                        'streaming VF HD',
                        '')

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = utils.unescape(desc).encode(
                    'utf-8')  # retire les balises HTML
            except BaseException:
                pass

            display_title = ('%s %s (%s)') % (title, qual, year)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            if '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSxE',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
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
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class="pagination">.+?de (\\d*).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "<span class='title'>(.+?)<i>|class='numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    entry[0].replace(
                        'Regarder',
                        '') +
                    '[/COLOR]')

            else:
                url = entry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    'saison \\g<1> Episode \\g<2>',
                    entry[1])
                title = movie_title + ' ' + SxE

                display_title = movie_title + ' ' + \
                    re.sub('saison \\d+ ', '', SxE)

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    html_content = request.request()
    pattern = "data-type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+).+?server'>(.+?)<.+?flags/(\\w+)"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        # trie par numéro de serveur
        sortedList = sorted(results[1], key=lambda item: item[2])
        output_parameter_handler = OutputParameterHandler()
        for entry in sortedList:

            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dtype = entry[0]
            dpost = entry[1]
            dnum = entry[2]
            pdata = dpost + '.' + dtype + '.' + dnum
            title = entry[3].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '') .replace(
                ')',
                '').replace(
                    '[',
                    '').replace(
                        ']',
                '')
            sServer = entry[4]
            lang = entry[5].replace('fr', 'VF').replace('en', 'VOSTFR')

            if 'freebiesforyou.net' in sServer or 'youtube.com' in sServer:
                continue
            title = ('%s [%s] (%s)') % (movie_title, title, lang)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParameters("action", "doo_player_ajax")
    request.addParameters("post", pdata.split('.')[0])
    request.addParameters("type", pdata.split('.')[1])
    request.addParameters("nume", pdata.split('.')[2])
    html_content = request.request(json_decode=True)

    if 'dood' in html_content or 'evoload' in html_content:
        pattern = '(http.+?)$'
    else:
        pattern = '(http.+?)[\'|"]'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            if 'zustreamv2/viplayer' in hoster_url:
                continue

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
