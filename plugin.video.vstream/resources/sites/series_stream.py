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

SITE_IDENTIFIER = 'series_stream'
SITE_NAME = 'Séries Stream'
SITE_DESC = 'Voir une panoplie de séries en streaming VF et VOSTFR avec qualité full HD et en illimité.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showYears')
SERIE_LIST = (True, 'showAlpha')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
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

    liste = [
        [
            'Action', 'action'], [
            'Animation', 'animation'], [
                'Aventure', 'aventure'], [
                    'Biopic', 'biopic'], [
                        'Comédie', 'comedie'], [
                            'Drame', 'drame'], [
                                'Epouvante Horreur', 'epouvante-horreur'], [
                                    'Espionnage', 'espionnage'], [
                                        'Famille', 'famille'], [
                                            'Fantastique', 'fantastique'], [
                                                'Guerre', 'guerre'], [
                                                    'Historique', 'historique'], [
                                                        'Judiciaire', 'judiciaire'], [
                                                            'Musical', 'musical'], [
                                                                'Policier', 'policier'], [
                                                                    'Romance', 'romance'], [
                                                                        'Science Fiction', 'science-fiction'], [
                                                                            'Sci-Fi & Fantasy', 'sci-fi-et-fantasy'], [
                                                                                'Thriller', 'thriller'], [
                                                                                    'Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1989, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/annee/' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0', str('0')], ['1', str('1')], ['2', str('2')], ['3', str('3')], ['4', str('4')], ['5', str('5')],
             ['6', str('6')], ['7', str('7')], ['8', str('8')], ['9', str('9')],
             ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F'], ['G', 'G'], ['H', 'H'],
             ['I', 'I'], ['J', 'J'], ['K', 'K'], ['L', 'L'], ['M', 'M'], ['N', 'N'], ['O', 'O'], ['P', 'P'],
             ['Q', 'Q'], ['R', 'R'], ['S', 'S'], ['T', 'T'], ['U', 'U'], ['V', 'V'], ['W', 'W'], ['X', 'X'],
             ['Y', 'Y'], ['Z', 'Z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/alphabet/' + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'radius-3">\\s*<a href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN[:-1] + entry[1]
            title = entry[2]

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

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
    pattern = '>([0-9]+)</a></div>.+?next"><a href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        number_next = re.search('-([0-9]+)', next_page).group(1)
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
        pattern = 'class="fsynopsis"><p>(.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'short-images radius-3".+?href="([^"]+)".+?<img src="([^"]+)".+?<figcaption>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:

            url = entry[0]
            thumb = URL_MAIN[:-1] + entry[1]
            title = movie_title + ' ' + entry[2]

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

    pattern = 'class="saision_LI2">\\s*<a href="([^"]+)">\\s*<span>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            title = movie_title + ' ' + entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'data-num="([^"]+).+?data-code="([^"]+).+?DIV_5.+?>([^<]+).+?src="/images/([^"]+).png'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            dataNum = entry[0]
            dataCode = entry[1]
            host = entry[2].capitalize()
            lang = entry[3].upper()

            # filtrage des hosters
            hoster = HosterGui().checkHoster(host)
            if not hoster:
                continue

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)
            lien = URL_MAIN + 'streamer.php?p=' + dataNum + '&c=' + dataCode

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', lien)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

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
