# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# plus vraiment le meme site
import re
import requests
import xbmc

from resources.lib.comaddon import dialog, Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'topreplay'
SITE_NAME = 'TopReplay'
SITE_DESC = 'Replay TV'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenres')
REPLAYTV_TVSHOWS = (True, 'showTvShows')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')


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

    output_parameter_handler.addParameter('site_url', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Nouveautés',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Genres',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_TVSHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_TVSHOWS[1],
        'Emissions TV',
        'tv.png',
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
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = 'main-menu'
    end = '/ul'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            if 'Accueil' in title:
                continue

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showTvShows():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = 'ÉMISSIONS TV'
    end = '</div></div> </aside>'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)</a>'
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
            title = entry[1]
            if 'Contactez' in title:
                continue

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # &hellip'
    pattern = '<article.+?href="([^"]+)">([^<]+).+?img.+?src="([^"]+).+?<div class="entry"><p>(.+?)Vous pouvez toujours regarder'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            thumb = entry[2]
            desc = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'replay.png',
                thumb,
                desc,
                output_parameter_handler)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'title>TopReplay - Page [\\d+] sur (\\d+).+?href="([^"]+)"\\s*>Chargez plus'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    # premiere page
    pattern = 'href="([^"]+)"\\s*>Chargez plus'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next
        return next_page, paging

    return False, 'none'


def showLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a class="myButton" href="([^<]+)" target="_blank"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for hoster_url in results[1]:
            output_parameter_handler.addParameter('site_url', hoster_url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                movie_title,
                'replay.png',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    if 'mon-tele' in url:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(url, headers={'User-Agent': UA})
        html_content = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y)
                                  for x, y in s.cookies.items()])

        parser = Parser()
        pattern = '<input type="hidden".+?value="([^"]+)"'
        results = parser.parse(html_content, pattern)

        from resources.lib import librecaptcha
        test = librecaptcha.get_token(
            api_key="6LezIsIZAAAAABMSqc7opxGc3xyCuXtAtV4VlTtN",
            site_url="https://mon-tele.com/",
            user_agent=UA,
            gui=False,
            debug=False
        )

        if results[0]:
            data = "_method=" + results[1][0] + "&_csrfToken=" + results[1][1] + "&ref=&f_n=" + results[1][2]\
                              + "&g-recaptcha-response=" + test + "&_Token%5Bfields%5D=" + Quote(results[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(results[1][4])

            request_handler = RequestHandler(url)
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('Referer', url)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Content-Length', len(data))
            request_handler.addHeaderEntry(
                'Content-Type', "application/x-www-form-urlencoded")
            request_handler.addHeaderEntry('Cookie', cookie_string)
            request_handler.addParametersLine(data)
            html_content = request_handler.request()

        parser = Parser()
        pattern = '<input type="hidden".+?value="([^"]+)"'
        results = parser.parse(html_content, pattern)

        if results[0]:
            data = "_method=" + results[1][0] + "&_csrfToken=" + results[1][1] + "&ad_form_data="\
                              + Quote(results[1][2]) + "&_Token%5Bfields%5D=" + Quote(results[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(results[1][4])

            # Obligatoire pour validé les cookies.
            xbmc.sleep(15000)
            request_handler = RequestHandler(
                'https://mon-tele.com/obtenirliens/links/go')
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('Referer', url)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Content-Length', len(data))
            request_handler.addHeaderEntry(
                'Content-Type', "application/x-www-form-urlencoded; charset=UTF-8")
            request_handler.addHeaderEntry(
                'X-Requested-With', 'XMLHttpRequest')
            request_handler.addHeaderEntry('Cookie', cookie_string)
            request_handler.addParametersLine(data)
            html_content = request_handler.request()

            pattern = 'url":"([^"]+)"'
            results = parser.parse(html_content, pattern)
            if results[0]:
                hoster_url = results[1][0]
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)
    else:
        hoster_url = url
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
