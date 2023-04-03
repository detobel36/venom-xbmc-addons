# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'fullmatchtv'
SITE_NAME = 'Fullmatchtv'
SITE_DESC = 'Sports Replay'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

# SPORT_SPORTS = (True, 'load')
SPORT_REPLAY = (True, 'load')
REPLAYTV_REPLAYTV = (True, 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

MOVIE_AFL = (URL_MAIN + 'afl/', 'showMovies')
MOVIE_MOTOR = (URL_MAIN + 'motorsports/', 'showMovies')
MOVIE_NBA = (URL_MAIN + 'nba/', 'showMovies')
MOVIE_NFL = (URL_MAIN + 'nfl/', 'showMovies')
MOVIE_NHL = (URL_MAIN + 'nhl/', 'showMovies')
MOVIE_MLB = (URL_MAIN + 'mlb/', 'showMovies')
MOVIE_RUGBY = (URL_MAIN + 'rugby/', 'showMovies')
MOVIE_MMA = (URL_MAIN + 'wwe-mma/', 'showMovies')


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

    output_parameter_handler.addParameter('site_url', MOVIE_AFL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_AFL[1],
        'AFL',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MOTOR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOTOR[1],
        'MOTORSPORT',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NBA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NBA[1],
        'NBA',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NFL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NFL[1],
        'NFL',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NHL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NHL[1],
        'NHL',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MLB[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MLB[1],
        'MLB',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_RUGBY[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_RUGBY[1],
        'RUGBY',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MMA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MMA[1],
        'WWE-MMA',
        'sport.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()

    if search:
        url = search
        pattern = '(?:<div class="td_module_16 td_module_wrap td-animation-stack">|<div class="td-module-container td-category-pos-image">.+?<div class="td-module-thumb">).+?href="([^"]+).+?title="([^"]+).+?.+?(?:src="([^"]+)|url.+?([^\']+))'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        pattern = '(?:<div class="td_module_mx7 td_module_wrap td-animation-stack">|<div class="td-module-container td-category-pos-image">.+?<div class="td-module-thumb">).+?href="([^"]+).+?title="([^"]+).+?.+?(?:src="([^"]+)|url.+?([^\']+))'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

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

            url = entry[0]
            thumb = entry[2]
            title = entry[1]
            display_title = title

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showLink',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)
        progress_.VSclose(progress_)

        gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    start = '<div class="td-post-content tagdiv-type">'
    end = '<div class="td-post-source-tags">'
    html_content = parser.abParse(html_content, start, end)
    pattern = 'Part (\\d).+?<iframe.+?src="([^"]+)"'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        pattern = '<iframe.+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:

                hoster_url = entry
                if hoster_url.startswith('//'):
                    hoster_url = 'https:' + hoster_url

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    else:
        if not results[0]:
            gui.addText(SITE_IDENTIFIER)
        if results[0]:
            total = len(results[1])
            progress_ = Progress().VScreate(SITE_NAME)
            for entry in results[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                sPartie = entry[0]
                hoster_url = entry[1]
                if hoster_url.startswith('//'):
                    hoster_url = 'https:' + hoster_url
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title + ' Partie' + sPartie)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

            progress_.VSclose(progress_)

    gui.setEndOfDirectory()
