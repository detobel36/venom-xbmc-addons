# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'mysteriam'
SITE_NAME = 'Mysteriam'
SITE_DESC = 'Documentaire streaming '

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

DOC_DOCS = (True, 'load')
DOC_NEWS = (URL_MAIN + 'documents-videos.html', 'showMovies')
DOC_GENRES = (
    URL_MAIN +
    'videos-documentaires/categories-videos.html',
    'showGenres')


def load():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="item-title hasTooltip" title="([^"]+).+?href="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = URL_MAIN + aEntry[1]
            title = aEntry[0]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'doc.png',
                '',
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '', 'Derniers Docus')
    sPattern = 'Thumbnail Image -->.+?title="([^"]+).+?src="([^"]+).+?href="([^"]+).+?src="([^"]+).+?info-description">([^<]+)'

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

            sMedia = aEntry[1]
            if 'video.png' not in sMedia:
                continue
            title = aEntry[0]
            sUrl2 = URL_MAIN[:-1] + aEntry[2]
            sThumb = URL_MAIN[:-1] + aEntry[3]
            desc = aEntry[4]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
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

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'pagenav">[0-9]+</span></li><li><a title="(\\d+)" href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberNext = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sPaging = sNumberNext
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

    sPattern = '<iframe.+?src="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in list(set(aResult[1])):
            sHosterUrl = str(aEntry).replace('?&rel=0', '')

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
