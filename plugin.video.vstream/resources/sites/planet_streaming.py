# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import urlEncode
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Films en Streaming complet VF HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'exclu/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Top exclu)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD)',
        'hd.png',
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
    if search_text:
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
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
    nextPageSearch = input_parameter_handler.getValue('nextPageSearch')
    url = input_parameter_handler.getValue('site_url')

    if nextPageSearch:
        search = url

    if search:
        if URL_SEARCH[0] in search:
            search = search.replace(URL_SEARCH[0], '')

        if nextPageSearch:
            query_args = (('do', 'search'), ('subaction', 'search'),
                          ('search_start', nextPageSearch), ('story', search))
        else:
            query_args = (
                ('do', 'search'), ('subaction', 'search'), ('story', search))

        data = urlEncode(query_args)

        request_handler = RequestHandler(URL_SEARCH[0])
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addParametersLine(data)
        request_handler.addParameters('User-Agent', UA)
        html_content = request_handler.request()

    else:
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    if search:
        pattern = '<div class="fullstream fullstreaming">.+?<img src="([^"]+)".+?<h3 class="mov-title"><a href="([^"]+)" >([^<]+)</a>.+?<strong>(?:Qualit|Version).+?">(.+?)</a>.+?</*strong>'
    else:
        pattern = 'class="fullstream fullstreaming".+?src="([^"]+).+?alt="([^"]+).+?<strong>(?:Qualit|Version).+?>(.+?)</a>.+?</*strong>.+?xfsearch.+?>([^<]+).+?itemprop="description".+?;">([^<]+).+?<a href="([^"]+)'

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

            year = ''
            if search:
                thumb = entry[0]
                if thumb.startswith('/'):
                    thumb = URL_MAIN[:-1] + thumb

                site_url = re.sub('www\\.', '', entry[1])
                title = entry[2]
                qual = entry[3]
                qual = qual.replace(
                    ':',
                    '').replace(
                    ' ',
                    '').replace(
                    ',',
                    '/')
                desc = ''

            else:
                thumb = entry[0]
                if thumb.startswith('/'):
                    thumb = "https:" + thumb

                title = entry[1]
                qual = entry[2]
                qual = qual.replace(
                    ':',
                    '').replace(
                    ' ',
                    '').replace(
                    ',',
                    '/')

                # Certain film n'ont pas de date.
                try:
                    year = re.search('(\\d{4})', entry[3]).group(1)
                except BaseException:
                    pass

                desc = entry[4]
                site_url = re.sub('www\\.', '', entry[5])

            display_title = '%s [%s]' % (title, qual)

            output_parameter_handler.addParameter('site_url', site_url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                'films.png',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        if search:
            pattern = 'nextlink" id="nextlink" onclick="javascript:list_submit\\(([0-9]+)\\); return\\(false\\)" href="#">Suivant'
            results = parser.parse(html_content, pattern)
            if results[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', search)
                output_parameter_handler.addParameter(
                    'nextPageSearch', results[1][0])
                number = re.search('([0-9]+)', results[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

        else:
            next_page = __checkForNextPage(html_content)
            if next_page:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', next_page)
                number = re.search('/page/([0-9]+)', next_page).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

    if nextPageSearch:
        gui.setEndOfDirectory()

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a href="([^"]+)">Suivant &#8594;'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        return re.sub('www\\.', '', results[1][0])

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<i class="fa fa-play-circle-o"></i>([^<]+)</div>|<a href="([^"]+)" title="([^"]+)" target="seriePlayer"'
    results = parser.parse(html_content, pattern)
    sethost = set()

    if results[0]:
        for entry in results[1]:

            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
                continue

            hoster_url = entry[1]
            if hoster_url not in sethost:
                sethost.add(hoster_url)
            else:
                continue

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
