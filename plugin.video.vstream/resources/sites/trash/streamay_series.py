# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'streamay_series'
SITE_NAME = 'StreamAy Séries'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = "https://www.sakstream.site/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_LAST = (URL_MAIN, 'showLastEpisode')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
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

    output_parameter_handler.addParameter('site_url', SERIE_LAST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LAST[1],
        'Episodes (Derniers ajouts)',
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
    if (search_text):
        showSeries(URL_SEARCH[0] + search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'action'], [
            'Action & aventure', 'action-et-adventure'], [
                'Animation', 'animation'], [
                    'Aventure', 'aventure'], [
                        'Biopic', 'biopic'], [
                            'Comédie', 'comaedie'], [
                                'Comédie dramatique', 'drame-comaedie'], [
                                    'Documentaire', 'documentaire'], [
                                        'Drame', 'drame'], [
                                            'Epouvante-Horreur', 'epouvante-horreur'], [
                                                'Famille', 'famille'], [
                                                    'Fantastique', 'fantastique'], [
                                                        'Guerre', 'guerre'], [
                                                            'Horreur', 'horreur'], [
                                                                'Policier', 'policier'], [
                                                                    'Romance', 'romance'], [
                                                                        'Thriller', 'thriller'], [
                                                                            'Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series-vf/genres/' + url + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showLastEpisode():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'left fx-1.+?href="([^"]+).+?izobritenie">([^<]+).+?span>([^<]+).+?<span>([^<]+)'
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

            url = entry[0]
            title = entry[1] + ' S' + entry[2] + ' E' + entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'series',
                '',
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # for the search
    html_content = html_content.replace(' js-tip', '')

    pattern = 'th-in" href="([^"]+).+?src="([^"]+)" alt="([^"]+)'
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
            title = entry[2]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
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
    pattern = 'navigation">.+?</span><a href="([^"]+).+?>([^<]+)</a></span><span class="pnext">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = 'full-text clearfix">([^<]*)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'th-item">.+?href="([^"]+).+?src="([^"]+).+?nowrap">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            title = movie_title + ' ' + entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
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

    pattern = '([^"]+)"><div class="fsa-ep">([^<]+)'
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

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-url="([^"]+).+?<img src="/icon/([^/]+).png'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]
            lang = entry[1].upper()

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title + ' (' + lang + ')')
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
