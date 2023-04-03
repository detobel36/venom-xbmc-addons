# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import base64
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager
from resources.lib.util import cUtil

# Detecte si c'est Kodi 19 ou plus
if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
    isPython3 = True
else:
    isPython3 = False

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream'
SITE_DESC = 'Films, Séries & Mangas en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

# URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=9&story=', 'showMovies')
# URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=10&story=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
# MOVIE_VF = (URL_MAIN + 'films/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/VOSTFR/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'qualit/HDLight/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie-tv-streaming', 'showSeries')
SERIE_VFS = (URL_MAIN + 'serie/VF/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'serie/VOSTFR/', 'showSeries')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showSeries')


def decode_url_Serie(url, s_id, tmp=''):
    v = url
    if 'singh' in s_id:
        fields = url.split('nbsp')
        try:
            if isPython3:
                t = base64.b64encode(base64.b64encode(fields[1].encode()))
            else:
                t = base64.b64encode(base64.b64encode(fields[1]))
        except IndexError:
            if isPython3:
                t = base64.b64encode(base64.b64encode(fields[0].encode()))
            else:
                t = base64.b64encode(base64.b64encode(fields[0]))
        else:
            return
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if s_id == 'honey':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if s_id == 'yoyo':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if s_id == 'seriePlayer':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    return v


def decode_url(url, s_id, tmp=''):
    v = url
    if s_id == 'seriePlayer':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if s_id == 'gGotop1':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if s_id == 'gGotop2':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=2&&c_id=" + str(t)

    if s_id == 'gGotop3':
        fields = url.split('nbsq')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=3&&c_id=" + str(t)

    if s_id == 'gGotop4':
        fields = url.split('nbsr')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=4&&c_id=" + str(t)

    if s_id == 'gGotop5':
        fields = url.split('nbss')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/dl.php?p_id=5&&c_id=" + str(t)

    return v


