# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import Progress  # , VSlog
import re
import base64

SITE_IDENTIFIER = 'films_cafe'
SITE_NAME = 'Films Cafe'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = 'https://ww1.films.cafe/'

MOVIE_NEWS = (URL_MAIN + 'tous-les-films/?sort=date', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'tous-les-films/', 'load')
MOVIE_VIEWS = (URL_MAIN + 'tous-les-films/?sort=views', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'tous-les-films/?sort=comments', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'tous-les-films/?sort=imdb', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'


def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except BaseException:
        return chain


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

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_COMMENTS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/action/'])
    liste.append(['Animation', URL_MAIN + 'category/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'category/arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'category/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'category/biopic/'])
    liste.append(['Bollywood', URL_MAIN + 'category/bollywood/'])
    liste.append(['Comédie', URL_MAIN + 'category/comedie/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'category/drame/'])
    liste.append(['Espionnage', URL_MAIN + 'category/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'category/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'category/fantastique/'])
    liste.append(['Fiction', URL_MAIN + 'category/science-fiction/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre/'])
    liste.append(['Historique', URL_MAIN + 'category/historique/'])
    liste.append(['Horreur', URL_MAIN + 'category/horreur/'])
    liste.append(['Musical', URL_MAIN + 'category/musical/'])
    liste.append(['Péplum', URL_MAIN + 'category/peplum/'])
    liste.append(['Policier', URL_MAIN + 'category/policier/'])
    liste.append(['Romance', URL_MAIN + 'category/romance/'])
    liste.append(['Thriller', URL_MAIN + 'category/thriller/'])
    liste.append(['Western', URL_MAIN + 'category/western/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    url = URL_MAIN + 'tous-les-films/?release-year='

    liste = []
    liste.append(['2018', url + '2018'])
    liste.append(['2017', url + '2017'])
    liste.append(['2016', url + '2016'])
    liste.append(['2015', url + '2015'])
    liste.append(['2014', url + '2014'])
    liste.append(['2013', url + '2013'])
    liste.append(['2012', url + '2012'])
    liste.append(['2011', url + '2011'])
    liste.append(['<2010', url + '2010'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
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

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="movie-preview-content".+?src="([^"]+)".+?href="([^"]+)" title="([^"]+)".+?<p class=.story.>(.+?)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            url = entry[1]
            title = entry[2]
            desc = entry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'films.png',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if not search:
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
    pattern = 'class="current".+?<a href="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<a  id="([^"]+)".+?>► (.+?)<'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            sPost = entry[0].split("_")
            host = entry[1].capitalize()
            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('sPostId', sPost[0])
            output_parameter_handler.addParameter('sTabId', sPost[1])
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sPostId = input_parameter_handler.getValue('sPostId')
    sTabId = input_parameter_handler.getValue('sTabId')

    # trouve la vrais url
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    url2 = request_handler.getRealUrl() + 'wp-admin/admin-ajax.php'

    request_handler = RequestHandler(url2)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry(
        'User-Agent',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    request_handler.addParameters('action', 'fetch_iframes_from_post')
    request_handler.addParameters('post_id', sPostId)
    request_handler.addParameters('tab_id', sTabId)
    html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            # https://drive.google.com/file/d/' + s_id + '/view' #?pli=1
            # https://docs.google.com/file/d/1Li4nfkHuLPYkZ7JxAIYVoQBBxHy4l6Up/preview

            hoster_url = entry

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, '')

    gui.setEndOfDirectory()
