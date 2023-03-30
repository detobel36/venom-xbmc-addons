# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser


SITE_IDENTIFIER = 'bd_streams'
SITE_NAME = 'BD Streams'
SITE_DESC = 'Match de foot en direct'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_LIVE = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')


def load():
    gui = Gui()
    sUrl = URL_MAIN

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<li class='archivedate'><a href='(.+?)'>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sUrl = aResult[1][0]
        sPattern = "<h3 class='post-title entry-title'><a href='(.+?)'>(.+?)</a>"
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if not aResult[0]:
            gui.addText(SITE_IDENTIFIER)
        else:
            output_parameter_handler = OutputParameterHandler()
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                title = aEntry[1]
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('desc', title)
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showLink',
                    title,
                    'genres.png',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SPORT_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'load',
        'Football',
        'genres.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    sPattern = 'player = new Clappr\\.Player.+?source: "([^"]+)'
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sHosterUrl = aResult[1][0].strip()
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, '')

    gui.setEndOfDirectory()
