# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # 06/02/2021
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress  # , VSlog
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamcomplet'
SITE_NAME = 'StreamComplet'
SITE_DESC = 'Les meilleurs films en version française'

URL_MAIN = 'https://www2.stream-complet.me/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_MOVIE = ('http://', 'load')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
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

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

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
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'action'], [
            'Animation', 'animation'], [
                'Aventure', 'aventure'], [
                    'Comédie', 'comedie'], [
                        'Drame', 'drame'], [
                            'Fiction', 'fiction'], [
                                'Guerre', 'guerre'], [
                                    'Historique', 'historique'], [
                                        'Horreur', 'horreur'], [
                                            'Musique', 'musical'], [
                                                'Policier', 'policier'], [
                                                    'Romance', 'romance'], [
                                                        'Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/' + url + '/')
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
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)".+?<div class="(movies">(.+?)<|moviefilm">)'
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

            if (entry[0] == '/'):
                continue

            url = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN[:-1] + entry[1]
            title = entry[2]
            year = entry[4]

            # tris search
            if search and total > 3:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/([0-9]+)/', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<span class="current">.+?<a class="page larger" href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        return URL_MAIN + results[1][0]

    return False


def showLinks():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<li class="player link" data-player="([^"]+)">.+?<span class="p-name">([^"]+)</span>'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            sDisplayName = ('%s [COLOR coral]%s[/COLOR]') % (title, entry[1])

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayName,
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
    # vimple redirect to ok or openload
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    pattern = 'url=([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

#
#
# Ancien code du site .xyz
# si retour en arriere
#
#

#    pattern = '<iframe.+?src="(http(?:|s):\/\/media\.vimple\.me.+?f=([^"]+))"'
#    results = parser.parse(html_content, pattern)
#    if results[0]:

#        url2 = results[1][0][0]
#
#        request_handler = RequestHandler(url2)
#        request_handler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0')
#        request_handler.addHeaderEntry('Referer', url)
#        html_content = request_handler.request()
#
#        pattern = '<iframe src="([^"]+)"'
#        results = parser.parse(html_content, pattern)
#
#        if results[0]:
#            hoster_url = 'https:' + results[1][0]
#            #VSlog(hoster_url)
#            hoster = HosterGui().checkHoster(hoster_url)
#            if (hoster):
#                hoster.setDisplayName(movie_title)
#                hoster.setFileName(movie_title)
#                HosterGui().showHoster(gui, hoster, hoster_url, thumb)
#        else:
#            html_content = parser.abParse(html_content, "<script>", "</script><script>")
#
#            pattern = 'eval\s*\(\s*function(?:.|\s)+?{}\)\)'
#            results = parser.parse(html_content, pattern)
#            if results[0]:
#                html_content = cPacker().unpack(results[1][0])
#                html_content = html_content.replace('\\', '')
#                #VSlog(html_content)
#                code = re.search('(https://openload.+?embed\/.+?\/)', html_content)
#                if code:
#                    hoster_url = code.group(1)
#                   #VSlog(hoster_url)
#                   hoster = HosterGui().checkHoster(hoster_url)
#                   if (hoster):
#                       hoster.setDisplayName(movie_title)
#                       hoster.setFileName(movie_title)
#                       HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    gui.setEndOfDirectory()
