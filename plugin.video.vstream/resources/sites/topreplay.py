# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# plus vraiment le meme site
import re
import requests
import xbmc

from resources.lib.comaddon import dialog, Progress, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'topreplay'
SITE_NAME = 'TopReplay'
SITE_DESC = 'Replay TV'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenres')
REPLAYTV_TVSHOWS = (True, 'showTvShows')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')


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

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Nouveautés',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Genres',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_TVSHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_TVSHOWS[1],
        'Emissions TV',
        'tv.png',
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


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'main-menu'
    sEnd = '/ul'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1]
            if 'Accueil' in title:
                continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showTvShows():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'ÉMISSIONS TV'
    sEnd = '</div></div> </aside>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)</a>'
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
            title = aEntry[1]
            if 'Contactez' in title:
                continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'replay.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # &hellip'
    sPattern = '<article.+?href="([^"]+)">([^<]+).+?img.+?src="([^"]+).+?<div class="entry"><p>(.+?)Vous pouvez toujours regarder'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1]
            sThumb = aEntry[2]
            desc = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'replay.png',
                sThumb,
                desc,
                output_parameter_handler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'title>TopReplay - Page [\\d+] sur (\\d+).+?href="([^"]+)"\\s*>Chargez plus'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    # premiere page
    sPattern = 'href="([^"]+)"\\s*>Chargez plus'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="myButton" href="([^<]+)" target="_blank"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for sHosterUrl in aResult[1]:
            output_parameter_handler.addParameter('siteUrl', sHosterUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                sMovieTitle,
                'replay.png',
                sThumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    if 'mon-tele' in sUrl:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(sUrl, headers={'User-Agent': UA})
        sHtmlContent = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y)
                                  for x, y in s.cookies.items()])

        oParser = Parser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        from resources.lib import librecaptcha
        test = librecaptcha.get_token(
            api_key="6LezIsIZAAAAABMSqc7opxGc3xyCuXtAtV4VlTtN",
            site_url="https://mon-tele.com/",
            user_agent=UA,
            gui=False,
            debug=False
        )

        if aResult[0]:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + aResult[1][1] + "&ref=&f_n=" + aResult[1][2]\
                              + "&g-recaptcha-response=" + test + "&_Token%5Bfields%5D=" + Quote(aResult[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])

            oRequestHandler = RequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Length', len(data))
            oRequestHandler.addHeaderEntry(
                'Content-Type', "application/x-www-form-urlencoded")
            oRequestHandler.addHeaderEntry('Cookie', cookie_string)
            oRequestHandler.addParametersLine(data)
            sHtmlContent = oRequestHandler.request()

        oParser = Parser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + aResult[1][1] + "&ad_form_data="\
                              + Quote(aResult[1][2]) + "&_Token%5Bfields%5D=" + Quote(aResult[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])

            # Obligatoire pour validé les cookies.
            xbmc.sleep(15000)
            oRequestHandler = RequestHandler(
                'https://mon-tele.com/obtenirliens/links/go')
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Length', len(data))
            oRequestHandler.addHeaderEntry(
                'Content-Type', "application/x-www-form-urlencoded; charset=UTF-8")
            oRequestHandler.addHeaderEntry(
                'X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Cookie', cookie_string)
            oRequestHandler.addParametersLine(data)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'url":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)
    else:
        sHosterUrl = sUrl
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
