# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import json
import re

from resources.lib.comaddon import Addon, dialog, Progress, SiteManager, VSlog
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'extreme_down'
SITE_NAME = '[COLOR violet]Extreme Down[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

# Utiliser ce site pour retrouver le nom de domaine :
# https://www.extreme-down.info/

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (
    URL_SEARCH[0] +
    'do=search&subaction=search&titleonly=3&speedsearch=1&story=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_SEARCH[0] +
    'do=search&subaction=search&titleonly=3&speedsearch=2&story=',
    'showMovies')
URL_SEARCH_ANIMS = (
    URL_SEARCH[0] +
    'do=search&subaction=search&titleonly=3&speedsearch=4&story=',
    'showMovies')
URL_SEARCH_MISC = (
    URL_SEARCH[0] +
    'do=search&subaction=search&titleonly=3&speedsearch=3&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'films-new-hd/new-bluray-1080p/', 'showMovies')
MOVIE_NEWS2021 = (URL_MAIN + 'films-new-hd/', 'showMovies')
# MOVIE_GENRES = (True, 'showGenres')
# MOVIE_ANNEES = (True, 'showMovieYears')

MOVIE_VOSTFR = (URL_MAIN + 'films-vostfr/dvdrip-vostfr', 'showMovies')
MOVIE_4K = (URL_MAIN + 'films-new-ultrahd/', 'showMovies')
MOVIE_720 = (URL_MAIN + 'films-new-hd/new-bluray-720p/', 'showMovies')
MOVIE_1080X265 = (URL_MAIN + 'films-hd/films-1080p-x265', 'showMovies')
MOVIE_BLURAYVOSTFR = (
    URL_MAIN +
    'films-vostfr/films-1080p-vostfr',
    'showMovies')
MOVIE_3D = (URL_MAIN + 'films-new-hd/new-full-bluray-3d', 'showMovies')
MOVIE_FULL1080P = (URL_MAIN + 'films-new-hd/new-full-bluray', 'showMovies')
MOVIE_FULL4K = (
    URL_MAIN +
    'films-new-ultrahd/new-full-bluray-ultrahd-4k',
    'showMovies')
MOVIE_WEBRIP4K = (URL_MAIN + 'films-new-ultrahd/new-webrip-4k', "showMovies")
MOVIE_REMUX4K = (URL_MAIN + 'films-new-ultrahd/new-ultrahd-4k', "showMovies")
MOVIE_LIGHT720 = (URL_MAIN + 'films-hdlight/hdlight-720p', 'showMovies')
MOVIE_LIGHT1080 = (URL_MAIN + 'films-hdlight/hdlight-1080p', 'showMovies')
MOVIE_LIGHTBDRIP = (URL_MAIN + 'films-new-hd/new-bdrip-720p', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-sd/dvdrip', 'showMovies')
MOVIE_OLDDVD = (URL_MAIN + 'films-sd/ancien-dvdrip', 'showMovies')
MOVIE_FILMO = (URL_MAIN + 'films-sd/filmographie', 'showMovies')
MOVIE_CLASSIQUE_SD = (URL_MAIN + 'films-classique/classiques-sd', 'showMovies')
MOVIE_CLASSIQUE_HD = (URL_MAIN + 'films-classique/classiques-hd', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_HD = (URL_MAIN + 'series-hd/1080p-series-vf', 'showMovies')
# SERIE_GENRES = (True, 'showGenres')
# SERIE_ANNEES = (True, 'showSerieYears')
SERIE_VOSTFRS = (URL_MAIN + 'series-hd/1080p-series-vostfr/', 'showMovies')
SERIE_720VO = (URL_MAIN + 'series-hd/hd-series-vostfr', 'showMovies')
SERIE_720VF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies')
SERIE_4K = (URL_MAIN + 'series-hd/hd-x265-hevc/', 'showMovies')
SERIE_MULTI = (URL_MAIN + 'series-hd/hd-series-multi/', 'showMovies')
SERIE_SDVO = (URL_MAIN + 'series/vostfr/', 'showMovies')
SERIE_SDVF = (URL_MAIN + 'series/vf/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'mangas/manga-films/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/series-vostfr/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/series-vf/', 'showMovies')
ANIM_MULTI = (URL_MAIN + 'mangas/series-multi/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS = (URL_MAIN + 'theatre/', 'showMovies')


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
        'showMenuAutre',
        'Autres',
        'tv.png',
        output_parameter_handler)

    if not Addon().getSetting('hoster_alldebrid_token'):
        output_parameter_handler.addParameter('site_url', 'http://venom/')
        gui.addDir(
            SITE_IDENTIFIER,
            'getToken',
            '[COLOR red]Les utilisateurs d\'Alldebrid cliquez ici.[/COLOR]',
            'films.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Films)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS2021[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS2021[1],
        'Nouveauté 2021 HD',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD1080[1],
        'Bluray 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Bluray 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_720[1],
        'Bluray 720P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_1080X265[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1080X265[1],
        'Bluray 1080P H265/HEVC',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_BLURAYVOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAYVOSTFR[1],
        'Bluray VOSTFR',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Bluray 3D',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_FULL1080P[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FULL1080P[1],
        'REMUX 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_FULL4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FULL4K[1],
        'Bluray 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_REMUX4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_REMUX4K[1],
        'Remux 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_WEBRIP4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_WEBRIP4K[1],
        'Webrip 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIGHT720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHT720[1],
        'HD light 720P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIGHT1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHT1080[1],
        'HD light 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIGHTBDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHTBDRIP[1],
        'HD light BDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films BDRIP/DVDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_OLDDVD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_OLDDVD[1],
        'Ancien DVDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_FILMO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FILMO[1],
        'Filmographie',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_CLASSIQUE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_CLASSIQUE_HD[1],
        'Films Classique HD',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_CLASSIQUE_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_CLASSIQUE_SD[1],
        'Films Classique SD',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Séries)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD[1],
        'Séries 1080p VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries 1080p VOSTFR',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_720VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_720VF[1],
        'Séries 720p VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_720VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_720VO[1],
        'Séries 720p VOSTFR',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_4K[1],
        'Séries 4K H265/HEVC',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_MULTI[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MULTI[1],
        'Séries multilangue',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SDVF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SDVF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SDVO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SDVO[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMangas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Animes)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animes (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_FILM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_FILM[1],
        "Film d'animation japonais (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        "Animés VOSTFR (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        "Animés VF (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MULTI[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MULTI[1],
        "Animés multilangue (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAutre():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MISC[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Autres)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    output_parameter_handler.addParameter('misc', True)
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        "Documentaire (Derniers ajouts)",
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPECTACLE_NEWS[0])
    output_parameter_handler.addParameter('misc', True)
    gui.addDir(
        SITE_IDENTIFIER,
        SPECTACLE_NEWS[1],
        "Spectacle et théatre (Derniers ajouts)",
        'buzz.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def getToken():
    gui = Gui()

    sToken = gui.showKeyBoard(heading="Entrez votre token alldebrid")
    cPremiumHandler('alldebrid').setToken(sToken)
    dialog().VSinfo('Token ajouté', "Extreme-Download", 5)
    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url += search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

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


def showMovieYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1913, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    nextPageSearch = input_parameter_handler.getValue('nextPageSearch')
    site_url = input_parameter_handler.getValue('site_url')
    sMisc = input_parameter_handler.getValue('misc')  # Autre contenu

    if nextPageSearch:
        search = site_url

    cat = None
    if search:
        site_url = search

        if nextPageSearch:
            search += '&search_start=' + nextPageSearch
        request_handler = RequestHandler(site_url)
        html_content = request_handler.request()

        html_content = parser.abParse(
            html_content, 'de la recherche', 'À propos')

        cat = int(re.search('speedsearch=(\\d)', search).group(1))
        search = re.search('story=(.+?)($|&)', search).group(1)
        util = cUtil()
        search = util.CleanName(search)
    else:
        request_handler = RequestHandler(site_url)
        html_content = request_handler.request()

    pattern = 'class="top-last thumbnails" href="([^"]+)".+?"img-post" src="([^"]+).+?alt="([^"]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    titles = set()

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

            # on enleve les softwares
            if 'PC' in entry[2]:  # for the search
                continue

            url2 = entry[0]
            thumb = entry[1]
            if ' - ' in entry[2]:
                title = entry[2].split(' - ')[0]
                qual = entry[2].split(' - ')[1]
                qual = qual.replace(
                    'Avec TRUEFRENCH',
                    '').replace(
                    'TRUEFRENCH',
                    '').replace(
                    'FRENCH ',
                    '')

                if 'Saison' in qual:  # Pour les séries et animes
                    # * et non pas + car parfois "Saison integrale" pas de chiffre
                    saison = re.search('(Saison [0-9]*)', qual).group(1)
                    title = title + ' ' + saison
                    qual = re.sub('Saison [0-9]+ ', '', qual)

                if '(E' in entry[2]:
                    res = re.search('\\(E([0-9]+ .+? [0-9]+)\\)', entry[2])
                    try:
                        title = title + ' E' + \
                            res.group(1).replace('Ã', ' - ').replace('à', ' - ').split('[')[0]
                    except BaseException:
                        pass

            else:
                # .replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')
                title = entry[2]
                qual = ''

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            key = title + "-" + thumb
            if key in titles:
                continue
            titles.add(key)

            if search and total > 5:
                if not util.CheckOccurence(search, title):
                    continue

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)

            if cat == 3 or sMisc:
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif cat == 1 or '/films' in site_url or '/manga-films/' in site_url:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif cat == 4 or '/mangas/' in site_url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        if search:
            pattern = 'name="nextlink" id="nextlink" onclick="javascript:list_submit\\(([0-9]+)\\); return\\(false\\)" href="#">Suivant'
            results = parser.parse(html_content, pattern)
            if results[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', site_url)
                output_parameter_handler.addParameter('misc', sMisc)
                output_parameter_handler.addParameter(
                    'nextPageSearch', results[1][0])
                sNumPage = re.search('([0-9]+)', results[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + sNumPage,
                    output_parameter_handler)

        else:
            next_page = __checkForNextPage(html_content)
            if next_page:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', next_page)
                output_parameter_handler.addParameter('misc', sMisc)
                sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + sNumPage,
                    output_parameter_handler)

    if nextPageSearch:
        gui.setEndOfDirectory()

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a href="([^"]+)">Suivant &.+?</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showMoviesLinks(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = '<blockquote.+?>([^<]+)<'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = cUtil().removeHtmlTags(results[1][0])
    except BaseException:
        pass

    pattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)</title>'
    results = parser.parse(html_content, pattern)

    qual = ''
    if results[1]:
        movie_title = results[1][0][1]
        qual = results[1][0][2].replace('"', '')

    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    display_title = ('%s (%s)') % (movie_title, qual)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', display_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addLink(
        SITE_IDENTIFIER,
        'showLinks',
        display_title,
        thumb,
        desc,
        output_parameter_handler,
        input_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    pattern = '<a class="btn-other" href="([^<]+)">([^<]+)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            qual = entry[1]
            title = ('%s [%s]') % (movie_title, qual)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('display_title', title)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLinks',
                title,
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
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = '<blockquote.+?>([^<]+)<'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = cUtil().removeHtmlTags(results[1][0])

    except BaseException:
        pass

    pattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)(VOSTFR|VF)*.+?</title>'
    results = parser.parse(html_content, pattern)
    # VSlog(results)
    if results[1]:
        movie_title = results[1][0][1]

    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    pattern = '<meta property="og:title" content=".+? - (.+?)(VOSTFR|VF)*/>'
    results = parser.parse(html_content, pattern)
    # VSlog(results)

    qual = ''
    title = movie_title
    if results[0]:
        qual = results[1][0][0].replace('"', '')
        if 'Saison' in qual:  # N° de saison dans la qualite
            # * et non pas + car parfois "Saison integrale" pas de chiffre
            saison = re.search('(Saison [0-9]*)', qual).group(1)
            qual = re.sub('Saison [0-9]+ ', '', qual)
            title = movie_title + ' ' + saison

    display_title = ('%s (%s)') % (title, qual)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', display_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addSeason(
        SITE_IDENTIFIER,
        'showLinks',
        display_title,
        '',
        thumb,
        desc,
        output_parameter_handler)

    sHtmlContent1 = cutQual(html_content)
    sPattern1 = '<a class="btn-other" href="([^"]+)">([^<]+)</a>'

    aResult1 = parser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        output_parameter_handler = OutputParameterHandler()
        for entry in aResult1[1]:
            url = entry[0]
            qual = entry[1]
            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showLinks',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    sHtmlContent2 = cutSais(html_content)
    sPattern2 = '<a class="btn-other" href="([^"]+)">([^<]+)<'

    aResult2 = parser.parse(sHtmlContent2, sPattern2)

    if aResult2[0] is True:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        output_parameter_handler = OutputParameterHandler()
        for entry in aResult2[1]:

            url = entry[0]
            title = movie_title + ' ' + entry[1].replace('Saison ', 'S')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Detection de la taille des fichier pour separer les fichier premium des
    # parties en .rar
    if 'saison' not in url:
        fileSize = re.findall(
            '<strong>Taille</strong><span style="float: right;">([^<]+)</span></td>',
            html_content)
        if 'et' in str(fileSize[0]):
            taille = str(fileSize[:-7])
        else:
            taille = str(fileSize[0])

        if ' Go' in taille:
            size, unite = taille.split(' ')
            if float(size) > 4.85:
                if "1 Lien" in html_content:
                    VSlog('1 Lien premium')
                    pattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<div class="prez_2">1 Lien Uptobox</div>\\s*.+?>\\s*.+?<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>.+?\\s*<div class="showNFO"'
                else:
                    VSlog('Pas lien premium')
                    pattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)* Premi*um</strong>'
            else:
                pattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
        else:
            pattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
    else:
        pattern = '<div class="prez_7">([^<]+)</div>|<a title=".+?" href="([^"]+)" target="_blank"><strong class="hebergeur">([^<]+)</strong>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    # Il n'existe que des fichiers en parties, non fonctionnel
    if (results[0] is False) and float(size) > 4.85:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        if 'saison' in url:
            results[1].insert(0, ('Episode 1', '', ''))

        ep = ""
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                ep = entry[0]
            else:
                url2 = entry[1]

                if 'saison' in url:
                    title = movie_title + ' ' + ep
                else:
                    title = movie_title

                if 'saison' in url:
                    display_title = (
                        '%s [COLOR coral]%s[/COLOR]') % (title, entry[2])
                else:
                    display_title = (
                        '%s [COLOR coral]%s[/COLOR]') % (movie_title, str(entry[2]))

                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)

                if 'saison' in url:
                    gui.addEpisode(
                        SITE_IDENTIFIER,
                        'showHosters',
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

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    Token_Alldebrid = Addon().getSetting('hoster_alldebrid_token')
    if Token_Alldebrid != "":
        sUrl_Bypass = "https://api.alldebrid.com/v4/link/redirector?agent=service&version=1.0-&apikey="
        sUrl_Bypass += Token_Alldebrid + "&link=" + url

        request_handler = RequestHandler(sUrl_Bypass)
        html_content = json.loads(request_handler.request())

        HostURL = html_content["data"]["links"]
        for hoster_url in HostURL:

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        from resources.lib import librecaptcha
        test = librecaptcha.get_token(
            api_key="6LeH9lwUAAAAAGgg9ZVf7yOm0zb0LlcSai8t8-2o",
            site_url=url,
            user_agent=UA,
            gui=False,
            debug=False)

        if test is None:
            gui.addText(
                SITE_IDENTIFIER,
                '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

        else:
            # N'affiche pas directement le liens car sinon Kodi crash.
            display_title = "Recaptcha passé avec succès, cliquez pour afficher les liens"
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('Token', test)
            gui.addLink(
                SITE_IDENTIFIER,
                'getHost',
                display_title,
                thumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def getHost(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    test = input_parameter_handler.getValue('Token')

    data = 'g-recaptcha-response=' + test + '&submit_captcha=1'
    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip')
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', len(str(data)))
    request_handler.addParametersLine(data)
    html_content = request_handler.request()

    pattern = '<div><span class="lien"><a target="_blank" href="(.+?)">'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:
            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def cutQual(html_content):
    parser = Parser()
    pattern = '<span class="other-qualities">&Eacute;galement disponible en :</span>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''


def cutSais(html_content):
    parser = Parser()
    pattern = '<span class="other-qualities">Autres saisons :</span>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''
