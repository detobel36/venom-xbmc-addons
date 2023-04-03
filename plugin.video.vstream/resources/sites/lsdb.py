# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'lsdb'
SITE_NAME = 'Liveset Database'
SITE_DESC = 'liveset podcast et autre de musique électronique'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json
# URL_MAIN = 'https://lsdb.eu'  # Pas de / car peut poser probleme

URL_SEARCH = (URL_MAIN + '/search?q=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NEWS = (URL_MAIN + '/livesets', 'showMovies')
NETS_GENRES = (True, 'showGenres')
NETS_EVENTS = (URL_MAIN + '/events/index/1', 'showEvents')
NETS_SHOWS = (URL_MAIN + '/events/index/2', 'showShows')
NETS_PODCAST = (URL_MAIN + '/events/index/3', 'showPodcast')
NETS_PROMO = (URL_MAIN + '/events/index/4', 'showPromo')


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

    output_parameter_handler.addParameter('site_url', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Les nouveaux liveset',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Les genres musicaux',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_EVENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_EVENTS[1],
        'Les évènements ',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_SHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_SHOWS[1],
        'Les shows',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_PODCAST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_PODCAST[1],
        'Les podcasts',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_PROMO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_PROMO[1],
        'Les promotions',
        'replay.png',
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

    liste = [['Ambient', 'genre/ambient'], ['Acid', 'genre/acid'], ['Autre', 'genre/other'],
             ['Breakbeat', 'genre/breakbeat'], ['Breakcore', 'genre/breakcore'], ['Chiptune ', 'genre/chiptune'],
             ['Classic hardstyle', 'tag/classic-hardstyle'], ['Crossbreed', 'genre/crossbreed'],
             ['Dance', 'genre/dance'], ['Darkcore', 'genre/darkcore'], ['Deep House', 'genre/deephouse'],
             ['Disco', 'genre/disco'], ['Dark Psy', 'genre/darkpsy'], ['Darkstep', 'genre/darkstep'],
             ['Drum and bass', 'genre/drumnbass'], ['Dubstep', 'genre/dubstep'],
             ['Early hardcore', 'genre/earlyhardcore'], ['Early hardstyle', 'genre/earlyhardstyle'],
             ['Early terror', 'genre/earlyterror'], ['EBM', 'genre/ebm'], ['Eclectic', 'genre/eclectic'],
             ['Electro', 'genre/electro'], ['Euphoric hardstyle', 'tag/euphoric-hardstyle'], ['Fidget', 'genre/fidget'],
             ['Frenchcore', 'genre/frenchcore'], ['Funk', 'genre/funk'], ['Garage', 'genre/garage'],
             ['Goa', 'genre/goa'], ['Grime', 'genre/grim'], ['Hands-up', 'genre/handsup'],
             ['Happy hardcore', 'genre/happyhardcore'], ['Hardcore', 'genre/hardcore'], ['Hardstyle', 'genre/hardstyle'],
             ['Hardtechno', 'genre/hardtechno'], ['Hardtek', 'genre/hardtek'], ['Hardtrance', 'genre/hardtrance'],
             ['House', 'genre/house'], ['Industrial', 'genre/industrial'],
             ['Industrial hardcore', 'genre/industrialhardcore'], ['IDM', 'genre/idm'], ['Jump', 'genre/jump'],
             ['Jungle', 'genre/jungle'], ['Liquid', 'genre/liquid'], ['Lounge', 'genre/lounge'],
             ['Minimal', 'genre/minimal'], ['Moombahton', 'genre/moombahton'], ['Noise', 'genre/noise'],
             ['Oldschool', 'genre/oldschool'], ['Progressive', 'genre/progressive'],
             ['Progressive House', 'genre/progressivehouse'], ['Progressive Trance', 'genre/progressivetrance'],
             ['Psytrance', 'genre/psytrance'], ['Raw Hardstyle', 'tag/raw-hardstyle'], ['Speedcore', 'genre/speedcore'],
             ['Schranz', 'genre/schranz'], ['Speedcore', 'genre/speedcore'], ['Splittercore', 'genre/splittercore'],
             ['Tech house', 'genre/techhouse'], ['Techno', 'genre/techno'], ['Techtrance', 'genre/techtrance'],
             ['Tek', 'genre/tek'], ['Tekno', 'genre/tekno'], ['Terror', 'genre/terror'], ['Trance', 'genre/trance'],
             ['Tribal House', 'genre/tribalhouse'], ['UK Happy hardcore', 'genre/ukhappyhardcore'],
             ['UK Hardcore', 'genre/ukhardcore'], ['UK Hardhouse', 'genre/ukhardhouse'],
             ['Vocal Trance', 'genre/vocaltrance'], ['Witch house', 'genre/witchhouse']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + '/' + url + '/')
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
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a href="([^"]+)">\\s*<time datetime=.+?</time>\\s*<span class=".+?<i class=".+?></i>\\s*([^"]+)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showIsdb',
                title,
                'replay.png',
                '',
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showIsdb():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a href="([^"]+)" class="split button expand text-left.+?> *([^<> ]+)*[.].+?<'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = URL_MAIN + entry[0]
            hoster = entry[1].capitalize()
            thumb = 'special://home/addons/plugin.video.vstream/resources/art/replay.png'

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, hoster)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()


def showEvents():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<i class=".+?"></i>\\s* <a href="([^"]+)">\\s*([^"]+)\\s*</a>'

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

            url2 = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'annees.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showEvents',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def showShows():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<i class=".+?"></i>\\s* <a href="([^"]+)">\\s*([^"]+)\\s*</a>'

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

            url2 = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showShows',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def showPodcast():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<i class=".+?"></i>\\s* <a href="([^"]+)">\\s*([^"]+)\\s*</a>'

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

            url2 = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showPodcast',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def showPromo():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<i class=".+?"></i>\\s* <a href="([^"]+)">\\s*([^"]+)\\s*</a>'

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

            url2 = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showPromo',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class="active"><a href="".+?href="([^"]+).+?>(\\d+)</a></li>\\s*</ul>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<br />\\s*<a href="([^"]+)">.+?</a>.+?<br />'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
