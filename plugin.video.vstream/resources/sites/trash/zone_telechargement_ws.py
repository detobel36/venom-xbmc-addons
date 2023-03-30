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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
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
        'showMenuAutres',
        'Autres',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Exclus (Films populaires)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Blu-rays (720p & 1080p)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films (3D)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (x265 & x264)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films (4k)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANIME[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANIME[1],
        'Dessins Animés (Derniers ajouts)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films (BDRIP)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_TS_CAM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TS_CAM[1],
        'Films (TS, CAM, R5, DVDSCR)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VFSTFR[1],
        'Films en francais sous titre francais (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_MKV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MKV[1],
        'Films (dvdrip mkv)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VO[1],
        'Films en Version original (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_INTEGRAL[0])
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
    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_720[1],
        'Séries 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_1080[1],
        'Séries 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VO[1],
        'Séries (VO)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANCIENNE_SERIE[0])
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
    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animes (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_720[1],
        'Animés 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_1080[1],
        'Animés 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_720[1],
        'Animés 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_1080[1],
        'Animés 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', FILM_ANIM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        FILM_ANIM[1],
        'Films d\'animés ',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTEN[0])
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
    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', TV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TV_NEWS[1],
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SPECT_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPECT_NEWS[1],
        'Spectacles',
        'star.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sSearchText = Quote(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText + \
            '&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=0'
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    UrlGenre = input_parameter_handler.getValue('siteUrl')

    liste = [['Action', 'Action'], ['Animation', 'Animation'], ['Arts Martiaux', 'martiaux'], ['Aventure', 'Aventure'],
             ['Biopic', 'Biopic'], ['Comédie Dramatique', 'Dramatique'], ['Comédie Musicale', 'Musical'],
             ['Comédie', 'Comedie'], ['Divers', 'Divers'], ['Documentaires', 'Documentaire'], ['Drame', 'Drame'],
             ['Epouvante Horreur', 'Epouvante'], ['Espionnage', 'Espionnage'], ['Famille', 'Famille'],
             ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'], ['Historique', 'Historique'], ['Musical', 'musicale'],
             ['Péplum', 'Peplum'], ['Policier', 'Policier'], ['Romance', 'Romance'], ['Science Fiction', 'Science'],
             ['Thriller', 'Thriller'], ['Western', 'Western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', UrlGenre.format(sUrl))
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace('index.php', '')
    if sSearch:
        sUrl = sSearch

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+)<.+?<b>([^<]+)<.+?">([^<]+)<'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            title = aEntry[2]
            sQual = aEntry[3]
            sLang = aEntry[4]

            # on vire le tiret des series
            title = title.replace(
                ' - Saison',
                ' Saison').replace(
                'COMPLETE',
                'Complete')
            sMovieTitle = title.split('Saison')[0]

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
            key = title + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            sDisplayTitle = ('%s [%s] %s') % (title, sQual, sLang)

            if not sThumb.startswith('https'):
                sThumb = URL_MAIN + sThumb

            if not sUrl2.startswith('https'):
                sUrl2 = URL_MAIN + sUrl2

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter(
                'sDisplayTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sQual', sQual)

            if 'anime' in sUrl or 'anime' in sUrl2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif 'serie' in sUrl or 'serie' in sUrl2:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', sThumb, '', output_parameter_handler)
            elif DOC_NEWS[0] in sUrl or TV_NEWS[0] in sUrl or SPECT_NEWS[0] in sUrl or CONCERT_NEWS[0] in sUrl:
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif 'collection' in sUrl or 'integrale' in sUrl:
                gui.addMoviePack(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif ' Saison ' in title:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        if 'controller.php' in sUrl:
            sPattern = '<a href="#" class="nav" data-cstart="([^"]+)">Suivant</a></div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', re.sub(
                    'cstart=(\\d+)', 'cstart=' + str(aResult[1][0]), sUrl))
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

        else:
            sNextPage, sPaging = __checkForNextPage(sHtmlContent)
            if sNextPage:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sNextPage)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + sPaging,
                    output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '>([^<]+)</a> *<a href="([^"]+)">Suivant</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        if not sNextPage.startswith('https'):
            sNextPage = URL_MAIN + sNextPage
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showMoviesLinks(input_parameter_handler=False):
    # VSlog('mode film')
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sDisplayTitle = input_parameter_handler.getValue('sDisplayTitle')
    if not sDisplayTitle:   # Si on arrive par un marque-page
        sDisplayTitle = sMovieTitle
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "onaregarde" in sUrl:
        oParser = Parser()
        sPattern = '<a type="submit".+?href="([^"]+)"'
        sUrl = oParser.parse(sHtmlContent, sPattern)[1][0]

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis et de l'année
    desc = ''
    sYear = ''
    try:
        sPattern = '(<u>Date de .+</u>.+(\\d{4}(-| *<))|<u>Critiques.+?</u>).+synopsis.+?>(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            aEntry = aResult[1][0]
            sYear = aEntry[1]
            desc = cUtil().removeHtmlTags(aEntry[3])
    except BaseException:
        pass

    # la qualité courante est le lien en cours ici même
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('sYear', sYear)
    gui.addLink(
        SITE_IDENTIFIER,
        'showHosters',
        sDisplayTitle,
        sThumb,
        desc,
        output_parameter_handler,
        input_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)</b></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            title = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sDisplayTitle', title)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)
            gui.addLink(
                SITE_IDENTIFIER,
                'showMoviesLinks',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    # VSlog('mode serie')
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "onaregarde" in sUrl:
        oParser = Parser()
        sPattern = '<a type="submit".+?href="([^"]+)"'
        sUrl = oParser.parse(sHtmlContent, sPattern)[1][0]

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis
    desc = sMovieTitle   # Ne pas laisser vide sinon un texte automatique faux va être calculé
    try:
        sPattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = cUtil().removeHtmlTags(aResult[1][0][1])
    except BaseException:
        pass

    # on recherche d'abord la qualité courante
    sPattern = 'smallsep.+?Qualité([^<]+)<.+?img src="([^"]+)".+?alt=.+?- Saison ([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # sQual = ''
    # sLang = ''
    if aResult[1] is True:
        aEntry = aResult[1][0]
        sQual = aEntry[0].split('|')[0]
        sLang = aEntry[0].split('|')[1]
        # change pour chaque saison, il faut la rechercher si on navigue entre
        # saisons
        sThumb = aEntry[1]
        title = sMovieTitle + ' S' + aEntry[2]

        sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('desc', desc)
        output_parameter_handler.addParameter('sQual', sQual)
        gui.addSeason(
            SITE_IDENTIFIER,
            'showSeriesHosters',
            sDisplayTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult1[1]:
            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (title, sQual, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sQual', sQual)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    # on regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if aResult2[0] is True:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult2[1]:
            sSaison = aEntry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]

            title = sMovieTitle + ' ' + aEntry[1] + aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                sThumb,
                sMovieTitle,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    # VSlog('showHosters')
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "zt-protect" in sUrl:
        # Dl Protect present aussi a cette étape.
        sHtmlContent = DecryptDlProtecte(sUrl)
    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Si ça ressemble aux liens premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)

    oParser = Parser()

    sPattern = '<div style="font-weight:bold;color:.+?</span>(.+?)</div>|<a class="btnToLink".+?href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                if 'Interchangeables' not in aEntry[0]:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR red]' +
                        aEntry[0] +
                        '[/COLOR]')
            else:
                sDisplayTitle = sMovieTitle

                output_parameter_handler.addParameter('siteUrl', aEntry[1])
                output_parameter_handler.addParameter('baseUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sYear', sYear)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    sDisplayTitle,
                    sThumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    # VSlog('showSeriesHosters')
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    try:
        desc = unicodedata.normalize(
            'NFD', desc).encode(
            'ascii', 'ignore').decode('unicode_escape')
        desc = desc.encode('latin-1')
    except BaseException:
        pass

    if "zt-protect" in sUrl:
        # Dl Protect present aussi a cette étape.
        sHtmlContent = DecryptDlProtecte(sUrl)
    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)

    sPattern = '<div style="font-weight.+?>([^<]+)</div>|<a class="btnToLink".+?href="([^"]+)".+?Episode ([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                if 'Télécharger' in aEntry[0]:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR olive]' +
                        aEntry[0] +
                        '[/COLOR]')
                else:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR red]' +
                        aEntry[0] +
                        '[/COLOR]')
            else:
                sName = 'E' + aEntry[2]
                sName = sName.replace('Télécharger', '')
                sUrl2 = aEntry[1]
                title = sMovieTitle + ' ' + sName

                output_parameter_handler.addParameter('baseUrl', sUrl)
                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def Display_protected_link(input_parameter_handler=False):
    # VSlog('Display_protected_link')
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    # baseUrl = input_parameter_handler.getValue('baseUrl')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    # Est-ce un lien dl-protect ?
    if sUrl:

        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            # Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = 'class="alert alert-primary".+?href="(.+?)"'
                aResult_dlprotecte = oParser.parse(
                    sHtmlContent, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if aResult_dlprotecte[0]:

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry

            title = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                title = sMovieTitle + ' episode ' + episode

            episode += 1

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(title)
                oHoster.setFileName(title)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = Parser()
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = Parser()
    sPattern = '<h3>Saisons.+?galement disponibles.+?</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def CutNonPremiumlinks(sHtmlContent):
    oParser = Parser()
    sPattern = '(?:Lien.+?Premium - 1 lien|Lien.+?Premium)(.+?)</b></font></a></center>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return sHtmlContent


def CutPremiumlinks(sHtmlContent):
    oParser = Parser()
    sPattern = '(?i) par .{1,2}pisode(.+?)$'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return sHtmlContent


def DecryptDlProtecte(url):

    if not url:
        return ''

    oRequestHandler = RequestHandler(url)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    return str(sHtmlContent)
