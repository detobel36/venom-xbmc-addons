# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Addon, SiteManager
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
sColor = Addon().getSetting("deco_color")

SITE_IDENTIFIER = 'streamingdivx'
SITE_NAME = 'Streamingdivx'
SITE_DESC = 'Films VF en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Comédie-dramatique', 'comedie-dramatique'],
             ['Comédie-musicale', 'comedie-musicale'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Epouvante Horreur', 'epouvante-horreur'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science-fiction', 'science-fiction'], ['Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/' + url)
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
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="short-images.+?href="([^"]+)" title="([^"]+)" class=.+?<img src="([^"]+).+?(?:<div class="short-content">|<a href=.+?qualite.+?>(.*?)</a>.+?<a href=.+?langue.+?>(.*?)</a>)'

    results = parser.parse(html_content, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            if url.startswith('/'):
                url = URL_MAIN[:-1] + url

            title = entry[1].replace(
                'Streaming',
                '').replace(
                'streaming',
                '').replace(
                'série',
                '')
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            thumb = entry[2]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            # pb d'url sur les images lors des recherches
            thumb = thumb.replace('wwww.', 'www.')

            qual = ''
            if entry[3]:
                qual = entry[3]

            lang = ''
            if entry[4]:
                lang = entry[4]

            display_title = ('%s [%s] (%s)') % (title, qual, lang.upper())

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)

            if 'series/' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

    if not search:  # une seule page par recherche
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
    pattern = ">([^<]+)</a></div></div><div class=\"col-lg-1 col-sm-2 col-xs-2 pages-next\"><a href=['\"]([^'\"]+)"
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page-([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        if next_page.startswith('/'):
            next_page = URL_MAIN[:-1] + next_page

        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # syno
    desc = ''
    try:
        pattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = '<div class="short-images.+?<a href="([^"]+)" class="short-images.+?<img src="([^"]+)" alt="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):

            url = entry[0]
            if url.startswith('/'):
                url = URL_MAIN[:-1] + url

            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            title = entry[2].replace(
                'Streaming',
                '').replace(
                'streaming',
                '') .replace(
                'Voir la série',
                '').replace(
                'en  VF et VOSTFR',
                '')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = parser.abParse(
        html_content,
        '<div class="episode-list">',
        'Series similaires')

    pattern = '<div class="sai.+?<a href="([^"]+)".+?<span>(.+?)</span>'

    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):

            url = entry[0]
            if not url.startswith('http'):
                url = URL_MAIN + url

            title = entry[1]

            display_title = ('%s %s') % (movie_title, title)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
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
    # streamer.php?p=169&c=V1RJeGMxcHVSbmhhUnpGMFltNU9kMWxYVW5sWlVUMDk=
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request = RequestHandler(url)
    html_content = request.request()

    url = request.getRealUrl()

    # syno
    desc = ''
    try:
        pattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    sPattern2 = 'class="stream.*?">.+?data-num="([^"]+)" data-code="([^"]+)".+?<i class="([^"]+)".+?src="([^"]+)"'

    results = parser.parse(html_content, sPattern2)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            host = entry[2].replace(
                'server player-',
                '').replace(
                'télécharger sur ',
                '').capitalize()

            # Filtre des host
            hoster = HosterGui().checkHoster(host)
            if not hoster:
                continue

            lang = entry[3].split(
                '/')[-1].replace('.png', '').replace('?ver=41', '').upper()

            display_title = (
                '%s (%s) [COLOR %s]%s[/COLOR]') % (movie_title, lang, sColor, host)

            output_parameter_handler.addParameter('datanum', entry[0])
            output_parameter_handler.addParameter('datacode', entry[1])
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sReferer = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    datanum = input_parameter_handler.getValue('datanum')
    datacode = input_parameter_handler.getValue('datacode')

    url = URL_MAIN + 'streamer.php?p=' + datanum + '&c=' + datacode

    request = RequestHandler(url)
    # request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addHeaderEntry('Referer', sReferer)
    html_content = request.request()

    hoster_url = request.getRealUrl()
    if URL_MAIN in hoster_url:
        parser = Parser()
        sPattern2 = 'href="(.+?)"'
        hoster_url = parser.parse(html_content, sPattern2)[1][0]

    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
