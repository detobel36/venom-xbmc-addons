# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import unicodedata
import requests
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import dialog, SiteManager
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'BuzzMonClick'
SITE_DESC = 'Films & Séries en Streaming de qualité entièrement gratuit.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = ('https://buzzmonclick.net/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMoviesSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Replay TV',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'divertissement/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Divertissement',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'tele-realite/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Télé-Réalité',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Documentaires', 'documentaires'], ['Divertissement', 'divertissement'],
             ['Infos/Magazines', 'infos-magazine'], ['Télé-Réalité', 'tele-realite']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="post-[0-9]+".+?<a class="clip-link.+?title="([^"]+)" href="([^"]+).+?img src="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            try:
                title = unicode(aEntry[0], 'utf-8')  # converti en unicode
                title = unicodedata.normalize(
                    'NFD', title).encode(
                    'ascii', 'ignore')  # vire accent
                # title = unescape(str(title))
                title = title.encode("utf-8")
            except NameError:
                title = aEntry[0]

            # mise en page
            title = title.replace(
                'Permalien pour', '').replace(
                '&prime;', '\'')
            title = re.sub(
                '(?:,)* (?:Replay |Video )*du ([0-9]+ [a-zA-z]+ [0-9]+)',
                ' (\\1)',
                title)
            title = re.sub(', (?:Replay|Video)$', '', title)
            sUrl = aEntry[1]
            sThumb = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'doc.png',
                sThumb,
                '',
                output_parameter_handler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'class="nextpostslink" rel="next" href="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'wp-block-button.+?(?:href=|src=)"([^"]+)".+?>(?:([^<]+)|)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sHost = aEntry[1]
            if sHost == "":
                sHost = aEntry[0].split('/')[2].split('.')[0]

            sUrl = aEntry[0]
            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    if 'forum-tv' in sUrl:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(sUrl, headers={'User-Agent': UA})
        sHtmlContent = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y)
                                  for x, y in s.cookies.items()])

        oParser = Parser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + \
                aResult[1][1] + "&ad_form_data=" + Quote(aResult[1][2])
            data += "&_Token%5Bfields%5D=" + \
                Quote(aResult[1][3]) + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])
            # Obligatoire pour validé les cookies.
            xbmc.sleep(6000)
            oRequestHandler = RequestHandler(
                'https://forum-tv.org/adslinkme/links/go')
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry(
                'Accept', 'application/json, text/javascript, */*; q=0.01')
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
                oHoster = False

                if 'replay.forum-tv.org' in sHosterUrl:
                    oRequestHandler = RequestHandler(sHosterUrl)
                    sHtmlContent = oRequestHandler.request()
                    sPattern = 'iframe.+?src="([^"]+)'
                    oParser = Parser()
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        sHosterUrl = aResult[1][0]
                    oHoster = HosterGui().checkHoster(sHosterUrl)

                elif 'dood.forum-tv.org' in sHosterUrl:
                    showDoodHosters(sMovieTitle, sHosterUrl)
                else:
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


def showDoodHosters(sMovieTitle, sUrl):
    gui = Gui()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a href="([^"]+)".+?value=\'([^\']+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sHost = aEntry[1]

            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sMovieTitle,
                output_parameter_handler)
