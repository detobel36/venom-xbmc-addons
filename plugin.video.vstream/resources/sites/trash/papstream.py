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
return False  # 06/02/2021


SITE_IDENTIFIER = 'papstream'
SITE_NAME = 'PapStream'
SITE_DESC = 'Films, Séries'

URL_MAIN = 'https://www.papstream.in/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche/', 'showMovies')

# recherche globale MOVIE/TVSHOWS
key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

MOVIE_MOVIE = (URL_MAIN + 'films.html', 'showMoviesMenu')
MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (URL_MAIN + 'series.html', 'showSeriesMenu')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (URL_MAIN + 'animes.html', 'showAnimesMenu')
ANIM_NEWS = (URL_MAIN + 'animes.html', 'showMovies')
# ANIM_GENRES = (URL_MAIN + 'animes/', 'showGenres')
ANIM_ANNEES = (True, 'showAnimeYears')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'


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

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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


def showSeriesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    liste.append(['Action', url + 'action/'])
    liste.append(['Animation', url + 'animation/'])
    liste.append(['Aventure', url + 'aventure/'])
    liste.append(['Biopic', url + 'biopic/'])
    liste.append(['Comédie', url + 'comedie/'])
    liste.append(['Comédie Dramatique', url + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', url + 'comedie-musicale/'])
    liste.append(['Documentaire', url + 'documentaire/'])
    liste.append(['Drame', url + 'drame/'])
    liste.append(['Epouvante Horreur', url + 'epouvante-horreur/'])
    liste.append(['Famille', url + 'famille/'])
    liste.append(['Fantastique', url + 'fantastique/'])
    liste.append(['Guerre', url + 'guerre/'])
    liste.append(['Policier', url + 'policier/'])
    liste.append(['Romance', url + 'romance/'])
    liste.append(['Science Fiction', url + 'science-fiction/'])
    liste.append(['Thriller', url + 'thriller/'])

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


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1918, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/annee-' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/annee-' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimeYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1965, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'animes/annee/' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False
    if search:
        KeySearch = search
        if key_search_movies in KeySearch:
            KeySearch = str(KeySearch).replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in KeySearch:
            KeySearch = str(KeySearch).replace(key_search_series, '')
            bSearchSerie = True
        url = URL_SEARCH[0] + KeySearch
        request_handler = RequestHandler(url)

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)

    html_content = request_handler.request()
    pattern = 'class="short-images-link".+?img src="([^"]+)".+?<a.+?>([^<]+).+?.+?<a.+?>([^<]+).+?short-link">\\s*<a href="([^"]+)".+?>([^<]+)<\\/a>'
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

            thumb = URL_MAIN[:-1] + entry[0]
            url2 = URL_MAIN[:-1] + entry[3].replace(
                '/animes/films/', '/films/').replace('/animes/series/', '/series/')
            title = entry[4]
            qual = entry[1]
            lang = entry[2].replace('French', 'VF')

            if bSearchMovie:
                if '/series/' in url2:
                    continue
            if bSearchSerie:
                if '/films/' in url2:
                    continue
            display_title = ('%s (%s) [%s]') % (title, qual, lang)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/animes/' in url2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    'animes.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '/series/' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    'films.png',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('-([0-9]+).html', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<div class="pages-numbers".+?<span>.+?</span><a href=["\']([^"\']+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return URL_MAIN[:-1] + results[1][0]

    return False


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    pattern = '</a>\\s*:\\s*</h2>\\s*(.+?)<div'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = results[1][0]

    # Decoupage pour cibler la partie des saisons
    pattern = '<div id="full-video">(.+?)<div class="fstory'
    results = parser.parse(html_content, pattern)
    if results[0]:
        html_content = results

    pattern = '<a href="([^"]+)" title=".+?(saison\\s\\d+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):
            url2 = entry[0]
            if url2.startswith('/'):
                url2 = URL_MAIN[:-1] + url2
            sSaison = entry[1]
            title = ("%s %s") % (movie_title, sSaison)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

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
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    desc = input_parameter_handler.getValue('desc')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="saision_LI2">\\s*<a title="(.+?)"\\s*href=["\']([^"\']+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry[0].replace(' en streaming', '')
            url2 = URL_MAIN[:-1] + entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if (not desc):
        pattern = '</a>\\s*:\\s*</h2>\\s*(.+?)<div'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].replace(' en Streaming Complet ', ': ')

    pattern = '"#"\\srel="([^"]+).+?class="server.+?<img src="([^"]+).+?<span style=".+?">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            lang = entry[1].replace(
                '/Public/images/',
                '').replace(
                '.png',
                '')
            qual = entry[2].replace('(', '').replace(')', '')

            if 'alliance4creativity' in url2:
                continue

            hoster = HosterGui().checkHoster(url2)
            if (hoster):
                host = hoster.getDisplayName()
            else:
                host = GetHostname(url2)

            title = '%s [%s] (%s) [COLOR coral]%s[/COLOR]' % (movie_title,
                                                              qual, lang.upper(), host)

            output_parameter_handler.addParameter('refUrl', url)
            output_parameter_handler.addParameter('url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
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
    refUrl = input_parameter_handler.getValue('refUrl')
    url = input_parameter_handler.getValue('url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    if url.startswith('/'):
        url = URL_MAIN[:-1] + url

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', refUrl)
    request_handler.request()
    vUrl = request_handler.getRealUrl()

    if vUrl:
        hoster_url = vUrl
        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def GetHostname(url):

    try:
        if 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        host = url

    return host.capitalize()
