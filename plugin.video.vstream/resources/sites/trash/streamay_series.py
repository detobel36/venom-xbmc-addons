# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'streamay_series'
SITE_NAME = 'StreamAy Séries'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = "https://www.sakstream.site/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_LAST = (URL_MAIN, 'showLastEpisode')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showSeries')
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

    output_parameter_handler.addParameter('siteUrl', SERIE_LAST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LAST[1],
        'Episodes (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        showSeries(URL_SEARCH[0] + sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'action'], [
            'Action & aventure', 'action-et-adventure'], [
                'Animation', 'animation'], [
                    'Aventure', 'aventure'], [
                        'Biopic', 'biopic'], [
                            'Comédie', 'comaedie'], [
                                'Comédie dramatique', 'drame-comaedie'], [
                                    'Documentaire', 'documentaire'], [
                                        'Drame', 'drame'], [
                                            'Epouvante-Horreur', 'epouvante-horreur'], [
                                                'Famille', 'famille'], [
                                                    'Fantastique', 'fantastique'], [
                                                        'Guerre', 'guerre'], [
                                                            'Horreur', 'horreur'], [
                                                                'Policier', 'policier'], [
                                                                    'Romance', 'romance'], [
                                                                        'Thriller', 'thriller'], [
                                                                            'Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'series-vf/genres/' + sUrl + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showLastEpisode():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'left fx-1.+?href="([^"]+).+?izobritenie">([^<]+).+?span>([^<]+).+?<span>([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            title = aEntry[1] + ' S' + aEntry[2] + ' E' + aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'series',
                '',
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # for the search
    sHtmlContent = sHtmlContent.replace(' js-tip', '')

    sPattern = 'th-in" href="([^"]+).+?src="([^"]+)" alt="([^"]+)'
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

            sUrl = aEntry[0]
            title = aEntry[2]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            output_parameter_handler.addParameter('siteUrl', sUrl)
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
    sPattern = 'navigation">.+?</span><a href="([^"]+).+?>([^<]+)</a></span><span class="pnext">'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'full-text clearfix">([^<]*)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = 'th-item">.+?href="([^"]+).+?src="([^"]+).+?nowrap">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            title = sMovieTitle + ' ' + aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
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

    sPattern = '([^"]+)"><div class="fsa-ep">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' ' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-url="([^"]+).+?<img src="/icon/([^/]+).png'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            sLang = aEntry[1].upper()

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle + ' (' + sLang + ')')
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
