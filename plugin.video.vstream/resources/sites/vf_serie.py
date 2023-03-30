# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'vf_serie'
SITE_NAME = 'VF Série'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showSeries'
URL_SEARCH = (URL_MAIN + '?s=', FUNCTION_SEARCH)
URL_SEARCH_SERIES = (URL_SEARCH[0], FUNCTION_SEARCH)

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming-gratuit/', 'showSeries')
SERIE_VIEWS = (URL_MAIN + 'les-meilleurs-series-tv/', 'showSeries')
SERIE_NOTES = (URL_MAIN + 'series-tv-les-plus-populaires/', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showAlpha')


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
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NOTES[1],
        'Séries (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()
    oUtil = cUtil()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'option class="level-0" value="\\d+">(.+?)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry
            if 'Non' in title or 'Nom' in title:  # "Non classé" et "Nom de la catégorie"
                continue

            sUrl = URL_MAIN + 'category/' + \
                oUtil.CleanName(title).replace(' ', '-')

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0-9', '0-9'], ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'],
             ['H', 'h'], ['I', 'i'], ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'],
             ['P', 'p'], ['Q', 'q'], ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'],
             ['X', 'x'], ['Y', 'y'], ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'lettre/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
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

    if '/lettre/' in sUrl:
        sPattern = '</span></td>.+?href="([^"]+).+?src="([^"]+).+?strong>([^<]+)'
    else:
        sPattern = 'TPost C.+?href="([^"]+).+?src="([^"]+).+?Title">([^<]+).+?Description"><p>([^<]+)'

    oParser = Parser()
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

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+/', '/w342/', 'https:' + aEntry[1])
            if sThumb.startswith('/'):
                sThumb = 'https' + sThumb
            title = aEntry[2]

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            if '/lettre/' in sUrl:
                desc = ''
            else:
                desc = aEntry[3]

            sDisplayTitle = title

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
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
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '>([^<]+)</a><a class="next page-numbers" href="([^"]+)">Next'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    desc = ''
    try:
        sPattern = 'Description"><p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = 'data-tab=.+?pan>([^<]+)|Num">([^<]+).+?src="([^"]+).+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sSaison = aEntry[0]
                title = sMovieTitle + ' Saison ' + sSaison
                sDisplayTitle = title

                sUrlSaison = sUrl + "?sNumSaison=" + sSaison
                output_parameter_handler.addParameter('siteUrl', sUrlSaison)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showSxE',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sUrl, sNumSaison = sUrl.split('?sNumSaison=')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    desc = ''
    try:
        sPattern = 'Description"><p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = 'data-tab=.+?pan>([^<]+)|Num">([^<]+).+?src="([^"]+).+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sSaison = aEntry[0]
            else:
                if sSaison != sNumSaison:
                    continue
                sEpisode = aEntry[1]
                sThumbEp = re.sub('/w\\d+/', '/w342/', 'https:' + aEntry[2])
                sUrl = aEntry[3]
                sTitleEp = aEntry[4]

                title = sMovieTitle + ' Episode ' + sEpisode
                sDisplayTitle = title

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showHoster',
                    sDisplayTitle,
                    '',
                    sThumbEp,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'class="TPlayerTb.+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            oRequestHandler = RequestHandler(aEntry)
            sHtmlContent = oRequestHandler.request()
            sPattern = '<iframe.+?src="([^"]+)'
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
