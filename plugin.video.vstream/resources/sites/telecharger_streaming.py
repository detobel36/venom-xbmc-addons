# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import SiteManager

SITE_IDENTIFIER = 'telecharger_streaming'
SITE_NAME = '[COLOR violet]Telecharger-streaming[/COLOR]'
SITE_DESC = 'films en streaming, Emissions en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_NEWS = (URL_MAIN + 'category/emissions-tv/', 'showMovies')
REPLAYTV_DIVERTISSEMENT = (
    URL_MAIN +
    'category/emissions-tv/divertissements-telerealite/',
    'showMovies')
REPLAYTV_INVESTIGATION = (
    URL_MAIN +
    'category/emissions-tv/reportages-investigations/',
    'showMovies')


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
        'Toutes les emissions',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', REPLAYTV_DIVERTISSEMENT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_DIVERTISSEMENT[1],
        'Emissions de Divertissements/Téléréalité',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_INVESTIGATION[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_INVESTIGATION[1],
        'Emissions de Reportages/Investigations',
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


def showMovies(search=''):
    gui = Gui()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_MISC[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
        pattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+)">.+?<p>.+?Synopsis :([^"]+)</p>'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        pattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+).+?<img.+?class="alignleft.+?src="([^"]+).+?Synopsis :(.+?)</p>'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if search:
                url2 = entry[0]
                title = entry[1]
                if not util.CheckOccurence(search_text, title):
                    continue  # Filtre de recherche
                thumb = ""
                desc = entry[2].replace('</strong>', '')
            else:
                url2 = entry[0]
                title = entry[1]
                thumb = entry[2]
                desc = entry[3].replace('</strong>', '')

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
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
    pattern = 'class="next" href="([^"]+)".+?<\\/a><a class="last" href="https.+?page\\/(\\d+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = GetAllLink(request_handler.request())

    parser = Parser()
    pattern = '<span style="color: #ff00ff;">([^<]+?)</span>|<a href="([^"]+)"'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            else:
                hoster_url = entry[1]
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def GetAllLink(html_content):
    parser = Parser()
    pattern = '<p><span id="more-.+?"></span></p>(.+?)(?:<p><strong><span style="color: #00ffff;">|<h3><strong>)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''
