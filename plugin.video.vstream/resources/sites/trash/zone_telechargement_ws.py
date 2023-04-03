# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import unicodedata

from resources.lib.comaddon import Progress, dialog, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
# Fonction de vStream qui remplace urllib.quote, pour simplifier le
# passage en python 3
from resources.lib.util import Quote, cUtil

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&q=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&q=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&q=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films/', 'showMovies')  # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'nouveaux-films/',
                'showMovies')  # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'film-bluray-3d/', 'showMovies')  # films en 3D
MOVIE_HD = (URL_MAIN + 'film-bluray-hd/', 'showMovies')  # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'film-x265-x264-hdlight/',
                 'showMovies')  # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies')  # films VOSTFR
MOVIE_4K = (URL_MAIN + 'films-ultra-hd-4k/', 'showMovies')  # films "4k"
MOVIE_GENRES = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&catid=0&q=&genre%5B%5D={}&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=1',
    'showGenre')
MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies')  # dessins animes
MOVIE_BDRIP = (URL_MAIN + 'film-dvdrip-bdrip/', 'showMovies')
MOVIE_TS_CAM = (URL_MAIN + 'tscam-films-2020/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'film-vfstfr/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'film-mkv/', 'showMovies')
MOVIE_VO = (URL_MAIN + 'films-vo/', 'showMovies')
MOVIE_INTEGRAL = (URL_MAIN + 'collections-films-integrale/', 'showMovies')

