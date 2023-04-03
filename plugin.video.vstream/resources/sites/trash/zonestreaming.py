# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress
from resources.lib.multihost import cJheberg
from resources.lib.util import cUtil
import re

# from base64 import urlsafe_b64encode
import htmlentitydefs
import unicodedata

# ancien dpstreaming_tv
SITE_IDENTIFIER = 'zonestreaming'
SITE_NAME = 'Zone Streaming'
SITE_DESC = 'NC'

URL_MAIN = 'https://megastreaming.ws/'

MOVIE_MOVIE = (True, 'showMoviesMenu')
MOVIE_NEWS = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'category/films/vostfr-films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'category/films-en-exclus/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (True, 'showSeriesMenu')
SERIE_NEWS = (URL_MAIN + 'category/series-tv/', 'showMovies')
SERIE_VFS = (
    URL_MAIN +
    'category/series-tv/series-streaming-vf/',
    'showMovies')
SERIE_VOSTFRS = (
    URL_MAIN +
    'category/series-tv/series-streaming-vostfr/',
    'showMovies')
SERIE_VFQ = (URL_MAIN + 'category/series-tv/vfq/', 'showMovies')
SERIE_LIST = (URL_MAIN + 'category/series-tv/', 'showAZ')

REPLAYTV_NEWS = (URL_MAIN + 'category/emissions-tv/', 'showMovies')
REPLAYTV_TELE = (URL_MAIN + 'category/emissions-tv/telerealite/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')

