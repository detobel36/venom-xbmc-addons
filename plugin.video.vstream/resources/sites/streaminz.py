# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streaminz'
SITE_NAME = 'Streaminz'
SITE_DESC = ' films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
# MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_NETFLIX = (URL_MAIN + 'reseau/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'reseau/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'reseau/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'reseau/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'reseau/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'reseau/youtube-premium/', 'showMovies')
SERIE_ARTE = (URL_MAIN + 'reseau/arte/', 'showMovies')
# SERIE_ANNEES = (True, 'showSeriesYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
# l'url ne permet pas de filtrer directement les films des séries mais est
# utilisée pour filtrer dans showmovies
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

    # output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

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

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

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

    # output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

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

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '</i>Genres</a>'
    end = '</i>Demandes</a>'
    html_content = parser.abParse(html_content, start, end)
    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()
            triAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in triAlpha:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
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

    output_parameter_handler.addParameter('site_url', SERIE_ARTE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_ARTE[1],
        'Séries (Arte)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '<span>Années</span>'
    end = '<span>Connexion</span>'
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
            sTypeYear = 'movies'

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('sTypeYear', sTypeYear)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSeriesYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '<span>Années</span>'
    end = '<span>Connexion</span>'
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
            sTypeYear = 'tvshows'

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('sTypeYear', sTypeYear)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
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
    util = cUtil()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    if search:
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)

        url = search.replace(' ', '+')
        pattern = 'class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?span class="([^"]+).+?<p>(.*?)<\\/p'
        # pour filtrage entre film et série
        _type = parser.parseSingleResult(url, '\\?post_types=(.+?)&')
    else:
        sTypeYear = input_parameter_handler.getValue('sTypeYear')
        if sTypeYear:
            pattern = '<article id="post-\\d+".+?class="item ([^"]+).+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div>'
        else:
            pattern = '<article id="post-\\d+".+?img src="([^"]+).+?alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div'

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

            qual = ''
            year = ''
            desc = ''
            if search:
                url = entry[0]
                thumb = entry[1]
                title = entry[2].replace(
                    'Streaming VF',
                    '').replace(
                    'en',
                    '').replace(
                    'Regarder',
                    '')
                sType1 = entry[3]
                desc = entry[4]
                # pour différencier la recherche entre films et séries
                if sType1 != _type[1]:
                    continue
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche
            elif sTypeYear:
                sType1 = entry[0]
                if sType1 != sTypeYear:  # pour différencier la recherche entre films et séries
                    continue
                thumb = entry[1]
                title = entry[2]
                if entry[3]:
                    qual = entry[3]
                if entry[4]:
                    year = entry[4]
                url = entry[5]
                if entry[6]:
                    desc = entry[6]
            else:
                thumb = entry[0]
                title = entry[1]
                if entry[2]:
                    qual = entry[2]
                if entry[3]:
                    year = entry[3]
                url = entry[4]
                if entry[5]:
                    desc = entry[5]

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = util.unescape(desc).encode(
                    'utf-8')  # retire les balises HTML
            except BaseException:
                pass

            display_title = ('%s [%s] (%s)') % (title, qual, year)

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
                    'showLink',
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
    pattern = 'span>Page .+?de (\\d+).+?href="([^"]+)"><i id='
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, False


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = ">([^<]+)</span><span class='title|numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]Saison ' +
                    entry[0] +
                    '[/COLOR]')

            else:
                url = entry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    ' Saison \\g<1> Episode \\g<2>',
                    entry[1])
                title = movie_title + SxE

                display_title = movie_title + ' ' + \
                    re.sub('saison \\d+ ', '', SxE)

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()

    if '/films/' in url:
        pattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    else:
        pattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?flags/(.+?).png"

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        # trie par numéro de serveur
        sortedList = sorted(results[1], key=lambda item: item[2])
        output_parameter_handler = OutputParameterHandler()
        for entry in sortedList:

            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            # fonctionne pour Film ou Série (pour info: série -> dtype = 'tv')
            dtype = 'movie'
            dpost = entry[0]
            dnum = entry[1]

            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype
            lang = entry[2].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '').replace(
                ')',
                '')
            if '|' in lang:
                lang = lang.split('|')[1].strip().replace('FRENCH', 'FR')

            if 'VIP - ' in entry[2]:  # Les liens VIP ne fonctionnent pas
                continue

            title = ('%s (%s)') % (movie_title, lang.upper())
            title = title + '[COLOR coral] Serveur#' + dnum + '[/COLOR]'

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
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

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
    pattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")'
    aResult1 = re.findall(pattern, html_content)

    pattern = 'embed_url":"([^"]+)"'
    aResult2 = re.findall(pattern, html_content)

    results = aResult1 + aResult2

    if results:
        for entry in results:

            hoster_url = entry.replace("\\", '')
            if 'youtube' in hoster_url:
                continue
            if 'dood' in hoster_url:
                hoster_url = hoster_url

            if 'club' in hoster_url:
                hoster_url = hoster_url
                request = RequestHandler(hoster_url)
                parser = Parser()
                sHtmlContent2 = request.request()

                pattern = "if.+?self.+?== top.+?replace\\('([^']+)"
                results = parser.parse(sHtmlContent2, pattern)
                for aEntry2 in results[1]:
                    hoster_url = 'https://waaw.to' + aEntry2

            # voir si filtrage ou non, car parfois le lien mp4 créé un blocage
            if 'streaminz.ml' in hoster_url:
                sid = hoster_url.split('/')[-1]
                hoster_url = hoster_url
                postdata = 'r=&d=streaminz.ml'
                urlapi = 'https://streaminz.ml/api/source/' + sid
                request = RequestHandler(urlapi)
                request.setRequestType(1)
                request.addHeaderEntry('Referer', hoster_url)
                request.addParametersLine(postdata)
                sHtmlContent2 = request.request()
                parser = Parser()
                pattern = '"data".+?file.+?"([^"]*).+?type.+?"([^"]*)'
                results = parser.parse(sHtmlContent2, pattern)
                if results[0]:
                    hoster_url = results[1][0][0] + '.' + results[1][0][1]

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
