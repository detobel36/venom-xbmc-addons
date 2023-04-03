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

SITE_IDENTIFIER = 'serie_streaming'
SITE_NAME = 'Série Streaming'
SITE_DESC = 'Serie Streaming - voir votre series streaming Gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + 'search.php?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showSeries')
SERIE_GENRES = (True, 'showGenres')


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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        showSeries(URL_SEARCH[0] + search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = 'allowGenrebydefault">'
    end = 'Dernières Episodes récents'
    html_content = parser.abParse(html_content, start, end)
    pattern = 'href="([^"]+).+?>([^<]+)'
    results = parser.parse(html_content, pattern)

    triAlpha = []
    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            triAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in triAlpha:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
        reqType = RequestHandler.REQUEST_TYPE_POST
        pattern = 'href="([^"]+).+?image: url\\((.+?)"title">([^<]+)'
        idxUrl = 0
        idxThumb = 1
        idxTitle = 2
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        reqType = RequestHandler.REQUEST_TYPE_GET
        pattern = 'item">.+?href="([^"]+)" title="([^"]+).+?-src="([^"]+)'
        idxUrl = 0
        idxTitle = 1
        idxThumb = 2

    request_handler = RequestHandler(url)
    request_handler.setRequestType(reqType)
    html_content = request_handler.request()
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[idxUrl]
            title = entry[idxTitle].strip()
            thumb = 'https:' + \
                entry[idxThumb].replace('posters//tv', 'posters/tv')

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                thumb,
                '',
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
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()

    pattern = "<a>\\d+</a></li><li><a href='([^']+).+?>([0-9]+)</a></li></ul>"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('page-([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    pattern = "<span>\\d+</span><li><a href='([^']+).+?>([0-9]+)</a></li></ul>"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('[-|/]([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = 'dci-desc">(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].split('streaming')[1]
    except BaseException:
        pass

    # pour ne pas prendre les propositions de la source
    start = 'dcr-rating">'
    end = 'regarder aussi'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'item">.+?href="([^"]+)" title="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:

            url = entry[0]
            title = entry[1]

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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'title"><a href="([^"]+)" title=.+?(episode [0-9]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = movie_title + ' ' + entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # streaming
    pattern = 'data-hex="([^"]+).+?data-code="([^"]+).+?mobile">([^<]+).+?language ([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sDataHex = entry[0]
            sDataCode = entry[1]
            host = entry[2].capitalize()
            lang = entry[3].upper()

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)
            lien = URL_MAIN + 'iframeCode=' + sDataCode + '/' + sDataHex

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', lien)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    # download
    pattern = 'tele"><a href=\'([^\']+).+?mobile">([^<]+).+?language ([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sDataCode = entry[0]
            host = entry[1].capitalize()
            lang = entry[2].upper()

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)
            lien = URL_MAIN[:-1] + sDataCode

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', lien)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', referer)

    request_handler.request()
    hoster_url = request_handler.getRealUrl()
    hoster = HosterGui().checkHoster(hoster_url)

    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
