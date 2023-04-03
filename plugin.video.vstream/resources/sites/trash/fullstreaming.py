# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

# site HS le 02/10/18
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'fullstreaming'
SITE_NAME = 'Full Streaming'
SITE_DESC = 'Films et Séries en streaming HD'

URL_MAIN = 'https://one4streaming.cc/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN, '')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_NEWS = (URL_MAIN + 'serie-tv/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-tv/', 'showMovies')


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
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


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
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = '<li class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-13.+?"><a href="([^<]+)">([^<]+)</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:
            title = entry[1].replace(
                '-720p',
                ' [720p]').replace(
                '-1080p',
                ' [1080p]')
            url = URL_MAIN[:-1] + entry[0]

            output_parameter_handler = OutputParameterHandler()
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

    for i in reversed(xrange(1964, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + '?filter-by=films&anne=' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div id="mt-.+?href="([^<]+)".+?src="([^<]+)" alt="([^<]+) Streaming.+?".+?class="calidad2">(.+?)<'

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

            url = entry[0]
            thumb = entry[1]
            title = entry[2].replace(' - Saison', ' Saison')
            qual = entry[3]
            desc = ''

            # Si recherche et trop de resultat, on nettoye
            if search and total > 2:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '-saison-' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    title,
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
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a href="([^<]+)" >Suivant</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # réécriture des liens beclic pour recuperer les bons hosters
    html_content = html_content.replace(
        'https://beclic.pw/op.php?s=',
        'https://oload.site/embed/')
    html_content = html_content.replace(
        'http://beclic.pw/op.php?s=',
        'https://oload.site/embed/')
    html_content = html_content.replace(
        'https://beclic.pw/jaja.php?s=',
        'https://jawcloud.co/embed-')
    html_content = html_content.replace(
        'https://beclic.pw/rapid.php?s=',
        'https://www.rapidvideo.com/e/')

    pattern = '<iframe.+?src="(.+?)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            if 'jawcloud' in hoster_url:
                hoster_url = hoster_url + '.html'
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(' class="selected"', '')
    # réécriture des liens beclic
    html_content = html_content.replace(
        'https://beclic.pw/op.php?s=',
        'https://oload.site/embed/')
    html_content = html_content.replace(
        'http://beclic.pw/op.php?s=',
        'https://oload.site/embed/')

    sEpisodesList = {}
    pattern = '<a href="#(div[0-9]+)">(.+?)</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for i in results[1]:
            sEpisodesList[i[0]] = i[1]

    pattern = '<div id="(div[^"]+)">.+?<iframe.+?src="(.+?)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            div = entry[0]
            sEpisodes = sEpisodesList.get(div, "Error")
            sEpisodes = sEpisodes.replace('Épisodes ', 'E')

            sMovieTitle2 = movie_title + sEpisodes

            hoster_url = entry[1]
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(sMovieTitle2)
                hoster.setFileName(sMovieTitle2)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
