# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons 9bed026547
import json
import re
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/66.0'

SITE_IDENTIFIER = 'streamingvoirfilms'
SITE_NAME = 'Streamingvoirfilms'
SITE_DESC = ' StreamingVoirfilms Vous propose un large choix des nouveaux et vieux films.'

URL_MAIN = 'https://streamingvoirfilms.com/'
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (
    URL_MAIN +
    'wp-json/dooplay/glossary/?term=$$&nonce=9bed026547&type=movies',
    'showAlpha')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_LIST = (
    URL_MAIN +
    'wp-json/dooplay/glossary/?term=$$&nonce=9bed026547&type=tvshows',
    'showAlpha')
SERIE_SEASONS = (URL_MAIN + 'saisons/', 'showMovies')

FUNCTION_SEARCH = 'showList'
URL_SEARCH = (URL_MAIN + 'wp-json/dooplay/search/?keyword=', 'showList')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showList')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showList')


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Films (Derniers ajouts)',
        'news.png',
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
        'Films (Liste)',
        'listes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Séries (Episode derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SEASONS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SEASONS[1],
        'Séries (Saison derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries (Toutes les séries)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showList(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/'])
    liste.append(['Action & Adventure', URL_MAIN + 'genre/action-adventure/'])
    liste.append(['Animation', URL_MAIN + 'genre/animation/'])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/'])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/'])
    liste.append(['Crime', URL_MAIN + 'genre/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'genre/drame/'])
    liste.append(['Familial', URL_MAIN + 'genre/familial/'])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'genre/histoire/'])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/'])
    liste.append(['Musique', URL_MAIN + 'genre/musique/'])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/'])
    liste.append(['Romance', URL_MAIN + 'genre/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'genre/science-fiction/'])
    liste.append(['Science Fiction & Fantastique',
                  URL_MAIN + 'genre/science-fiction-fantastique/'])
    liste.append(['Téléfilm', URL_MAIN + 'genre/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/'])
    liste.append(['Western', URL_MAIN + 'genre/western/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    # liste.append( ['#', url.replace('$$','09')] ) fonctionne pas sur le site
    liste.append(['A', url.replace('$$', 'a')])
    liste.append(['B', url.replace('$$', 'b')])
    liste.append(['C', url.replace('$$', 'c')])
    liste.append(['D', url.replace('$$', 'd')])
    liste.append(['E', url.replace('$$', 'e')])
    liste.append(['F', url.replace('$$', 'f')])
    liste.append(['G', url.replace('$$', 'g')])
    liste.append(['H', url.replace('$$', 'h')])
    liste.append(['I', url.replace('$$', 'i')])
    liste.append(['J', url.replace('$$', 'j')])
    liste.append(['K', url.replace('$$', 'k')])
    liste.append(['L', url.replace('$$', 'l')])
    liste.append(['M', url.replace('$$', 'm')])
    liste.append(['N', url.replace('$$', 'n')])
    liste.append(['O', url.replace('$$', 'o')])
    liste.append(['P', url.replace('$$', 'p')])
    liste.append(['Q', url.replace('$$', 'q')])
    liste.append(['R', url.replace('$$', 'r')])
    liste.append(['S', url.replace('$$', 's')])
    liste.append(['T', url.replace('$$', 't')])
    liste.append(['U', url.replace('$$', 'u')])
    liste.append(['V', url.replace('$$', 'v')])
    liste.append(['W', url.replace('$$', 'w')])
    liste.append(['X', url.replace('$$', 'x')])
    liste.append(['Y', url.replace('$$', 'y')])
    liste.append(['Z', url.replace('$$', 'z')])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showList',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search.replace(' ', '+') + '&nonce=9bed026547'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    page = json.loads(html_content)

    if page:
        for x in page:
            url = page[x]["url"]
            title = page[x]["title"].encode('utf-8')

            thumb = page[x]["img"].replace('90x135', '185x278')  # pas mieux

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if 'series' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisonEpisodes',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if '/films' in url or '/series' in url:
        pattern = 'data-src="([^"]+)" alt="([^"]+)">.+?<a href="([^"]+)".+?<div class="texto">([^<]+)<\\/div>'
    else:
        pattern = 'data-src="([^"]+)" alt="([^"]+)">.+?<a href="([^"]+)"'

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

            title = entry[1]
            url2 = entry[2]
            thumb = entry[0]
            desc = ''

            if '/films' in url or '/series' in url:
                desc = entry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/series' in url2 or '/saisons' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisonEpisodes',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif '/episodes' in url2:
                gui.addTV(SITE_IDENTIFIER, 'showLinks', title, '',
                          thumb, desc, output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class=\'arrow_pag\' href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSaisonEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = "<span class='title'>([^<]+)<i>|<div class='numerando'>(\\d+) - (\\d+)</div>.+?class='episodiotitle'><a href='([^']+)'"
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

            if (entry[0]):
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')

            else:
                url = entry[3]
                title = 'Saison ' + \
                    entry[1] + ' Episode' + entry[2] + ' ' + movie_title

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request = RequestHandler(url)
    html_content = request.request()

    sPattern2 = "data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)'>.+?<span class='title'>([^<]+)<\\/span><span class='server'>([^<]+)<\\/span>.+?<img src='([^']+)'>"
    results = parser.parse(html_content, sPattern2)

    if results[0]:
        for entry in results[1]:

            host = entry[4].capitalize()
            lang = entry[5].split('/')[-1].replace('.png', '').capitalize()
            qual = entry[3]

            postdata = 'action=doo_player_ajax&post=' + \
                entry[1] + '&nume=' + entry[2] + '&type=' + entry[0]

            display_title = ('%s (%s %s %s)') % (
                movie_title, lang, qual, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('postdata', postdata)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    postdata = input_parameter_handler.getValue('postdata')

    request = RequestHandler(URL_MAIN + '/wp-admin/admin-ajax.php')
    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    # request.addHeaderEntry('Accept', '*/*')
    # request.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
    # request.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    # request.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    request.addHeaderEntry('Referer', url)
    request.addParametersLine(postdata)
    html_content = request.request()

    pattern = "<iframe.+?src='([^']+)'"
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
