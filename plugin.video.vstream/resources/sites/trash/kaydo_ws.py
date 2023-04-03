# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Il faut faire le code pour le nouvel hoster.
from resources.lib.util import Noredirection
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import time
import base64
import re
return False


# copie du site http://www.kaydo.ws/
# copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hdss.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'mieux-notes/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showMovieGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tv-series-z/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'

UA = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'


def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except BaseException:
        return chain


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

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films et Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par lettre)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par lettre)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = []
    liste.append(['#', URL_MAIN + 'letter/0-9/'])
    liste.append(['A', URL_MAIN + 'letter/a/'])
    liste.append(['B', URL_MAIN + 'letter/b/'])
    liste.append(['C', URL_MAIN + 'letter/c/'])
    liste.append(['D', URL_MAIN + 'letter/d/'])
    liste.append(['E', URL_MAIN + 'letter/e/'])
    liste.append(['F', URL_MAIN + 'letter/f/'])
    liste.append(['G', URL_MAIN + 'letter/g/'])
    liste.append(['H', URL_MAIN + 'letter/h/'])
    liste.append(['I', URL_MAIN + 'letter/i/'])
    liste.append(['J', URL_MAIN + 'letter/j/'])
    liste.append(['K', URL_MAIN + 'letter/k/'])
    liste.append(['L', URL_MAIN + 'letter/l/'])
    liste.append(['M', URL_MAIN + 'letter/m/'])
    liste.append(['N', URL_MAIN + 'letter/n/'])
    liste.append(['O', URL_MAIN + 'letter/o/'])
    liste.append(['P', URL_MAIN + 'letter/p/'])
    liste.append(['Q', URL_MAIN + 'letter/q/'])
    liste.append(['R', URL_MAIN + 'letter/r/'])
    liste.append(['S', URL_MAIN + 'letter/s/'])
    liste.append(['T', URL_MAIN + 'letter/t/'])
    liste.append(['U', URL_MAIN + 'letter/u/'])
    liste.append(['V', URL_MAIN + 'letter/v/'])
    liste.append(['W', URL_MAIN + 'letter/w/'])
    liste.append(['X', URL_MAIN + 'letter/x/'])
    liste.append(['Y', URL_MAIN + 'letter/y/'])
    liste.append(['Z', URL_MAIN + 'letter/z/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
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


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
    return


def showMovieGenres():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    site_url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(site_url)
    html_content = request_handler.request()

    parser = Parser()
    html_content = parser.abParse(
        html_content,
        '"AAIco-movie_creation">Genres</label>',
        '</div>')
    pattern = 'data-val="([^"]+)" data-value="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sGenre = entry[0]
            if sGenre in ('random', 'Uncategorized'):
                continue
            sFilter = entry[1]
            url = site_url + '?s=trfilter&trfilter=1&geners%5B%5D=' + sFilter

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                sGenre,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    if URL_MAIN + 'letter/' in url:
        pattern = '<td class="MvTbImg">.+?href="([^"]+).+?src="([^"]*).+?class="MvTbTtl.+?<strong>([^<]*).+?<td>([^<]*).+?Qlty">([^<]+).+?<td>([^<]*)'
    else:
        pattern = 'class="TPost C".+?href="([^"]+).+?src="([^"]*).+?Title">([^<]+).+?(?:|Year">([^<]*).+?)(?:|Qlty">([^<]*).+?)Description"><p>([^<]+)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    # réécriture pour prendre les séries dans le menu des genres
    # html_content = html_content.replace('<span class="Qlty">TV</span></div><h3', '</div><h3')

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

            site_url = entry[0]
            thumb = re.sub('/w\\d+', '/w342', entry[1])
            if thumb.startswith('//'):
                thumb = 'https:' + thumb
            title = entry[2]
            year = entry[3]
            qual = entry[4]
            desc = entry[5]
            if year.lower() == 'unknown':
                year = ''
            if qual.lower() == 'unknown':
                qual = ''

            display_title = ('%s [%s] (%s)') % (title, qual, year)

            output_parameter_handler.addParameter('site_url', site_url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)

            if '/serie/' in site_url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'ShowSaisonEpisodes',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if (next_page):
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
    pattern = '>([^<]+?)</a><a class="next page-numbers" href="([^"]+?)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def ShowSaisonEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="Title AA-Season.+?>Season <span>([^<]+)</span>|class="MvTbImg">.+?img src.+?["|;]([^\"]+?)["|;].+?href="([^"]+)">([^<]+)<'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]Saison: ' +
                    entry[0] +
                    '[/COLOR]')
            else:
                thumb = re.sub('/w\\d+', '/w342', entry[1], 1)
                if thumb.startswith('//'):
                    thumb = 'https:' + thumb
                url2 = entry[2]
                title = entry[3]

                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    # UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    gui = Gui()
    parser = Parser()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Recuperer variable pour url de base
    pattern = 'trembed=(\\d+).+?trid=(\\d+).+?trtype=(\\d+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        list_site_film = []
        for entry in results[1]:

            site = URL_MAIN + "?trembed=" + \
                entry[0] + "&trid=" + entry[1] + "&trtype=" + entry[2]
            if entry[2] == '1':
                if site not in list_site_film:
                    list_site_film.append(site)
                else:
                    continue  # inutile de faire des requetes identiques pour les films

            request_handler = RequestHandler(site)
            html_content = request_handler.request()

            slug = re.search(
                '"Video".+?src=".+?v=(.+?)"',
                html_content).group(1)

            hoster_url = "https://geoip.redirect-ads.com/?v=" + slug

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def decode(t):
    a = len(t) - 1
    trde = ''
    while a >= 0:
        trde = trde + t[a]
        a -= 1

    return trde
