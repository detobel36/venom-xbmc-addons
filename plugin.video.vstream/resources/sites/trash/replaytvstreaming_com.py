from resources.lib.comaddon import Progress  # , VSlog
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False  # Désactivé le 08/04/2020

# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#


SITE_IDENTIFIER = 'replaytvstreaming_com'
SITE_NAME = 'Replay Tv Streaming'
SITE_DESC = 'Replay TV'

URL_MAIN = 'https://replaytvstreaming.com/'

MOVIE_MOVIE = (URL_MAIN + 'film', 'showMovies')

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=',
    'showMovies')
URL_SEARCH_MISC = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=',
    'showMovies')
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Replay (Derniers ajouts)',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Replay (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        search_text = search_text.replace(' ', '+')

        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Emissions et Magazines', URL_MAIN + 'emission-magazine'])
    liste.append(['Documentaires', URL_MAIN + 'documentaire'])
    liste.append(['Spectacles', URL_MAIN + 'spectacle'])
    liste.append(['Sports', URL_MAIN + 'sport'])
    liste.append(['Téléfilms Fiction', URL_MAIN + 'telefilm-fiction'])
    liste.append(['Films', URL_MAIN + 'film'])

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
        url = URL_SEARCH[0] + search

        request_handler = RequestHandler(url)
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)

        html_content = request_handler.request()
        pattern = '<div class="item-box"><a class="item-link" href="([^"]+)"><div class="item-img"><img src="([^"]+)".+?<div class="item-title">([^<]+)<'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = '<div class="item-box"><a class="item-link" href="([^"]+)">.+?<img src="([^"]+)".+?<div class="item-title">([^<]+)<\\/div><div class="item-info clearfix">([^<]+)<\\/div>'

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
            title = entry[2]
            thumb = entry[1]
            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb

            desc = ''
            if len(entry) > 3:
                desc = entry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '<span class="pnext"><a href="([^"]+)">SUIVANT<\\/a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showLinks(page, video):
    url = 'http://replaytvstreaming.com/engine/ajax/re_video_part.php?block=video&page=' + \
        page + '&id=' + video

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    url = html_content
    return url


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<div id="video_[0-9]+" class="epizode re_poleta.+?" data-re_idnews="([^"]+)" data-re_xfn="video" data-re_page="([^"]+)">([^<]+)</div>'
    results = parser.parse(html_content, pattern)

    sTest = ''

    if results[0]:
        for entry in results[1]:

            sPage = entry[1]
            sVideoID = entry[0]
            hoster_url = showLinks(sPage, sVideoID)
            hoster_url = cUtil().unescape(hoster_url)

            title = entry[2]

            if 'Lecteur' not in title and sTest != title:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR olive]' +
                    title +
                    '[/COLOR]')
                sTest = title

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    else:
        pattern = '<div class="playe.+?" data-show_player="video"><iframe.+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)

        if results[0]:
            hoster_url = results[1][0]
            hoster_url = cUtil().unescape(hoster_url)

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
