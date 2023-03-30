# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.comaddon import SiteManager, VSlog
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'cinemay_cc'
SITE_NAME = 'Cinemay_cc'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-box-office', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = ('', 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'serie-streaming', 'showMovies')
SERIE_GENRES = (True, 'showGenresTVShow')
SERIE_ANNEES = (True, 'showMovieYearsTVShow')
SERIE_LIST = ('', 'showAlphaTVShow')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'annees.png',
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Liste alphabétique)',
        'az.png',
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

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (les plus vus)',
        'annees.png',
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


def showMenuSeries():
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

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        gui.setEndOfDirectory()
        return


def showGenresTVShow():
    showGenres(sTypeSerie='/series')


def showGenres(sTypeSerie=''):
    gui = Gui()

    listegenre = [
        'action',
        'action-adventure',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'histoire',
        'horreur',
        'kids',
        'musique',
        'musical',
        'mystere',
        'news',
        'science-fiction',
        'science-fiction-fantastique',
        'reality',
        'romance',
        'soap',
        'talk',
        'telefilm',
        'thriller',
        'war-politics',
        'western']

    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:

        sUrl = URL_MAIN + 'categories/' + igenre + sTypeSerie
        title = igenre.capitalize()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlphaTVShow():
    showAlpha(sTypeSerie='/series')


def showAlpha(sTypeSerie=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sType = input_parameter_handler.getValue('siteUrl')

    liste = [['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'], ['H', 'h'],
             ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'], ['Q', 'q'],
             ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'],
             ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'letter/' + sUrl + str(sType) + sTypeSerie)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYearsTVShow():
    showMovieYears(sTypeSerie='/series')


def showMovieYears(sTypeSerie=''):
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2001, 2023)):  # pas grand chose 32 - 90
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + Year + sTypeSerie)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    if sSearch:
        bvalid, stoken, scookie = getTokens()
        if bvalid:
            oUtil = cUtil()
            sSearchText = oUtil.CleanName(sSearch)
            sSearch = sSearch.replace(' ', '+').replace('%20', '+')
            pdata = '_token=' + stoken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            oRequestHandler = RequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)
            # oRequestHandler.request()
            sHtmlContent = oRequestHandler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # title img year surl
    sPattern = '<figure>.+?data-src="([^"]+.jpg)" (?:alt|title)="([^"]+).+?year">([^<]*).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            desc = ''
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[0])
            title = aEntry[1].replace(
                'film en streaming', '').replace(
                'série en streaming', '')

            # Titre recherché
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sYear = aEntry[2]
            sUrl2 = aEntry[3]
            sDisplayTitle = title + '(' + sYear + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)

            if sSearch:
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showSelectType',
                    sDisplayTitle,
                    sThumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)
            elif '/serie' in sUrl or 'série en streaming' in aEntry[1]:
                sDisplayTitle = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
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
    sPattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-numbers'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSelectType(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    desc = ''
    oParser = Parser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('sYear', sYear)

    if 'class="num-epi">' in sHtmlContent:

        gui.addTV(
            SITE_IDENTIFIER,
            'showSaison',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)
    else:
        gui.addMovie(
            SITE_IDENTIFIER,
            'showLink',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSaison():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    sPattern = '<a href="#season.+?class.+?saison (\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sNumSaison = aEntry
            sSaison = 'Saison ' + sNumSaison
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            sDisplayTitle = sMovieTitle + ' ' + sSaison
            title = sMovieTitle

            output_parameter_handler.addParameter('siteUrl', sUrlSaison)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showSXE',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sStart = 'class="num-epi">' + sNumSaison
    sEnd = 'id="season-'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = 'class="num-epi">\\d+x([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            Ep = aEntry[0]
            sUrl2 = aEntry[1]
            Saison = 'Saison' + ' ' + sNumSaison
            title = sMovieTitle + ' ' + Saison + ' Episode' + Ep

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
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
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = Parser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if False and 'class="num-epi">' in sHtmlContent and 'episode' not in sUrl:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('desc', desc)
        gui.addTV(
            SITE_IDENTIFIER,
            'showSXE',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

        gui.setEndOfDirectory()
        return

    sPattern = 'data-url="([^"]+).+?server.+?alt="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oHosterGui = HosterGui()
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sKey = aEntry[0]
            sHost = aEntry[1].replace(
                'www.', '').replace(
                'embed.mystream.to', 'mystream')
            sHost = re.sub('\\.\\w+', '', sHost).capitalize()
            if not oHosterGui.checkHoster(sHost):
                continue

            sLang = aEntry[2].upper()
            sUrl2 = URL_MAIN + 'll/captcha?hash=' + sKey
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
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

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.*?src=([^\\s]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]

        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getTokens():
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'id="menu.+?name=_token value="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?cinemay_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; cinemay_session=' + site_session + ';'
    return True, token, cook


def cleanDesc(desc):
    list_comment = ['Voir film ', 'en streaming', 'Voir Serie ']
    for s in list_comment:
        desc = desc.replace(s, '')

    return desc
