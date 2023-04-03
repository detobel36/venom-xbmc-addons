# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'cine974'
SITE_NAME = 'Ciné 974'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'streaming/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'src="([^"]+)" alt="([^"]+)" class="sc.+?synop">([^<]*).+?href="([^"]+)">Regarder'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
        gui.setEndOfDirectory()
        return

    total = len(results[1])
    progress_ = Progress().VScreate(SITE_NAME)
    output_parameter_handler = OutputParameterHandler()
    for entry in results[1]:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break

        thumb = entry[0]
        if thumb.startswith('/'):
            thumb = URL_MAIN[:-1] + thumb
        title = entry[1]
        desc = entry[2]
        url2 = entry[3]
        if url2.startswith('/'):
            url2 = URL_MAIN[:-1] + url2

        output_parameter_handler.addParameter('site_url', url2)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('desc', desc)

        gui.addMovie(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            '',
            thumb,
            desc,
            output_parameter_handler)

    progress_.VSclose(progress_)

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
    pattern = '>(\\d+)</a></li><li><a href="([^"]+)"><i class="fa fa-angle-right'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        number_next = re.search('p=([0-9]+)', results[1][0][1]).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<iframe width="100%" height="400" src="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            link = re.sub('.+?embed/', '', entry)
            link = link.replace('?rel=0', '')
            hoster_url = 'https://www.youtube.com/watch?v=' + link

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
