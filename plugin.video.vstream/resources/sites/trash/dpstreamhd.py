# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'dpstreamhd'
SITE_NAME = 'DpStream HD'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VIEWS = (URL_MAIN + 'film-box-office', 'showMovies')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'serie-streaming', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
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
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    # https://serie.dpstreamhd.com/categories/romance
    # Aucun résultats: war-politics, soap, kids, talk, news, science-fiction-fantastique, action-adventure, Musical
    # reality
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
        'mystere',
        'romance',
        'science-fiction',
        'telefilm',
        'thriller',
        'western']

    url1g = URL_MAIN + 'categories/'

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


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        bvalid, stoken, scookie = getTokens()
        if bvalid:
            util = cUtil()
            search_text = util.CleanName(search)
            pdata = '_token=' + stoken + '&search=' + search
            url = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            request_handler = RequestHandler(url)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
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

    # thumb note ref title
    pattern = 'class="post.+?src=([^ ]+.jpg) alt.+?svg></i>([^<]+).+?href="([^"]+).+?entry-title">([^<]+)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            desc = 'Note :' + entry[1]
            url2 = entry[2]
            title = entry[3]
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if '-serie-' not in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showSXE', title, '',
                          thumb, desc, output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-nav">Next'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


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

    pattern = 'résume de.+?<br>([^<]+)'
    aResult_ = parser.parse(html_content, pattern)
    if aResult_[0] is True:
        sDescColor = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult_[1][0])
        if desc:
            desc = desc + '\r\n' + sDescColor
        else:
            desc = sDescColor

    pattern = 'class="numep">([^<]+).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    list_saison = []

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        sSaison = ''
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
                gui.addTV(SITE_IDENTIFIER, 'showLink', title, '',
                          thumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()

    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request = RequestHandler(url)
    html_content = request.request()

    pattern = 'année<.span>\\s*([^<]+).+?résume de.+?<br>([^<]+)'
    aResult_ = parser.parse(html_content, pattern)
    year = ''
    desc = 'no description'
    if aResult_[0] is True:
        aresult = aResult_[1][0]
        year = aresult[0]
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aresult[1])

    pattern = 'data-url="([^"]+).+?alt="([^"]+)'
    results = parser.parse(html_content, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            key = entry[0]
            host = entry[1].replace(
                'www.', '').replace(
                'embed.mystream.to', 'mystream')
            host = re.sub('\\.\\w+', '', host).capitalize()
            url2 = URL_MAIN + 'll/captcha?hash=' + key

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, year, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('thumb', thumb)
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
    pattern = 'name=_token.+?value="([^"]+).+?class="filter-options'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        token = results[1][0]

    pattern = 'XSRF-TOKEN=([^;]+).+?dpstreamhd_session=([^;]+)'
    results = parser.parse(sHeader, pattern)

    if not results[0]:
        return False, 'none', 'none'

    if results[0]:
        XSRF_TOKEN = results[1][0][0]
        site_session = results[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; dpstreamhd_session=' + site_session + ';'
    return True, token, cook
