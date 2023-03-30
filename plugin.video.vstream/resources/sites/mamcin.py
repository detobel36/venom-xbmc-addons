# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# jordigarnacho

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'mamcin'
SITE_NAME = 'Mamcin'
SITE_DESC = 'Plus belle la vie'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_REPLAYTV = (True, 'load')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = (URL_MAIN, 'showMovies')


# loader function
def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Plus Belle La Vie', 'news.png', output_parameter_handler)

    oGui.setEndOfDirectory()


# genre definition
def showGenres():
    oGui = Gui()

    liste = []
    liste.append(['News', URL_MAIN + 'non-classe/'])

    output_parameter_handler = OutputParameterHandler()
    for sTitle, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


# function to extract episodes
def showMovies(sSearch=''):
    oGui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="featured-image"><a href="([^"]+)" title="([^"]+)"><img width=".+?" height=".+?" src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # first post filter
            if (str(aEntry[2]) != "https://www.mamcin.com/wp-content/uploads/2017/10/plus-belle-la-vie-episode-suivant-en-avance.jpg"):
                sUrl = aEntry[0]
                sTitle = aEntry[1]
                sThumb = aEntry[2]

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', sTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sPaging = re.search('page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


# search the next page
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class="previous"><a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


# search hosts
def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    # add dailymotion sources
    sPattern = '<iframe.+?src="(.+?)?logo=0&info=0"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if not aEntry.startswith('http'):
                sHosterUrl = 'https:' + aEntry
            else:
                sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # add sendvid sources
    sPattern = '<(?:source|iframe).+?src="(.+?)" width'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if not sHosterUrl.startswith('http'):
                sHosterUrl = 'https:' + aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
