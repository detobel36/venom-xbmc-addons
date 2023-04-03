# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 27 https://cinemey.com/
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import re
return False  # HS voir https://cinemay.cc/ memes films et series


SITE_IDENTIFIER = 'cinemey'
SITE_NAME = 'Cinemey'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = 'https://cinemey.com/'
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VIEWS = (URL_MAIN + 'classement-box-office-film', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'les-series-en-streaming', 'showMovies')

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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    # https://cinemey.com/categorie/romance
    # Aucun résultats war-politics, soap, kids, talk, news,
    # science-fiction-fantastique, reality, action-adventure
    listegenre = [
        'action',
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
        'musique',
        'Musical',
        'mystere',
        'romance',
        'science-fiction',
        'telefilm',
        'thriller',
        'western']

    url1g = URL_MAIN + 'categorie/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    # https://cinemey.com/annee/2020
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2001, 2023)):  # pas grand chose 32 - 90
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'annee/' + Year)
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

    if search:

        bvalid, stoken, scookie = GetTokens()
        if bvalid:
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
            request_handler.request()

            # constatation : on est oblige de faire 2 requetes
            # dans le cas ou le mot recherché est composé ?
            xbmc.sleep(500)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', URL_MAIN)
            request_handler.addHeaderEntry('Cookie', scookie)
            request_handler.addParametersLine(pdata)

            html_content = request_handler.request()

        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # title img year surl
    pattern = '<article class.+?data-url.+?title="([^"]*).+?img src=([^\\s]*).+?year">([^<]+).+?href="([^"]+)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            desc = ''
            title = entry[0]
            thumb = entry[1]
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
                    output_parameter_handler)
            elif SERIE_NEWS[0] in url:
                display_title = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSXE',
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
        if (next_page):
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


def showSelectType():
    gui = Gui()

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
            'showSXE',
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


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'class="description">.*?<br>([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = 'class="num-epi">([^<]+).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    list_saison = []

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if 'x' in entry[0]:
                # class="numep">1x13<
                saison, episode = entry[0].split('x')
                if saison not in list_saison:
                    list_saison.append(saison)
                    sSaison = 'Saison ' + saison
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue]' +
                        sSaison +
                        '[/COLOR]')

                url2 = entry[1]
                title = movie_title + ' ' + sSaison + ' Episode' + episode

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


def showLink():
    gui = Gui()

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

            hoster = oHosterGui.checkHoster(host)
            if not hoster:
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
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe.*?src=([^\\s]+)'
    results = re.findall(pattern, html_content)
    if results:
        hoster_url = results[0]

        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def GetTokens():
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = request_handler.getResponseHeader()
    pattern = '<nav id="menu.+?name=_token.+?value="([^"]+).+?<div class="typeahead'
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
