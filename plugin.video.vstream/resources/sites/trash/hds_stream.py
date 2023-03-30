# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'hds_stream'
SITE_NAME = 'Hds-stream'
SITE_DESC = 'Film streaming HD complet en vf. Des films et séries pour les fan de streaming hds.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIES = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')
# MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

#     output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
#     gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_MOVIES[1],
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

#     output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
#     gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'menu-item-object-genres.+?<a href="([^"]+)".*?>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        genres = set(aResult[1])
        genres = sorted(genres, key=lambda genre: genre[1])
        output_parameter_handler = OutputParameterHandler()
        for aEntry in genres:
            sUrl = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(
        sHtmlContent,
        '<h2>Films Par Années</h2>',
        '<h2>Films Par Genres</h2>')

    sPattern = '<li><a href="([^"]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sYear = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                sYear,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
        sPattern = 'class="result-item">.*?href="([^"]+)"><img src="([^"]+).*?class="title"><a.*?>([^<]+).*?class="year">([^<]+).*?class="contenido"><p>([^<]+)'
    elif 'tendance/' in sUrl:
        sPattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+).*?, ([^<]+)</span>'
    else:
        sPattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+).*?, ([^<]+)</span>.*?<div class="texto">([^<]*)'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

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

            if sSearch:
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
                title = aEntry[2]
                sYear = aEntry[3]
                desc = aEntry[4]
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche
            else:
                sThumb = aEntry[0]
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sUrl2 = aEntry[1]
                title = aEntry[2]
                sYear = aEntry[3]
                if 'tendance/' in sUrl:
                    desc = ''
                else:
                    desc = aEntry[4]

            sDisplayTitle = ('%s (%s)') % (title, sYear)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/series' in sUrl2:
                gui.addTV(SITE_IDENTIFIER, 'showSxE', title, '',
                          sThumb, desc, output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
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
    sPattern = '>Page \\d+ de (\\d+)</span>.*?<span class="current.+?href=["\']([^"\']+/page/\\d+)/["\'] class="inactive'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
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
    sPattern = "span class='title'>([^<]+)|class='numerando'>\\d - ([^<]+).+?class='episodiotitle'><a href='([^']+)'>([^<]+)"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    sSaison = ''
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sSaison = aEntry[0].replace('eason', 'aison')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    sSaison +
                    '[/COLOR]')
            else:
                sUrl = aEntry[2]
                EpTitle = aEntry[3]
                Ep = aEntry[1]
                sDisplayTitle = EpTitle + ' ' + sSaison + ' Episode ' + Ep
                title = sMovieTitle + ' | ' + sDisplayTitle

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = "class='dooplay_player_option' data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        url_main = GET_REAL_URLMAIN(sUrl)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = url_main + 'wp-admin/admin-ajax.php'
            dType = aEntry[0]
            dPost = aEntry[1]
            dNum = aEntry[2]
            pdata = 'action=doo_player_ajax&post=' + \
                dPost + '&nume=' + dNum + '&type=' + dType
            sHost = 'Serveur ' + dNum

            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLink',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = "id='player-option-.+?data-type='([^']+).+?data-post='([^']+).+?data-nume='([^']+).+?'server'>([^.|^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        url_main = GET_REAL_URLMAIN(sUrl)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = url_main + 'wp-admin/admin-ajax.php'
            dType = aEntry[0]
            dPost = aEntry[1]
            dNum = aEntry[2]
            pdata = 'action=doo_player_ajax&post=' + \
                dPost + '&nume=' + dNum + '&type=' + dType
            if (aEntry[3]).startswith('Unknown'):
                sHost = 'Serveur ' + dNum
            else:
                sHost = aEntry[3].capitalize()

            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLink',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
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
        'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7')
    oRequest.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request().replace('\\', '')

    sPattern = '(http[^"]+)'
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


def GET_REAL_URLMAIN(url):
    sd = url.split('.')
    sdm = URL_MAIN.split('.')
    return URL_MAIN.replace(sdm[0], sd[0])
