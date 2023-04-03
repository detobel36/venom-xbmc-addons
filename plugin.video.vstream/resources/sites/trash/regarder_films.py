# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'regarder_films'
SITE_NAME = 'Regarder-films-gratuit'
SITE_DESC = 'Série streaming gratuit illimité vf et vostfr.'

URL_MAIN = 'http://regarder-film-gratuit.online/'

SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_SERIES = (URL_MAIN, 'load')
SERIE_LIST = (URL_MAIN + 'liste-de-series/', 'showAlpha')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showAlpha():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(SERIE_LIST[0])
    html_content = request_handler.request()

    pattern = '<font color="red".+?>(.+?)<\\/font>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLetter = str(entry).replace('=', '')
            dAZ = str(entry)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('dAZ', dAZ)
            gui.addDir(
                SITE_IDENTIFIER,
                'showList',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'az.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    request_handler = RequestHandler(SERIE_LIST[0])
    dAZ = input_parameter_handler.getValue('dAZ')
    html_content = request_handler.request()

    # Decoupage pour cibler la partie selectionnée
    pattern = '<font color="red".+?>' + dAZ + '</font>(.+?)<p><strong>'
    results = parser.parse(html_content, pattern)

    # regex pour listage series sur la partie decoupée
    pattern = '<a href="([^"]+)".+?>(.+?)<\\/a>'
    results = parser.parse(results, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = str(entry[0])
            # on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in url:
                continue
            title = str(entry[1]).decode("unicode_escape").encode(
                "latin-1").replace('&#8217;', '\'').replace('&#8212;', '-')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'az.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Dessin animés', URL_MAIN + 'category/dessins-animes/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['News', URL_MAIN + 'category/news/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="post".+?<h2><a class="title" href="(.+?)" rel="bookmark">(.+?)</a>.+?src="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Si recherche et trop de resultat, on nettoye
            if search and total > 2:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        entry[1]) == 0:
                    continue

            url = str(entry[0])
            title = str(entry[1]).replace(
                '&#8212;', '-').replace('&#8217;', '\'')
            thumb = str(entry[2])
            # on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in thumb:
                continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'serieHosters', title,
                      '', thumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class="nextpostslink" rel="next" href="(.+?)">..<'
    results = re.findall(pattern, html_content, re.UNICODE)
    if (results):
        return results[0]

    return False


def serieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    # recuperation thumb
    thumb = ''
    pattern = '<p><img src="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        thumb = results[1][0]

    # if 'streamzz' in url:
        # pattern = '<div class="boton reloading"><a href="([^"]+)">'
    # else:
    pattern = '<center><.+?<stron.+?((?:VF|VOSTFR|VO)).+?trong>|<p><a href="([^"]+)".+?target="_blank">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                lang = entry[0].replace('&#8230;', '').replace(':', '')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    lang +
                    '[/COLOR]')
            else:
                hoster_url = entry[1]
                hoster = HosterGui().checkHoster(hoster_url)

                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
