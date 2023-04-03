# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 44 https://funeralforamanga.fr/
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress


SITE_IDENTIFIER = 'funeralforamanga'
SITE_NAME = 'Funeral for a manga'
SITE_DESC = 'animés en streaming'

URL_MAIN = 'https://funeralforamanga.fr/'

ANIM_ANIMS = ('http://', 'load')

ANIM_NEWS = (URL_MAIN + 'videos?sk=c&unlicenced=1&p=1', 'showMovies')
ANIM_POPULAR = (URL_MAIN + 'videos?sk=b&unlicenced=1&p=1&', 'showMovies')
ANIM_ANNEES = (True, 'showAllYears')
ANIM_ALPHA = (True, 'showAllAlpha')
ANIM_GENRES = (True, 'showAllGenre')
ANIM_VFS = (URL_MAIN + 'videos?sk=c&unlicenced=1&lang=vf&p=1', 'showMovies')
ANIM_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&unlicenced=1&lang=vostfr&p=1',
    'showMovies')

ANIM_SERIE_NEWS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&p=1',
    'showMovies')
ANIM_SERIE_POPULAR = (
    URL_MAIN +
    'videos?sk=b&filter=serie&unlicenced=1&p=1',
    'showMovies')
ANIM_SERIE_ANNEES = (True, 'showSerieYears')
ANIM_SERIE_ALPHA = (True, 'showSerieAlpha')
ANIM_SERIE_GENRES = (True, 'showSerieGenre')
ANIM_SERIE_VFS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&lang=vf&p=1',
    'showMovies')
ANIM_SERIE_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&lang=vostfr&p=1',
    'showMovies')

ANIM_MOVIE_NEWS = (
    URL_MAIN +
    '/videos?sk=c&filter=movie&unlicenced=1&p=1',
    'showMovies')
ANIM_MOVIE_POPULAR = (
    URL_MAIN +
    '/videos?sk=b&filter=movie&unlicenced=1&p=1',
    'showMovies')
ANIM_MOVIE_ANNEES = (True, 'showMovieYears')
ANIM_MOVIE_ALPHA = (True, 'showMovieAlpha')
ANIM_MOVIE_GENRES = (True, 'showMovieGenre')
ANIM_MOVIE_VFS = (
    URL_MAIN +
    'videos?sk=c&filter=movie&unlicenced=1&lang=vf&p=1',
    'showMovies')
ANIM_MOVIE_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&filter=movie&unlicenced=1&lang=vostfrp=1',
    'showMovies')

URL_SEARCH_ANIMS = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_INTERNALSEARCH_SERIES = (
    URL_MAIN +
    'videos?filter=serie&unlicenced=1&q=',
    'showMovies')
URL_INTERNALSEARCH_MOVIES = (
    URL_MAIN +
    'videos?filter=movie&unlicenced=1&q=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


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

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_POPULAR[1],
        'Animés (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ALPHA[1],
        'Animés (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_NEWS[1],
        'Animés Séries (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_POPULAR[1],
        'Animés Séries (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_ANNEES[1],
        'Animés Séries (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_ALPHA[1],
        'Animés Séries (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_GENRES[1],
        'Animés Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_VOSTFRS[1],
        'Animés Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_VFS[1],
        'Animés Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_NEWS[1],
        'Animés Films (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_POPULAR[1],
        'Animés Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_ANNEES[1],
        'Animés Films (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_ALPHA[1],
        'Animés Films (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_GENRES[1],
        'Animés Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_VOSTFRS[1],
        'Animés Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_VFS[1],
        'Animés Films (VF)',
        'vf.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieAlpha():
    showAllAlpha('movie')


def showSerieAlpha():
    showAllAlpha('serie')


def showAllAlpha(sfilter=''):
    gui = Gui()
    import string
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)

    url1 = 'videos?sk=a&alpha='
    url2 = '&filter=' + sfilter + '&unlicenced=1&p=1'

    output_parameter_handler = OutputParameterHandler()
    for alpha in listalpha:
        title = str(alpha).upper()
        url = URL_MAIN + url1 + alpha + url2
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    showAllYears('movie')


def showSerieYears():
    showAllYears('serie')