DOC_NEWS = (URL_MAIN + 'category/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\\w+;", fixup, text)


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films (Menu)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries (Menu)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Replay tv',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
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
    output_parameter_handler.addParameter('site_url', SERIE_VFQ[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFQ[1],
        'Séries (VFQ)',
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
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showAZ():
    gui = Gui()

    liste = []
    liste.append(["0-9", URL_MAIN + "category/series-streaming/0-9/"])
    liste.append(["A-B-C", URL_MAIN + "category/series-streaming/a-b-c/"])
    liste.append(["D-E-F", URL_MAIN + "category/series-streaming/d-e-f/"])
    liste.append(["G-H-I", URL_MAIN + "category/series-streaming/g-h-i/"])
    liste.append(["J-K-L", URL_MAIN + "category/series-streaming/j-k-l/"])
    liste.append(["M-N-O", URL_MAIN + "category/series-streaming/m-n-o/"])
    liste.append(["P-Q-R", URL_MAIN + "category/series-streaming/p-q-r/"])
    liste.append(["S-T-U", URL_MAIN + "category/series-streaming/s-t-u/"])
    liste.append(["V-W-X-Y-Z", URL_MAIN +
                  "category/series-streaming/v-w-x-y-z/"])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/films-streaming/action/'])
    liste.append(['Animation', URL_MAIN +
                  'category/films-streaming/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN +
                  'category/films-streaming/arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN +
                  'category/films-streaming/aventure-films/'])
    liste.append(['Biopic', URL_MAIN + 'category/films-streaming/biopic/'])
    liste.append(['Comédie', URL_MAIN + 'category/films-streaming/comedie/'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                  'category/films-streaming/comedie-dramatique/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'category/films-streaming/drame/'])
    liste.append(['Espionnage', URL_MAIN +
                  'category/films-streaming/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'category/films-streaming/famille/'])
    liste.append(['Fantastique', URL_MAIN +
                  'category/films-streaming/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'category/films-streaming/guerre/'])
    liste.append(['Historique', URL_MAIN +
                  'category/films-streaming/historique/'])
    liste.append(['Horreur', URL_MAIN + 'category/films-streaming/horreur/'])
    liste.append(['Musical', URL_MAIN + 'category/films-streaming/musical/'])
    liste.append(['Policier', URL_MAIN + 'category/films-streaming/policier/'])
    liste.append(['Romance', URL_MAIN + 'category/films-streaming/romance/'])
    liste.append(['Science-Fiction', URL_MAIN +
                  'category/films-streaming/science-fiction/'])
    liste.append(['Spectacle', URL_MAIN +
                  'category/films-streaming/spectacle/'])
    liste.append(['Thriller', URL_MAIN + 'category/films-streaming/thriller/'])
    liste.append(['Western', URL_MAIN + 'category/films-streaming/western/'])

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


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = html_content.replace(
        ' [Streaming]',
        '').replace(
        ' [Streaming',
        '').replace(
            ' [Telecharger]',
            '').replace(
                ' [Téléchargement]',
                '').replace(
                    ' [Telechargement]',
        '')
    pattern = '<div class="post-thumb is-image"><a href="([^"]+)".+?title="([^"]+)".+?src="([^"]+)".+?<p>([^<]+)<\\/p>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addNone(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            title = entry[1].replace('&prime;', '\'')
            title = title.replace('Saiosn', 'Saison')
            thumb = entry[2]
            desc = entry[3]
            # Filtre recherche
            if search and total > 3:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            # Mangas et Series fonctionnent pareil
            if '/series-tv/' in url or '-saison-' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeries',
                    title,
                    'series.png',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'films.png',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class="next page-numbers" href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSeries():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Nettoyage du code, a simplifier, mais je trouve pas ce qui ne va pas
    html_content = html_content.decode('utf-8', 'replace')
    html_content = unicodedata.normalize('NFD', html_content).encode(
        'ascii', 'ignore').decode('unicode_escape')  # vire accent et '\'
    html_content = html_content.encode('utf-8')  # On remet en utf-8

    html_content = html_content.replace(
        '<strong>Telechargement VOSTFR',
        '').replace(
        '<strong>Telechargement VF',
        '').replace(
            '<strong>Telechargement',
        '')
    html_content = html_content.replace('<a href="http://www.multiup.org', '')
    # supprimme pour récuperer les new regex different
    html_content = html_content.replace(
        '<span style="color: #ff9900;">New</span>', '')
    html_content = html_content.replace(
        '<span class="su-lightbox" data-mfp-src', '<a href')

    # récupération des Synopsis
    desc = ''
    try:
        pattern = '(?:<p style="text-align: center;"|<p align="center")>([^<]+)<\\/p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
            desc = desc.replace('&#8217;', '\'').replace('&#8230;', '...')
    except BaseException:
        pass

    pattern = '<span style="color: #33cccc; font-size: large;"><b>([^<]+)|>(.pisode[^<]{2,12})<(?!\\/a>)(.{0,10}a href="http.+?)(?:<.p>|<br|<.div)'
    results = parser.parse(html_content, pattern)

    # astuce en cas d'episode unique
    if not results[0]:
        # gui.setEndOfDirectory()
        showHosters()
        return

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            else:
                movie_title = movie_title.replace('[Complete]', '')
                title = movie_title + ' ' + entry[1]
                url = entry[2]

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'serieHosters',
                    title,
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<span style="color: #ff990.+?>([^<]+)<|large button.+?href="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')

            else:
                # nettoyage du titre
                movie_title = re.sub('\\[\\w+ \\w+]', '', movie_title)
                movie_title = re.sub('\\[\\w+]', '', movie_title)

                hoster_url = entry[1]
                # pour récuperer tous les liens
                if '&url=' in hoster_url:
                    hoster_url = hoster_url.split('&url=')[1]

                # pour récuperer le lien jwplayer(GoogleDrive)
                if 'filmhdstream' in hoster_url:
                    request_handler = RequestHandler(hoster_url)
                    html_content = request_handler.request()
                    pattern = '<iframe.+?src="([^"]+)"'
                    results = parser.parse(html_content, pattern)
                    if results[0]:
                        for entry in results[1]:
                            hoster_url = entry

                            hoster = HosterGui().checkHoster(hoster_url)
                            if (hoster):
                                hoster.setDisplayName(movie_title)
                                hoster.setFileName(movie_title)
                                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

                # pour récuperer les liens jheberg
                elif 'jheberg' in hoster_url:
                    results = cJheberg().GetUrls(hoster_url)
                    if results:
                        for entry in results:
                            hoster_url = entry

                            hoster = HosterGui().checkHoster(hoster_url)
                            if (hoster):
                                hoster.setDisplayName(movie_title)
                                hoster.setFileName(movie_title)
                                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

                else:
                    hoster = HosterGui().checkHoster(hoster_url)
                    if (hoster):
                        hoster.setDisplayName(movie_title)
                        hoster.setFileName(movie_title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def serieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()

    pattern = 'href="([^"]+)"'
    results = parser.parse(url, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            hoster_url = entry
            # pour récuperer tous les liens 2 variantes
            if '&url==' in hoster_url:
                hoster_url = hoster_url.split('&url==')[1]
            elif '&url=' in hoster_url:
                hoster_url = hoster_url.split('&url=')[1]

            # pour récuperer le lien jwplayer(GoogleDrive)
            if 'filmhdstream' in hoster_url:
                request_handler = RequestHandler(hoster_url)
                html_content = request_handler.request()
                pattern = '<iframe.+?src="([^"]+)"'
                results = parser.parse(html_content, pattern)
                if results[0]:
                    for entry in results[1]:
                        hoster_url = entry

                        hoster = HosterGui().checkHoster(hoster_url)
                        if (hoster):
                            hoster.setDisplayName(movie_title)
                            hoster.setFileName(movie_title)
                            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

            # pour récuperer les liens jheberg
            elif 'jheberg' in hoster_url:
                results = cJheberg().GetUrls(hoster_url)
                if results:
                    for entry in results:
                        hoster_url = entry

                        hoster = HosterGui().checkHoster(hoster_url)
                        if (hoster):
                            hoster.setDisplayName(movie_title)
                            hoster.setFileName(movie_title)
                            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

            else:
                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
