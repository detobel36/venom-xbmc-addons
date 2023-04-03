# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.comaddon import SiteManager, VSlog
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'cinemay_cc'
SITE_NAME = 'Cinemay_cc'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-box-office', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = ('', 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'serie-streaming', 'showMovies')
SERIE_GENRES = (True, 'showGenresTVShow')
SERIE_ANNEES = (True, 'showMovieYearsTVShow')
SERIE_LIST = ('', 'showAlphaTVShow')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')


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

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Liste alphabétique)',
        'az.png',
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
        'Séries (Liste alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
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

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (les plus vus)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenresTVShow():
    showGenres(sTypeSerie='/series')


def showGenres(sTypeSerie=''):
    gui = Gui()

    listegenre = [
        'action',
        'action-adventure',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'histoire',
        'horreur',
        'kids',
        'musique',
        'musical',
        'mystere',
        'news',
        'science-fiction',
        'science-fiction-fantastique',
        'reality',
        'romance',
        'soap',
        'talk',
        'telefilm',
        'thriller',
        'war-politics',
        'western']

    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:

        url = URL_MAIN + 'categories/' + igenre + sTypeSerie
        title = igenre.capitalize()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlphaTVShow():
    showAlpha(sTypeSerie='/series')


def showAlpha(sTypeSerie=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    _type = input_parameter_handler.getValue('site_url')

    liste = [['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'], ['H', 'h'],
             ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'], ['Q', 'q'],
             ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'],
             ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'letter/' + url + str(_type) + sTypeSerie)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYearsTVShow():
    showMovieYears(sTypeSerie='/series')


def showMovieYears(sTypeSerie=''):
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2001, 2023)):  # pas grand chose 32 - 90
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'annee/' + Year + sTypeSerie)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    if search:
        bvalid, stoken, scookie = getTokens()
        if bvalid:
            util = cUtil()
            search_text = util.CleanName(search)
            search = search.replace(' ', '+').replace('%20', '+')
            pdata = '_token=' + stoken + '&search=' + search
            url = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            request_handler = RequestHandler(url)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', URL_MAIN)
            request_handler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            request_handler.addHeaderEntry('Cookie', scookie)
            request_handler.addParametersLine(pdata)
            # request_handler.request()
            html_content = request_handler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # title img year surl
    pattern = '<figure>.+?data-src="([^"]+.jpg)" (?:alt|title)="([^"]+).+?year">([^<]*).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            desc = ''
            thumb = re.sub('/w\\d+/', '/w342/', entry[0])
            title = entry[1].replace(
                'film en streaming', '').replace(
                'série en streaming', '')

            # Titre recherché
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            year = entry[2]
            url2 = entry[3]
            display_title = title + '(' + year + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if search:
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showSelectType',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)
            elif '/serie' in url or 'série en streaming' in entry[1]:
                display_title = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    if not search:
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
    pattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-numbers'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSelectType(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    html_content = request.request()

    desc = ''
    parser = Parser()
    pattern = 'class="description">.*?<br>([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', movie_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('year', year)

    if 'class="num-epi">' in html_content:

        gui.addTV(
            SITE_IDENTIFIER,
            'showSaison',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)
    else:
        gui.addMovie(
            SITE_IDENTIFIER,
            'showLink',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSaison():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    pattern = '<a href="#season.+?class.+?saison (\\d+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sNumSaison = entry
            sSaison = 'Saison ' + sNumSaison
            sUrlSaison = url + "?sNumSaison=" + sNumSaison
            display_title = movie_title + ' ' + sSaison
            title = movie_title

            output_parameter_handler.addParameter('site_url', sUrlSaison)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showSXE',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    url, sNumSaison = url.split('?sNumSaison=')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    start = 'class="num-epi">' + sNumSaison
    end = 'id="season-'
    html_content = parser.abParse(html_content, start, end)
    pattern = 'class="description">.*?<br>([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = 'class="num-epi">\\d+x([^<]+).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            Ep = entry[0]
            url2 = entry[1]
            Saison = 'Saison' + ' ' + sNumSaison
            title = movie_title + ' ' + Saison + ' Episode' + Ep

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
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


def showLink(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    html_content = request.request()

    parser = Parser()
    pattern = 'class="description">.*?<br>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if False and 'class="num-epi">' in html_content and 'episode' not in url:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('desc', desc)
        gui.addTV(
            SITE_IDENTIFIER,
            'showSXE',
            movie_title,
            '',
            thumb,
            desc,
            output_parameter_handler)

        gui.setEndOfDirectory()
        return

    pattern = 'data-url="([^"]+).+?server.+?alt="([^"]+).+?alt="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        oHosterGui = HosterGui()
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            key = entry[0]
            host = entry[1].replace(
                'www.', '').replace(
                'embed.mystream.to', 'mystream')
            host = re.sub('\\.\\w+', '', host).capitalize()
            if not oHosterGui.checkHoster(host):
                continue

            lang = entry[2].upper()
            url2 = URL_MAIN + 'll/captcha?hash=' + key
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('lang', lang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe.*?src=([^\\s]+)'
    results = re.findall(pattern, html_content)
    if results:
        hoster_url = results[0]

        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getTokens():
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = request_handler.getResponseHeader()
    pattern = 'id="menu.+?name=_token value="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        token = results[1][0]

    pattern = 'XSRF-TOKEN=([^;]+).+?cinemay_session=([^;]+)'
    results = parser.parse(sHeader, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        XSRF_TOKEN = results[1][0][0]
        site_session = results[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; cinemay_session=' + site_session + ';'
    return True, token, cook


def cleanDesc(desc):
    list_comment = ['Voir film ', 'en streaming', 'Voir Serie ']
    for s in list_comment:
        desc = desc.replace(s, '')

    return desc
