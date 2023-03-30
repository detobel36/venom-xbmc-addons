# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# jordigarnacho

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'mamcin'
SITE_NAME = 'Mamcin'
SITE_DESC = 'Plus belle la vie'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_REPLAYTV = (True, 'load')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = (URL_MAIN, 'showMovies')


# loader function
def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Plus Belle La Vie',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


# genre definition
def showGenres():
    gui = Gui()

    liste = []
    liste.append(['News', URL_MAIN + 'non-classe/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


# function to extract episodes
def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="featured-image"><a href="([^"]+)" title="([^"]+)"><img width=".+?" height=".+?" src="([^"]+)'

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

            # first post filter
            if (str(
                    aEntry[2]) != "https://www.mamcin.com/wp-content/uploads/2017/10/plus-belle-la-vie-episode-suivant-en-avance.jpg"):
                sUrl = aEntry[0]
                title = aEntry[1]
                sThumb = aEntry[2]

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sPaging = re.search('page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


# search the next page
def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<li class="previous"><a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


# search hosts
def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

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
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

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
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
