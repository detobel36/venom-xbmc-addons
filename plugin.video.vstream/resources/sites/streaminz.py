# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streaminz'
SITE_NAME = 'Streaminz'
SITE_DESC = ' films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
# MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_NETFLIX = (URL_MAIN + 'reseau/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'reseau/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'reseau/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'reseau/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'reseau/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'reseau/youtube-premium/', 'showMovies')
SERIE_ARTE = (URL_MAIN + 'reseau/arte/', 'showMovies')
# SERIE_ANNEES = (True, 'showSeriesYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
# l'url ne permet pas de filtrer directement les films des séries mais est
# utilisée pour filtrer dans showmovies
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

    # output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

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

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

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

    # output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

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

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '</i>Genres</a>'
    sEnd = '</i>Demandes</a>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1].capitalize()
            triAlpha.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, sUrl in triAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
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

    output_parameter_handler.addParameter('siteUrl', SERIE_ARTE[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_ARTE[1],
        'Séries (Arte)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<span>Années</span>'
    sEnd = '<span>Connexion</span>'
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
            sTypeYear = 'movies'

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sTypeYear', sTypeYear)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSeriesYears():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<span>Années</span>'
    sEnd = '<span>Connexion</span>'
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
            sTypeYear = 'tvshows'

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sTypeYear', sTypeYear)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
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
    oUtil = cUtil()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        sUrl = sSearch.replace(' ', '+')
        sPattern = 'class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?span class="([^"]+).+?<p>(.*?)<\\/p'
        # pour filtrage entre film et série
        sType = oParser.parseSingleResult(sUrl, '\\?post_types=(.+?)&')
    else:
        sTypeYear = input_parameter_handler.getValue('sTypeYear')
        if sTypeYear:
            sPattern = '<article id="post-\\d+".+?class="item ([^"]+).+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div>'
        else:
            sPattern = '<article id="post-\\d+".+?img src="([^"]+).+?alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
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
                title = aEntry[2].replace(
                    'Streaming VF',
                    '').replace(
                    'en',
                    '').replace(
                    'Regarder',
                    '')
                sType1 = aEntry[3]
                desc = aEntry[4]
                # pour différencier la recherche entre films et séries
                if sType1 != sType[1]:
                    continue
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche
            elif sTypeYear:
                sType1 = aEntry[0]
                if sType1 != sTypeYear:  # pour différencier la recherche entre films et séries
                    continue
                sThumb = aEntry[1]
                title = aEntry[2]
                if aEntry[3]:
                    sQual = aEntry[3]
                if aEntry[4]:
                    sYear = aEntry[4]
                sUrl = aEntry[5]
                if aEntry[6]:
                    desc = aEntry[6]
            else:
                sThumb = aEntry[0]
                title = aEntry[1]
                if aEntry[2]:
                    sQual = aEntry[2]
                if aEntry[3]:
                    sYear = aEntry[3]
                sUrl = aEntry[4]
                if aEntry[5]:
                    desc = aEntry[5]

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = oUtil.unescape(desc).encode(
                    'utf-8')  # retire les balises HTML
            except BaseException:
                pass

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sYear)

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
                    'showLink',
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
    sPattern = 'span>Page .+?de (\\d+).+?href="([^"]+)"><i id='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, False


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = ">([^<]+)</span><span class='title|numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]Saison ' +
                    aEntry[0] +
                    '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    ' Saison \\g<1> Episode \\g<2>',
                    aEntry[1])
                title = sMovieTitle + SxE

                sDisplayTitle = sMovieTitle + ' ' + \
                    re.sub('saison \\d+ ', '', SxE)

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLink',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if '/films/' in sUrl:
        sPattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    else:
        sPattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?flags/(.+?).png"

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            # fonctionne pour Film ou Série (pour info: série -> dtype = 'tv')
            dtype = 'movie'
            dpost = aEntry[0]
            dnum = aEntry[1]

            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype
            sLang = aEntry[2].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '').replace(
                ')',
                '')
            if '|' in sLang:
                sLang = sLang.split('|')[1].strip().replace('FRENCH', 'FR')

            if 'VIP - ' in aEntry[2]:  # Les liens VIP ne fonctionnent pas
                continue

            title = ('%s (%s)') % (sMovieTitle, sLang.upper())
            title = title + '[COLOR coral] Serveur#' + dnum + '[/COLOR]'

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
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")'
    aResult1 = re.findall(sPattern, sHtmlContent)

    sPattern = 'embed_url":"([^"]+)"'
    aResult2 = re.findall(sPattern, sHtmlContent)

    aResult = aResult1 + aResult2

    if aResult:
        for aEntry in aResult:

            sHosterUrl = aEntry.replace("\\", '')
            if 'youtube' in sHosterUrl:
                continue
            if 'dood' in sHosterUrl:
                sHosterUrl = sHosterUrl

            if 'club' in sHosterUrl:
                sHosterUrl = sHosterUrl
                oRequest = RequestHandler(sHosterUrl)
                oParser = Parser()
                sHtmlContent2 = oRequest.request()

                sPattern = "if.+?self.+?== top.+?replace\\('([^']+)"
                aResult = oParser.parse(sHtmlContent2, sPattern)
                for aEntry2 in aResult[1]:
                    sHosterUrl = 'https://waaw.to' + aEntry2

            # voir si filtrage ou non, car parfois le lien mp4 créé un blocage
            if 'streaminz.ml' in sHosterUrl:
                sid = sHosterUrl.split('/')[-1]
                sHosterUrl = sHosterUrl
                postdata = 'r=&d=streaminz.ml'
                urlapi = 'https://streaminz.ml/api/source/' + sid
                oRequest = RequestHandler(urlapi)
                oRequest.setRequestType(1)
                oRequest.addHeaderEntry('Referer', sHosterUrl)
                oRequest.addParametersLine(postdata)
                sHtmlContent2 = oRequest.request()
                oParser = Parser()
                sPattern = '"data".+?file.+?"([^"]*).+?type.+?"([^"]*)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0][0] + '.' + aResult[1][0][1]

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
