# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import unicodedata
import requests
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import dialog, SiteManager
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'BuzzMonClick'
SITE_DESC = 'Films & Séries en Streaming de qualité entièrement gratuit.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = ('https://buzzmonclick.net/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMoviesSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Replay TV',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'divertissement/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Divertissement',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'tele-realite/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Télé-Réalité',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Documentaires', 'documentaires'], ['Divertissement', 'divertissement'],
             ['Infos/Magazines', 'infos-magazine'], ['Télé-Réalité', 'tele-realite']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
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
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div id="post-[0-9]+".+?<a class="clip-link.+?title="([^"]+)" href="([^"]+).+?img src="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            try:
                title = unicode(entry[0], 'utf-8')  # converti en unicode
                title = unicodedata.normalize(
                    'NFD', title).encode(
                    'ascii', 'ignore')  # vire accent
                # title = unescape(str(title))
                title = title.encode("utf-8")
            except NameError:
                title = entry[0]

            # mise en page
            title = title.replace(
                'Permalien pour', '').replace(
                '&prime;', '\'')
            title = re.sub(
                '(?:,)* (?:Replay |Video )*du ([0-9]+ [a-zA-z]+ [0-9]+)',
                ' (\\1)',
                title)
            title = re.sub(', (?:Replay|Video)$', '', title)
            url = entry[1]
            thumb = entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'doc.png',
                thumb,
                '',
                output_parameter_handler)

        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = 'class="nextpostslink" rel="next" href="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'wp-block-button.+?(?:href=|src=)"([^"]+)".+?>(?:([^<]+)|)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            host = entry[1]
            if host == "":
                host = entry[0].split('/')[2].split('.')[0]

            url = entry[0]
            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)

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

    if 'forum-tv' in url:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(url, headers={'User-Agent': UA})
        html_content = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y)
                                  for x, y in s.cookies.items()])

        parser = Parser()
        pattern = '<input type="hidden".+?value="([^"]+)"'
        results = parser.parse(html_content, pattern)

        if results[0]:
            data = "_method=" + results[1][0] + "&_csrfToken=" + \
                results[1][1] + "&ad_form_data=" + Quote(results[1][2])
            data += "&_Token%5Bfields%5D=" + \
                Quote(results[1][3]) + "&_Token%5Bunlocked%5D=" + Quote(results[1][4])
            # Obligatoire pour validé les cookies.
            xbmc.sleep(6000)
            request_handler = RequestHandler(
                'https://forum-tv.org/adslinkme/links/go')
            request_handler.setRequestType(1)
            request_handler.addHeaderEntry('Referer', url)
            request_handler.addHeaderEntry(
                'Accept', 'application/json, text/javascript, */*; q=0.01')
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
                hoster = False

                if 'replay.forum-tv.org' in hoster_url:
                    request_handler = RequestHandler(hoster_url)
                    html_content = request_handler.request()
                    pattern = 'iframe.+?src="([^"]+)'
                    parser = Parser()
                    results = parser.parse(html_content, pattern)
                    if results[0]:
                        hoster_url = results[1][0]
                    hoster = HosterGui().checkHoster(hoster_url)

                elif 'dood.forum-tv.org' in hoster_url:
                    showDoodHosters(movie_title, hoster_url)
                else:
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


def showDoodHosters(movie_title, url):
    gui = Gui()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a href="([^"]+)".+?value=\'([^\']+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            host = entry[1]

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                movie_title,
                output_parameter_handler)
