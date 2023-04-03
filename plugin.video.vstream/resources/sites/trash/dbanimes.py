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

SITE_IDENTIFIER = 'dbanimes'
SITE_NAME = 'DBanimes'
SITE_DESC = 'animés en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_VOSTFRS = (URL_MAIN + 'genre/anime-vostfr/', 'showAnimes')
ANIM_NEWS = (URL_MAIN + 'genre/anime-vostfr/', 'showAnimes')
ANIM_MOVIES = (URL_MAIN + 'films/', 'showAnimes')
# ANIM_LIST = (URL_MAIN + 'liste/a/', 'showAlpha')
ANIM_GENRES = (True, 'showGenres')
ANIM_LAST_EPISODES = (URL_MAIN, 'showAnimes')
key_serie = '?key_serie&s='
key_film = '?key_film&s='

URL_SEARCH = (URL_MAIN + '?s=', 'showAnimes')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showAnimes')
URL_INTERNALSEARCH_SERIES = (URL_MAIN + key_serie, 'showAnimes')
URL_INTERNALSEARCH_MOVIES = (URL_MAIN + key_film, 'showAnimes')
FUNCTION_SEARCH = 'showAnimes'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_LAST_EPISODES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LAST_EPISODES[1],
        'Animés (Derniers épisodes)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIES[1],
        'Animés (Films)',
        'animes.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Ordre alphabétique)', 'az.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [['Action & aventure', 'action-adventure'], ['Aventure', 'aventure'],
             ['Comédie', 'comedie'], ['Crime', 'crime'], ['Drame', 'drame'], ['Fantasy', 'fantasy']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genre/anime-' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'class=liste><a href=(\\S+).+?mb-2">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            sLetter = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('AZ', sLetter)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAnimes',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'az.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_INTERNALSEARCH_MOVIES[0] + search_text
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_INTERNALSEARCH_SERIES[0] + search_text
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showAnimes(search=''):
    gui = Gui()
    if search:
        url = search.replace(' ', '+') + '&post_type=anime&submit='
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'movie-gride-agile1.+?href="([^"]+)" title="([^"]+).+?src="([^"]+)'
    parser = Parser()
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

            desc = ''
            url2 = entry[0]
            title = entry[1].replace('VOSTFR', '').replace('vostfr', '').replace(
                'Vostfr', '')  # à confirmer : tous vostr meme ceux  notés non vostfr
            title = title.replace(
                'Saision', 'Saison').replace(
                'Sasion', 'Saison')
            display_title = title
            thumb = entry[2]

            if key_serie in url:
                if 'film' in title.lower():
                    continue
            if key_film in url:
                if 'film' not in title.lower():
                    continue

            if 'film' in title.lower():
                title = title.replace(
                    'Film', '').replace(
                    'film', '')  # à reverifier .replace('Movie', '')
                display_title = title + ' [Film]'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if URL_MAIN + 'films/' == url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showAnimes',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '>(\\d+)</a></li><li><a class="next page-numbers" href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, False


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    pattern = 'Synopsis\\s*:(.*?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                       cleanDesc(results[1][0]))

    year = ''
    pattern = 'Année de Production.+?(\\d{4}).+?/div'
    results = parser.parse(html_content, pattern)
    if results[0]:
        year = results[1][0]

    pattern = 'href="([^"]+)" class="btn btn-default mb-2" title=.+?>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME, large=total > 50)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            url = entry[0]
            sEpisode = entry[1]
            title = movie_title + ' ' + sEpisode
            display_title = title
            if year:
                display_title = title + '(' + year + ')'

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)
    # i = 0
    if results[0]:
        for entry in results[1]:
            hoster_url = entry.strip()
            if hoster_url.startswith('//'):
                hoster_url = 'https:' + hoster_url

            # host = getHostName(hoster_url)
            # i = i + 1
            # display_title = '%s [COLOR coral]%s[/COLOR]' % (movie_title, host)

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getHostName(url):
    hoster = HosterGui().checkHoster(url)
    if hoster:
        return hoster.getDisplayName()
    try:
        if 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        host = url
    return host.capitalize()


def cleanDesc(desc):
    parser = Parser()
    pattern = '(<.+?>)'
    results = parser.parse(desc, pattern)
    if results[0]:
        for entry in results[1]:
            desc = desc.replace(entry, '')
    return desc
