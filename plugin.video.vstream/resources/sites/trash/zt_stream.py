# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress
from resources.lib.util import Quote, cUtil
return false


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'zt_stream'
SITE_NAME = '[COLOR violet]ZT-Stream[/COLOR]'
SITE_DESC = 'Zone Telechargement en Streaming'

URL_MAIN = 'https://www.zone-telechargement.stream/'

URL_SEARCH = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&q=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&catid=0&categorie%5B%5D=2&q=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'engine/ajax/controller.php?mod=filter&catid=0&categorie%5B%5D=15&q=',
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
    'engine/ajax/controller.php?mod=filter&catid=0&q=&genre%5B%5D={}&note=0&categorie%5B%5D=2&art=0&AiffchageMode=0&inputTirePar=0&cstart=1',
    'showGenre')
MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies')  # dessins animes
MOVIE_BDRIP = (URL_MAIN + 'film-dvdrip-bdrip/', 'showMovies')
MOVIE_TS_CAM = (URL_MAIN + 'tscam-films-2020/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'film-vfstfr/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'film-mkv/', 'showMovies')
MOVIE_VO = (URL_MAIN + 'films-vo/', 'showMovies')
MOVIE_INTEGRAL = (URL_MAIN + 'collections-films-integrale/', 'showMovies')

SERIE_SERIES = ('http://', 'showMenuSeries')
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

