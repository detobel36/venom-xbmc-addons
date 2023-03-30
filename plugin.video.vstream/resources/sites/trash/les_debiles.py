# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'les_debiles'
SITE_NAME = 'Les Débiles'
SITE_DESC = 'Vidéos drôles, du buzz, des fails et des vidéos insolites'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN, 'showMovies')
URL_SEARCH_MISC = (URL_MAIN, 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenre')
NETS_CATS = (True, 'showGenres')


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

    output_parameter_handler.addParameter('siteUrl', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos du net',
        'buzz.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', NETS_CATS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_CATS[1],
        'Vidéos (Catégories)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()

    liste = [['Nouveautés', 'videos-s0-1'], ['Top Vues', 'videos-s1-1'], ['Top Vote', 'videos-s2-1'],
             ['Hit Parade', 'videos-s5-1'], ['Fatality', 'videos-s7-1'], ['Vidéos Longues', 'videos-s3-1']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + sUrl + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN + 'categories.html')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li><a href="([^>]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        idx = sSearch.rfind("/") + 1
        sUrl = sSearch[:idx] + "".join([i for i in sSearch[idx:] if i.isalpha() or i in [
                                       " ", "/"]]).replace(" ", "-") + '-s0-r1.html'.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('&gt;&gt;', 'suivante')

    sPattern = 'class="blockthumb">.+?class="imageitem" src="([^"]+)".+?class="titleitem"><a href="([^"]+)">(.+?)</a>'

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
            sUrl = aEntry[1]
            title = aEntry[2]

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
            sPaging = re.search('-([0-9]+).html', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href="([^"]+)">suivante</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # lien direct mp4
    sPattern = "<source src='([^']+)' type='video/mp4'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    # lien dailymotion
    if not aResult[0]:
        sPattern = 'src="([^"]+)\\?.+?" allowfullscreen></iframe>'
        aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Certains URL "dailymotion" sont écrits : //www.dailymotion.com
            if sHosterUrl[:4] != 'http':
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)
    else:
        # play premium vid
        vidpremium = sHtmlContent.find('alt="Video Premium"')
        if vidpremium != -1:
            sPattern = "window.location.href = '([^']+)';"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0].replace(
                    'download-', '').replace('.html', '')

                sHosterUrl = 'http://videos.lesdebiles.com/' + sHosterUrl + '.mp4'

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)
        else:
            gui.addText(SITE_IDENTIFIER, '(Video non visible)')

    gui.setEndOfDirectory()
