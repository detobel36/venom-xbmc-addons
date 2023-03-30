# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# disable 03/08/2020
from resources.lib.util import cUtil, Unquote
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Progress  # , VSlog
import re
import base64
return False


SITE_IDENTIFIER = 'filmstreaming'
SITE_NAME = 'Film Streaming'
SITE_DESC = 'Films en streaming'
URL_MAIN = 'https://www.filmstreamingvf.watch/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + '?v_sortby=views&v_orderby=desc', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (URL_MAIN, 'AlphaSearch')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')


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
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Ordre alphabétique)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sSearch = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sSearch)
        gui.setEndOfDirectory()
        return


def showSearchOld():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        showSearchMovies(sSearchText)
        gui.setEndOfDirectory()
        return


def showSearchMovies(sSearch=''):
    gui = Gui()

    sSearch = Unquote(sSearch)
    sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
    pdata = 'nonce=3293a1b68c&action=tr_livearch&trsearch=' + \
        sSearch  # la valeur nonce change

    oRequest = RequestHandler(sUrl2)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addParameters('Referer', URL_MAIN)
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()
    sPattern = '<div class="TPost B">.+?<a href="([^"]+)">.+?<img src="([^"]+)".+?<div class="Title">([^<]+)</div>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = re.sub('/w\\d+', '/w342', aEntry[1], 1)
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            title = aEntry[2]

            # filtre search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch, title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
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


def showGenres():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(MOVIE_NEWS[0])
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(
        sHtmlContent,
        'class=Title>Film Streaming Par Genres</div>',
        '</div></aside>')

    sPattern = '<li class="cat-item cat-item-.+?"><a href=([^>]+)>([^<]+)</a>([^<]+)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1] + aEntry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def AlphaSearch():
    gui = Gui()

    for i in range(0, 27):
        if (i == 0):
            sLetter = '0-9'
        else:
            sLetter = chr(64 + i)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'letters/' + sLetter + '/page/1/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showList',
            'Lettre [COLOR coral]' +
            sLetter +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class=Num>.+?href=(.+?) class=MvTbImg.+?src=([^ ]+).+?<strong>([^<]+)</strong> </a></td><td>([^<]*)<.+?class=Qlty>([^<]+)<'
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

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+', '/w342', aEntry[1], 1)
            if sThumb.startswith('/'):
                sThumb = 'http:' + sThumb
            title = aEntry[2]
            sYear = aEntry[3]
            sQual = aEntry[4]

            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        if aResult:
            sPattern = 'page/(\\d+)/'
            aResult = oParser.parse(sUrl, sPattern)
            if aResult[0]:
                number = int(aResult[1][0]) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', re.sub(
                    'page/(\\d+)/', 'page/' + str(number) + '/', sUrl))
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showList',
                    '[COLOR teal]Page ' +
                    str(number) +
                    ' >>>[/COLOR]',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(
        sHtmlContent,
        'MovieList Rows',
        '</body></html>')
    sPattern = 'class=Image>.+?src=([^ ]+) .+?class=Qlty>([^<]+).+?href=([^>]+)><div class=Title>([^<]+).+?Description><p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = re.sub('/w\\d+', '/w342', aEntry[0], 1)
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb

            sQual = aEntry[1]
            sUrl = aEntry[2]
            title = aEntry[3]
            desc = aEntry[4]

            sDisplayTitle = ('%s [%s]') % (title, sQual)

            # filtre search
            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch, title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                number +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="*([^">]+)"*>Next'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # qual, lang
    sPattern = 'class=AAIco-language>([^<]+)</p><p class=AAIco-dns>.+?<p class=AAIco-equalizer>([^<]+)<'
    aResult1 = re.findall(sPattern, sHtmlContent, re.DOTALL)
    # VSlog(str(aResult1)) #Commenter ou supprimer cette ligne une fois fini

    sPattern2 = '<div id=VideoOption\\d+ class="*Vid.+?>([^<]+)</div>'
    aResult2 = re.findall(sPattern2, sHtmlContent, re.DOTALL)
    # VSlog(str(aResult2)) #Commenter ou supprimer cette ligne une fois fini

    aResult = zip(aResult2, [x[1] + '] (' + x[0] for x in aResult1])
    # VSlog(str(aResult)) #Commenter ou supprimer cette ligne une fois fini

    if (aResult):
        for aEntry in aResult:
            sHtmlContent = base64.b64decode(aEntry[0])
            # VSlog(sHtmlContent)

            sHosterUrl = ''
            # Pour Python 3, besoin de repasser en str.
            try:
                sUrl = re.search('src="([^"]+)"', sHtmlContent)
            except TypeError:
                sUrl = re.search('src="([^"]+)"', sHtmlContent.decode())
            sHosterUrl = sUrl.group(1)

            oRequestHandler = RequestHandler(sHosterUrl)
            sHtmlContent = oRequestHandler.request()
            sUrl = re.search('<iframe id="iframe" src="([^"]+)"', sHtmlContent)
            if sUrl:
                sHosterUrl = sUrl.group(1)

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle + ' [' + aEntry[1] + ')')
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
