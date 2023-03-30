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

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = '_1seriestreaming'
SITE_NAME = '1 Serie Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showSeries')
SERIE_VIEWS = (URL_MAIN + 'series-populaires', 'showSeries')
SERIE_LIST = (URL_MAIN, 'showAlpha')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = ('', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Populaires)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showSerieYears():
    # for i in itertools.chain(range(5, 7), [8, 9]): afficher dans l'ordre
    # (pense bete ne pas effacer)
    gui = Gui()
    from itertools import chain
    generator = chain([1955], range(1957, 2023))

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(list(generator)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0', str('0')], ['1', str('1')], ['2', str('2')], ['3', str('3')], ['4', str('4')], ['5', str('5')],
             ['6', str('6')], ['7', str('7')], ['8', str('8')], ['9', str('9')],
             ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F'], ['G', 'G'], ['H', 'H'],
             ['I', 'I'], ['J', 'J'], ['K', 'K'], ['L', 'L'], ['M', 'M'], ['N', 'N'], ['O', 'O'], ['P', 'P'],
             ['Q', 'Q'], ['R', 'R'], ['S', 'S'], ['T', 'T'], ['U', 'U'], ['V', 'V'], ['W', 'W'], ['X', 'X'],
             ['Y', 'Y'], ['Z', 'Z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'alphabet/' + sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [['Action & Aventure', 'action-adventure'], ['Animation', 'animation'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Guerre', 'guerre'], ['Guerre & Politique', 'war-politics'], ['Histoire', 'histoire'], ['Kids', 'kids'],
             ['Musical', 'musical'], ['Musique', 'musique'], ['Mystère', 'mystere'], ['News', 'news'],
             ['Réalité', 'reality'], ['Romance', 'romance'], ['Science-fiction', 'science-fiction'],
             ['Science-Fiction Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Sport', 'sport'],
             ['Talk', 'talk'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'categories/' + sUrl + '/series')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)
        sSearch = sSearch.replace(' ', '+').replace('&20', '+')
        bValid, sToken, sCookie = getTokens()
        if bValid:
            sUrl = URL_MAIN + 'search'
            pdata = '_token=' + sToken + '&search=' + sSearch

            oRequestHandler = RequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Cookie', sCookie)
            oRequestHandler.addParametersLine(pdata)
            sHtmlContent = oRequestHandler.request()
        else:
            gui.addText(SITE_IDENTIFIER)
            return
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'link"><img src=([^ ]+).+?href="([^"]+).+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = re.sub('/w\\d+/', '/w342/', aEntry[0])
            sUrl2 = aEntry[1]
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2
            title = aEntry[2]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

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
    sPattern = '> \\d+ </span><a href="([^"]+).+?>([^<]+)</a></div></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page=([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'fsynopsis"><p>([^<]+)<br>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = 'link"><img src=([^ ]+).+?href="([^"]+).+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if 'no-poster.svg' not in aEntry[0]:
                sThumb = aEntry[0]
            else:
                sThumb = sThumb
            sUrl = aEntry[1]
            title = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
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

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'LI2"><a href="([^"]+)"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            title = sMovieTitle + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'code="([^"]+).+?</i>([^<]+).+?flag/([^ ]+).png'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sHost = aEntry[1].replace('www.', '')
            sHost = re.sub('\\..+', '', sHost).capitalize()
            if not HosterGui().checkHoster(sHost):
                continue

            sLang = aEntry[2].replace('default', '').upper()
            sUrl = URL_MAIN + 'll/captcha?hash=' + aEntry[0]
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('desc', desc)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequest = RequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)

    sHtmlContent = oRequest.request()
    sHosterUrl = oRequest.getRealUrl()

    if 'captcha' not in sHosterUrl:
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                   input_parameter_handler=input_parameter_handler)
    else:
        oParser = Parser()
        sPattern = 'src=([^ ]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getTokens():
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN + 'accueil')
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'name=_token value="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    token = aResult[1][0]
    sPattern = 'XSRF-TOKEN=([^;]+).+?.+?1seriestreaming_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]
    else:
        return False, 'none', 'none'

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + \
        '; 1seriestreaming_session=' + site_session + ';'
    return True, token, cook
