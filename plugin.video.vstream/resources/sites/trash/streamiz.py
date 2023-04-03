# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 37 https://streamiz-filmze.org/ 24122020
# url instable et de plus en plus souvent  redirection vers streamcomplet3
# (clone qui le remplace)
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


SITE_IDENTIFIER = 'streamiz'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Films en streaming.'

URL_MAIN = 'https://streamiz-filmze.org/v7/'


MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/box-office/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/vostfr/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    liste = []
    listegenre = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'drame',
        'guerre',
        'historique',
        'horreur',
        'musical',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western',
        'documentaire',
        'spectacle']

    # href="/films/action/
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'films/' + igenre + '/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
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

    if search:

        search = search.replace(' ', '+').replace('%20', '+')
        pData = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + search
        url = URL_MAIN + 'index.php?do=search'
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', URL_MAIN)
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addParametersLine(pData)
        html_content = request_handler.request()

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # on ne récupère pas les films aléatoire
    end = html_content.find('<b>Film aléatoire</b>')
    html_content = html_content[:end]

    parser = Parser()
    pattern = 'images radius-3">.+?src="([^"]*)" alt="([^"]*).+?(?:|rip"><.+?>([^<]*).+?)link"><a href="([^"]*)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            title = entry[1]
            lang = entry[2]
            url2 = entry[3]

            display_title = ('%s (%s)') % (title, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '>([^<]+)</a> *</div></div><div class="col-lg-1 col-sm-2 col-xs-2 pages-next"><a href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showLinks():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'Synopsis.+?info-text">([^<]*)'
    results = parser.parse(html_content, pattern)
    desc = 'streamiz-filmze.org'
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    pattern = '<iframe.+?src="([^"]*)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:
            url = entry

            hoster = HosterGui().checkHoster(url)
            if (hoster):
                hostName = hoster.getDisplayName()
            else:
                hostName = getHostName(url)

            display_title = ('%s [COLOR coral]%s[/COLOR]') % (title, hostName)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
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

    hoster_url = url
    hoster = HosterGui().checkHoster(hoster_url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def getHostName(url):

    try:
        if 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        host = url

    return host.capitalize()
