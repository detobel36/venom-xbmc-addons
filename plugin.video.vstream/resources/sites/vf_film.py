# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'vf_film'
SITE_NAME = 'VF Film'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'tous-les-films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-meilleurs-films-en-streaming/', 'showMovies')
MOVIE_NOTES = (
    URL_MAIN +
    'films-les-plus-populaires-en-streaming/',
    'showMovies')
MOVIE_GENRES = (True, 'showGenres')


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

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_MOVIES[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()
    util = cUtil()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = 'option class="level-0" value="\\d+">(.+?)</option>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry
            if 'Uncategorized' in title:
                continue

            url = URL_MAIN + 'genre/' + \
                util.CleanName(title).replace(' ', '-')

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

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if '/lettre/' in url:
        pattern = '</span></td>.+?href="([^"]+).+?src="([^"]+).+?strong>([^<]+).+?<td>([^<]+)'
    else:
        pattern = 'TPost C.+?href="([^"]+).+?src="([^"]+).+?Title">([^<]+).+?Description"><p>([^<]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            thumb = re.sub('/w\\d+/', '/w342/', 'https:' + entry[1])
            title = entry[2]
            if '/lettre/' in url:
                desc = ''
                year = entry[3]
            else:
                desc = entry[3]
                year = ''

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            display_title = title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHoster',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

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
    pattern = '>([^<]+)</a> <a class="next page-numbers" href="([^"]+)">Suivant'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHoster(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    # hoster
    pattern = 'tplayernv.+?<span>([^<]+)<'
    results = parser.parse(html_content, pattern)
    if results[0]:
        hosters = results[1]
        numHoster = 0
        # url
        pattern = 'class="TPlayerTb.+?src=(?:"|&quot;)(.+?)(?:"|&quot;)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:

                hoster = HosterGui().checkHoster(hosters[numHoster])
                numHoster += 1
                if not hoster:
                    continue

                request_handler = RequestHandler(entry)
                html_content = request_handler.request()
                pattern = '<iframe.+?src="([^"]+)'
                results = parser.parse(html_content, pattern)

                if results[0]:
                    hoster_url = results[1][0]
                    hoster = HosterGui().checkHoster(hoster_url)
                    if hoster:
                        hoster.setDisplayName(movie_title)
                        hoster.setFileName(movie_title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
