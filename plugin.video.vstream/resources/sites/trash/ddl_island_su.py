# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Recaptcha
import urllib2
import urllib
import re
import random
from resources.lib.config import GestionCookie
from resources.lib.comaddon import Progress, dialog, xbmc, xbmcgui, VSlog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False


UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'ddl_island_su'
SITE_NAME = '[COLOR violet]DDL-Island[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = 'https://ww3.ddl-island.su/'
URL_DECRYPT = 'http://www.dl-protect.ru'

URL_SEARCH_MOVIES = (
    URL_MAIN +
    'recherche.php?categorie=99&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'recherche.php?categorie=98&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH_ANIMES = (
    URL_MAIN +
    'recherche.php?categorie=5&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH_MANGAS = (
    URL_MAIN +
    'recherche.php?categorie=3&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH_EMISSIONS_TV = (
    URL_MAIN +
    'recherche.php?categorie=17&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH_SPECTACLES = (
    URL_MAIN +
    'recherche.php?categorie=2&rechercher=Rechercher&fastr_type=ddl&find=',
    'showMovies')
URL_SEARCH = (URL_MAIN + 'index.php?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_SD = (
    URL_MAIN +
    'telechargement/films-1.html&order=2',
    'showMovies')  # derniers films en SD
MOVIE_HD = (
    URL_MAIN +
    'telechargement/films-hd-13.html&order=2',
    'showMovies')  # derniers films en HD
MOVIE_3D = (
    URL_MAIN +
    'telechargement/films-3d-21.html&order=2',
    'showMovies')  # derniers films en 3D
MOVIE_SD_VIEWS = (
    URL_MAIN +
    'telechargement/films-1.html&order=3',
    'showMovies')  # derniers films en SD
MOVIE_HD_VIEWS = (
    URL_MAIN +
    'telechargement/films-hd-13.html&order=3',
    'showMovies')  # derniers films en HD
MOVIE_3D_VIEWS = (
    URL_MAIN +
    'telechargement/films-3d-21.html&order=3',
    'showMovies')  # derniers films en 3D
MOVIE_TOP = (URL_MAIN + 'telechargement-top-films',
             'showMovies')  # derniers films en 3D
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')

ANIMES = (URL_MAIN + 'telechargement/dessins-animes-5.html&order=2',
          'showMovies')  # derniers dessins animés

ANIM_ANIMS = (URL_MAIN + 'telechargement/mangas-3.html&order=2',
              'showMovies')  # derniers dessins animés

EMISSIONS_TV = (
    URL_MAIN +
    'telechargement/emissions-tv-17.html&order=2',
    'showMovies')  # dernieres émissions TV

SPECTACLES = (
    URL_MAIN +
    'telechargement/comedies-spectacles-2.html&order=2',
    'showMovies')  # dernieres émissions TV

SERIES_SD = (
    URL_MAIN +
    'telechargement/series-tv-6.html&order=2',
    'showMovies')  # derniers films en SD
SERIES_HD = (
    URL_MAIN +
    'telechargement/series-hd-20.html&order=2',
    'showMovies')  # derniers films en HD
SERIES_SD_VIEWS = (
    URL_MAIN +
    'telechargement/series-tv-6.html&order=3',
    'showMovies')  # derniers films en SD
SERIES_HD_VIEWS = (
    URL_MAIN +
    'telechargement/series-tv-6.html&order=3',
    'showMovies')  # derniers films en HD
SERIES_TOP = (URL_MAIN + 'telechargement-top-series',
              'showMovies')  # derniers films en 3D
SERIES_GENRES_SD = (True, 'showGenreSeriesSD')
SERIES_GENRES_HD = (True, 'showGenreSeriesHD')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuDessinsAnimes',
        'Dessins Animés',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMangas',
        'Mangas',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSpectacles',
        'Spectacles',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuEmissionsTV',
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovies',
        'Recherche de films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD[1],
        'Films SD (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films HD (Derniers ajouts)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films en 3D (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_SD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SD_VIEWS[1],
        'Films SD (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD_VIEWS[1],
        'Films HD (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_3D_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D_VIEWS[1],
        'Films en 3D (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Top du Mois)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES_SD[1],
        'Films SD (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES_HD[1],
        'Films HD (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSeries',
        'Recherche de séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_SD[1],
        'Séries SD (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_HD[1],
        'Séries HD (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_SD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_SD_VIEWS[1],
        'Séries SD (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_HD_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_HD_VIEWS[1],
        'Séries HD (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_TOP[1],
        'Séries (Top du Mois)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_GENRES_SD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_GENRES_SD[1],
        'Séries SD (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIES_GENRES_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_GENRES_HD[1],
        'Séries HD (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuDessinsAnimes():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchAnimes',
        'Recherche de Dessins Animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIMES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIMES[1],
        'Dessins Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMangas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMangas',
        'Recherche de Mangas',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Mangas (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSpectacles():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSpectacles',
        'Recherche de Spectacles',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchEmissionsTV',
        'Recherche d\'émissions TV',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', EMISSIONS_TV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        EMISSIONS_TV[1],
        'Emissions TV (Derniers ajouts)',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchMovies():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_MOVIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSeries():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_SERIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchAnimes():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_ANIMES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMangas():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_MANGAS[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSpectacles():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_SPECTACLES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchEmissionsTV():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_EMISSIONS_TV[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenreMoviesSD():
    showGenres("films-1.html&order=2")


def showGenreMoviesHD():
    showGenres("films-hd-13.html&order=2")


def showGenreSeriesSD():
    showGenres("series-tv-6.html")


def showGenreSeriesHD():
    showGenres("series-hd-20.html")


def showGenres(basePath):
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'telechargement+5/' + basePath])
    liste.append(['Animation', URL_MAIN + 'telechargement+4/' + basePath])
    liste.append(['Arts Martiaux', URL_MAIN + 'telechargement+64/' + basePath])
    liste.append(['Aventure', URL_MAIN + 'telechargement+20/' + basePath])
    liste.append(['Biographie', URL_MAIN + 'telechargement+38/' + basePath])
    liste.append(['Biopic', URL_MAIN + 'telechargement+28/' + basePath])
    liste.append(['Combat', URL_MAIN + 'telechargement+35/' + basePath])
    liste.append(['Comédie', URL_MAIN + 'telechargement+1/' + basePath])
    liste.append(['Comédie dramatique', URL_MAIN +
                 'telechargement+12/' + basePath])
    liste.append(['Comédie musicale', URL_MAIN +
                 'telechargement+33/' + basePath])
    liste.append(['Comédie romantique', URL_MAIN +
                 'telechargement+53/' + basePath])
    liste.append(['Comique', URL_MAIN + 'telechargement+51/' + basePath])
    liste.append(['Court métrage', URL_MAIN + 'telechargement+45/' + basePath])
    liste.append(['Criminalité', URL_MAIN + 'telechargement+40/' + basePath])
    liste.append(['Dessin animé', URL_MAIN + 'telechargement+27/' + basePath])
    liste.append(['Divers', URL_MAIN + 'telechargement+34/' + basePath])
    liste.append(['Divertissement', URL_MAIN +
                 'telechargement+66/' + basePath])
    liste.append(['Documentaire', URL_MAIN + 'telechargement+9/' + basePath])
    liste.append(['Drame', URL_MAIN + 'telechargement+3/' + basePath])
    liste.append(['Epouvante', URL_MAIN + 'telechargement+41/' + basePath])
    liste.append(['Epouvante-horreur', URL_MAIN +
                 'telechargement+17/' + basePath])
    liste.append(['Erotique', URL_MAIN + 'telechargement+24/' + basePath])
    liste.append(['Espionnage', URL_MAIN + 'telechargement+13/' + basePath])
    liste.append(['Famille', URL_MAIN + 'telechargement+31/' + basePath])
    liste.append(['Fantastique', URL_MAIN + 'telechargement+16/' + basePath])
    liste.append(['Football', URL_MAIN + 'telechargement+32/' + basePath])
    liste.append(['Guerre', URL_MAIN + 'telechargement+22/' + basePath])
    liste.append(['Historique', URL_MAIN + 'telechargement+21/' + basePath])
    liste.append(['Horreur', URL_MAIN + 'telechargement+15/' + basePath])
    liste.append(['Humour', URL_MAIN + 'telechargement+44/' + basePath])
    liste.append(['Jeunesse', URL_MAIN + 'telechargement+19/' + basePath])
    liste.append(['Judiciaire', URL_MAIN + 'telechargement+67/' + basePath])
    liste.append(['Karaté', URL_MAIN + 'telechargement+23/' + basePath])
    liste.append(['Manga', URL_MAIN + 'telechargement+58/' + basePath])
    liste.append(['Médical', URL_MAIN + 'telechargement+47/' + basePath])
    liste.append(['Musical', URL_MAIN + 'telechargement+10/' + basePath])
    liste.append(['Mystère', URL_MAIN + 'telechargement+26/' + basePath])
    liste.append(['Péplum', URL_MAIN + 'telechargement+54/' + basePath])
    liste.append(['Policier', URL_MAIN + 'telechargement+2/' + basePath])
    liste.append(['Reportage', URL_MAIN + 'telechargement+57/' + basePath])
    liste.append(['Romance', URL_MAIN + 'telechargement+6/' + basePath])
    liste.append(['Science fiction', URL_MAIN +
                 'telechargement+7/' + basePath])
    liste.append(['Sketches', URL_MAIN + 'telechargement+14/' + basePath])
    liste.append(['Spectacle', URL_MAIN + 'telechargement+39/' + basePath])
    liste.append(['Sport', URL_MAIN + 'telechargement+68/' + basePath])
    liste.append(['Suspense', URL_MAIN + 'telechargement+42/' + basePath])
    liste.append(['Téléréalité', URL_MAIN + 'telechargement+18/' + basePath])
    liste.append(['Thriller', URL_MAIN + 'telechargement+8/' + basePath])
    liste.append(['Western', URL_MAIN + 'telechargement+11/' + basePath])

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


def getIdFromUrl(url):
    pattern = "\\/(telechargemen.+?\\/)"
    parser = Parser()
    results = parser.parse(url, pattern)
    if results[0]:
        return results[1][0]
    return


def showMovies(search=''):
    gui = Gui()
    bGlobal_Search = False
    if search:

        # par defaut
        url = search.replace(' ', '+')

        if URL_SEARCH[0] in search:
            bGlobal_Search = True

        # partie en test
        input_parameter_handler = InputParameterHandler()
        _type = input_parameter_handler.getValue('type')

        if _type:
            if _type == "film":
                url = url.replace(URL_SEARCH[0], URL_SEARCH_MOVIES[0])
            if _type == "serie":
                url = url.replace(URL_SEARCH[0], URL_SEARCH_SERIES[0])
            if _type == "anime":
                url = url.replace(URL_SEARCH[0], URL_SEARCH_ANIMS[0])

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    # print url
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # print html_content
    desc = ''
    qual = ''
    sSaison = ''
    lang = ''
    # sEpisode = ''
    if 'top' in url:
        pattern = '<div class="fiche_top20"><a class="top20" href="([^"]+)"><img src="([^"]+)" title="([^\\|]+)\\|\\|[^\\|]+?\\|\\|([^\\|]+)\\|\\|[^\\|]+?\\|\\|([^"]+)" /></a></div>'
    elif 'series' in url:
        pattern = '<div class="fiche_listing"><a href="([^"]+)"><img src="([^"]+)" alt="T.+?charger([^"]+)"[^\\|]+?\\| *Qualit&eacute; : ([^<]+)<br /><br />([^<]+)<br /><br />'
    else:
        pattern = '<div class="fiche_listing"><a href="([^"]+)"><img src="([^"]+)" alt="T.+?charger([^"]+)"[^\\|]+?".+?Cat&eacute;gorie :([^<]+)<br /><br />([^<]+)<br /><br />'

    parser = Parser()
    results = parser.parse(html_content, pattern)
    # print results

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
            if '-films-' in url2 or '-series-' in url2:
                qual = 'SD'
                if '-hd-' in entry[0]:
                    qual = 'HD'
                if '-3d-' in entry[0]:
                    qual = '3D'
            else:
                qual = entry[3].replace('&eacute;', 'é')
            desc = entry[4].replace(
                '&rsquo;',
                '\'').replace(
                '&ldquo;',
                '"').replace(
                '&rdquo;',
                '"').replace(
                '&hellip;',
                '...')
            title = entry[2]
            # print url2
            thumb = entry[1]
            # Reformatage display_title
            sSaison = ''
            lang = ''
            # sEpisode = ''
            title2 = title.split(" - ")
            title = title2[0]
            if 'top' in url:
                title = ' ' + title2[0]
            # on vire le titre pour rechercher saison dans title2
            del title2[0]
            a = filter(lambda x: 'Saison' in x, title2)
            if a:
                sSaison = a[0]
                sSaison = sSaison.replace('Saison ', 'S')
            if 'VOSTFR' in title2:
                lang = 'VOSTFR'

            display_title = ('%s %s [%s] (%s)') % (
                sSaison, title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if 'series' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
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
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    # tPassage en mode vignette sauf en cas de recherche globale
    # if not bGlobal_Search:
        # xbmc.executebuiltin('Container.SetViewMode(500)')

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    parser = Parser()
    pattern = '<div class="page">.+?</div></td><td align="center"><a href="([^"]+)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        # print results
        if 'recherche.php' in results[1][0]:
            return URL_MAIN + results[1][0]
        else:
            videoId = getIdFromUrl(url)
            return URL_MAIN + videoId + results[1][0]

    return False


def showMoviesReleases():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    url = input_parameter_handler.getValue('site_url')
    url = url.replace('.html', '')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<option value="([^"]+)"  id="([^"]+)"'
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

            if 'rapidgator' not in entry[1] and 'turbobit' not in entry[
                    1] and 'uploaded' not in entry[1] and 'uptobox' not in entry[1]:

                title = entry[1]
                title = title.decode("iso-8859-1", 'ignore')
                title = title.encode("utf-8", 'ignore')

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

            progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # fh = open('c:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    parser = Parser()
    pattern = "<li><a[^<>]+Saison[^<>]+?href='([^']+)'>([^<>]+)<\\/a>(?:&nbsp;<img src=.+?title=(.+?) width|)"
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

            url = entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSeriesReleases():
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    url = input_parameter_handler.getValue('site_url')
    url = url.replace('.html', '')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    gui = Gui()

    parser = Parser()
    # cut de la zone des releases
    pattern = 'Episode :</span>(.+?)>Hébergeur :'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        pattern = 'Release :</span>(.+?)>Hébergeur :'
        results = parser.parse(html_content, pattern)
    html_content = results[1][0]

    pattern = '<option value="([^"]+)"  id="([^"]+)"'
    results = parser.parse(html_content, pattern)
    # print results

    # Affichage du menu
    gui.addText(SITE_IDENTIFIER, movie_title)
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Episodes disponibles:[/COLOR]')

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = '[COLOR skyblue]' + entry[1] + '[/COLOR]'
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[0])
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    url = url.replace('.html', '')

    # print url
    url = url.replace(' & ', '+%26+').replace(' ', '+')
    # VSlog(url)
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<span class=\'providers.+?\' title=\'([^\']+)\'>.+?<a href=\'([^\']+)\' target=\'_blank\' data-title="([^"]+)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            host = entry[0]
            url = entry[1]
            title = entry[2].replace('.mkv', '')
            title = ('%s [COLOR coral]%s[/COLOR]') % (title, host)
            if title.startswith('Telecharger '):
                title = title.replace('Telecharger ', '')

            # test si le host est supporte par vstream.
            hoster = HosterGui().checkHoster(host.lower())
            if host == 'Revivelink':
                hoster = True

            if (hoster):
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    title,
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def Display_protected_link():
    # VSlog('Display_protected_link')
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    # Ne marche pas
    if (False):
        code = {
            '123455600123455602123455610123455615': 'http://uptobox.com/',
            '1234556001234556071234556111234556153': 'http://turbobit.net/',
            '123455600123455605123455615': 'http://ul.to/',
            '123455600123455608123455610123455615': 'http://nitroflare.com/',
            '123455601123455603123455610123455615123455617': 'https://1fichier.com/?',
            '123455600123455606123455611123455615': 'http://rapidgator.net/'}

        for k in code:
            match = re.search(k + '(.+)$', url)
            if match:
                hoster_url = code[k] + match.group(1)
                hoster_url = hoster_url.replace('123455615', '/')
                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)
                gui.setEndOfDirectory()
                return

    # Est ce un lien dl-protect ?
    if URL_DECRYPT in url:
        html_content = DecryptDlProtecte(url)

        if html_content:
            # Si redirection
            if html_content.startswith('http'):
                aResult_dlprotecte = (True, [html_content])
            else:
                sPattern_dlprotecte = '<b>Lien :</b></td><td><a href="(.+?)">'
                aResult_dlprotecte = parser.parse(
                    html_content, sPattern_dlprotecte)

        else:
            oDialog = dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not url.startswith('http'):
            url = 'http://' + url
        aResult_dlprotecte = (True, [url])

    # print aResult_dlprotecte

    if (aResult_dlprotecte[0]):

        episode = 1

        for entry in aResult_dlprotecte[1]:
            hoster_url = entry
            # print hoster_url

            title = movie_title
            if len(aResult_dlprotecte[1]) > 1:
                title = movie_title + ' episode ' + episode

            episode += 1

            if 'stream' in hoster_url:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', hoster_url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showStreamingHosters',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def DecryptDlProtecte(url):

    VSlog('DecryptDlProtecte : ' + url)
    dialogs = dialog()

    if not (url):
        return ''

    # url2 = 'https://www.dl-protecte.org/php/Qaptcha.jquery.php'
    # url2 = 'https://www.protect-zt.com/php/Qaptcha.jquery.php'
    url2 = 'https://' + url.split('/')[2] + '/php/Qaptcha.jquery.php'

    # VSlog(url2)

    # Make random key
    s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@"
    RandomKey = ''.join(random.choice(s) for i in range(32))

    request_handler = RequestHandler(url2)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('Host', 'www.dl-protect.ru')
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Accept', 'application/json, text/javascript, */*; q=0.01')
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    request_handler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    request_handler.addParameters('action', 'qaptcha')
    request_handler.addParameters('qaptcha_key', RandomKey)

    html_content = request_handler.request()

    cookies = request_handler.GetCookies()
    GestionCookie().SaveCookie('dl_protect.ru', cookies)
    # VSlog( 'result'  + html_content)

    if '"error":false' not in html_content:
        VSlog('Captcha rate')
        VSlog(html_content)
        return

    # tempo pas necessaire
    # Gui().showInfo("Patientez", 'Décodage en cours', 2)
    # xbmc.sleep(1000)

    # Ancienne methode avec POST
    # query_args = ( ( 'YnJYHKk4xYUUu4uWQdxxuH@JEJ2yrmJS', '' ) , ('submit', 'Valider' ) )
    # data = urllib.urlencode(query_args)

    # Nouvelle methode avec multipart
    # multipart_form_data = { RandomKey : '', 'submit' : 'Valider' }

    import string
    _BOUNDARY_CHARS = string.digits + string.ascii_letters
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))

    multipart_form_data = {RandomKey: '', 'submit': 'Valider'}
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)
    # VSlog( 'header 2'  + str(headersMulti))
    # VSlog( 'data 2'  + str(data))

    # 2 eme requete pour avoir le lien
    cookies = GestionCookie().Readcookie('dl_protect.ru')
    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('Host', 'www.dl-protect.ru')
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request_handler.addHeaderEntry(
        'Content-Length',
        headersMulti['Content-Length'])
    request_handler.addHeaderEntry(
        'Content-Type', headersMulti['Content-Type'])
    request_handler.addHeaderEntry('Cookie', cookies)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    request_handler.addParametersLine(data)

    html_content = request_handler.request()

    # fh = open('d:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    return html_content

# ******************************************************************************
# from
# http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/


"""Encode multipart form data to upload files via POST."""


def encode_multipart(fields, files, boundary=None):
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
    import random
    import string

    _BOUNDARY_CHARS = string.digits + string.ascii_letters

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            value,
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(
                filename)[0] or 'application/octet-stream'
        lines.extend(
            ('--{0}'.format(boundary),
             'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                escape_quote(name),
                escape_quote(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                value['content'],
             ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)
