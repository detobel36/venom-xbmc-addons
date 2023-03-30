# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import addon, SiteManager
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'streamingdivx'
SITE_NAME = 'Streamingdivx'
SITE_DESC = 'Films VF en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?q=', 'showMovies')
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Séries (Derniers ajouts)',
        'news.png',
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

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Comédie-dramatique', 'comedie-dramatique'],
             ['Comédie-musicale', 'comedie-musicale'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Epouvante Horreur', 'epouvante-horreur'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science-fiction', 'science-fiction'], ['Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films/' + sUrl)
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
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="short-images.+?href="([^"]+)" title="([^"]+)" class=.+?<img src="([^"]+).+?(?:<div class="short-content">|<a href=.+?qualite.+?>(.*?)</a>.+?<a href=.+?langue.+?>(.*?)</a>)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            title = aEntry[1].replace(
                'Streaming',
                '').replace(
                'streaming',
                '').replace(
                'série',
                '')
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            # pb d'url sur les images lors des recherches
            sThumb = sThumb.replace('wwww.', 'www.')

            sQual = ''
            if aEntry[3]:
                sQual = aEntry[3]

            sLang = ''
            if aEntry[4]:
                sLang = aEntry[4]

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang.upper())

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sQual', sQual)

            if 'series/' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

    if not sSearch:  # une seule page par recherche
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
    oParser = Parser()
    sPattern = ">([^<]+)</a></div></div><div class=\"col-lg-1 col-sm-2 col-xs-2 pages-next\"><a href=['\"]([^'\"]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page-([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        if sNextPage.startswith('/'):
            sNextPage = URL_MAIN[:-1] + sNextPage

        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # syno
    desc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = '<div class="short-images.+?<a href="([^"]+)" class="short-images.+?<img src="([^"]+)" alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            title = aEntry[2].replace(
                'Streaming',
                '').replace(
                'streaming',
                '') .replace(
                'Voir la série',
                '').replace(
                'en  VF et VOSTFR',
                '')

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
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
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(
        sHtmlContent,
        '<div class="episode-list">',
        'Series similaires')

    sPattern = '<div class="sai.+?<a href="([^"]+)".+?<span>(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl

            title = aEntry[1]

            sDisplayTitle = ('%s %s') % (sMovieTitle, title)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    # streamer.php?p=169&c=V1RJeGMxcHVSbmhhUnpGMFltNU9kMWxYVW5sWlVUMDk=
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sUrl = oRequest.getRealUrl()

    # syno
    desc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern2 = 'class="stream.*?">.+?data-num="([^"]+)" data-code="([^"]+)".+?<i class="([^"]+)".+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern2)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sHost = aEntry[2].replace(
                'server player-',
                '').replace(
                'télécharger sur ',
                '').capitalize()

            # Filtre des host
            oHoster = HosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sLang = aEntry[3].split(
                '/')[-1].replace('.png', '').replace('?ver=41', '').upper()

            sDisplayTitle = (
                '%s (%s) [COLOR %s]%s[/COLOR]') % (sMovieTitle, sLang, sColor, sHost)

            output_parameter_handler.addParameter('datanum', aEntry[0])
            output_parameter_handler.addParameter('datacode', aEntry[1])
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHost)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sReferer = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    datanum = input_parameter_handler.getValue('datanum')
    datacode = input_parameter_handler.getValue('datacode')

    sUrl = URL_MAIN + 'streamer.php?p=' + datanum + '&c=' + datacode

    oRequest = RequestHandler(sUrl)
    # oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sReferer)
    sHtmlContent = oRequest.request()

    sHosterUrl = oRequest.getRealUrl()
    if URL_MAIN in sHosterUrl:
        oParser = Parser()
        sPattern2 = 'href="(.+?)"'
        sHosterUrl = oParser.parse(sHtmlContent, sPattern2)[1][0]

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
