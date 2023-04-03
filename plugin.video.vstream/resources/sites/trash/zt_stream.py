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
        'showMenuMangas',
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Exclus (Films populaires)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Blu-rays (720p & 1080p)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_3D[1],
        'Films (3D)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (x265 & x264)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_4K[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_4K[1],
        'Films (4k)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_ANIME[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANIME[1],
        'Dessins Animés (Derniers ajouts)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BDRIP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIP[1],
        'Films (BDRIP)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_TS_CAM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TS_CAM[1],
        'Films (TS , CAM, R5 ,DVDSCR)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VFSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VFSTFR[1],
        'Films en Francais sous titre Francais (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MKV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MKV[1],
        'Films (dvdrip mkv)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VO[1],
        'Films en Version original (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # Un seul film est proposé dans les coffrets
    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', MOVIE_INTEGRAL[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_INTEGRAL[1], 'Integral de films (Derniers ajouts)', 'news.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_720[1],
        'Séries 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS_1080[1],
        'Séries 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VO[1],
        'Séries (VO)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANCIENNE_SERIE[0])
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
    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animes (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VF_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_720[1],
        'Animes 720p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VF_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VF_1080[1],
        'Animes 1080p (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animes (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_720[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_720[1],
        'Animes 720p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS_1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS_1080[1],
        'Animes 1080p (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', FILM_ANIM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        FILM_ANIM[1],
        'Films d\'animes ',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTEN[0])
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
    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', TV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TV_NEWS[1],
        'Emissions TV',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    if (search_text):
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        url = url + Quote(search_text)
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    UrlGenre = input_parameter_handler.getValue('site_url')

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

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
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
    parser = Parser()

    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url.replace('https', 'http'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    pattern = 'class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+).+?class=.+?<b>([^<]+)</span.+?">([^<]+)</span'

    results = parser.parse(html_content, pattern)

    titles = set()  # filtrer les titres similaires

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = entry[2]
            url2 = entry[1]
            thumb = entry[0]
            qual = entry[3]
            lang = entry[4]

            # on vire le tiret des series
            title = title.replace(
                ' - Saison',
                ' Saison').replace(
                'COMPLETE',
                'Complete')
            if not '[Complete]' in title:
                title = title.replace('COMPLETE', '[Complete]')

            # nettoyage du titre
            display_title = title.replace('Complete', 'Complète')
            title = re.sub('\\[\\w+]', '', title)

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au
            # moment du choix de la qualité
            key = title + "-" + thumb
            if key in titles:
                continue
            titles.add(key)

            display_title = ('%s [%s] %s') % (title, qual, lang)

            if not thumb.startswith('https'):
                thumb = URL_MAIN[:-1] + thumb

            if not url2.startswith('https'):
                url2 = URL_MAIN[:-1] + url2

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter(
                'display_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)

            if 'anime' in url or 'anime' in url2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif 'serie' in url or 'serie' in url2 or '-saison-' in url2:
                gui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', title,
                          '', thumb, '', output_parameter_handler)
            elif 'collection' in url or 'integrale' in url:
                gui.addMoviePack(
                    SITE_IDENTIFIER,
                    'showMoviesLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
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

        if search:  # une seule page de résultats
            return

        if 'controller.php' in url:  # par genre
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
                    '[COLOR teal]Page ' +
                    number +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

        else:
            next_page = __checkForNextPage(html_content)
            if (next_page):
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', next_page)
                number = re.search('/page/([0-9]+)', next_page).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    '[COLOR teal]Page ' +
                    number +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'href="([^"]+)">Suivant</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page_data = results[1][0]
        if not next_page_data.startswith('https'):
            next_page_data = URL_MAIN[:-1] + next_page_data
        return next_page_data
    return False


def showMoviesLinks(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    display_title = input_parameter_handler.getValue('display_title')
    if not display_title:  # Si on arrive par un marque-page
        display_title = movie_title
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url.replace('https', 'http'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis et de l'année
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

    # la qualité courante est le lien en cours ici-même
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
        output_parameter_handler)

    # On regarde si dispo dans d'autres qualités
    pattern = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            qual = entry[1]
            lang = entry[2]
            title = ('%s [%s] %s') % (movie_title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('display_title', title)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url.replace('https', 'http'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    # Affichage du texte
    gui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis
    # Ne pas laisser vide sinon un texte faux venant du cache va etre utilisé
    desc = movie_title
    try:
        pattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = cUtil().removeHtmlTags(results[1][0][1])
    except BaseException:
        pass

    # On recherche d'abord la qualité courante
    pattern = '<div style="[^"]+?">.+?Qualité (.+?) [|] (.+?)<.+?img src="(([^"]+))"'
    results = parser.parse(html_content, pattern)

    qual = ''
    lang = ''
    if (results[1]):
        entry = results[1][0]
        qual = entry[0]
        lang = entry[1]
        # Change pour chaque saison, il faut la rechercher si on navigue entre
        # saisons
        thumb = entry[2]
    display_title = ('%s [%s] (%s)') % (movie_title, qual, lang)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', movie_title)
    output_parameter_handler.addParameter('thumb', thumb)
    output_parameter_handler.addParameter('desc', desc)
    gui.addTV(
        SITE_IDENTIFIER,
        'showSerieEpisodes',
        display_title,
        '',
        thumb,
        desc,
        output_parameter_handler)

    # On regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(html_content)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = parser.parse(sHtmlContent1, sPattern1)

    if (aResult1[0]):
        for entry in aResult1[1]:

            if 'animes' in url:
                url = URL_MAIN + 'animes' + entry[0]
            else:
                url = URL_MAIN + 'telecharger-serie' + entry[0]
            qual = entry[1]
            lang = entry[2]
            display_title = ('%s [%s] %s') % (movie_title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSerieEpisodes',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    # On regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(html_content)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = parser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if (aResult2[0]):
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        for entry in aResult2[1]:

            sSaison = entry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in url:
                url = URL_MAIN + 'animes' + entry[0]
            else:
                url = URL_MAIN + 'telecharger-serie' + entry[0]
            movie_title = entry[1] + entry[2]
            title = '[COLOR skyblue]' + movie_title + '[/COLOR]'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSeriesLinks',
                title,
                'series.png',
                thumb,
                movie_title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url.replace('https', 'http'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    parser = Parser()
    # '>Regarder' à la fin permet de ne pas prendre les liens en plusieurs parties
    pattern = 'class="btnToLink" target="_blank" href="([^"]+)">Regarder'
    results = parser.parse(html_content, pattern)

    if results[0]:
        # Un seul lien, on va directement chercher le hoster
        url = results[1][0]
        hoster_url = get_protected_link(url)
        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def showSerieEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url.replace('https', 'http'))
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'class="btnToLink" target="_blank" href="([^"]+)">Episode (.+?)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = entry[0]
            numEpisode = entry[1]

            display_title = 'Episode %s - %s' % (numEpisode, movie_title)
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter(
                'display_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                display_title,
                '',
                thumb,
                movie_title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    display_title = input_parameter_handler.getValue('display_title')
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    hoster_url = get_protected_link(url)
    hoster = HosterGui().checkHoster(hoster_url)
    if (hoster):
        hoster.setDisplayName(display_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    gui.setEndOfDirectory()


def get_protected_link(url):
    if not url:
        return ''

    parser = Parser()

    html_content = DecryptDlProtecte(url)
    if html_content:

        # Si redirection
        if html_content.startswith('http'):
            return html_content

        sPattern_dlprotecte = '<iframe.+?src="([^"]+)"'
        aResult_dlprotecte = parser.parse(html_content, sPattern_dlprotecte)
        if aResult_dlprotecte[0]:
            return aResult_dlprotecte[1][0]


def CutQual(html_content):
    parser = Parser()
    pattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if (results[0]):
        return results[1][0]
    else:
        return html_content

    return ''


def CutSais(html_content):
    parser = Parser()
    pattern = '<h3>Saisons.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    results = parser.parse(html_content, pattern)
    if (results[0]):
        return results[1][0]
    return ''


def DecryptDlProtecte(url):

    if not (url):
        return ''

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'form action="([^"]+).+?type="hidden" name="_token" value="([^"]+).+?input type="hidden" value="([^"]+)'
    result = parser.parse(html_content, pattern)

    if (result[0]):
        restUrl = str(result[1][0][0])
        token = str(result[1][0][1])
        # urlData = str(result[1][0][2])

    else:
        pattern = '<(.+?)action="([^"]+)" method="([^"]+).+?hidden".+?value="([^"]+)'
        result = parser.parse(html_content, pattern)

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

    request_handler = RequestHandler(restUrl)
    if method == "post":
        request_handler.setRequestType(1)
    request_handler.addParameters("_token", token)
    html_content = request_handler.request()

    return html_content
