# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # NPAI 04/02/2022

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = "https://www.film-streamingk.biz/"

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
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

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'views.png',
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


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # Inutilisable
    # output_parameter_handler.addParameter('site_url', SERIE_EPISODES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_EPISODES[1], 'Séries (Episodes)', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_AMAZON[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_CANAL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_DISNEY[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_APPLE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_YOUTUBE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (Youtube Originals)',
        'series.png',
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
                        'Crime', 'crime'], [
                            'Drame', 'drame'], [
                                'Familial', 'familial'], [
                                    'Fantastique', 'fantastique'], [
                                        'Guerre', 'guerre'], [
                                            'Horreur', 'horreur'], [
                                                'Histoire', 'histoire'], [
                                                    'Romance', 'romance'], [
                                                        'Thriller', 'thriller'], [
                                                            'Science-Fiction', 'science-fiction'], [
                                                                'Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genre/' + url + '/')
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
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        url = search
        util = cUtil()
        search = util.CleanName(search.replace(URL_SEARCH[0], ''))
        pattern = 'class="image">.*?<a href="([^"]+)">\\s*<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)'
    elif 'episodes' in url:
        pattern = 'class="poster">.*?<img src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)'
    else:
        pattern = 'class="poster"> *<img src="([^"]+)".+?<a href="([^"]+)" *title="([^"]+)".+?class="texto">([^<]*)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # for the first thumb in the movies "featured movies"
    if 'class="archive_post">' in html_content:
        html_content = parser.abParse(
            html_content, 'class="archive_post">', '')
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Si recherche et trop de resultat, on filtre
            if search and total > 5:
                if not util.CheckOccurence(search, entry[2]):
                    continue

            if search:
                url = entry[0]
                thumb = entry[1]
                title = entry[2]
                desc = entry[3]
            elif 'episodes' in url:
                thumb = entry[0]
                title = entry[1]
                url = entry[2]
                desc = ''
            else:
                thumb = entry[0]
                url = entry[1]
                title = entry[2].replace('streaming', ' ')
                desc = entry[3]

            # si utile il faut retirer output_parameter_handler.addParameter(desc)
            # if desc:  # désactivé le 17/06/2020,
                # try:
                # desc = cUtil().unescape(desc.decode('utf8'))
                # except AttributeError:
                # desc = cUtil().unescape(desc)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if 'series' in url:
                gui.addTV(SITE_IDENTIFIER, 'showSxE', title, '',
                          thumb, desc, output_parameter_handler)
            elif 'episodes' in url:
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
    pattern = 'Page \\d+ de ([^<]+).+?arrow_pag\' *href="([^"]+)"><i id=\'nextpagination'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<span class="title">(.+?)<|class="numerando">([^"]+)</div><div class="episodiotitle"><a href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    entry[0] +
                    '[/COLOR]')

            else:
                url = entry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    'saison \\g<1> Episode \\g<2>',
                    entry[1])
                title = movie_title + ' ' + SxE

                # "MARQUER LU" à besoin de la saison et de l'épisode # movie_title + ' ' + re.sub('saison \d+ ', '', SxE)
                sDisplaytitle = title

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplaytitle,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()

    if 'episodes' in url:
        pattern = 'dooplay_player_option.+?data-post="(\\d+)".+?data-nume="([^"]+).+?title">([^<]+)'
    else:
        pattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='([^']+).+?title'>([^<]+)"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if ('trailer' in entry[1]):
                continue
            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            if 'episodes' in url:
                dtype = 'tv'
            else:
                dtype = 'movie'
            dpost = entry[0]
            dnum = entry[1]
            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype

            # trie des hosters
            hoster = entry[2].capitalize()
            hoster = HosterGui().checkHoster(hoster)
            if not hoster:
                continue

            sDisplaytitle = '%s [COLOR coral]%s[/COLOR]' % (
                movie_title, hoster)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('pdata', pdata)
            output_parameter_handler.addParameter('host', hoster)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplaytitle,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParametersLine(pdata)

    html_content = request.request()
    pattern = "<iframe.+?src='(.+?)'"
    results = re.findall(pattern, html_content)

    if results:
        for entry in results:
            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
