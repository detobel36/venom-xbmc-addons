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
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'hds_fm'
SITE_NAME = 'Hds-fm'
SITE_DESC = 'Films et Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/VOSTFR/', 'showMovies')
MOVIE_VF = (URL_MAIN + 'film/French/', 'showMovies')

MOVIE_HDLIGHT = (URL_MAIN + 'qualit/HDLight/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'serie-tv-streaming/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

SERIE_VFS = (URL_MAIN + 'serie/VF/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/VOSTFR/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on n'utilise pas le globale
MY_SEARCH_MOVIES = (True, 'myShowSearchMovie')
MY_SEARCH_SERIES = (True, 'myShowSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
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

    output_parameter_handler.addParameter('site_url', MOVIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF[1],
        'Films (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (HD Light)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
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

    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF[1],
        'Films (VF)',
        'vf.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def myShowSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = key_search_series + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def myShowSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = key_search_movies + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    # genre enlevés tous les films hs : Walt-Disney, Super_héros
    # arts-martiaux 4 films marche sur 150

    liste = []
    listegenre = [
        'action',
        'animation',
        'arts-martiaux',
        'aventure',
        'biopic',
        'comédie',
        'comédie-dramatique',
        'comédie-musicale',
        'drame',
        'documentaire',
        'epouvante_horreur',
        'espionnage',
        'famille',
        'fantastique',
        'musical',
        'guerre',
        'historique',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    # https://www1.hds.fm/film-genre/action
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'film-genre/' + igenre])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieGenres():
    gui = Gui()
    liste = []
    listegenre = [
        'Action',
        'Animation',
        'Arts-martiaux',
        'Aventure',
        'Biopic',
        'Comédie',
        'Drame',
        'Epouvante_horreur',
        'Famille',
        'Historique',
        'Judiciaire',
        'Médical',
        'Policier',
        'Romance',
        'Science-fiction',
        'Sport-event',
        'Thriller',
        'Western']

    # https://www1.hds.fm/serie-genre/Drame/
    for igenre in listegenre:
        urlgenre = igenre
        if igenre == 'judiciaire':
            urlgenre = 'judiciare'
        liste.append([igenre.capitalize(), URL_MAIN +
                     'serie-genre/' + urlgenre + '/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
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

    bSearchMovie = False
    bSearchSerie = False
    if search:
        search = search.replace('%20', ' ')
        if key_search_movies in search:
            search = search.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in search:
            search = search.replace(key_search_series, '')
            bSearchSerie = True

        util = cUtil()
        search_text = util.CleanName(search)
        sSearch2 = search.replace('-', '').strip().lower()
        url = URL_SEARCH[0] + sSearch2
        request = RequestHandler(url)
        html_content = request.request()

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # ref thumb title
    pattern = 'class="TPostMv">.+?href="([^"]*).+?src="([^"]*).+?class="Qlty".+?class="Qlty.+?>([^<]*).+?center">([^<]*)'
    results = parser.parse(html_content, pattern)

    # itemss = 0

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

            url2 = entry[0]
            thumb = entry[1]
            lang = entry[2]
            title = entry[3]

            if bSearchMovie:
                if ' saison ' in title.lower():
                    continue
            if bSearchSerie:
                if ' saison ' not in title.lower():
                    continue

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue  # Filtre de recherche

            display_title = ('%s (%s)') % (
                title.replace('- Saison', ' Saison'), lang)
            if search and not bSearchMovie and not bSearchSerie:
                if '/serie' in url or '- saison ' in title.lower():
                    display_title = display_title + ' [Série]'
                else:
                    display_title = display_title + ' [Film]'

            if 'http' not in url2:
                url2 = URL_MAIN[:-1] + url2

            if 'http' not in thumb:
                thumb = URL_MAIN[:-1] + thumb

            # pour le debugage source avec bcpdechance d'etre hs
            # films didfficile a obtenir apres id= 18729
            # if not ('/serie' in url or ' saison ' in title.lower()):
                # idmovie = get_id_int_Movie(url2)
                # if idmovie  <= 18729:
                # display_title = display_title + ' *'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url or '- saison ' in title.lower():
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        bNextPage, next_page, sNumPage = __checkForNextPage(html_content)
        if bNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    number_next = ''
    number_max = ''
    sNumPage = ''

    if '<a class="next"' not in html_content:
        return False, 'none', 'none'

    if 'class="end"' in html_content:
        pattern = 'class="end".+?">(\\d+)'
    else:
        pattern = '(\\d+)<.a>\\s*<a\\sclass="next"'

    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0]

    pattern = 'class="next.+?href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0]  # minimum requis
        if 'htpp' not in next_page:
            next_page = URL_MAIN[:-1] + next_page
            if '/31/32/' in next_page:  # bug page 31
                next_page = re.sub('/31', '', next_page)
        try:
            number_next = re.search('/(\\d+)/', next_page).group(1)
        except BaseException:
            pass

        if number_next:
            sNumPage = number_next
            if number_max:
                sNumPage = sNumPage + '/' + number_max

        if next_page:
            return True, next_page, sNumPage

    return False, 'none', 'none'


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if 'saison' not in movie_title.lower():
        pattern = 'saison-(\\d+)'
        results = parser.parse(url, pattern)
        if results[0]:
            movie_title = movie_title + ' Saison ' + results[1][0]

    pattern = '<div class="Description">.*?>([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'Hds Film'
    if results[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :',
                                                       cleanDesc(results[1][0]))

    pattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\\d+)"\\s*href="([^"]+).+?title="([^"]+).+?data-rel="([^"]+)'
    results = parser.parse(html_content, pattern)

    bFind = ''
    validEntry = ''
    lang = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                lang = entry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and entry[1]:
                validEntry = True
                sFirst_Url = entry[1]
                sEpisode = entry[2]
                sRel_Episode = entry[3]

                title = movie_title.replace(
                    '- Saison', ' Saison') + ' ' + sEpisode
                display_title = title + ' (' + lang + ')'

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('lang', lang)
                output_parameter_handler.addParameter(
                    'sRel_Episode', sRel_Episode)
                output_parameter_handler.addParameter('sFirst_Url', sFirst_Url)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    if not validEntry:
        gui.addText(SITE_IDENTIFIER, '# Aucune vidéo trouvée #')

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sRel_Episode = input_parameter_handler.getValue('sRel_Episode')
    sFirst_Url = input_parameter_handler.getValue('sFirst_Url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div id="' + sRel_Episode + \
        '" class="fullsfeature".*?<a (id="singh.*?<div style="height)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        # cas ou il n'y a qu'un seul lien  pas de référence  dans <div id="episodexx" class="fullsfeature">
        # le pattern est normalement hs
        if sFirst_Url:
            url2 = sFirst_Url
            # host = '[COLOR coral]' + getHostName(url2) + '[/COLOR]'

            # display_title = movie_title + ' ' + host
            hoster_url = url2
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    if results[0]:
        html = results[1][0]
        pattern = 'href="([^"]+).*?aria-hidden'
        aResultUrl = parser.parse(html, pattern)
        if aResultUrl[0] is True:
            for entry in aResultUrl[1]:
                url2 = entry
                # host = getHostName(url2)
                if len(results[1]) == 1 and 'openload' in url2:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue

                if isBlackHost(url2):
                    continue

                # if 'hqq.tv' in url2:
                    # continue

                # if 'www' in host.lower():
                    # host = getHostName(url2)

                # host = '[COLOR coral]' + host + '[/COLOR]'
                # display_title = movie_title + ' ' + host

                hoster_url = url2
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a style=".+?cid="([^"]+).+?fa-play.+?i>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url2 = entry[0]
            host = entry[1].strip().capitalize()
            if len(results[1]) == 1:
                if 'openload' in host.lower():
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue
                if 'oload' in host.lower():
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] oload : site non sécurisé [/COLOR]')
                    continue

            if isBlackHost(url2):
                continue

            # if 'hqq.tv' in url2:
                # continue

            hoster_url = url2
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


# teste id movie
def get_id_int_Movie(url):

    try:
        number = re.search('https.+?\\/(\\d+)', url).group(1)
        return int(number)
    except BaseException:
        return 20000
        pass
    return 20000


def getHostName(url):

    try:
        if 'opsktp' in url:
            host = re.search('http.+?opsktp.+?\\/([^\\/]+)', url).group(1)

        elif 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        host = url

    return host.capitalize()


def cleanDesc(desc):
    parser = Parser()
    pattern = '(Résumé.+?streaming Complet)'
    results = parser.parse(desc, pattern)

    if results[0]:
        desc = desc.replace(results[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        desc = desc.replace(s, '')

    return desc


def isBlackHost(url):
    black_host = [
        'youflix',
        'verystream',
        'javascript',
        '4k-pl',
        'ffsplayer',
        'french-stream.ga',
        'oload.stream',
        'french-player.ga',
        'streamango.com',
        'hqq.tv']

    urllower = url.lower()
    for host in black_host:
        if host.lower() in urllower:
            return True
    return False
