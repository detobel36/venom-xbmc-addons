# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# disable 03/08/2020
from resources.lib.util import cUtil, Unquote
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Progress  # , VSlog
import re
import base64
return False


SITE_IDENTIFIER = 'filmstreaming'
SITE_NAME = 'Film Streaming'
SITE_DESC = 'Films en streaming'
URL_MAIN = 'https://www.filmstreamingvf.watch/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + '?v_sortby=views&v_orderby=desc', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (URL_MAIN, 'AlphaSearch')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')


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
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Ordre alphabétique)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        search = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(search)
        gui.setEndOfDirectory()
        return


def showSearchOld():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        showSearchMovies(search_text)
        gui.setEndOfDirectory()
        return


def showSearchMovies(search=''):
    gui = Gui()

    search = Unquote(search)
    url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
    pdata = 'nonce=3293a1b68c&action=tr_livearch&trsearch=' + \
        search  # la valeur nonce change

    request = RequestHandler(url2)
    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addParameters('Referer', URL_MAIN)
    request.addParametersLine(pdata)

    html_content = request.request()
    pattern = '<div class="TPost B">.+?<a href="([^"]+)">.+?<img src="([^"]+)".+?<div class="Title">([^<]+)</div>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            thumb = re.sub('/w\\d+', '/w342', entry[1], 1)
            if thumb.startswith('/'):
                thumb = 'https:' + thumb
            title = entry[2]

            # filtre search
            if search and total > 3:
                if cUtil().CheckOccurence(search, title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
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


def showGenres():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(MOVIE_NEWS[0])
    html_content = request_handler.request()

    html_content = parser.abParse(
        html_content,
        'class=Title>Film Streaming Par Genres</div>',
        '</div></aside>')

    pattern = '<li class="cat-item cat-item-.+?"><a href=([^>]+)>([^<]+)</a>([^<]+)</li>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1] + entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def AlphaSearch():
    gui = Gui()

    for i in range(0, 27):
        if (i == 0):
            sLetter = '0-9'
        else:
            sLetter = chr(64 + i)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'letters/' + sLetter + '/page/1/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showList',
            'Lettre [COLOR coral]' +
            sLetter +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class=Num>.+?href=(.+?) class=MvTbImg.+?src=([^ ]+).+?<strong>([^<]+)</strong> </a></td><td>([^<]*)<.+?class=Qlty>([^<]+)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            thumb = re.sub('/w\\d+', '/w342', entry[1], 1)
            if thumb.startswith('/'):
                thumb = 'http:' + thumb
            title = entry[2]
            year = entry[3]
            qual = entry[4]

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        if results:
            pattern = 'page/(\\d+)/'
            results = parser.parse(url, pattern)
            if results[0]:
                number = int(results[1][0]) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', re.sub(
                    'page/(\\d+)/', 'page/' + str(number) + '/', url))
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showList',
                    '[COLOR teal]Page ' +
                    str(number) +
                    ' >>>[/COLOR]',
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
    html_content = parser.abParse(
        html_content,
        'MovieList Rows',
        '</body></html>')
    pattern = 'class=Image>.+?src=([^ ]+) .+?class=Qlty>([^<]+).+?href=([^>]+)><div class=Title>([^<]+).+?Description><p>(.+?)</p>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = re.sub('/w\\d+', '/w342', entry[0], 1)
            if thumb.startswith('/'):
                thumb = 'https:' + thumb

            qual = entry[1]
            url = entry[2]
            title = entry[3]
            desc = entry[4]

            display_title = ('%s [%s]') % (title, qual)

            # filtre search
            if search and total > 5:
                if cUtil().CheckOccurence(search, title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                number +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = 'href="*([^">]+)"*>Next'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # qual, lang
    pattern = 'class=AAIco-language>([^<]+)</p><p class=AAIco-dns>.+?<p class=AAIco-equalizer>([^<]+)<'
    aResult1 = re.findall(pattern, html_content, re.DOTALL)
    # VSlog(str(aResult1)) #Commenter ou supprimer cette ligne une fois fini

    sPattern2 = '<div id=VideoOption\\d+ class="*Vid.+?>([^<]+)</div>'
    aResult2 = re.findall(sPattern2, html_content, re.DOTALL)
    # VSlog(str(aResult2)) #Commenter ou supprimer cette ligne une fois fini

    results = zip(aResult2, [x[1] + '] (' + x[0] for x in aResult1])
    # VSlog(str(results)) #Commenter ou supprimer cette ligne une fois fini

    if (results):
        for entry in results:
            html_content = base64.b64decode(entry[0])
            # VSlog(html_content)

            hoster_url = ''
            # Pour Python 3, besoin de repasser en str.
            try:
                url = re.search('src="([^"]+)"', html_content)
            except TypeError:
                url = re.search('src="([^"]+)"', html_content.decode())
            hoster_url = url.group(1)

            request_handler = RequestHandler(hoster_url)
            html_content = request_handler.request()
            url = re.search('<iframe id="iframe" src="([^"]+)"', html_content)
            if url:
                hoster_url = url.group(1)

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title + ' [' + entry[1] + ')')
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
