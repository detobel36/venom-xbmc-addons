# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress  # , VSlog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return false


SITE_IDENTIFIER = 'film_vf_gratuit'
SITE_NAME = 'Film VF gratuit'
SITE_DESC = 'Films en streaming'

URL_MAIN = 'http://streamgeo.net/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = ('http://', 'load')
MOVIE_VIEWS = (URL_MAIN + 'tendance/', 'showMovies')
# MOVIE_NOTES = (URL_MAIN + 'evaluation/', 'showMovies') #plante kodi
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')


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
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', output_parameter_handler)

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

    request_handler = RequestHandler(MOVIE_NEWS[0])
    html_content = request_handler.request()

    pattern = '<li class="cat-item cat-item.+?"><a href="([^"]+)".+?>([^<]+)<\\/a> *<i>([^<]+)<\\/i>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:

            title = entry[1] + ' (' + entry[2] + ')'
            url = entry[0]

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
    parser = Parser()

    request_handler = RequestHandler(MOVIE_NEWS[0])
    html_content = request_handler.request()

    pattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:

            title = entry[1]
            url = entry[0]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="(?:image|poster)".+?img src="([^"]+)" alt="([^"]+)".+?(?:|class="quality">([^<]+)<.+?)<a href="([^"]+)">'
    # pattern pour le synopsis
    if 'tendance/' not in url and 'evaluations/' not in url:
        pattern = pattern + '.+?(?:<div class="texto">|<p>)(.+?)<'
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

            thumb = entry[0].replace('w92', 'w342').replace('w185', 'w342')
            title = entry[1]
            qual = entry[2]
            url2 = entry[3]
            desc = ''
            if 'tendance/' not in url and 'evaluation/' not in url:
                desc = entry[4].replace('&#38;', '&')

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

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
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<span class="current">.+?</span><a href=\'([^\']+)'
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
    html_content = html_content.replace('https://www.youtube.com/embed/', '')

    pattern = "<li id='player-option-[0-9]+' class='dooplay_player_option' data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)'>"
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = geturl(entry)

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def geturl(entry):
    parser = Parser()

    sPost = entry[1]
    sNume = entry[2]
    _type = entry[0]

    pdata = 'action=doo_player_ajax&post=' + \
        sPost + '&nume=' + sNume + '&type=' + _type

    url = URL_MAIN + 'wp-admin/admin-ajax.php'

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    request.addParametersLine(pdata)

    html_content = request.request()

    pattern = "<iframe.+?src='([^']+)'"
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    else:
        return ''
