# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'cine974'
SITE_NAME = 'Ciné 974'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'streaming/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'src="([^"]+)" alt="([^"]+)" class="sc.+?synop">([^<]*).+?href="([^"]+)">Regarder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
        gui.setEndOfDirectory()
        return

    total = len(aResult[1])
    progress_ = Progress().VScreate(SITE_NAME)
    output_parameter_handler = OutputParameterHandler()
    for aEntry in aResult[1]:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break

        sThumb = aEntry[0]
        if sThumb.startswith('/'):
            sThumb = URL_MAIN[:-1] + sThumb
        title = aEntry[1]
        desc = aEntry[2]
        sUrl2 = aEntry[3]
        if sUrl2.startswith('/'):
            sUrl2 = URL_MAIN[:-1] + sUrl2

        output_parameter_handler.addParameter('siteUrl', sUrl2)
        output_parameter_handler.addParameter('sMovieTitle', title)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('desc', desc)

        gui.addMovie(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    progress_.VSclose(progress_)

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
    sPattern = '>(\\d+)</a></li><li><a href="([^"]+)"><i class="fa fa-angle-right'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('p=([0-9]+)', aResult[1][0][1]).group(1)
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
    sPattern = '<iframe width="100%" height="400" src="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            link = re.sub('.+?embed/', '', aEntry)
            link = link.replace('?rel=0', '')
            sHosterUrl = 'https://www.youtube.com/watch?v=' + link

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
