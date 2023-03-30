# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import json
import re

from resources.lib.comaddon import addon, dialog, Progress, SiteManager, VSlog
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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMangas',
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuAutre',
        'Autres',
        'tv.png',
        output_parameter_handler)

    if not addon().getSetting('hoster_alldebrid_token'):
        output_parameter_handler.addParameter('siteUrl', 'http://venom/')
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Films)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS2021[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS2021[1],
        'Nouveauté 2021 HD',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HD1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD1080[1],
        'Bluray 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Bluray 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_720[1],
        'Bluray 720P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_1080X265[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_1080X265[1],
        'Bluray 1080P H265/HEVC',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_BLURAYVOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAYVOSTFR[1],
        'Bluray VOSTFR',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Bluray 3D',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_FULL1080P[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FULL1080P[1],
        'REMUX 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_FULL4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FULL4K[1],
        'Bluray 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_REMUX4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_REMUX4K[1],
        'Remux 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_WEBRIP4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_WEBRIP4K[1],
        'Webrip 4K',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIGHT720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHT720[1],
        'HD light 720P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIGHT1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHT1080[1],
        'HD light 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIGHTBDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIGHTBDRIP[1],
        'HD light BDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films BDRIP/DVDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_OLDDVD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_OLDDVD[1],
        'Ancien DVDRIP',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_FILMO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FILMO[1],
        'Filmographie',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_CLASSIQUE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_CLASSIQUE_HD[1],
        'Films Classique HD',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_CLASSIQUE_SD[0])
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Séries)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD[1],
        'Séries 1080p VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries 1080p VOSTFR',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_720VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_720VF[1],
        'Séries 720p VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_720VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_720VO[1],
        'Séries 720p VOSTFR',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_4K[1],
        'Séries 4K H265/HEVC',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_MULTI[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MULTI[1],
        'Séries multilangue',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SDVF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SDVF[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SDVO[0])
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Animes)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animes (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_FILM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_FILM[1],
        "Film d'animation japonais (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        "Animés VOSTFR (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        "Animés VF (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MULTI[0])
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Autres)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    output_parameter_handler.addParameter('misc', True)
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        "Documentaire (Derniers ajouts)",
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SPECTACLE_NEWS[0])
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
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl += sSearchText
        showMovies(sUrl)
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
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
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
            'siteUrl', URL_MAIN + 'films/annee-' + Year)
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
            'siteUrl', URL_MAIN + 'series/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    nextPageSearch = input_parameter_handler.getValue('nextPageSearch')
    siteUrl = input_parameter_handler.getValue('siteUrl')
    sMisc = input_parameter_handler.getValue('misc')  # Autre contenu

    if nextPageSearch:
        sSearch = siteUrl

    sCat = None
    if sSearch:
        siteUrl = sSearch

        if nextPageSearch:
            sSearch += '&search_start=' + nextPageSearch
        oRequestHandler = RequestHandler(siteUrl)
        sHtmlContent = oRequestHandler.request()

        sHtmlContent = oParser.abParse(
            sHtmlContent, 'de la recherche', 'À propos')

        sCat = int(re.search('speedsearch=(\\d)', sSearch).group(1))
        sSearch = re.search('story=(.+?)($|&)', sSearch).group(1)
        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch)
    else:
        oRequestHandler = RequestHandler(siteUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'class="top-last thumbnails" href="([^"]+)".+?"img-post" src="([^"]+).+?alt="([^"]+)'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # on enleve les softwares
            if 'PC' in aEntry[2]:  # for the search
                continue

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if ' - ' in aEntry[2]:
                title = aEntry[2].split(' - ')[0]
                sQual = aEntry[2].split(' - ')[1]
                sQual = sQual.replace(
                    'Avec TRUEFRENCH',
                    '').replace(
                    'TRUEFRENCH',
                    '').replace(
                    'FRENCH ',
                    '')

                if 'Saison' in sQual:  # Pour les séries et animes
                    # * et non pas + car parfois "Saison integrale" pas de chiffre
                    saison = re.search('(Saison [0-9]*)', sQual).group(1)
                    title = title + ' ' + saison
                    sQual = re.sub('Saison [0-9]+ ', '', sQual)

                if '(E' in aEntry[2]:
                    res = re.search('\\(E([0-9]+ .+? [0-9]+)\\)', aEntry[2])
                    try:
                        title = title + ' E' + \
                            res.group(1).replace('Ã', ' - ').replace('à', ' - ').split('[')[0]
                    except BaseException:
                        pass

            else:
                # .replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')
                title = aEntry[2]
                sQual = ''

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            key = title + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, title):
                    continue

            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sQual', sQual)

            if sCat == 3 or sMisc:
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif sCat == 1 or '/films' in siteUrl or '/manga-films/' in siteUrl:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif sCat == 4 or '/mangas/' in siteUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = 'name="nextlink" id="nextlink" onclick="javascript:list_submit\\(([0-9]+)\\); return\\(false\\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', siteUrl)
                output_parameter_handler.addParameter('misc', sMisc)
                output_parameter_handler.addParameter(
                    'nextPageSearch', aResult[1][0])
                sNumPage = re.search('([0-9]+)', aResult[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + sNumPage,
                    output_parameter_handler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sNextPage)
                output_parameter_handler.addParameter('misc', sMisc)
                sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + sNumPage,
                    output_parameter_handler)

    if nextPageSearch:
        gui.setEndOfDirectory()

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href="([^"]+)">Suivant &.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showMoviesLinks(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = cUtil().removeHtmlTags(aResult[1][0])
    except BaseException:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    if aResult[1]:
        sMovieTitle = aResult[1][0][1]
        sQual = aResult[1][0][2].replace('"', '')

    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    sDisplayTitle = ('%s (%s)') % (sMovieTitle, sQual)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addLink(
        SITE_IDENTIFIER,
        'showLinks',
        sDisplayTitle,
        sThumb,
        desc,
        output_parameter_handler,
        input_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a class="btn-other" href="([^<]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            title = ('%s [%s]') % (sMovieTitle, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sDisplayTitle', title)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = cUtil().removeHtmlTags(aResult[1][0])

    except BaseException:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)(VOSTFR|VF)*.+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)
    if aResult[1]:
        sMovieTitle = aResult[1][0][1]

    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    sPattern = '<meta property="og:title" content=".+? - (.+?)(VOSTFR|VF)*/>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    sQual = ''
    title = sMovieTitle
    if aResult[0]:
        sQual = aResult[1][0][0].replace('"', '')
        if 'Saison' in sQual:  # N° de saison dans la qualite
            # * et non pas + car parfois "Saison integrale" pas de chiffre
            saison = re.search('(Saison [0-9]*)', sQual).group(1)
            sQual = re.sub('Saison [0-9]+ ', '', sQual)
            title = sMovieTitle + ' ' + saison

    sDisplayTitle = ('%s (%s)') % (title, sQual)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addSeason(
        SITE_IDENTIFIER,
        'showLinks',
        sDisplayTitle,
        '',
        sThumb,
        desc,
        output_parameter_handler)

    sHtmlContent1 = cutQual(sHtmlContent)
    sPattern1 = '<a class="btn-other" href="([^"]+)">([^<]+)</a>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult1[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showLinks',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    sHtmlContent2 = cutSais(sHtmlContent)
    sPattern2 = '<a class="btn-other" href="([^"]+)">([^<]+)<'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    if aResult2[0] is True:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult2[1]:

            sUrl = aEntry[0]
            title = sMovieTitle + ' ' + aEntry[1].replace('Saison ', 'S')

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Detection de la taille des fichier pour separer les fichier premium des
    # parties en .rar
    if 'saison' not in sUrl:
        fileSize = re.findall(
            '<strong>Taille</strong><span style="float: right;">([^<]+)</span></td>',
            sHtmlContent)
        if 'et' in str(fileSize[0]):
            taille = str(fileSize[:-7])
        else:
            taille = str(fileSize[0])

        if ' Go' in taille:
            size, unite = taille.split(' ')
            if float(size) > 4.85:
                if "1 Lien" in sHtmlContent:
                    VSlog('1 Lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<div class="prez_2">1 Lien Uptobox</div>\\s*.+?>\\s*.+?<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>.+?\\s*<div class="showNFO"'
                else:
                    VSlog('Pas lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)* Premi*um</strong>'
            else:
                sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
        else:
            sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
    else:
        sPattern = '<div class="prez_7">([^<]+)</div>|<a title=".+?" href="([^"]+)" target="_blank"><strong class="hebergeur">([^<]+)</strong>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Il n'existe que des fichiers en parties, non fonctionnel
    if (aResult[0] is False) and float(size) > 4.85:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        if 'saison' in sUrl:
            aResult[1].insert(0, ('Episode 1', '', ''))

        ep = ""
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                ep = aEntry[0]
            else:
                sUrl2 = aEntry[1]

                if 'saison' in sUrl:
                    title = sMovieTitle + ' ' + ep
                else:
                    title = sMovieTitle

                if 'saison' in sUrl:
                    sDisplayTitle = (
                        '%s [COLOR coral]%s[/COLOR]') % (title, aEntry[2])
                else:
                    sDisplayTitle = (
                        '%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, str(aEntry[2]))

                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)

                if 'saison' in sUrl:
                    gui.addEpisode(
                        SITE_IDENTIFIER,
                        'showHosters',
                        sDisplayTitle,
                        '',
                        sThumb,
                        desc,
                        output_parameter_handler)
                else:
                    gui.addMovie(
                        SITE_IDENTIFIER,
                        'showHosters',
                        sDisplayTitle,
                        '',
                        sThumb,
                        desc,
                        output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    Token_Alldebrid = addon().getSetting('hoster_alldebrid_token')
    if Token_Alldebrid != "":
        sUrl_Bypass = "https://api.alldebrid.com/v4/link/redirector?agent=service&version=1.0-&apikey="
        sUrl_Bypass += Token_Alldebrid + "&link=" + sUrl

        oRequestHandler = RequestHandler(sUrl_Bypass)
        sHtmlContent = json.loads(oRequestHandler.request())

        HostURL = sHtmlContent["data"]["links"]
        for sHosterUrl in HostURL:

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        from resources.lib import librecaptcha
        test = librecaptcha.get_token(
            api_key="6LeH9lwUAAAAAGgg9ZVf7yOm0zb0LlcSai8t8-2o",
            site_url=sUrl,
            user_agent=UA,
            gui=False,
            debug=False)

        if test is None:
            gui.addText(
                SITE_IDENTIFIER,
                '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

        else:
            # N'affiche pas directement le liens car sinon Kodi crash.
            sDisplayTitle = "Recaptcha passé avec succès, cliquez pour afficher les liens"
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('Token', test)
            gui.addLink(
                SITE_IDENTIFIER,
                'getHost',
                sDisplayTitle,
                sThumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def getHost(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    test = input_parameter_handler.getValue('Token')

    data = 'g-recaptcha-response=' + test + '&submit_captcha=1'
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry(
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div><span class="lien"><a target="_blank" href="(.+?)">'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def cutQual(sHtmlContent):
    oParser = Parser()
    sPattern = '<span class="other-qualities">&Eacute;galement disponible en :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def cutSais(sHtmlContent):
    oParser = Parser()
    sPattern = '<span class="other-qualities">Autres saisons :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
