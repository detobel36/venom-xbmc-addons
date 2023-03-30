# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.util import cUtil
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
DEBUG = False

if DEBUG:

    import sys  # pydevd module need to be copied in Kodi\system\python\Lib\pysrc
    # sys.path.append('H:\Program Files\Kodi\system\Python\Lib\pysrc')

    try:
        import pydevd  # with the addon script.module.pydevd, only use `import pydevd`
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write(
            "Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

SITE_IDENTIFIER = 'novaflix'
SITE_NAME = 'Novaflix'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)


# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'films-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
# MOVIE_LIST = (URL_MAIN, 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'series-en-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN, 'showSeriesGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

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

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Années)',
        'annees.png',
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
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<span class="fal fa-film">'
    sEnd = '<li class="header__menu-main">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesGenres():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<span class="fal fa-television">'
    sEnd = '<li class="header__menu-main">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    import datetime
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + sYear)
        output_parameter_handler.addParameter('sYear', sYear)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    import datetime
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + sYear)
        output_parameter_handler.addParameter('sYear', sYear)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sYear = input_parameter_handler.getValue('sYear')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20 ', '+')
    sPattern = 'class=".+?grid-item.+?src="([^"]+).+?alt="([^"]+).+?href="([^"]+).+?>([^<]+).+?season">([^<]+).+?language">([^<]+)'
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            title = aEntry[1]
            sQual = aEntry[3]
            sLang = aEntry[4]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue  # Filtre de recherche

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang)
            desc = ''
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)

            if '/series' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
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
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
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
    sPattern = 'id="pagination".+?\\d+</span>.<a href="([^"]+)">(\\d+)(</a> *</div|<.+?(\\d+)</a> *</div)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        nextPage = aResult[1][0]
        sNextPage = nextPage[0]
        sNumberNext = nextPage[1]
        sNumberMax = nextPage[3]
        if not sNumberMax:
            sNumberMax = sNumberNext
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging
    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(
        sHtmlContent, 'Saisons de la serie', '/section')

    sPattern = 'grid-item".+?src="([^"]+).+?season">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN + aEntry[1]
            sSais = aEntry[1]

            title = sMovieTitle + ' ' + sSais

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sYear', sYear)
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
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="sect__content d-grid">'
    sEnd = '<div class="page__comments pmovie__stretch">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+).+?(Episode \\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl2 = aEntry[0]
            sEp = aEntry[1]

            title = sMovieTitle + ' ' + sEp

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sThumb', sThumb)
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
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')
    isSerie = '-episode.html' in sUrl

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    sHtmlContent = oRequestHandler.request()

    if isSerie:  # episode d'une série
        sPattern = 'class="ser_pl" data-id="([^"]+)" data-name="([^"]+)'
    else:        # Film
        sPattern = 'class="nopl" data-id="(\\d+)" data-name="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sLang = None
        sUrl2 = URL_MAIN + 'engine/ajax/getxfield.php'
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if isSerie:  # episode d'une série
                sUrl2 = URL_MAIN + 'engine/ajax/Season.php'
                dataId = aEntry[0]
                sHost = dataName = aEntry[1].strip()
                pdata = 'mod=xfield_ajax&id=' + dataId + '&name=' + dataName
                pdata = str(pdata)
                sLang = 'VF'  # tag la langue pour l'enchainement
                if '-' in sHost:
                    sHost, sLang = sHost.split('-')
            else:
                dataId = aEntry[0]
                sHost = dataName = aEntry[1].strip()
                pdata = 'mod=xfield_ajax&id=' + dataId + '&name=' + dataName
                pdata = str(pdata)

            if not HosterGui().checkHoster(sHost):
                continue

            sDisplayTitle = sMovieTitle
            if sLang:
                sDisplayTitle += '[%s] ' % sLang.upper()

            sDisplayTitle += ' [COLOR coral]%s[/COLOR]' % sHost.capitalize()

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'hostersLink',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def hostersLink():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7')

    if 'episode' in pdata:
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
    else:
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    sPattern = '(http[^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)
    gui.setEndOfDirectory()
