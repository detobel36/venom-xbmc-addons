# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import siteManager

SITE_IDENTIFIER = 'telecharger_streaming'
SITE_NAME = '[COLOR violet]Telecharger-streaming[/COLOR]'
SITE_DESC = 'films en streaming, Emissions en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_NEWS = (URL_MAIN + 'category/emissions-tv/', 'showMovies')
REPLAYTV_DIVERTISSEMENT = (URL_MAIN + 'category/emissions-tv/divertissements-telerealite/', 'showMovies')
REPLAYTV_INVESTIGATION = (URL_MAIN + 'category/emissions-tv/reportages-investigations/', 'showMovies')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Toutes les emissions', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_DIVERTISSEMENT[0])
    oGui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_DIVERTISSEMENT[1],
        'Emissions de Divertissements/Téléréalité',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_INVESTIGATION[0])
    oGui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_INVESTIGATION[1],
        'Emissions de Reportages/Investigations',
        'tv.png',
        output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = Gui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_MISC[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
        sPattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+)">.+?<p>.+?Synopsis :([^"]+)</p>'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sPattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+).+?<img.+?class="alignleft.+?src="([^"]+).+?Synopsis :(.+?)</p>'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if sSearch:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche
                sThumb = ""
                sDesc = aEntry[2].replace('</strong>', '')
            else:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]
                sThumb = aEntry[2]
                sDesc = aEntry[3].replace('</strong>', '')

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, output_parameter_handler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, output_parameter_handler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="next" href="([^"]+)".+?<\\/a><a class="last" href="https.+?page\\/(\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = GetAllLink(oRequestHandler.request())

    oParser = cParser()
    sPattern = '<span style="color: #ff00ff;">([^<]+?)</span>|<a href="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def GetAllLink(sHtmlContent):
    oParser = cParser()
    sPattern = '<p><span id="more-.+?"></span></p>(.+?)(?:<p><strong><span style="color: #00ffff;">|<h3><strong>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