def showAllYears(sfilter=''):
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1983, 2023)):
        year = str(i)
        url1 = 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&aired-min=' + \
            year + '&aired-max=' + year + '&p=1'
        output_parameter_handler.addParameter('site_url', URL_MAIN + url1)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showMovieGenre():
    showAllGenre('movie')


def showSerieGenre():
    showAllGenre('serie')


def showAllGenre(sfilter=''):
    gui = Gui()

    listegenre = [
        'action',
        'aventure',
        'comedie',
        'drame',
        'fantastique',
        'horreur',
        'policier',
        'romance',
        'science-fiction',
        'sexy',
        'sport']

    url1 = URL_MAIN + 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&genres='
    url2 = '&p=1'
    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:
        title = igenre.capitalize()
        url = url1 + igenre + url2
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_INTERNALSEARCH_MOVIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_INTERNALSEARCH_SERIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):

    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = "col-sm-4 col-md-3\">.+?href=\"([^\"]+).+?url\\(\'([^']+).+?<span class=.anime-label.+?uppercase.>([^<]+).+?anime-header.>([^<]+)"

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

            url2 = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN[:-1] + entry[1]
            _type = entry[2]
            title = entry[3]
            display_title = title + ' [' + _type + ']'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addAnime(
                SITE_IDENTIFIER,
                'showEpisodesxMovies',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)
        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content, url)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)
        gui.setEndOfDirectory()


def __checkForNextPage(html_content, url):
    number_max = ''
    pattern = '"text-muted">page.+?sur\\s*(\\d+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0]

    pattern = '&p=(\\d+)'
    results = parser.parse(url, pattern)
    if results[0]:
        sNumberCurrent = results[1][0]
        iNumberCurrent = int(sNumberCurrent)
        iNumberNext = iNumberCurrent + 1
        number_next = str(iNumberNext)
        next_page = url.replace('&p=' + sNumberCurrent, '&p=' + number_next)
        if number_max:
            if int(number_max) >= iNumberNext:
                return next_page, number_next + '/' + number_max
        else:
            return next_page, number_next
    return False, False


def showEpisodesxMovies():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    pattern = '<h4>Intrigue<.h4>(.+?)</p>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                       cleanDesc(results[1][0]))

    if 'aucune vidéo disponible' in html_content:
        gui.addText(SITE_IDENTIFIER, 'Aucune video disponible')
        gui.setEndOfDirectory()
        return

    sHtmlContent1 = parser.abParse(
        html_content,
        '<h4 class="list-group-item-heading">',
        '<div id="footer')

    pattern = '<h4 class="list-group-item-heading">([^<]+)<.h4>|<a href="([^"]+).+?(?:group-item-text">|>)([^<]+)(?:<.p>|<.a>)'
    pattern = pattern
    results = parser.parse(sHtmlContent1, pattern)

    lang = ''
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                lang = entry[0]
                continue

            if lang:
                url = URL_MAIN[:-1] + entry[1]
                title = movie_title + ' ' + \
                    entry[2].replace('Épisode', 'Episode')

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('lang', lang)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="subsection">.+?label-default">\\D*(\\d+)([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            s_id = entry[0]
            host = entry[1].replace(' ', '').replace('-', '')
            host = re.sub('\\.\\w+', '', host)
            pdata = 'id=' + s_id
            movie_title = re.sub('\\[.+?\\]', '', movie_title)
            display_title = (
                '%s [COLOR coral]%s[/COLOR]') % (movie_title, host)
            url2 = URL_MAIN + 'remote/ajax-load_video'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('siteRefer', url)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    pdata = input_parameter_handler.getValue('pdata')
    siteRefer = input_parameter_handler.getValue('siteRefer')

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', siteRefer)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addParametersLine(pdata)
    html_content = request_handler.request()

    pattern = 'frame.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        hoster_url = results[1][0]
        if 'https:' not in hoster_url:
            hoster_url = 'https:' + hoster_url
        # VSlog(hoster_url)
        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def cleanDesc(desc):
    parser = Parser()
    pattern = '(<.+?>)'
    results = parser.parse(desc, pattern)
    if results[0]:
        for entry in results[1]:
            desc = desc.replace(entry, '')
    return desc
