# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'bd_streams'
SITE_NAME = 'BD Streams'
SITE_DESC = 'Match de foot en direct'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_LIVE = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')


def load():
    oGui = Gui()
    sUrl = URL_MAIN

    oParser = cParser()
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
            oGui.addText(SITE_IDENTIFIER)
        else:
            oOutputParameterHandler = OutputParameterHandler()
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sTitle = aEntry[1]
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sTitle)
                oGui.addDir(SITE_IDENTIFIER, 'showLink', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = Gui()
    oOutputParameterHandler = OutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'load', 'Football', 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showLink():
    oGui = Gui()
    oParser = cParser()

    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

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
            HosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()
