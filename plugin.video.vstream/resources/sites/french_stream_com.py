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


def decode_url_Serie(url, sId, tmp=''):
    v = url
    if 'singh' in sId:
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

    if sId == 'honey':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if sId == 'yoyo':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if sId == 'seriePlayer':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    return v


def decode_url(url, sId, tmp=''):
    v = url
    if sId == 'seriePlayer':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if sId == 'gGotop1':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if sId == 'gGotop2':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=2&&c_id=" + str(t)

    if sId == 'gGotop3':
        fields = url.split('nbsq')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=3&&c_id=" + str(t)

    if sId == 'gGotop4':
        fields = url.split('nbsr')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=4&&c_id=" + str(t)

    if sId == 'gGotop5':
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
        sId = re.search(pat, url, re.DOTALL).group(1)
        hAsh = re.search(pat, url, re.DOTALL).group(2)
        hAsh = base64.b64decode(base64.b64decode(hAsh))

        if sId == '2':
            url2 = 'https://oload.stream/embed/'
        elif sId == '3':
            url2 = 'https://vidlox.me/embed-'
        elif sId == '4':
            url2 = 'https://hqq.watch/player/embed_player.php?vid='

        url2 = url2 + hAsh
        return url2
    except BaseException:
        return ''
    return ''


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSeries',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', MOVIE_VF[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD-VF)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSeries',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
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
    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchSeries():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showSeries(sUrl)
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
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'film-genre/' + sUrl + '/')
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
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'serie-genre/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'film-ripz".+?href="([^"]+)" title="[^"]+">.+?<img src="([^"]+).+?class="short-titl.+?>([^<]+)<(/div|br>(.+?)<)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            title = aEntry[2]

            if sSearch and ' - Saison ' in title:  # La recherche retourne aussi des séries
                continue

            # on recupere le titre dans le poster car le site ne l'affiche pas
            # toujours
            if title == ' ':
                title = aEntry[1].replace(
                    '/static/poster/',
                    '').replace(
                    '-',
                    ' ').replace(
                    '.jpg',
                    '').title()

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            # Année parfois
            sYear = ''
            if len(aEntry) > 4:
                sYear = aEntry[4]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

    if not sSearch:
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


def showSeries(sSearch=''):
    gui = Gui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="short-poster.+?href="([^"]+)".+?img src="([^"]*)".*?class="short-title.+?>([^<]+)<'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            title = aEntry[2]

            if sSearch and ' - Saison ' not in title:  # La recherche retourne aussi des films
                continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            # filtre pour réorienter les mangas
            # if '/manga' in sUrl:
                # sType = 'mangas'
            # else:
                # sType = 'autre'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            # output_parameter_handler.addParameter('sType', sType)

            if '/manga' in sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'mangaHosters',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', sThumb, '', output_parameter_handler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'href="([^"]+)">>></a>.+?>(\\d+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    sPattern = '>([^<]+)</a>\\s*<a href="([^"]+)">>>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a style="display.+?cid="([^"]+)'
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


def showEpisode():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    # sType = input_parameter_handler.getValue('sType')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    try:
        sPattern = 'id="s-desc">.+? : (.+?)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = re.sub('Résumé.+?$', '', aResult[1][0])
    except BaseException:
        pass

    sPattern = '</i> *(VF|VOSTFR) *</div>|<a id="([^"]+)".+?target="seriePlayer".+?"([^"]+)" data-rel="([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    sLang = ''
    if aResult:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult:

            if aEntry[0]:
                sLang = aEntry[0]
            else:
                # sId = aEntry[1]
                title = sMovieTitle + ' ' + aEntry[2]
                sDisplayTitle = '%s [%s]' % (title, sLang)
                sData = aEntry[3]

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sData', sData)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sLang', sLang)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sData = input_parameter_handler.getValue('sData')

    # if sData == 'episode1': #episode final au lieu du 1er donc pour le moment
    # return
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sData + '" class="fullsfeature"(.+?)<div style='
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        block = aResult[1][0]
    else:
        return

    sPattern = '<a (?:id="([^"]+)"|onclick=".+?") *surl="([^"]+)"'
    aResult = oParser.parse(block, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                url = aEntry[1]
                tmp = ''
                try:
                    tmp = re.search(
                        'input id="tmp".+?value="([^"]+)"',
                        sHtmlContent,
                        re.DOTALL).group(1)
                except BaseException:
                    pass

                if '/embed' in url or 'opsktp' in url or 'videovard' in url or 'iframe' in url or 'jetload' in url:
                    sHosterUrl = url
                else:
                    url2 = decode_url_Serie(url, aEntry[0], tmp)
                    # second convertion
                    sHosterUrl = resolveUrl(url2)

            else:
                sHosterUrl = aEntry[1]

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:

                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def mangaHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '</i> *(VF|VOSTFR) *</div>|<a style="padding:5px 0;" id=".+?" *cid="([^"]+)".+?</i>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]')
            else:
                title = aEntry[2] + sMovieTitle
                sHosterUrl = aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(title)
                    oHoster.setFileName(title)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    # redirection en cas d'absence de résultat
    if not aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            sMovieTitle,
            sThumb,
            '',
            output_parameter_handler,
            input_parameter_handler)

    gui.setEndOfDirectory()
