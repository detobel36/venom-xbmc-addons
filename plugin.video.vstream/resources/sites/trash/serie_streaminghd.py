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
return False  # 13/02/21 WAAW en hoster


SITE_IDENTIFIER = 'serie_streaminghd'
SITE_NAME = 'Série-StreamingHD'
SITE_DESC = 'Séries en streaming vf, vostfr'

URL_MAIN = "https://planet-serie.com/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_TOP = (URL_MAIN + 'top-serie/', 'showSeries')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showSeries')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showSeries')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_TOP[1],
        'Séries (Populaire)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSeries(search=''):
    gui = Gui()
    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'fullstreaming"><img src="([^"]+).+?alt="([^"]+).+?xqualitytaftaf"><strong>([^<]+).+?href="([^"]+)" *>([^<]+)'
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

            thumb = entry[0]
            if thumb.startswith('/'):
                thumb = 'https:' + thumb

            title = entry[1]
            saison = entry[2]
            site_url = entry[3]
            lang = entry[4]

            if '{title}' in title:
                title = lang
                lang = ''
            elif 'VF - VOSTFR' in lang:
                lang = 'VF/VOSTFR'
            elif 'VF' in lang:
                lang = 'VF'
            elif 'VOSTFR' in lang:
                lang = 'VOSTFR'

            display_title = ('%s %s (%s)') % (title, saison, lang)

            output_parameter_handler.addParameter('site_url', site_url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                'series.png',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>([^<]+)</a>  <a href="([^"]+)">Suivant'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
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

    # Liens VF
    sHtmlTab = parser.abParse(
        html_content,
        '<div class="VF-tab">',
        '<div id="fsElementsContainer">')
    if sHtmlTab:
        pattern = '<a href="([^"]+)".+?</i> Episode *([0-9]+)'
        results = parser.parse(sHtmlTab, pattern)

        if results[0]:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VF[/COLOR]')

            for entry in results[1]:
                hoster_url = entry[0]
                sMovieTitle2 = movie_title + ' Episode ' + entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(sMovieTitle2)
                    hoster.setFileName(sMovieTitle2)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    # Liens VOSTFR
    sHtmlTab = parser.abParse(
        html_content,
        '<div class="VOSTFR-tab">',
        '<div class="VF-tab">')
    if sHtmlTab:

        pattern = '<a href="([^"]+)".+?</i> Ep *([0-9]+)'
        results = parser.parse(sHtmlTab, pattern)

        if results[0]:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VOSTFR[/COLOR]')

            for entry in results[1]:
                hoster_url = entry[0]
                sMovieTitle2 = movie_title + ' Episode ' + entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(sMovieTitle2)
                    hoster.setFileName(sMovieTitle2)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
