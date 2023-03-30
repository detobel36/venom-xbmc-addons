# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager
from resources.lib.util import cUtil

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

SITE_IDENTIFIER = 'alloflix'
SITE_NAME = 'Alloflix'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')
MOVIE_ANNEES = (True, 'showYears')

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film/', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/', 'showSeriesGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films & Séries (Par années)',
        'annees.png',
        output_parameter_handler)

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

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

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

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showYears():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN + 'accueil/')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="btn sm" href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="cat-item.+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0] + '?type=movies'
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesGenres():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="cat-item.+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0] + '?type=series'
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
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
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20 ', '+')

    sPattern = 'class="entry-title">([^<]+).+?data-src="([^"]+).+?year">([^<]*).+?href="([^"]+)'
    oRequestHandler = RequestHandler(sUrl)
    # on ne prend pas les populaires qui sinon sont présent à chaque fois
    sStart = '<!doctype html>'
    sEnd = '<h3 class="widget-title">Populaires'
    sHtmlContent = oParser.abParse(oRequestHandler.request(), sStart, sEnd)
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            title = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            sYear = aEntry[2]
            sUrl2 = aEntry[3]

            if '/annee/' in sUrl:
                if '/film/' in sUrl2:
                    sDisplayTitle = title + ' [COLOR coral]{Films}[/COLOR]'
                else:
                    sDisplayTitle = title + ' [COLOR coral]{Séries}[/COLOR]'
            else:
                sDisplayTitle = title

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue  # Filtre de recherche

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/serie' in sUrl or '/serie/' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            # elif 'serie' in sUrl2:
                # gui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
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


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '>([0-9]+)</a><a href="([^"]+)">SUIVANT'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging
    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sPattern = 'class=description><p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = 'choose-season">.+?href=([^"]+\\/).+?right">([^<]+).+?inline">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sSais = aEntry[1] + aEntry[2]
            title = sMovieTitle + ' ' + sSais

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<span class=num-epi>\\dx(\\d+).+?href=(\\S+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[1]
            sEp = 'Episode ' + aEntry[0]
            title = sMovieTitle + ' ' + sEp

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')

    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ""
    sPattern = 'class=description>(.+?)<\\/'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])
        desc = desc.replace('<p>', '')

    sPattern = '(iframe src|iframe data-src)="([^"]+)|href=#options-(\\d).+?server>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        sLang = None
        tab = aResult[1]
        n = len(tab) // 2

        for i in range(n):
            sUrl2 = tab[i][1]
            # dataNum = tab[i+n][2]
            sHost = tab[i + n][3]
            if ' -' in sHost:
                sHost, sLang = sHost.split(' -')

            sDisplayTitle = sMovieTitle
            if sLang:
                sLang = sLang.replace(' ', '')
                sDisplayTitle += ' (%s) ' % sLang.upper()

            sDisplayTitle += ' [COLOR coral]%s[/COLOR]' % sHost.capitalize()

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sHost', sHost)
            gui.addLink(
                SITE_IDENTIFIER,
                'hostersLink',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def hostersLink():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    referer = input_parameter_handler.getValue('referer')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7')
    sHtmlContent = oRequest.request()

    sPattern = 'src=(\\S+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)
    gui.setEndOfDirectory()
