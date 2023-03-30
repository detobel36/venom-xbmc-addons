from resources.lib.comaddon import Progress  # , VSlog
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False  # Désactivé le 08/04/2020

# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#


SITE_IDENTIFIER = 'replaytvstreaming_com'
SITE_NAME = 'Replay Tv Streaming'
SITE_DESC = 'Replay TV'

URL_MAIN = 'https://replaytvstreaming.com/'

MOVIE_MOVIE = (URL_MAIN + 'film', 'showMovies')

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=',
    'showMovies')
URL_SEARCH_MISC = (
    URL_MAIN +
    'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Replay (Derniers ajouts)',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Replay (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sSearchText = sSearchText.replace(' ', '+')

        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Emissions et Magazines', URL_MAIN + 'emission-magazine'])
    liste.append(['Documentaires', URL_MAIN + 'documentaire'])
    liste.append(['Spectacles', URL_MAIN + 'spectacle'])
    liste.append(['Sports', URL_MAIN + 'sport'])
    liste.append(['Téléfilms Fiction', URL_MAIN + 'telefilm-fiction'])
    liste.append(['Films', URL_MAIN + 'film'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
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
        sUrl = URL_SEARCH[0] + sSearch

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)

        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="item-box"><a class="item-link" href="([^"]+)"><div class="item-img"><img src="([^"]+)".+?<div class="item-title">([^<]+)<'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="item-box"><a class="item-link" href="([^"]+)">.+?<img src="([^"]+)".+?<div class="item-title">([^<]+)<\\/div><div class="item-info clearfix">([^<]+)<\\/div>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            title = aEntry[2]
            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            desc = ''
            if len(aEntry) > 3:
                desc = aEntry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="([^"]+)">SUIVANT<\\/a>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showLinks(page, video):
    sUrl = 'http://replaytvstreaming.com/engine/ajax/re_video_part.php?block=video&page=' + \
        page + '&id=' + video

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url = sHtmlContent
    return url


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<div id="video_[0-9]+" class="epizode re_poleta.+?" data-re_idnews="([^"]+)" data-re_xfn="video" data-re_page="([^"]+)">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTest = ''

    if aResult[0]:
        for aEntry in aResult[1]:

            sPage = aEntry[1]
            sVideoID = aEntry[0]
            sHosterUrl = showLinks(sPage, sVideoID)
            sHosterUrl = cUtil().unescape(sHosterUrl)

            title = aEntry[2]

            if 'Lecteur' not in title and sTest != title:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR olive]' +
                    title +
                    '[/COLOR]')
                sTest = title

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)
    else:
        sPattern = '<div class="playe.+?" data-show_player="video"><iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHosterUrl = aResult[1][0]
            sHosterUrl = cUtil().unescape(sHosterUrl)

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
