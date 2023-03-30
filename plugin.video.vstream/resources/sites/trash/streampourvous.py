# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streampourvous'
SITE_NAME = 'StreampourVous'
SITE_DESC = 'films,'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film-streaming/', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'film-streaming/', 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/animation/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (URL_MAIN + 'serie-streaming/', 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Animations)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Animations)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showNetwork():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NETFLIX[0])
    output_parameter_handler.addParameter('sTmdbId', 213)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_CANAL[0])
    output_parameter_handler.addParameter('sTmdbId', 285)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_AMAZON[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 1024)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_DISNEY[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 2739)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_APPLE[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 2552)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (YouTube Originals)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<ul class="genres scrolling">'
    sEnd = '><nav class="releases"><h2>Année de production</h2>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+).+?<i>(\\d*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1].capitalize()
            sNumber = aEntry[2]  # + ' Films'
            if sNumber < '2':
                sNumber = sNumber + ' Film'
            else:
                sNumber = sNumber + ' Films'
            sDisplayTitle = ('%s (%s)') % (title, sNumber)
            TriAlpha.append((sDisplayTitle, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for sDisplayTitle, sUrl in TriAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                sDisplayTitle,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<h2>Année de production</h2><ul class="releases scrolling">'
    sEnd = 'class="primary"><div class="columenu">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1].capitalize()

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showYearsSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1997, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'sortie/' + Year + '/?post_types=tvshows')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oParser = Parser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?<p>(.+?)</p>'

    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sStart = 'class="animation-2 items">'
        sEnd = '<div class=\'resppages\'>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = 'class="item.+?"><div class="poster.+?src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)href="([^"]+).+?<span>([0-9]{4}).+?texto">(.*?)</div'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        utils = cUtil()
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sQual = ''
            sYear = ''
            desc = ''
            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                title = aEntry[2]
                desc = aEntry[3]
            else:
                sThumb = aEntry[0]
                title = re.sub('\\([0-9]{4}\\)', '', aEntry[1])
                if aEntry[2]:
                    sQual = aEntry[2]  # parfois sLang
                sUrl = aEntry[3]
                sYear = aEntry[4]
                if aEntry[5]:
                    desc = aEntry[5].replace(
                        'Voir',
                        '').replace(
                        'Film complet streaming VF HD',
                        '') .replace(
                        'streaming VF HD',
                        '')

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = utils.unescape(desc).encode(
                    'utf-8')  # retire les balises HTML
            except BaseException:
                pass

            sDisplayTitle = ('%s %s (%s)') % (title, sQual, sYear)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            if '/serie' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSxE',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

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


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'class="pagination">.+?de (\\d*).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<span class='title'>(.+?)<i>|class='numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    aEntry[0].replace(
                        'Regarder',
                        '') +
                    '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    'saison \\g<1> Episode \\g<2>',
                    aEntry[1])
                title = sMovieTitle + ' ' + SxE

                sDisplayTitle = sMovieTitle + ' ' + \
                    re.sub('saison \\d+ ', '', SxE)

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = "data-type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+).+?server'>(.+?)<.+?flags/(\\w+)"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dtype = aEntry[0]
            dpost = aEntry[1]
            dnum = aEntry[2]
            pdata = dpost + '.' + dtype + '.' + dnum
            title = aEntry[3].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '') .replace(
                ')',
                '').replace(
                    '[',
                    '').replace(
                        ']',
                '')
            sServer = aEntry[4]
            sLang = aEntry[5].replace('fr', 'VF').replace('en', 'VOSTFR')

            if 'freebiesforyou.net' in sServer or 'youtube.com' in sServer:
                continue
            title = ('%s [%s] (%s)') % (sMovieTitle, title, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequest.addParameters("action", "doo_player_ajax")
    oRequest.addParameters("post", pdata.split('.')[0])
    oRequest.addParameters("type", pdata.split('.')[1])
    oRequest.addParameters("nume", pdata.split('.')[2])
    sHtmlContent = oRequest.request(jsonDecode=True)

    if 'dood' in sHtmlContent or 'evoload' in sHtmlContent:
        sPattern = '(http.+?)$'
    else:
        sPattern = '(http.+?)[\'|"]'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if 'zustreamv2/viplayer' in sHosterUrl:
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
