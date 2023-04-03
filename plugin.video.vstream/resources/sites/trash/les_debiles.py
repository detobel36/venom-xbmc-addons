# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'les_debiles'
SITE_NAME = 'Les Débiles'
SITE_DESC = 'Vidéos drôles, du buzz, des fails et des vidéos insolites'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN, 'showMovies')
URL_SEARCH_MISC = (URL_MAIN, 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenre')
NETS_CATS = (True, 'showGenres')


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

    output_parameter_handler.addParameter('site_url', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos du net',
        'buzz.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_CATS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_CATS[1],
        'Vidéos (Catégories)',
        'genres.png',
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


def showGenre():
    gui = Gui()

    liste = [['Nouveautés', 'videos-s0-1'], ['Top Vues', 'videos-s1-1'], ['Top Vote', 'videos-s2-1'],
             ['Hit Parade', 'videos-s5-1'], ['Fatality', 'videos-s7-1'], ['Vidéos Longues', 'videos-s3-1']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + url + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN + 'categories.html')
    html_content = request_handler.request()

    pattern = '<li><a href="([^>]+)">([^<]+)</a></li>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            title = entry[1]

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
        idx = search.rfind("/") + 1
        url = search[:idx] + "".join([i for i in search[idx:] if i.isalpha() or i in [
                                       " ", "/"]]).replace(" ", "-") + '-s0-r1.html'.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace('&gt;&gt;', 'suivante')

    pattern = 'class="blockthumb">.+?class="imageitem" src="([^"]+)".+?class="titleitem"><a href="([^"]+)">(.+?)</a>'

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

            thumb = entry[0]
            url = entry[1]
            title = entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            paging = re.search('-([0-9]+).html', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a href="([^"]+)">suivante</a></li>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # lien direct mp4
    pattern = "<source src='([^']+)' type='video/mp4'"
    results = parser.parse(html_content, pattern)

    # lien dailymotion
    if not results[0]:
        pattern = 'src="([^"]+)\\?.+?" allowfullscreen></iframe>'
        results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            # Certains URL "dailymotion" sont écrits : //www.dailymotion.com
            if hoster_url[:4] != 'http':
                hoster_url = 'http:' + hoster_url

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)
    else:
        # play premium vid
        vidpremium = html_content.find('alt="Video Premium"')
        if vidpremium != -1:
            pattern = "window.location.href = '([^']+)';"
            results = parser.parse(html_content, pattern)
            if results[0]:
                hoster_url = results[1][0].replace(
                    'download-', '').replace('.html', '')

                hoster_url = 'http://videos.lesdebiles.com/' + hoster_url + '.mp4'

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)
        else:
            gui.addText(SITE_IDENTIFIER, '(Video non visible)')

    gui.setEndOfDirectory()
