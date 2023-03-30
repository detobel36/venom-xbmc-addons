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
return False  # 13/02/21 WAAW en hoster


SITE_IDENTIFIER = 'serie_streaminghd'
SITE_NAME = 'Série-StreamingHD'
SITE_DESC = 'Séries en streaming vf, vostfr'

URL_MAIN = "https://planet-serie.com/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_TOP = (URL_MAIN + 'top-serie/', 'showSeries')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showSeries')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showSeries')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showSeries')
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

    output_parameter_handler.addParameter('siteUrl', SERIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_TOP[1],
        'Séries (Populaire)',
        'series.png',
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showSeries(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'fullstreaming"><img src="([^"]+).+?alt="([^"]+).+?xqualitytaftaf"><strong>([^<]+).+?href="([^"]+)" *>([^<]+)'
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

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb

            title = aEntry[1]
            saison = aEntry[2]
            siteUrl = aEntry[3]
            sLang = aEntry[4]

            if '{title}' in title:
                title = sLang
                sLang = ''
            elif 'VF - VOSTFR' in sLang:
                sLang = 'VF/VOSTFR'
            elif 'VF' in sLang:
                sLang = 'VF'
            elif 'VOSTFR' in sLang:
                sLang = 'VOSTFR'

            sDisplayTitle = ('%s %s (%s)') % (title, saison, sLang)

            output_parameter_handler.addParameter('siteUrl', siteUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                'series.png',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
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
    sPattern = '>([^<]+)</a>  <a href="([^"]+)">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    # Liens VF
    sHtmlTab = oParser.abParse(
        sHtmlContent,
        '<div class="VF-tab">',
        '<div id="fsElementsContainer">')
    if sHtmlTab:
        sPattern = '<a href="([^"]+)".+?</i> Episode *([0-9]+)'
        aResult = oParser.parse(sHtmlTab, sPattern)

        if aResult[0]:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VF[/COLOR]')

            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + ' Episode ' + aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    # Liens VOSTFR
    sHtmlTab = oParser.abParse(
        sHtmlContent,
        '<div class="VOSTFR-tab">',
        '<div class="VF-tab">')
    if sHtmlTab:

        sPattern = '<a href="([^"]+)".+?</i> Ep *([0-9]+)'
        aResult = oParser.parse(sHtmlTab, sPattern)

        if aResult[0]:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VOSTFR[/COLOR]')

            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + ' Episode ' + aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
