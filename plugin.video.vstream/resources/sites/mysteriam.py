# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'mysteriam'
SITE_NAME = 'Mysteriam'
SITE_DESC = 'Documentaire streaming '

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

DOC_DOCS = (True, 'load')
DOC_NEWS = (URL_MAIN + 'documents-videos.html', 'showMovies')
DOC_GENRES = (
    URL_MAIN +
    'videos-documentaires/categories-videos.html',
    'showGenres')


def load():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="item-title hasTooltip" title="([^"]+).+?href="([^"]+)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = URL_MAIN + entry[1]
            title = entry[0]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'doc.png',
                '',
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = parser.abParse(html_content, '', 'Derniers Docus')
    pattern = 'Thumbnail Image -->.+?title="([^"]+).+?src="([^"]+).+?href="([^"]+).+?src="([^"]+).+?info-description">([^<]+)'

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

            sMedia = entry[1]
            if 'video.png' not in sMedia:
                continue
            title = entry[0]
            url2 = URL_MAIN[:-1] + entry[2]
            thumb = URL_MAIN[:-1] + entry[3]
            desc = entry[4]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
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

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = 'pagenav">[0-9]+</span></li><li><a title="(\\d+)" href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_next = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        paging = number_next
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

    pattern = '<iframe.+?src="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in list(set(results[1])):
            hoster_url = str(entry).replace('?&rel=0', '')

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
