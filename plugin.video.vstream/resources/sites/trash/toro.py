# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # désactivée le 03122020 site HS depuis plus de 1 mois


SITE_IDENTIFIER = 'toro'
SITE_NAME = 'Toro'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = 'https://www.torostreaming.com/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-en-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'genre/', 'showGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming/', 'showMovies')
SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
SERIE_LAST = (URL_MAIN + 'dernieres-saisons/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films & Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films & Séries (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_LAST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LAST[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Films & Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)</a>([^<]+)<'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1] + aEntry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = []
    liste.append(['09', URL_MAIN + 'lettre/09/'])
    liste.append(['A', URL_MAIN + 'lettre/a/'])
    liste.append(['B', URL_MAIN + 'lettre/b/'])
    liste.append(['C', URL_MAIN + 'lettre/c/'])
    liste.append(['D', URL_MAIN + 'lettre/d/'])
    liste.append(['E', URL_MAIN + 'lettre/e/'])
    liste.append(['F', URL_MAIN + 'lettre/f/'])
    liste.append(['G', URL_MAIN + 'lettre/g/'])
    liste.append(['H', URL_MAIN + 'lettre/h/'])
    liste.append(['I', URL_MAIN + 'lettre/i/'])
    liste.append(['J', URL_MAIN + 'lettre/j/'])
    liste.append(['K', URL_MAIN + 'lettre/k/'])
    liste.append(['L', URL_MAIN + 'lettre/l/'])
    liste.append(['M', URL_MAIN + 'lettre/m/'])
    liste.append(['N', URL_MAIN + 'lettre/n/'])
    liste.append(['O', URL_MAIN + 'lettre/o/'])
    liste.append(['P', URL_MAIN + 'lettre/p/'])
    liste.append(['Q', URL_MAIN + 'lettre/q/'])
    liste.append(['R', URL_MAIN + 'lettre/r/'])
    liste.append(['S', URL_MAIN + 'lettre/s/'])
    liste.append(['T', URL_MAIN + 'lettre/t/'])
    liste.append(['U', URL_MAIN + 'lettre/u/'])
    liste.append(['V', URL_MAIN + 'lettre/v/'])
    liste.append(['W', URL_MAIN + 'lettre/w/'])
    liste.append(['X', URL_MAIN + 'lettre/x/'])
    liste.append(['Y', URL_MAIN + 'lettre/y/'])
    liste.append(['Z', URL_MAIN + 'lettre/z/'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'ShowList',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+).jpg".+?<strong>([^<]+)<.+?<td>([^<]+)'
    # sPattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+).jpg".class.+?<strong>([^<]+)<.+?<td>([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1] + '.jpg'
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb  # pas d'image de qualité d'mage trouvé
            title = aEntry[2]
            sYear = aEntry[3]

            sDisplayTitle = title + ' (' + sYear + ')'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if 'series-/' in sUrl or '/serie-' in sUrl or '/serie/' in sUrl:
                gui.addTV(SITE_IDENTIFIER, 'showSXE', sDisplayTitle,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sPattern = 'next page-numbers".+?page\\/(\\d{1,3})'
            aResult = oParser.parse(sHtmlContent, sPattern)
            page = ''
            if aResult[0]:
                page = aResult[1][0]
            gui.addNext(
                SITE_IDENTIFIER,
                'ShowList',
                '[COLOR teal]Page ' +
                page +
                ' >>>[/COLOR]',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # sPattern = 'class="TPost C">.+?href="([^"]+)".+?img src="([^"]+)".+?title">([^<]+).+?year">([^<]+)'
    sPattern = 'class="TPost C">.+?href="([^"]+)".+?img src="([^"]+).jpg".+?title">([^<]+).+?year">([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            # sThumb = re.sub('/w\d+', '/w342', aEntry[1])  # meilleur
            # resolution pour les thumbs venant de tmdb
            sThumb = aEntry[1] + '.jpg'
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            title = aEntry[2]
            sYear = aEntry[3]
            # VSlog(sUrl2)
            sDisplayTitle = title + ' (' + sYear + ')'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/series/' in sUrl2 or '/serie-' in sUrl2 or '/serie/' in sUrl2:  # a revoir les cas
                gui.addTV(SITE_IDENTIFIER, 'showSXE', sDisplayTitle,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage):
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sNextPage)
                number = re.search('page/([0-9]+)/', sNextPage).group(1)
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
    sPattern = 'next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    # récupération du synopsis
    desc = ''
    sPattern = 'class="Description"><p>(.+?)</p>'
    aResultDesc = oParser.parse(sHtmlContent, sPattern)
    if aResultDesc[0]:
        desc = aResultDesc[1][0]

    sPattern = 'class="Title AA-Season.+?tab="(\\d)|class="Num">(\\d{1,2}).+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                sSaison = 'Saison ' + aEntry[0]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    sSaison +
                    '[/COLOR]')
            else:
                sUrl = aEntry[2]
                Ep = aEntry[1]
                title = sMovieTitle + ' Episode' + Ep

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sYear', sYear)
                output_parameter_handler.addParameter('desc', desc)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-tplayernv.+?span>([^<]+)'
    aResult0 = re.findall(sPattern, sHtmlContent)
    sPattern = 'id="Opt\\d.+?src=.+?trembed=(\\d).+?trid=(\\d{5})'
    aResult1 = re.findall(sPattern, sHtmlContent)

    # récupération du synopsis
    desc = ''
    sPattern = 'class="Description"><p>(.+?)</p>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = aResult[1][0]

    nbElement = len(aResult0)
    for i in range(nbElement):
        # print (aResult0[i] + ' ' + aResult1[i][0]+ ' ' + aResult1[i][1])
        sHost = aResult0[i]
        sCode = aResult1[i][0]
        sCode1 = aResult1[i][1]
        title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
        sUrl = URL_MAIN + '?trembed=' + sCode + '&trid=' + sCode1 + '&trtype=1'

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sYear', sYear)

        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            sThumb,
            desc,
            output_parameter_handler)

    sPattern = 'trdownload=(\\d+).+?trid=(\\d+).+?alt.+?noscript>([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHost = aEntry[2]
            sCode = aEntry[0]
            sCode1 = aEntry[1]
            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            sUrl = URL_MAIN + '?trdownload=' + sCode + '&trid=' + sCode1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', sUrl)
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

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-tplayernv.+?span>([^<]+)'
    aResult0 = re.findall(sPattern, sHtmlContent)
    sPattern = 'id="Opt\\d.+?src=.+?trembed=(\\d).+?trid=(\\d{5,6})'
    aResult1 = re.findall(sPattern, sHtmlContent)

    nbElement = len(aResult0)
    for i in range(nbElement):
        # print (aResult0[i] + ' ' + aResult1[i][0]+ ' ' + aResult1[i][1])
        sHost = aResult0[i]
        sCode = aResult1[i][0]
        sCode1 = aResult1[i][1]
        title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

        sUrl = URL_MAIN + '?trembed=' + sCode + '&trid=' + sCode1 + '&trtype=2'

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sYear', sYear)

        gui.addLink(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            sThumb,
            desc,
            output_parameter_handler)

    sPattern = 'trdownload=(\\d+).+?trid=(\\d+).+?alt.+?noscript>([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHost = aEntry[2]
            sCode = aEntry[0]
            sCode1 = aEntry[1]
            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            sUrl = URL_MAIN + '?trdownload=' + sCode + '&trid=' + sCode1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sYear', sYear)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
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
    oRequestHandler = RequestHandler(sUrl)

    oRequestHandler.request()
    sHtmlContent = oRequestHandler.request()
    urlreal = oRequestHandler.getRealUrl()

    if 'trembed=' not in urlreal:
        sHosterUrl = urlreal  # liens de téléchargements
    else:
        sPattern = 'src="([^"]+)"'
        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]  # link stream

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