SPORT_SPORTS = (URL_MAIN + 'sport/', 'showMovies')  # sports
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
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMangas',
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Exclus (Films populaires)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Blu-rays (720p & 1080p)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films (3D)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (x265 & x264)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films (4k)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANIME[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANIME[1],
        'Dessins Animés (Derniers ajouts)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films (BDRIP)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_TS_CAM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TS_CAM[1],
        'Films (TS , CAM, R5 ,DVDSCR)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VFSTFR[1],
        'Films en Francais sous titre Francais (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MKV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MKV[1],
        'Films (dvdrip mkv)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VO[1],
        'Films en Version original (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # Un seul film est proposé dans les coffrets
    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('siteUrl', MOVIE_INTEGRAL[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_INTEGRAL[1], 'Integral de films (Derniers ajouts)', 'news.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_720[1],
        'Séries 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_1080[1],
        'Séries 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VO[1],
        'Séries (VO)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANCIENNE_SERIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANCIENNE_SERIE[1],
        'Ancienne series (Derniers)',
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_720[1],
        'Animes 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_1080[1],
        'Animes 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animes (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_720[1],
        'Animes 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_1080[1],
        'Animes 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', FILM_ANIM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        FILM_ANIM[1],
        'Films d\'animes ',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTEN[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTEN[1],
        'Animes (VOSTEN)',
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', TV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TV_NEWS[1],
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    if (sSearchText):
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    UrlGenre = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', 'Action'])
    liste.append(['Animation', 'Animation'])
    liste.append(['Arts Martiaux', 'martiaux'])
    liste.append(['Aventure', 'Aventure'])
    liste.append(['Biopic', 'Biopic'])
    liste.append(['Comédie Dramatique', 'Dramatique'])
    liste.append(['Comédie Musicale', 'Musical'])
    liste.append(['Comédie', 'Comedie'])
    liste.append(['Divers', 'Divers'])
    liste.append(['Documentaires', 'Documentaire'])
    liste.append(['Drame', 'Drame'])
    liste.append(['Epouvante Horreur', 'Epouvante'])
    liste.append(['Espionnage', 'Espionnage'])
    liste.append(['Famille', 'Famille'])
    liste.append(['Fantastique', 'Fantastique'])
    liste.append(['Guerre', 'Guerre'])
    liste.append(['Historique', 'Historique'])
    liste.append(['Musical', 'musicale'])
    liste.append(['Péplum', 'Peplum'])
    liste.append(['Policier', 'Policier'])
    liste.append(['Romance', 'Romance'])
    liste.append(['Science Fiction', 'Science'])
    liste.append(['Thriller', 'Thriller'])
    liste.append(['Western', 'Western'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
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
    oParser = Parser()

    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+).+?class=.+?<b>([^<]+)</span.+?">([^<]+)</span'

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()  # filtrer les titres similaires

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = aEntry[2]
            sUrl2 = aEntry[1]
            sThumb = aEntry[0]
            sQual = aEntry[3]
            sLang = aEntry[4]

            # on vire le tiret des series
            title = title.replace(
                ' - Saison',
                ' Saison').replace(
                'COMPLETE',
                'Complete')
            if not '[Complete]' in title:
                title = title.replace('COMPLETE', '[Complete]')

            # nettoyage du titre
            sDisplayTitle = title.replace('Complete', 'Complète')
            title = re.sub('\\[\\w+]', '', title)

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            key = title + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            sDisplayTitle = ('%s [%s] %s') % (title, sQual, sLang)

            if not sThumb.startswith('https'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not sUrl2.startswith('https'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter(
                'sDisplayTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if 'anime' in sUrl or 'anime' in sUrl2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif 'serie' in sUrl or 'serie' in sUrl2 or '-saison-' in sUrl2:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', sThumb, '', output_parameter_handler)
            elif 'collection' in sUrl or 'integrale' in sUrl:
                gui.addMoviePack(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
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

        if sSearch:  # une seule page de résultats
            return

        if 'controller.php' in sUrl:  # par genre
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
                    '[COLOR teal]Page ' +
                    number +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage):
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sNextPage)
                number = re.search('/page/([0-9]+)', sNextPage).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    '[COLOR teal]Page ' +
                    number +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'href="([^"]+)">Suivant</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        nextPage = aResult[1][0]
        if not nextPage.startswith('https'):
            nextPage = URL_MAIN[:-1] + nextPage
        return nextPage
    return False


def showMoviesLinks(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sDisplayTitle = input_parameter_handler.getValue('sDisplayTitle')
    if not sDisplayTitle:  # Si on arrive par un marque-page
        sDisplayTitle = sMovieTitle
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis et de l'année
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

    # la qualité courante est le lien en cours ici-même
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
        output_parameter_handler)

    # On regarde si dispo dans d'autres qualités
    sPattern = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            title = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sDisplayTitle', title)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis
    # Ne pas laisser vide sinon un texte faux venant du cache va etre utilisé
    desc = sMovieTitle
    try:
        sPattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = cUtil().removeHtmlTags(aResult[1][0][1])
    except BaseException:
        pass

    # On recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?) [|] (.+?)<.+?img src="(([^"]+))"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    sLang = ''
    if (aResult[1]):
        aEntry = aResult[1][0]
        sQual = aEntry[0]
        sLang = aEntry[1]
        # Change pour chaque saison, il faut la rechercher si on navigue entre
        # saisons
        sThumb = aEntry[2]
    sDisplayTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addTV(
        SITE_IDENTIFIER,
        'showSerieEpisodes',
        sDisplayTitle,
        '',
        sThumb,
        desc,
        output_parameter_handler)

    # On regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if (aResult1[0]):
        for aEntry in aResult1[1]:

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSerieEpisodes',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    # On regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if (aResult2[0]):
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        for aEntry in aResult2[1]:

            sSaison = aEntry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sMovieTitle = aEntry[1] + aEntry[2]
            title = '[COLOR skyblue]' + sMovieTitle + '[/COLOR]'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                sThumb,
                sMovieTitle,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    # '>Regarder' à la fin permet de ne pas prendre les liens en plusieurs parties
    sPattern = 'class="btnToLink" target="_blank" href="([^"]+)">Regarder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        # Un seul lien, on va directement chercher le hoster
        sUrl = aResult[1][0]
        sHosterUrl = get_protected_link(sUrl)
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


def showSerieEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'class="btnToLink" target="_blank" href="([^"]+)">Episode (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            numEpisode = aEntry[1]

            sDisplayTitle = 'Episode %s - %s' % (numEpisode, sMovieTitle)
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter(
                'sDisplayTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                sDisplayTitle,
                '',
                sThumb,
                sMovieTitle,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sDisplayTitle = input_parameter_handler.getValue('sDisplayTitle')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sHosterUrl = get_protected_link(sUrl)
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)
    gui.setEndOfDirectory()


def get_protected_link(sUrl):
    if not sUrl:
        return ''

    oParser = Parser()

    sHtmlContent = DecryptDlProtecte(sUrl)
    if sHtmlContent:

        # Si redirection
        if sHtmlContent.startswith('http'):
            return sHtmlContent

        sPattern_dlprotecte = '<iframe.+?src="([^"]+)"'
        aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)
        if aResult_dlprotecte[0]:
            return aResult_dlprotecte[1][0]


def CutQual(sHtmlContent):
    oParser = Parser()
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = Parser()
    sPattern = '<h3>Saisons.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''


def DecryptDlProtecte(url):

    if not (url):
        return ''

    oRequestHandler = RequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'form action="([^"]+).+?type="hidden" name="_token" value="([^"]+).+?input type="hidden" value="([^"]+)'
    result = oParser.parse(sHtmlContent, sPattern)

    if (result[0]):
        restUrl = str(result[1][0][0])
        token = str(result[1][0][1])
        # urlData = str(result[1][0][2])

    else:
        sPattern = '<(.+?)action="([^"]+)" method="([^"]+).+?hidden".+?value="([^"]+)'
        result = oParser.parse(sHtmlContent, sPattern)

        if (result[0]):
            if "<!-----" not in (str(result[1][0][0])):
                restUrl = str(result[1][0][0])
                method = str(result[1][0][1])
                token = str(result[1][0][2])
            else:
                restUrl = str(result[1][1][1]).replace("}", '%7D')
                method = str(result[1][1][2])
                token = str(result[1][1][3])

            if restUrl.startswith('/'):
                restUrl = 'https://' + url.split('/')[2] + restUrl

    oRequestHandler = RequestHandler(restUrl)
    if method == "post":
        oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters("_token", token)
    sHtmlContent = oRequestHandler.request()

    return sHtmlContent
