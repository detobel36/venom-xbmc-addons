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

SITE_IDENTIFIER = 'french_stream_lol'
SITE_NAME = 'French-stream-lol'
SITE_DESC = 'Films & séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'xfsearch/qualit/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/film-sous-titre/', 'showMovies')
MOVIE_VF_FRENCH = (URL_MAIN + 'xfsearch/version-film/French/', 'showMovies')
MOVIE_VF_TRUEFRENCH = (
    URL_MAIN +
    'xfsearch/version-film/TrueFrench/',
    'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'xfsearch/qualit/HDLight/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + 'film/film-netflix/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'xfsearch/version-serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VFS = (URL_MAIN + 'serie/serie-en-vf-streaming/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/serie-en-vostfr-streaming/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

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

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
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

    output_parameter_handler.addParameter('site_url', MOVIE_VF_FRENCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_FRENCH[1],
        'Films (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_FRENCH[1],
        'Films (Netflix)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VF_TRUEFRENCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_TRUEFRENCH[1],
        'Films (True French)',
        'films.png',
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

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

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


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = key_search_series + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
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

    liste = []
    listegenre = [
        'action',
        'animation',
        'arts-martiaux',
        'aventure',
        'biopic',
        'comedie',
        'drame',
        'documentaire',
        'epouvante-horreur',
        'espionnage',
        'famille',
        'fantastique',
        'guerre',
        'historique',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + igenre + '/'])

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

    liste = [['Action', 'serie-action'], ['Animation', 'animation-serie'], ['Aventure', 'aventure-serie'],
             ['Biopic', 'biopic-serie'], ['Comédie', 'serie-comedie'], ['Drame', 'drame-serie'],
             ['Famille', 'familles-serie'], ['Fantastique', 'serie-fantastique'], ['Historique', 'serie-historique'],
             ['Horreur', 'serie-horreur'], ['Judiciaire', 'serie-judiciare'], ['Médical', 'serie-medical'],
             ['Policier', 'serie-policier'], ['Romance', 'serie-romance'], ['Science-fiction', 'serie-science-fiction'],
             ['Thriller', 'serie-thriller'], ['Western', 'serie-western'], ['K-Drama', 'serie/k-drama']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
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

    bSearchMovie = False
    bSearchSerie = False
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)

        # url = URL_SEARCH[0]  # sert a rien
        search = search.replace(' ', '+').replace('%20', '+')

        if key_search_movies in search:
            search = search.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in search:
            search = search.replace(key_search_series, '')
            bSearchSerie = True

        url = URL_MAIN + 'index.php?story=' + search + '&do=search&subaction=search'
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        # la méthode suivante fonctionne mais pas à 100%
        # pdata = 'do=search&subaction=search&search_start=1&full_search=0&result_from=1&story=' + search
        # request = RequestHandler(URL_SEARCH[0])
        # request.setRequestType(1)
        # request.addHeaderEntry('Referer', URL_MAIN)
        # request.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        # request.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # request.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        # request.addParametersLine(pdata)
        # html_content = request.request()

    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    pattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]*)'
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

            url2 = entry[0]
            thumb = entry[1]
            if 'http' not in thumb:
                thumb = URL_MAIN[:-1] + thumb
            title = entry[2]

            if bSearchMovie:  # il n'y a jamais '/serie' dans url2
                if '- Saison' in entry[2]:
                    continue
            if bSearchSerie:
                if '- Saison' not in entry[2]:
                    continue

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            display_title = title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url2 or 'serie/' in url or '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif bSearchSerie is True or '- Saison' in entry[2]:
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
                    'showMovieLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '(\\d+)</a>\\s*</span><span class="pnext"><a href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


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

    pattern = 'id="s-desc">([^<]+)'
    results = parser.parse(html_content, pattern)
    desc = 'french stream lol'
    if results[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                       cleanDesc(results[1][0]))

    pattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\\d+)"\\s*href="([^"]+).+?data-rel="([^"]+).+?</i>([^<]+)'
    results = parser.parse(html_content, pattern)

    lang = ''
    bFind = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                lang = entry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and entry[1]:
                sFirst_Url = entry[1]
                sRel_Episode = entry[2]
                if sRel_Episode == "ABCDE":
                    sEpisode = 'Episode 2'
                else:
                    sEpisode = entry[3]

                title = movie_title + ' ' + sEpisode
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
                    'showSerieLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    lang = input_parameter_handler.getValue('lang')
    sFirst_Url = input_parameter_handler.getValue('sFirst_Url')
    movie_title = input_parameter_handler.getValue('movie_title')
    sRel_Episode = input_parameter_handler.getValue('sRel_Episode')
    if not sRel_Episode:
        numEpisode = input_parameter_handler.getValue(
            'sEpisode')  # Gestion Up_Next
        if numEpisode:
            numEpisode = int(numEpisode)
            if 'VO' in lang:
                numEpisode += 32
            if numEpisode == 2:
                sRel_Episode = 'ABCDE'
            else:
                sRel_Episode = 'episode%d' % numEpisode

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div id="' + sRel_Episode + \
        '" class="fullsfeature".*?<li><a (id="singh.*?<div style="height)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        # dans cas ou il n'y a qu'un seul lien il n'y a pas de reference  dans <div id="episodexx" class="fullsfeature">
        # le pattern devient alors normalement hs
        if sFirst_Url:
            hoster_url = sFirst_Url
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
                hoster_url = entry

                if 'http' not in hoster_url:  # liens naze du site url
                    continue

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showMovieLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    pattern = '<li>\\s*<a.*?href="([^"]+).+?<\\/i>([^<]+)<'
    results = parser.parse(html_content, pattern)

    sHosterName = ''

    if results[0]:
        for entry in results[1]:

            if 'FRENCH' not in entry[1] and 'VOSTFR' not in entry[1]:
                sHosterName = entry[1].strip()
                continue
            lang = entry[1].strip()
            display_title = '%s [%s] (%s)' % (movie_title, lang, sHosterName)

            hoster_url = entry[0]
            if 'http' not in hoster_url:  # liens nazes du site url
                continue

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(display_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


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
