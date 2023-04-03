# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import xbmc
import xbmcgui

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil, Quote
from resources.lib.config import GestionCookie
from resources.lib.comaddon import Progress, dialog, isMatrix, SiteManager

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'free_telechargement_org'
SITE_NAME = '[COLOR violet]Free-Téléchargement[/COLOR]'
SITE_DESC = 'Fichiers en DDL, HD, Films, Séries, Mangas Etc...'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# ne pas mettre 'er' ou 'ement' à la fin, perte de hosters
URL_PROTECT = 'liens.free-telecharg'

FUNCTION_SEARCH = 'showSearchResult'
URL_SEARCH = (URL_MAIN + '1/recherche/1.html?rech_fiche=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (
    URL_MAIN +
    '1/recherche/1.html?rech_cat=video&rech_fiche=',
    FUNCTION_SEARCH)
URL_SEARCH_SERIES = (
    URL_MAIN +
    '1/recherche/1.html?rech_cat=serie&rech_fiche=',
    FUNCTION_SEARCH)
URL_SEARCH_ANIMS = (
    URL_MAIN +
    '1/recherche/1.html?rech_cat=Animations&rech_fiche=',
    FUNCTION_SEARCH)
URL_SEARCH_MISC = (
    URL_MAIN +
    '1/recherche/1.html?rech_cat=videos&rech_fiche=',
    FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_SD_DVDRIP = (
    URL_MAIN +
    '1/categorie-Films+DVDRiP+et+BDRiP/1.html',
    'showMovies')
MOVIE_SD_CAM = (
    URL_MAIN +
    '1/categorie-Films+CAM+TS+R5+et+DVDSCR/1.html',
    'showMovies')
MOVIE_SD_VOSTFR = (
    URL_MAIN +
    '1/categorie-Films+VOSTFR+et+VO/1.html',
    'showMovies')
MOVIE_SD_CLASSIQUE = (
    URL_MAIN +
    '1/categorie-Films+Classiques/1.html',
    'showMovies')
MOVIE_SD_VIEWS = (URL_MAIN + '1/films/affichage', 'showMovies')
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')
MOVIE_HD = (
    URL_MAIN +
    '1/categorie-Films+BluRay+720p+et+1080p/1.html',
    'showMovies')
MOVIE_4K = (URL_MAIN + '1/categorie-Films+Bluray+4K/1.html', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + '1/films-hdlight/1.html', 'showMovies')
MOVIE_3D = (URL_MAIN + '1/categorie-Films+BluRay+3D/1.html', 'showMovies')
MOVIE_HD_VIEWS = (URL_MAIN + '1/films-bluray/affichage', 'showMovies')
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_SAGA = (URL_MAIN + '1/categorie-Sagas+Films/1.html', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_SD_EN_COURS_VF = (
    URL_MAIN +
    '1/categorie-Saisons+en+cours+VF+/1.html',
    'showMovies')
SERIE_SD_EN_COURS_VOSTFR = (
    URL_MAIN +
    '1/categorie-Saisons+en+cours+VOST/1.html',
    'showMovies')
SERIE_SD_TERMINE_VF = (
    URL_MAIN +
    '1/categorie-Saison+Termin%E9e+VF/1.html',
    'showMovies')
SERIE_SD_TERMINE_VOSTFR = (
    URL_MAIN +
    '1/categorie-Saison+Termin%E9e+VOST/1.html',
    'showMovies')
SERIE_HD_EN_COURS_VF = (
    URL_MAIN +
    '1/categorie-Saisons+en+cours+VF+HD/1.html',
    'showMovies')
SERIE_HD_EN_COURS_VOSTFR = (
    URL_MAIN +
    '1/categorie-Saisons+en+cours+VOST+HD/1.html',
    'showMovies')
SERIE_HD_TERMINE_VF = (
    URL_MAIN +
    '1/categorie-Saison+Termin%E9e+VF+HD/1.html',
    'showMovies')
SERIE_HD_TERMINE_VOSTFR = (
    URL_MAIN +
    '1/categorie-Saison+Termin%E9e+VOST+HD/1.html',
    'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + '1/animations/1', 'showMovies')
ANIM_VFS = (URL_MAIN + '1/categorie-Mangas+VF/1.html', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + '1/categorie-Mangas+VOST/1.html', 'showMovies')

EMISSIONS_TV = (URL_MAIN + '1/categorie-Emissions/1.html', 'showMovies')

SPECTACLES = (URL_MAIN + '1/categorie-Spectacles/1.html', 'showMovies')


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
        'Mangas',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSpectacles',
        'Spectacles',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuEmissionsTV',
        'Emissions TV',
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
        'Recherche de films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_VIEWS[1],
        'Films SD (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD_DVDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_DVDRIP[1],
        'Films SD DVDRIP & BDRIP (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD_CAM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_CAM[1],
        'Films SD CAM & DVDScr (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_VOSTFR[1],
        'Films SD VOSTFR (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SD_CLASSIQUE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_CLASSIQUE[1],
        'Films SD Classiques (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films HD 720p & 1080p (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films UHD 4K (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films HDLight (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films 3D (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD_VIEWS[1],
        'Films HD (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES_SD[1],
        'Films SD (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES_HD[1],
        'Films HD (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_SAGA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SAGA[1],
        'Films (Sagas)',
        'genres.png',
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
        'Recherche de séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SD_EN_COURS_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SD_EN_COURS_VF[1],
        'Séries SD VF en cours',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', SERIE_SD_EN_COURS_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SD_EN_COURS_VOSTFR[1],
        'Séries SD VOSTFR en cours',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SD_TERMINE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SD_TERMINE_VF[1],
        'Séries SD VF terminées',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', SERIE_SD_TERMINE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SD_TERMINE_VOSTFR[1],
        'Séries SD VOSTFR terminées',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_HD_EN_COURS_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD_EN_COURS_VF[1],
        'Séries HD VF en cours',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', SERIE_HD_EN_COURS_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD_EN_COURS_VOSTFR[1],
        'Séries HD VOSTFR en cours',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_HD_TERMINE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD_TERMINE_VF[1],
        'Séries HD VF terminées',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', SERIE_HD_TERMINE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD_TERMINE_VOSTFR[1],
        'Séries HD VOSTFR terminées',
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
        'Recherche d\'animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Dessins Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Mangas VF (Derniers ajouts)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Mangas VOSTFR (Derniers ajouts)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSpectacles():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MISC[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche de Spectacles',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPECTACLES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPECTACLES[1],
        'Spectacles (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuEmissionsTV():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MISC[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche émissions TV',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', EMISSIONS_TV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        EMISSIONS_TV[1],
        'Dernières émissions TV',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        search_text = Quote(search_text)
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        url = url + search_text
        showSearchResult(url)
        gui.setEndOfDirectory()
        return


def showGenreMoviesSD():
    showGenre("films+dvdrip+et+bdrip/")


def showGenreMoviesHD():
    showGenre("Films+BluRay+720p+et+1080p/")


def showGenre(basePath):
    gui = Gui()

    liste = [['Action', 'Action'], ['Animation', 'Animation'], ['Arts Martiaux', 'Arts%20Martiaux'],
             ['Aventure', 'Aventure'], ['Biographies', 'Biographies'], ['Comédie', 'Comedie'],
             ['Comédie dramatique', 'Comedie+Dramatique'], ['Comédie musicale', 'Comedie+Musicale'],
             ['Divers', 'Divers'], ['Drame', 'Drame'], ['Espionnage', 'Espionnage'], ['Famille', 'Famille'],
             ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'], ['Historique', 'Historiques'],
             ['Horreur', 'Horreur-Epouvante'], ['Péplum', 'Peplum'], ['Policier', 'Policiers'], ['Romance', 'Romance'],
             ['Science fiction', 'Science-Fiction'], ['Thriller', 'Thriller'], ['Western', 'Westerns']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + '1/genre-' + url + '/' + + basePath)
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
    for i in reversed(range(1950, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + '1/annee/?rech_year=' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchResult(search=''):
    util = cUtil()
    gui = Gui()
    input_parameter_handler = InputParameterHandler()

    search_text = search.replace(URL_SEARCH_MOVIES[0], '')
    search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
    search_text = search_text.replace(URL_SEARCH_MISC[0], '')
    search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
    search_text = util.CleanName(search_text)

    loop = 2

    if search:
        SD = HD = 0
        url = search
    else:
        SD = HD = -1
        url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    results = []
    NextPage = []

    while loop:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        html_content = html_content.replace(
            '<span style="background-color: yellow;"><font color="red">', '')
        pattern = '<b><p style="font-size: 18px;"><A href="([^"]+)">(.+?)<\\/A.+?<td align="center">\\s*<img src="([^"]+)".+?<b>Description : (.+?)<br /><br />'
        aResult1 = parser.parse(html_content, pattern)

        if aResult1[0] is False:
            gui.addText(SITE_IDENTIFIER)

        if aResult1[0]:
            results = results + aResult1[1]

            next_page = __checkForNextPage(html_content)
            if next_page:
                n = ' >>>'
                if search:
                    n = ' SD >>>'
                if loop == 2:
                    n = ' HD >>>'
                NextPage.append((n, next_page))

        loop = loop - 1
        if loop == 1:
            HD = len(results)
            if url.find('=video') > 0:
                url = url.replace('=video', '=Films+HD')
            elif url.find('=serie') > 0:
                url = url.replace('=serie', '=seriehd')
            else:
                loop = 0

    if results:
        i = 0
        output_parameter_handler = OutputParameterHandler()
        for entry in results:

            # titre ?
            if i == SD:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR olive]Qualitée SD[/COLOR]')
            if i == HD:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR olive]Qualitée HD[/COLOR]')
            i = i + 1

            qual = 'SD'
            if '-hd/' in entry[0] or 'bluray' in entry[0] or 'hdlight' in entry[0]:
                qual = 'HD'
            if '-3d/' in entry[0]:
                qual = '3D'

            title = str(
                entry[1]).replace(
                ' - Saison',
                ' Saison').replace(
                ' - saison',
                ' Saison')
            title = cUtil().removeHtmlTags(title)

            # Filtre recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            url2 = URL_MAIN + entry[0]

            desc = entry[3]
            desc = re.sub('<[^<]+?>', '', desc)  # retrait des balises html
            thumb = entry[2]

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)

            if '/mangas' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif 'series-' in url or '-Saison' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif '-Sagas' in url:
                gui.addMoviePack(
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

        if not search:
            for n, u in NextPage:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', u)
                sNumPage = re.search('/([0-9]+)/', u).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showSearchResult',
                    'Page ' + sNumPage + ' ' + n,
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

    pattern = '<table style="float:left;padding-left:8px"> *<td> *<div align="left"> *<a href="([^"]+)" onmouseover="Tip\\(\'<b>([^"]+?)</b>.+?Description :</b> <i>([^<]+?)<.+?<img src="([^"]+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            qual = 'SD'
            if '-hd/' in entry[0] or 'bluray' in entry[0] or 'hdlight' in entry[0]:
                qual = 'HD'
            if '-3d/' in entry[0]:
                qual = '3D'

            url2 = URL_MAIN + entry[0]
            title = entry[1].replace(
                ' - Saison',
                ' Saison').replace(
                ' - saison',
                ' Saison')

            desc = entry[2]
            if not isMatrix():
                desc = desc.decode("unicode_escape").encode("latin-1")

            thumb = entry[3]

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if '/mangas' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif 'series-' in url or '-Saison' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif '-Sagas' in url:
                gui.addMoviePack(
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

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('/([0-9]+)/', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<span class="courante">[^<]+</span> <a href="(.+?)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return URL_MAIN + results[1][0]

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # parfois présent, plus sure que de réduire la regex
    html_content = re.sub('</font>', '', html_content)

    # recuperation nom de la release
    if 'elease :' in html_content:
        pattern = 'elease :([^<]+)<'
    else:
        pattern = '<br /> *([^<]+)</p></center>'

    aResult1 = parser.parse(html_content, pattern)
    # VSlog(aResult1)

    if aResult1[0] is True:
        if 'Forced' in aResult1[1][0]:
            aResult1[1][0] = ''

    # cut de la zone des liens
    if 'Lien Premium' in html_content:
        pattern = 'Lien Premium(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if not results[0]:
            return
        html_content = results[1][0]

        if 'Interchangeables' in html_content:
            # cut de restes de liens non premiums
            pattern = '--(.+?)Interchangeables'
            results = parser.parse(html_content, pattern)
            if not results[0]:
                return
            html_content = results[1][0]

    else:
        pattern = '<div id="link">(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if not results[0]:
            return
        html_content = results[1][0]
        html_content = html_content.replace('&nbsp;', '')

    if '-multi' in html_content:
        pattern = 'target="_blank" href="([^"]+)"'
    else:
        pattern = '<b> *([^<]+)</b> </br> <a href="([^"]+)" target="_blank" *><b><font color="#00aeef">Cliquer ici'

    results = parser.parse(html_content, pattern)
    # VSlog(results)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if '-multi' in entry:
                sHostName = 'Liens Multi'
            else:
                # hosters non géré
                if 'nitroflare' in entry[1] or 'turbo' in entry[1] or 'q.gs' in entry[1]:
                    continue
                if 'hitfile' in entry[1] or 'hil.to' in entry[1]:  # hosters non géré
                    continue
                if 'uplooad' in entry[1] or 'rapidgator' in entry[1]:  # hoster non géré
                    continue

                sHostName = entry[0]
                # on récupère le nom du hoster dans l'url
                # Sinon les hosters sont souvent affiché en temps que
                # Free-telechargements
                if 'uptobox' in entry[1]:
                    sHostName = 'UpToBox'
                if 'uploaded' in entry[1]:
                    sHostName = 'Uploaded'
                if '1fichier' in entry[1]:
                    sHostName = '1Fichier'

                sHostName = cUtil().removeHtmlTags(sHostName)

            title = '[COLOR coral]' + sHostName + '[/COLOR]'

            if '-multi' in entry:
                output_parameter_handler.addParameter('site_url', entry)
            else:
                output_parameter_handler.addParameter('site_url', entry[1])

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'Display_protected_link',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # parfois présent, plus sure que de réduire la regex
    html_content = re.sub('</font>', '', html_content)

    parser = Parser()

    # recuperation nom de la release
    pattern = '</span> ([^<]+)</strong> :.'
    aResult1 = parser.parse(html_content, pattern)

    # cut de la zone des liens
    if 'Lien Premium' in html_content:
        pattern = 'Lien Premium *--(.+?)</div>'
    else:
        pattern = '<div id="link">(.+?)</div>'
    results = parser.parse(html_content, pattern)
    html_content = results[1][0]
    html_content = re.sub('<font color="[^"]+">', '', html_content)
    html_content = re.sub('</font>', '', html_content)
    # html_content = re.sub('link.php\?lien\=', '', html_content)

    if '-multi' in html_content:
        pattern = 'target="_blank" href="([^"]+)"'
    else:
        pattern = '<b> *([^<]+)</b> </br> <a href="([^"]+)" target="_blank" *><b><font color="#00aeef">Cliquer ici'

    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        gui.addText(SITE_IDENTIFIER, movie_title + aResult1[1][0])

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if total == 1:
                title = '[COLOR coral]' + 'Liens Premium' + '[/COLOR]'
                output_parameter_handler.addParameter('site_url', entry)
            else:
                title = '[COLOR coral]' + entry[0] + '[/COLOR]'
                output_parameter_handler.addParameter('site_url', entry[1])

            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'Display_protected_link',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def Display_protected_link(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    # Est ce un lien dl-protect ?
    if URL_PROTECT in url:
        if "lien=" in url:
            url = url.split('lien=')[1]
        html_content = DecryptddlProtect(url)

        if html_content:
            # Si redirection
            if html_content.startswith('http'):
                aResult_dlprotect = (True, [html_content])
            else:
                sPattern_dlprotect = 'target=_blank>([^<]+)<'
                aResult_dlprotect = parser.parse(
                    html_content, sPattern_dlprotect)

        else:
            dialog().VSok('Désolé, problème de captcha.')
            aResult_dlprotect = (False, False)
    # Si lien normal
    else:
        if not url.startswith('http'):
            url = 'http://' + url
        aResult_dlprotect = (True, [url])

    if aResult_dlprotect[0]:
        for entry in aResult_dlprotect[1]:
            hoster_url = entry

            title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def DecryptddlProtect(url):
    # VSlog('entering DecryptddlProtect')
    if not url:
        return ''

    # Get host
    tmp = url.split('/')
    host = tmp[0] + '//' + tmp[2] + '/'

    dialogs = dialog()
    # try to get previous cookie
    cookies = GestionCookie().Readcookie('liens_free-telechargement_org')

    request_handler = RequestHandler(url)
    if cookies:
        request_handler.addHeaderEntry('Cookie', cookies)
    html_content = request_handler.request()

    # A partir de la on a les bon cookies pr la protection cloudflare

    # Si ca demande le captcha
    if 'Veuillez recopier le captcha ci-dessus' in html_content:
        if cookies:
            GestionCookie().DeleteCookie('liens_free-telechargement_org')
            request_handler = RequestHandler(url)
            html_content = request_handler.request()

        s = re.findall(
            'src=".\\/([^<>"]+?)" alt="CAPTCHA Image"',
            html_content)
        if host in s[0]:
            image = s[0]
        else:
            image = host + s[0]

        captcha, cookies2 = get_response(image, cookies)
        cookies = cookies + '; ' + cookies2

        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            'Accept-Language',
            'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        request_handler.addHeaderEntry(
            'Accept',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addHeaderEntry('Referer', url)
        request_handler.addParameters('do', 'contact')
        request_handler.addParameters('ct_captcha', captcha)

        html_content = request_handler.request()

        if 'Code de securite incorrect' in html_content:
            dialogs.VSinfo("Mauvais Captcha")
            return 'rate'

        if 'Veuillez recopier le captcha ci-dessus' in html_content:
            dialogs.VSinfo("Rattage")
            return 'rate'

        # si captcha reussi
        # save cookies
        GestionCookie().SaveCookie('liens_free-telechargement_org', cookies)

    return html_content


def get_response(img, cookie):
    # on telecharge l'image
    import xbmcvfs

    dialogs = dialog()

    filename = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"
    # PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
    # filename  = os.path.join(PathCache, 'Captcha.raw')

    # hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', img)
    # host = re.sub(r'https*:\/\/', '', hostComplet)
    url = img

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    # request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry('Cookie', cookie)

    htmlcontent = request_handler.request()

    NewCookie = request_handler.GetCookies()

    downloaded_image = xbmcvfs.File(filename, 'wb')
    # downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

    # on affiche le dialogue
    solution = ''

    if True:
        # nouveau captcha
        try:
            # affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                # """
                # Dialog class for captcha
                # """
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    # image background captcha
                    self.getControl(1).setImage(
                        filename.encode("utf-8"), False)
                    # image petit captcha memory fail
                    self.getControl(2).setImage(
                        filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    # Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        # button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty('captcha', solution)
                        self.close()
                        return

                    elif controlId == 30:
                        # button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        # button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(
                            self.getControl(5000).getLabel(), '', False)
                        kb.doModal()

                        if kb.isConfirmed():
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    # touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogCaptcha.xml', path, 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        # ancien Captcha
        try:
            img = xbmcgui.ControlImage(
                450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            # xbmc.sleep(3000)
            kb = xbmc.Keyboard(
                "", "Tapez les Lettres/chiffres de l'image", False)
            kb.doModal()
            if kb.isConfirmed():
                solution = kb.getText()
                if solution == '':
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution, NewCookie