SERIE_SERIES = ('http://', 'showMenuTvShows')
SERIE_VFS = (URL_MAIN + 'serie-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'serie-vf-en-hd/', 'showMovies')
SERIE_VF_1080 = (URL_MAIN + 'serie-vf-1080p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'serie-vostfr-hd/', 'showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'serie-vostfr-1080p/', 'showMovies')
SERIE_VO = (URL_MAIN + 'serie-vo/', 'showMovies')
ANCIENNE_SERIE = (URL_MAIN + 'telecharger-serie/ancienne-serie/', 'showMovies')

ANIM_ANIMS = ('http://', 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
ANIM_VOSTEN = (URL_MAIN + 'animes-vosten/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-mangas/', 'showMovies')
OAV = (URL_MAIN + 'oav/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaire-gratuit/', 'showMovies')  # docs
DOC_DOCS = ('http://', 'load')

SPORT_REPLAY = (URL_MAIN + 'sport/', 'showMovies')  # sports
SPORT_SPORTS = SPORT_REPLAY
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies')  # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies')  # derniers spectacles
CONCERT_NEWS = (URL_MAIN + 'concert/', 'showMovies')  # derniers concerts
AUTOFORM_VID = (URL_MAIN + 'autoformations-videos/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
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


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Exclus (Films populaires)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Blu-rays (720p & 1080p)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films (3D)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (x265 & x264)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films (4k)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANIME[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANIME[1],
        'Dessins Animés (Derniers ajouts)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films (BDRIP)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TS_CAM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TS_CAM[1],
        'Films (TS, CAM, R5, DVDSCR)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VFSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VFSTFR[1],
        'Films en francais sous titre francais (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MKV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MKV[1],
        'Films (dvdrip mkv)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VO[1],
        'Films en Version original (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_INTEGRAL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_INTEGRAL[1],
        'Intégral de films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_720[1],
        'Séries 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_1080[1],
        'Séries 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VO[1],
        'Séries (VO)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANCIENNE_SERIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANCIENNE_SERIE[1],
        'Ancienne séries (Derniers)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMangas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animes (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_720[1],
        'Animés 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_1080[1],
        'Animés 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_720[1],
        'Animés 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_1080[1],
        'Animés 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', FILM_ANIM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        FILM_ANIM[1],
        'Films d\'animés ',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTEN[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTEN[1],
        'Animés (VOSTEN)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAutres():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', TV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TV_NEWS[1],
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPECT_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPECT_NEWS[1],
        'Spectacles',
        'star.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        search_text = Quote(search_text)
        url = URL_SEARCH[0] + search_text + \
            '&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=0'
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    UrlGenre = input_parameter_handler.getValue('site_url')

    liste = [['Action', 'Action'], ['Animation', 'Animation'], ['Arts Martiaux', 'martiaux'], ['Aventure', 'Aventure'],
             ['Biopic', 'Biopic'], ['Comédie Dramatique', 'Dramatique'], ['Comédie Musicale', 'Musical'],
             ['Comédie', 'Comedie'], ['Divers', 'Divers'], ['Documentaires', 'Documentaire'], ['Drame', 'Drame'],
             ['Epouvante Horreur', 'Epouvante'], ['Espionnage', 'Espionnage'], ['Famille', 'Famille'],
             ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'], ['Historique', 'Historique'], ['Musical', 'musicale'],
             ['Péplum', 'Peplum'], ['Policier', 'Policier'], ['Romance', 'Romance'], ['Science Fiction', 'Science'],
             ['Thriller', 'Thriller'], ['Western', 'Western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', UrlGenre.format(url))
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace('index.php', '')
    if search:
        url = search

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<img class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+)<.+?<b>([^<]+)<.+?">([^<]+)<'

    parser = Parser()
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

            thumb = entry[0]
            url2 = entry[1]
            title = entry[2]
            qual = entry[3]
            lang = entry[4]

            # on vire le tiret des series
            title = title.replace(
                ' - Saison',
                ' Saison').replace(
                'COMPLETE',
                'Complete')
            movie_title = title.split('Saison')[0]

            if '[Complete]' not in title:
                title = title.replace('COMPLETE', '[Complete]')

            # nettoyage du titre
            title = title.replace('Complete', 'Complète')
            title = re.sub('\\[\\w+]', '', title)

            try:
                title = str(title.encode('latin-1'), encoding="utf-8")
            except BaseException:
                pass

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            key = title + "-" + thumb
            if key in titles:
                continue
            titles.add(key)

            display_title = ('%s [%s] %s') % (title, qual, lang)

            if not thumb.startswith('https'):
                thumb = URL_MAIN + thumb

            if not url2.startswith('https'):
                url2 = URL_MAIN + url2

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter(
                'display_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)

            if 'anime' in url or 'anime' in url2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif 'serie' in url or 'serie' in url2:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', thumb, '', output_parameter_handler)
            elif DOC_NEWS[0] in url or TV_NEWS[0] in url or SPECT_NEWS[0] in url or CONCERT_NEWS[0] in url:
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif 'collection' in url or 'integrale' in url:
                gui.addMoviePack(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif ' Saison ' in title:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', thumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        if 'controller.php' in url:
            pattern = '<a href="#" class="nav" data-cstart="([^"]+)">Suivant</a></div>'
            results = parser.parse(html_content, pattern)
            if results[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', re.sub(
                    'cstart=(\\d+)', 'cstart=' + str(results[1][0]), url))
                number = re.search('([0-9]+)', results[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

        else:
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
    pattern = '>([^<]+)</a> *<a href="([^"]+)">Suivant</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        if not next_page.startswith('https'):
            next_page = URL_MAIN + next_page
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showMoviesLinks(input_parameter_handler=False):
    # VSlog('mode film')
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    display_title = input_parameter_handler.getValue('display_title')
    if not display_title:   # Si on arrive par un marque-page
        display_title = movie_title
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if "onaregarde" in url:
        parser = Parser()
        pattern = '<a type="submit".+?href="([^"]+)"'
        url = parser.parse(html_content, pattern)[1][0]

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis et de l'année
    desc = ''
    year = ''
    try:
        pattern = '(<u>Date de .+</u>.+(\\d{4}(-| *<))|<u>Critiques.+?</u>).+synopsis.+?>(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            entry = results[1][0]
            year = entry[1]
            desc = cUtil().removeHtmlTags(entry[3])
    except BaseException:
        pass

    # la qualité courante est le lien en cours ici même
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', movie_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('year', year)
    gui.addLink(
        SITE_IDENTIFIER,
        'showHosters',
        display_title,
        thumb,
        desc,
        output_parameter_handler,
        input_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    pattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)</b></span>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            qual = entry[1]
            lang = entry[2]
            title = ('%s [%s] %s') % (movie_title, qual, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('display_title', title)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)
            gui.addLink(
                SITE_IDENTIFIER,
                'showMoviesLinks',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    # VSlog('mode serie')
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if "onaregarde" in url:
        parser = Parser()
        pattern = '<a type="submit".+?href="([^"]+)"'
        url = parser.parse(html_content, pattern)[1][0]

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis
    desc = movie_title   # Ne pas laisser vide sinon un texte automatique faux va être calculé
    try:
        pattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = cUtil().removeHtmlTags(results[1][0][1])
    except BaseException:
        pass

    # on recherche d'abord la qualité courante
    pattern = 'smallsep.+?Qualité([^<]+)<.+?img src="([^"]+)".+?alt=.+?- Saison ([0-9]+)'
    results = parser.parse(html_content, pattern)

    # qual = ''
    # lang = ''
    if results[1] is True:
        entry = results[1][0]
        qual = entry[0].split('|')[0]
        lang = entry[0].split('|')[1]
        # change pour chaque saison, il faut la rechercher si on navigue entre
        # saisons
        thumb = entry[1]
        title = movie_title + ' S' + entry[2]

        display_title = ('%s [%s] (%s)') % (title, qual, lang)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('desc', desc)
        output_parameter_handler.addParameter('qual', qual)
        gui.addSeason(
            SITE_IDENTIFIER,
            'showSeriesHosters',
            display_title,
            '',
            thumb,
            desc,
            output_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(html_content)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = parser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        output_parameter_handler = OutputParameterHandler()
        for entry in aResult1[1]:
            if 'animes' in url:
                url = URL_MAIN + 'animes' + entry[0]
            else:
                url = URL_MAIN + 'telecharger-serie' + entry[0]
            qual = entry[1]
            lang = entry[2]
            display_title = ('%s [%s] %s') % (title, qual, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    # on regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(html_content)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = parser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if aResult2[0] is True:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')
        output_parameter_handler = OutputParameterHandler()
        for entry in aResult2[1]:
            sSaison = entry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in url:
                url = URL_MAIN + 'animes' + entry[0]
            else:
                url = URL_MAIN + 'telecharger-serie' + entry[0]

            title = movie_title + ' ' + entry[1] + entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                thumb,
                movie_title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    # VSlog('showHosters')
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if "zt-protect" in url:
        # Dl Protect present aussi a cette étape.
        html_content = DecryptDlProtecte(url)
    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # Si ça ressemble aux liens premiums on vire les liens non premium
    if 'Premium' in html_content or 'PREMIUM' in html_content:
        html_content = CutNonPremiumlinks(html_content)

    parser = Parser()

    pattern = '<div style="font-weight:bold;color:.+?</span>(.+?)</div>|<a class="btnToLink".+?href="(.+?)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                if 'Interchangeables' not in entry[0]:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR red]' +
                        entry[0] +
                        '[/COLOR]')
            else:
                display_title = movie_title

                output_parameter_handler.addParameter('site_url', entry[1])
                output_parameter_handler.addParameter('baseUrl', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('year', year)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    # VSlog('showSeriesHosters')
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    try:
        desc = unicodedata.normalize(
            'NFD', desc).encode(
            'ascii', 'ignore').decode('unicode_escape')
        desc = desc.encode('latin-1')
    except BaseException:
        pass

    if "zt-protect" in url:
        # Dl Protect present aussi a cette étape.
        html_content = DecryptDlProtecte(url)
    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    # Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in html_content or 'PREMIUM' in html_content or 'premium' in html_content:
        html_content = CutPremiumlinks(html_content)

    pattern = '<div style="font-weight.+?>([^<]+)</div>|<a class="btnToLink".+?href="([^"]+)".+?Episode ([0-9]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                if 'Télécharger' in entry[0]:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR olive]' +
                        entry[0] +
                        '[/COLOR]')
                else:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR red]' +
                        entry[0] +
                        '[/COLOR]')
            else:
                sName = 'E' + entry[2]
                sName = sName.replace('Télécharger', '')
                url2 = entry[1]
                title = movie_title + ' ' + sName

                output_parameter_handler.addParameter('baseUrl', url)
                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
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


def Display_protected_link(input_parameter_handler=False):
    # VSlog('Display_protected_link')
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    # baseUrl = input_parameter_handler.getValue('baseUrl')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    # Est-ce un lien dl-protect ?
    if url:

        html_content = DecryptDlProtecte(url)

        if html_content:
            # Si redirection
            if html_content.startswith('http'):
                aResult_dlprotecte = (True, [html_content])
            else:
                sPattern_dlprotecte = 'class="alert alert-primary".+?href="(.+?)"'
                aResult_dlprotecte = parser.parse(
                    html_content, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not url.startswith('http'):
            url = 'http://' + url
        aResult_dlprotecte = (True, [url])

    if aResult_dlprotecte[0]:

        episode = 1

        for entry in aResult_dlprotecte[1]:
            hoster_url = entry

            title = movie_title
            if len(aResult_dlprotecte[1]) > 1:
                title = movie_title + ' episode ' + episode

            episode += 1

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def CutQual(html_content):
    parser = Parser()
    pattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    else:
        return html_content

    return ''


def CutSais(html_content):
    parser = Parser()
    pattern = '<h3>Saisons.+?galement disponibles.+?</h3>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''


def CutNonPremiumlinks(html_content):
    parser = Parser()
    pattern = '(?:Lien.+?Premium - 1 lien|Lien.+?Premium)(.+?)</b></font></a></center>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return html_content


def CutPremiumlinks(html_content):
    parser = Parser()
    pattern = '(?i) par .{1,2}pisode(.+?)$'
    results = parser.parse(html_content, pattern)
    if results[0]:
        html_content = results[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return html_content


def DecryptDlProtecte(url):

    if not url:
        return ''

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    html_content = request_handler.request()

    return str(html_content)
