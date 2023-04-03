# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import requests

from resources.lib.comaddon import Progress, dialog, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'tirexo'
SITE_NAME = '[COLOR violet]Tirexo[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'

# Teste pour le moment avec une url fixe.
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&&catlist[]=2&story=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&catlist[]=15&story=',
    'showMovies')
URL_SEARCH_ANIMS = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&catlist[]=32&story=',
    'showMovies')
URL_SEARCH_MISC = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&catlist[]=75&catlist[]=76&catlist[]=77&catlist[]=79&catlist[]=101&story=',
    'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_COLLECTION = (URL_MAIN + 'collections/', 'showMovies')
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies')
MOVIE_SD = (URL_MAIN + 'films-bluray-hd/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films-mkv/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films-bluray-hd-1080/', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-dvdrip-bdrip/', 'showMovies')
MOVIE_SDLIGHT = (URL_MAIN + 'hdlight-720/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'hdlight-1080/', 'showMovies')
MOVIE_4KL = (URL_MAIN + 'film-ultra-hdlight-x265/', 'showMovies')
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-x265/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films-gratuit/', 'showMovies')
MOVIE_ANNEES = (URL_MAIN + 'films-gratuit/', 'showYears')

MOVIE_2020 = (URL_MAIN + 'films-2020-2030/', 'showMovies')
MOVIE_2010 = (URL_MAIN + 'films-2010-2019/', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009/', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999/', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989/', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979/', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969/', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959/', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1900-1950/', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenres')
SERIE_GENRES = ('telecharger-series/', 'showGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series-vf-en-hd/', 'showMovies')
SERIE_VF_1080 = (URL_MAIN + 'series-vf-1080p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series-vostfr-hd/', 'showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'series-vostfr-1080p/', 'showMovies')
SERIE_VO = (URL_MAIN + 'series-vo/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'telecharger-series/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'emissions-tv-documentaires/documentaire', 'showMovies')
SPORT_REPLAY = (URL_MAIN + 'emissions-tv-documentaires/sport', 'showMovies')
SPORT_SPORTS = SPORT_REPLAY
TV_NEWS = (URL_MAIN + 'emissions-tv-documentaires/emissions-tv/', 'showMovies')
SPECT_NEWS = (
    URL_MAIN +
    '?do=cat&category=emissions-tv-documentaires/spectacle&epoque=2022',
    'showMovies')
CONCERT_NEWS = (
    URL_MAIN +
    '?do=cat&category=musiques-mp3-gratuite/concerts&epoque=2022',
    'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

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

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMangas',
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuAutres',
        'Autres',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_COLLECTION[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_COLLECTION[1],
        'Les collections',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Exclus (Films populaires)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD[1],
        'Films (720p)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (1080p)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films (BDRIP)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films (4K)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MKV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MKV[1],
        'Films (dvdrip mkv)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SDLIGHT[1],
        'Films (720p - Light)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (1080p - Light)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_4KL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4KL[1],
        'Films (4K - light)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films (3D)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Derniers ajouts',
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
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 720p (VF)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 1080p (VF)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_720[1],
        'Séries 720p (VOSTFR)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_1080[1],
        'Séries 1080p (VOSTFR)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VO[1],
        'Séries (VO)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMangas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher Animes',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animes (VF)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_720[1],
        'Animes 720p (VF)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_1080[1],
        'Animes 1080p (VF)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animes (VOSTFR)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_720[1],
        'Animes 720p (VOSTFR)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_1080[1],
        'Animes 1080p (VOSTFR)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', FILM_ANIM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        FILM_ANIM[1],
        'Films d\'animes ',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_2020[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_2020[1],
        'Films (2020)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_2010[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_2010[1],
        'Films (2010)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_2000[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_2000[1],
        'Films (2000)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1990[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1990[1],
        'Films (1990)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1980[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1980[1],
        'Films (1980)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1970[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1970[1],
        'Films (1970)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1960[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1960[1],
        'Films (1960)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1950[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1950[1],
        'Films (1950)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1900[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1900[1],
        'Films (1900)',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAutres():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MISC[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher autres',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPORT_REPLAY[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_REPLAY[1],
        'Sports',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPECT_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPECT_NEWS[1],
        'Spectacles',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', CONCERT_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        CONCERT_NEWS[1],
        'Concerts',
        'music.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', TV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TV_NEWS[1],
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text  # + '&search_start=0'
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    URL_MOVIES = URL_MAIN + url + '?do=cat&category=telecharger-series&genre='

    listeGenres = [
        'Action',
        'Animation',
        'Arts Martiaux',
        'Aventure',
        'Biopic',
        'Bollywood',
        'Comédie Dramatique',
        'Comédie Musicale',
        'Comédie',
        'Documentaire',
        'Drame',
        'Epouvante-horreur',
        'Espionnage',
        'Famille',
        'Fantastique',
        'Guerre',
        'Historique',
        'Horreur',
        'Musical',
        'Péplum',
        'Policier',
        'Romance',
        'Science Fiction',
        'Thriller',
        'Western']

    output_parameter_handler = OutputParameterHandler()
    for genre in listeGenres:
        output_parameter_handler.addParameter(
            'site_url', URL_MOVIES + genre.replace(' ', '%20'))
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            genre,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
        search_text = search_text.replace(URL_SEARCH_MISC[0], '')
        search_text = util.CleanName(search_text)
        url = search

    if search or "index" in url:  # en mode recherche
        pattern = 'mov"><a class="mov-t nowrap" href="([^"]+)" title="([^"]+).+?data-content="(.*?)" class="mov-i img-box"><img src="([^"]+).+?annee-de-sortie.+?>(\\d+)<.+?category=.+?>(.+?)<'
        validUrl = [
            'films',
            'series',
            'animes',
            'concerts',
            'emissions-tv-documentaires']
    elif 'collections/' in url:
        pattern = 'tcarusel-item.+?href="([^"]+).+?title="([^"]+)" data-content="([^"]*).+?src="([^"]+)'
    else:
        pattern = '<div class="mov .+?href="([^"]+).+?title="([^"]+).+?data-content="([^"]*).+?src="([^"]+).+?annee-de-sortie.+?>(\\d+)<.+?saison">([^<]*)<'

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    results = parser.parse(html_content, pattern)

    titles = list()
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            year = ''
            cat = ''
            sSaison = ''
            if search or 'index' in url:
                # On exclus tout ce qui n'est pas lisible par Kodi.
                if any(x in entry[0] for x in validUrl):
                    title = entry[1]
                    if search:
                        if not util.CheckOccurence(search_text, title):
                            continue    # Filtre de recherche
                    url2 = entry[0]
                    desc = entry[2]
                    thumb = URL_MAIN[:-1] + entry[3]
                    year = entry[4]
                    cat = entry[5]
                else:
                    continue
            elif 'collections/' in url:
                url2 = entry[0]
                title = entry[1].replace(' - Saga', '')
                desc = entry[2]
                thumb = URL_MAIN[:-1] + entry[3]
            else:
                url2 = entry[0]
                desc = entry[2]
                thumb = URL_MAIN[:-1] + entry[3]
                title = entry[1]
                year = entry[4]
                sSaison = entry[5]

            titles.append(title)
            display_title = title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if sSaison or 'Anime' in cat:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif 'collections/' in url:
                gui.addMoviePack(
                    SITE_IDENTIFIER,
                    'showCollec',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        if not search:
            if 'index' in url:
                pattern = '<a name="nextlink".+?javascript:list_submit\\((.+?)\\)'
                results = parser.parse(html_content, pattern)
                if results[0]:
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', re.sub(
                        'search_start=(\\d+)', 'search_start=' + str(results[1][0]), url))
                    number = re.search('([0-9]+)', results[1][0]).group(1)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showMovies',
                        'Page ' + number,
                        output_parameter_handler)
            else:
                next_page, paging = __checkForNextPage(html_content)
                if next_page is not False:
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', next_page)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showMovies',
                        'Page ' + paging,
                        output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>(\\d+)</a></li><li><a href="([^"]+)"><span class="fa fa-arrow-right">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return URL_MAIN[:-1] + next_page, paging

    return False, 'none'


def showCollec():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    pattern = 'class="mov-t nowrap" href="([^"]+).+?data-content="([^"]*).+?<img src="([^"]+).+?title="([^"]+)'

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    results = parser.parse(html_content, pattern)

    titles = set()
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            desc = entry[1]
            thumb = entry[2]
            title = entry[3]

            # Enlever les films en doublons (même titre)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            if title in titles:
                continue
            titles.add(title)

            desc = re.sub('<[^<]+?>', '', desc)
            display_title = title

            if not thumb.startswith('http'):
                thumb = URL_MAIN[:-1] + thumb

            if not url2.startswith('http'):
                url2 = URL_MAIN[:-1] + url2

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showMoviesLinks',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMoviesLinks(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    # récupération du Synopsis
    if not desc:
        try:
            pattern = '<h3 class="">Description</h3>(.+?)</div>'
            results = parser.parse(html_content, pattern)
            if results[0]:
                desc = results[1][0]
        except BaseException:
            pass

    # liens download
    pattern = "domain=(.+?)'(.+?)/tbody"
    results = parser.parse(html_content, pattern)
    output_parameter_handler = OutputParameterHandler()
    if results[0]:
        pattern = "target='_blank' data-id='.+?' href='([^']+)"
        for entry in results[1]:
            host = entry[0]
            results = parser.parse(entry[1], pattern)
            if results[0]:
                for entry in results[1]:  # Plusieurs liens pour le même host
                    url2 = URL_MAIN[:-1] + entry
                    display_title = (
                        '%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

                    output_parameter_handler.addParameter('site_url', url2)
                    output_parameter_handler.addParameter(
                        'movie_title', movie_title)
                    output_parameter_handler.addParameter('thumb', thumb)
                    output_parameter_handler.addParameter('desc', desc)
                    gui.addLink(
                        SITE_IDENTIFIER,
                        'Display_protected_link',
                        display_title,
                        thumb,
                        desc,
                        output_parameter_handler)

    # lien STREAMING
    pattern = 'rel=.nofollow. class=.download. href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:  # Plusieurs liens pour le même host
            url2 = URL_MAIN[:-1] + entry
            display_title = ('%s [Streaming]') % movie_title

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersLink',
                display_title,
                thumb,
                desc,
                output_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    pattern = "value='([^']+)'.+?<b>([^<]+)<\\/b>.+?<b> \\(([^\\)]+)\\)"
    results = parser.parse(html_content, pattern)
    if results[0]:
        # Affichage du texte
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres qualités disponibles :[/COLOR]')
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            qual = entry[1]
            lang = entry[2]
            display_title = ('%s [%s] (%s)') % (movie_title, qual, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    pattern = 'href="https://www\\.themoviedb\\.org/(.+?)/(.+?)\\?'
    results = parser.parse(html_content, pattern)
    idTMDB = ''
    if results[0]:
        if results[1][0][0] == "tv":
            pass
        elif results[1][0][0] == "movie":
            return showMoviesLinks()
        idTMDB = results[1][0][1]

    # Affichage du texte
    gui.addText(
        SITE_IDENTIFIER,
        '[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    # récupération du Synopsis
    try:
        pattern = '<h3 class="">Description</h3>(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    # Mise à jour du titre
    pattern = '<h3 class="p-2">(.+?)</h3>'
    results = parser.parse(html_content, pattern)

    title = movie_title

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(html_content)

    sPattern1 = "value='(.+?)'.+?>(.+?)</b>.+?<b>(.+?)</b>.+?<b> \\((.+?)\\)"
    aResult1 = parser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        output_parameter_handler = OutputParameterHandler()
        for entry in aResult1[1]:
            if "Saison" not in entry[1]:
                title = movie_title + ' Saison ' + entry[1]
            else:
                title = movie_title + ' ' + entry[1].replace('<b>', '')

            qual = entry[2]
            lang = entry[3]
            display_title = ('%s [%s] (%s)') % (title, qual, lang)

            url = URL_MAIN + "?subaction=get_links&version=" + entry[0]
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('tmdb_id', idTMDB)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                display_title,
                'series.png',
                thumb,
                desc,
                output_parameter_handler)

    # Affichage du titre
    gui.addText(
        SITE_IDENTIFIER,
        '[COLOR olive]Autres saisons disponibles :[/COLOR]')

    # on regarde si dispo dans d'autres saison
    sHtmlContent1 = CutSais(html_content)

    sPattern1 = '<option value="([^"]+)">([^<]+)<'
    aResult1 = parser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        # Une ligne par saison, pas besoin d'afficher les qualités ici
        output_parameter_handler = OutputParameterHandler()
        for entry in aResult1[1]:

            sSaison = entry[1]
            display_title = ('%s %s') % (movie_title, sSaison)

            url = entry[0]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sSaison', sSaison)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                display_title,
                'series.png',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    if url.find("https") != url.rfind("https"):
        url = url[url.rfind("https"):]

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    parser = Parser()
    pattern = "domain=(.+?)\\.|'download' target='_blank' data-id='.+?' href='([^']+).+?(\\d+,\\d+\\s[kKmMgG][oO])"
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    re.sub(
                        '\\.\\w+',
                        '',
                        entry[0]) +
                    '[/COLOR]')

            else:
                if URL_MAIN not in entry[1]:
                    url2 = URL_MAIN[:-1] + entry[1]
                    title = movie_title + \
                        ' (' + entry[2] + ')' if entry[2] else movie_title
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url2)
                    output_parameter_handler.addParameter(
                        'movie_title', movie_title)
                    output_parameter_handler.addParameter('thumb', thumb)
                    gui.addLink(
                        SITE_IDENTIFIER,
                        'Display_protected_link',
                        title,
                        thumb,
                        desc,
                        output_parameter_handler,
                        input_parameter_handler)

        gui.setEndOfDirectory()
    else:
        showHosters()


def showHostersLink(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()
    parser = Parser()
    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        if not results[1][0].startswith('http'):
            hoster_url = "https:" + results[1][0]
        else:
            hoster_url = results[1][0]

        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url.replace(' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    parser = Parser()
    pattern = "\\?domain=(.+?)\\.|'download' target='_blank' data-id='.+?' href='([^']+).+?(Episode.+?\\d+).+?(\\d+,\\d+\\s[kKmMgG][oO])"
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    re.sub(
                        '\\.\\w+',
                        '',
                        entry[0]) +
                    '[/COLOR]')
            else:
                if URL_MAIN not in entry[2]:
                    url2 = URL_MAIN[:-1] + \
                        entry[1].replace('\\', '').replace('"', '')
                    title = movie_title + ' ' + \
                        entry[2].replace('FINAL ', '') + ' (' + entry[3] + ')'
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url2)
                    output_parameter_handler.addParameter(
                        'movie_title', title)
                    output_parameter_handler.addParameter('thumb', thumb)
                    gui.addEpisode(
                        SITE_IDENTIFIER,
                        'Display_protected_link',
                        title,
                        '',
                        thumb,
                        desc,
                        output_parameter_handler)

        gui.setEndOfDirectory()
    else:
        showHosters()


def Display_protected_link(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue(
        'site_url').replace('\\', '').replace('"', '')
    thumb = input_parameter_handler.getValue('thumb')

    if not url.startswith('http'):
        url = 'http://' + url

    request_handler = RequestHandler(
        url.replace(
            'link', 'streaming').replace(
            ' ', '%20'))
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<iframe.+?src="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:
            hoster_url = entry.replace('uptostream', 'uptobox')

            title = movie_title
            if len(results[1]) > 1:
                title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def CutQual(html_content):
    parser = Parser()
    pattern = '<select name="qualite".+?>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    else:
        return html_content

    return ''


def CutSais(html_content):
    parser = Parser()
    pattern = '<select id="saison".+?class="form-control">(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''


def DecryptDlProtecte(url):
    """ Nouvelle méthode pour dl protect qui passe par requests"""
    s = requests.Session()

    response = s.get(url)
    html_content = str(response.content)
    cookie_string = "; ".join([str(x) + "=" + str(y)
                              for x, y in s.cookies.items()])

    pattern = 'type="hidden" name="_token" value="(.+?)">'
    results = re.search(pattern, html_content).group(1)

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('Host', url.split('/')[2])
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request_handler.addHeaderEntry(
        'Content-Length', len(str("_token=" + results + "&getlink=1")))
    request_handler.addHeaderEntry(
        'Content-Type',
        "application/x-www-form-urlencoded")
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Cookie', cookie_string)
    request_handler.addParameters("_token", results)
    request_handler.addParametersLine("_token=" + results + "&getlink=1")

    html_content = request_handler.request()

    return html_content

# ******************************************************************************
# from
# http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/


"""Encode multipart form data to upload files via POST."""


def encode_multipart(fields, files, boundary):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    lines = []

    for name, value in fields.items():
        lines.extend(
            ('-----------------------------{0}'.format(boundary),
             'Content-Disposition: form-data; name="{0}"'.format(
                escape_quote(name)),
                '',
                str(value),
                '-----------------------------{0}--'.format(boundary),
                ''))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(
                filename)[0] or 'application/octet-stream'
        lines.extend(
            ('--{0}'.format(boundary),
             'Content-Disposition: form-data; name="{0}"'.format(
                escape_quote(name),
                escape_quote(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                value['content']))

    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
        'Content-Length': str(
            len(body))}

    return body, headers
