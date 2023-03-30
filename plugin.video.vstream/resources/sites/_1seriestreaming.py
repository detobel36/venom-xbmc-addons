# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from itertools import chain
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = '_1seriestreaming'
SITE_NAME = '1 Serie Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showSeries')
SERIE_VIEWS = (URL_MAIN + 'series-populaires', 'showSeries')
SERIE_LIST = (URL_MAIN, 'showAlpha')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = ('', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VIEWS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Populaires)', 'comments.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'listes.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSerieYears():
    # for i in itertools.chain(range(5, 7), [8, 9]): afficher dans l'ordre (pense bete ne pas effacer)
    gui = Gui()
    generator = chain([1955], range(1957, 2023))

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(list(generator)):
        year = str(i)
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'annee/' + year)
        gui.addDir(SITE_IDENTIFIER, 'showSeries', year, 'annees.png', output_parameter_handler)

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
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'alphabet/' + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [['Action & Aventure', 'action-adventure'], ['Animation', 'animation'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Guerre', 'guerre'], ['Guerre & Politique', 'war-politics'], ['Histoire', 'histoire'], ['Kids', 'kids'],
             ['Musical', 'musical'], ['Musique', 'musique'], ['Mystère', 'mystere'], ['News', 'news'],
             ['Réalité', 'reality'], ['Romance', 'romance'], ['Science-fiction', 'science-fiction'],
             ['Science-Fiction Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Sport', 'sport'],
             ['Talk', 'talk'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'categories/' + url + '/series')
        gui.addDir(SITE_IDENTIFIER, 'showSeries', title, 'genres.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    parser = cParser()

    if search:
        util = cUtil()
        search_text = util.CleanName(search)
        search = search.replace(' ', '+').replace('&20', '+')
        valid, token, cookie = getTokens()
        if valid:
            url = URL_MAIN + 'search'
            pdata = '_token=' + token + '&search=' + search

            request_handler = RequestHandler(url)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            request_handler.addHeaderEntry('Referer', URL_MAIN)
            request_handler.addHeaderEntry('Cookie', cookie)
            request_handler.addParametersLine(pdata)
            html_content = request_handler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('siteUrl')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    pattern = 'link"><img src=([^ ]+).+?href="([^"]+).+?>([^<]+)'
    result = parser.parse(html_content, pattern)
    if not result[0]:
        gui.addText(SITE_IDENTIFIER)

    if result[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in result[1]:
            thumb = re.sub('/w\\d+/', '/w342/', entry[0])
            url2 = entry[1]
            if url2.startswith('/'):
                url2 = URL_MAIN[:-1] + url2
            title = entry[2]
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('siteUrl', url2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'showSaisons', title, '', thumb, '', output_parameter_handler)

        nextPage, paging = __checkForNextPage(html_content)
        if nextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', nextPage)
            gui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + paging, output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    parser = cParser()
    pattern = '> \\d+ </span><a href="([^"]+).+?>([^<]+)</a></div></div>'
    result = parser.parse(sHtmlContent, pattern)
    if result[0]:
        nextPage = result[1][0][0]
        numberMax = result[1][0][1]
        numberNext = re.search('page=([0-9]+)', nextPage).group(1)
        paging = numberNext + '/' + numberMax
        return nextPage, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = cParser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('siteUrl')
    thumb = input_parameter_handler.getValue('sThumb')

    html_content = RequestHandler(url).request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = 'fsynopsis"><p>([^<]+)<br>'
        result = parser.parse(html_content, pattern)
        if result[0]:
            desc = result[1][0]
    except BaseException:
        pass

    pattern = 'link"><img src=([^ ]+).+?href="([^"]+).+?>([^<]+)'
    result = parser.parse(html_content, pattern)

    if result[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in result[1]:

            if 'no-poster.svg' not in entry[0]:
                thumb = entry[0]
            else:
                thumb = thumb
            url = entry[1]
            title = entry[2]

            output_parameter_handler.addParameter('siteUrl', url)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', thumb)
            output_parameter_handler.addParameter('sDesc', desc)
            gui.addSeason(SITE_IDENTIFIER, 'showEpisodes', title, '', thumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = cParser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('siteUrl')
    movie_title = input_parameter_handler.getValue('sMovieTitle')
    thumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('sDesc')

    html_content = RequestHandler(url).request()

    pattern = 'LI2"><a href="([^"]+)"><span>([^<]+)'
    result = parser.parse(html_content, pattern)

    if result[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in result[1]:

            url = entry[0]
            title = movie_title + entry[1]

            output_parameter_handler.addParameter('siteUrl', url)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', thumb)
            output_parameter_handler.addParameter('sDesc', desc)
            gui.addEpisode(SITE_IDENTIFIER, 'showLinks', title, '', thumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    parser = cParser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('siteUrl')
    movie_title = input_parameter_handler.getValue('sMovieTitle')
    thumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('sDesc')

    html_content = RequestHandler(url).request()

    pattern = 'code="([^"]+).+?</i>([^<]+).+?flag/([^ ]+).png'
    result = parser.parse(html_content, pattern)

    if result[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in result[1]:

            host = entry[1].replace('www.', '')
            host = re.sub('\\..+', '', host).capitalize()
            if not HosterGui().checkHoster(host):
                continue

            lang = entry[2].replace('default', '').upper()
            url = URL_MAIN + 'll/captcha?hash=' + entry[0]
            title = ('%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('siteUrl', url)
            output_parameter_handler.addParameter('sMovieTitle', movie_title)
            output_parameter_handler.addParameter('sThumb', thumb)
            output_parameter_handler.addParameter('sHost', host)
            output_parameter_handler.addParameter('sLang', lang)
            output_parameter_handler.addParameter('sDesc', desc)
            gui.addLink(SITE_IDENTIFIER, 'showHosters', title, thumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('siteUrl')
    movie_title = input_parameter_handler.getValue('sMovieTitle')
    thumb = input_parameter_handler.getValue('sThumb')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', url)

    html_content = request_handler.request()
    hoster_url = request_handler.getRealUrl()

    if 'captcha' not in hoster_url:
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    else:
        parser = cParser()
        pattern = 'src=([^ ]+)'
        result = parser.parse(html_content, pattern)
        if result[0]:
            hoster_url = result[1][0]
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def getTokens():
    parser = cParser()
    request_handler = RequestHandler(URL_MAIN + 'accueil')
    html_content = request_handler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    header = request_handler.getResponseHeader()
    pattern = 'name=_token value="([^"]+)'
    result = parser.parse(html_content, pattern)

    if not result[0]:
        return False, 'none', 'none'

    token = result[1][0]
    pattern = 'XSRF-TOKEN=([^;]+).+?.+?1seriestreaming_session=([^;]+)'
    result = parser.parse(header, pattern)

    if result[0]:
        XSRF_TOKEN = result[1][0][0]
        site_session = result[1][0][1]
    else:
        return False, 'none', 'none'

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; 1seriestreaming_session=' + site_session + ';'
    return True, token, cook