def resolveUrl(url):
    try:
        url2 = ''
        pat = 'p_id=([0-9]+).+?c_id=([^&]+)'
        s_id = re.search(pat, url, re.DOTALL).group(1)
        hAsh = re.search(pat, url, re.DOTALL).group(2)
        hAsh = base64.b64decode(base64.b64decode(hAsh))

        if s_id == '2':
            url2 = 'https://oload.stream/embed/'
        elif s_id == '3':
            url2 = 'https://vidlox.me/embed-'
        elif s_id == '4':
            url2 = 'https://hqq.watch/player/embed_player.php?vid='

        url2 = url2 + hAsh
        return url2
    except BaseException:
        return ''
    return ''


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSeries',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', MOVIE_VF[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD-VF)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSeries',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnims():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_MOVIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSeries():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_SERIES[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-Martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'com%C3%A9die'],
             ['Comédie Dramatique', 'com%C3%A9die-dramatique'], ['Comédie Musicale', 'com%C3%A9die-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante_horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Super héros', 'Super_héros'],
             ['Thriller', 'thriller'], ['Walt Disney', 'Walt-Disney'], ['Western', 'western'], ['Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'film-genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieGenres():
    gui = Gui()

    liste = [['Action', 'Action'], ['Animation', URL_MAIN + 'serie-genreAnimation'], ['Arts Martiaux', 'Arts-Martiaux'],
             ['Aventure', 'Aventure'], ['Biopic', 'Biopic'], ['Comédie', 'Comédie'],
             ['Comédie Dramatique', 'Comédie+dramatique'], ['Comédie Musicale', 'Comédie+musicale'],
             ['Documentaire', 'Documentaire'], ['Drame', 'Drame'], ['Epouvante Horreur', 'Epouvante-horreur'],
             ['Espionnage', 'Espionnage'], ['Famille', 'Famille'], ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'],
             ['Historique', 'Historique'], ['Judiciaire', 'Judiciaire'], ['Médical', 'Médical'], ['Musical', 'Musical'],
             ['Policier', 'Policier'], ['Romance', 'Romance'], ['Science Fiction', 'Science+fiction'], ['Soap', 'Soap'],
             ['Sport', 'Sport+event'], ['Thriller', 'Thriller'], ['Western', 'Western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'serie-genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'film-ripz".+?href="([^"]+)" title="[^"]+">.+?<img src="([^"]+).+?class="short-titl.+?>([^<]+)<(/div|br>(.+?)<)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = URL_MAIN[:-1] + entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            title = entry[2]

            if search and ' - Saison ' in title:  # La recherche retourne aussi des séries
                continue

            # on recupere le titre dans le poster car le site ne l'affiche pas
            # toujours
            if title == ' ':
                title = entry[1].replace(
                    '/static/poster/',
                    '').replace(
                    '-',
                    ' ').replace(
                    '.jpg',
                    '').title()

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            # Année parfois
            year = ''
            if len(entry) > 4:
                year = entry[4]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    if not search:
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


def showSeries(search=''):
    gui = Gui()

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="short-poster.+?href="([^"]+)".+?img src="([^"]*)".*?class="short-title.+?>([^<]+)<'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = URL_MAIN[:-1] + entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            title = entry[2]

            if search and ' - Saison ' not in title:  # La recherche retourne aussi des films
                continue

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            # filtre pour réorienter les mangas
            # if '/manga' in url:
                # _type = 'mangas'
            # else:
                # _type = 'autre'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            # output_parameter_handler.addParameter('_type', _type)

            if '/manga' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'mangaHosters',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', thumb, '', output_parameter_handler)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'href="([^"]+)">>></a>.+?>(\\d+)<'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    pattern = '>([^<]+)</a>\\s*<a href="([^"]+)">>>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a style="display.+?cid="([^"]+)'
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


def showEpisode():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    # _type = input_parameter_handler.getValue('_type')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    try:
        pattern = 'id="s-desc">.+? : (.+?)<'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = re.sub('Résumé.+?$', '', results[1][0])
    except BaseException:
        pass

    pattern = '</i> *(VF|VOSTFR) *</div>|<a id="([^"]+)".+?target="seriePlayer".+?"([^"]+)" data-rel="([^"]+)"'
    results = re.findall(pattern, html_content)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    lang = ''
    if results:
        output_parameter_handler = OutputParameterHandler()
        for entry in results:

            if entry[0]:
                lang = entry[0]
            else:
                # s_id = entry[1]
                title = movie_title + ' ' + entry[2]
                display_title = '%s [%s]' % (title, lang)
                sData = entry[3]

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('sData', sData)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('lang', lang)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sData = input_parameter_handler.getValue('sData')

    # if sData == 'episode1': #episode final au lieu du 1er donc pour le moment
    # return
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div id="' + sData + '" class="fullsfeature"(.+?)<div style='
    results = parser.parse(html_content, pattern)

    if results[0]:
        block = results[1][0]
    else:
        return

    pattern = '<a (?:id="([^"]+)"|onclick=".+?") *surl="([^"]+)"'
    results = parser.parse(block, pattern)

    if results[0]:
        for entry in results[1]:

            if entry[0]:
                url = entry[1]
                tmp = ''
                try:
                    tmp = re.search(
                        'input id="tmp".+?value="([^"]+)"',
                        html_content,
                        re.DOTALL).group(1)
                except BaseException:
                    pass

                if '/embed' in url or 'opsktp' in url or 'videovard' in url or 'iframe' in url or 'jetload' in url:
                    hoster_url = url
                else:
                    url2 = decode_url_Serie(url, entry[0], tmp)
                    # second convertion
                    hoster_url = resolveUrl(url2)

            else:
                hoster_url = entry[1]

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:

                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def mangaHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '</i> *(VF|VOSTFR) *</div>|<a style="padding:5px 0;" id=".+?" *cid="([^"]+)".+?</i>([^<]+)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            else:
                title = entry[2] + movie_title
                hoster_url = entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    # redirection en cas d'absence de résultat
    if not results[0]:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            movie_title,
            thumb,
            '',
            output_parameter_handler,
            input_parameter_handler)

    gui.setEndOfDirectory()
