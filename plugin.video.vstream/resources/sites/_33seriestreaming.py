# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

SITE_IDENTIFIER = '_33seriestreaming'
SITE_NAME = '33 Séries'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = "https://33seriestreaming.rip/"
# Clone -> https://33streaming.co/

# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = (URL_MAIN, 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showMovies')
SERIE_GENRES = (URL_MAIN, 'showSeriesGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&titleonly=3&catlist[]=1&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&titleonly=3&catlist[]=2&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = Gui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films & Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = Gui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = Gui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl += sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showAlpha():
    import string

    oGui = Gui()
    oOutputParameterHandler = cOutputParameterHandler()
    listalpha = [str(i) for i in range(1, 10)]
    listalpha.extend(list(string.ascii_lowercase))
    for alpha in listalpha:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'catalog/' + alpha + '/')
        oGui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            str(alpha).upper() +
            '[/COLOR]',
            'az.png',
            oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = Gui()

    liste = ['Action', 'Aventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame',
             'Familial', 'Fantastique', 'Histoire', 'Horreur', 'Musique', 'Thriller', 'Téléfilm', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in liste:
        sTitle = igenre.capitalize()
        sUrl = URL_MAIN + 'film-streaming/genre/' + igenre + '.html'
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = Gui()

    liste = ['Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids',
             'Musique', 'Mystère', 'Reality', 'Romance', 'Science-Fiction & Fantastique', 'Soap', 'Thriller', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in liste:
        sTitle = igenre.capitalize()
        sUrl = URL_MAIN + 'series-streaming/genre/' + igenre + '.html'
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    import datetime
    oGui = Gui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'film-streaming/annee/' + sYear + '.html')
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    import datetime
    oGui = Gui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series-streaming/annee/' + sYear + '.html')
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()
    oParser = cParser()
    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sYear = oInputParameterHandler.getValue('sYear')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20 ', '+')
    sPattern = 'class=".+?grid-item.+?href="([^"]+).+?-src="([^"]+).+?alt="([^"]+)'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[2]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            sDisplayTitle = sTitle
            sDesc = ''
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series' in sUrl2 or '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
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
    oGui = Gui()
    oParser = cParser()
    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'grid-item" href="([^"]+).+?-src="([^"]*).+?(saison \\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[1]
            sSais = aEntry[2]

            sTitle = sMovieTitle + ' ' + sSais

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = Gui()
    oParser = cParser()
    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="pmovie__subtitle"'
    sEnd = 'pmovie__bottom-btns'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+).+?(épisode \\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl2 = aEntry[0]
            sEp = aEntry[1]

            sTitle = sMovieTitle + ' ' + sEp

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()

    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')
    isSerie = '-episode.html' in sUrl

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    sHtmlContent = oRequestHandler.request()

    if isSerie:  # episode d'une série
        sPattern = 'class="ser_pl" data-name="([^"]+)" data-hash="([^"]+)" data-episode="(\\d+)".+?">([^<]+).+?img src="([^\\.]+)'
    else:        # Film
        sPattern = 'class="nopl" data-id="(\\d+)" data-name="([^"]+)" data-hash="([^"]+).+?">([^<]+).+?img src="([^\\.]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sUrl2 = URL_MAIN + 'engine/ajax/controller.php'
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if isSerie:  # episode d'une série
                dataName = aEntry[0]
                dataHash = aEntry[1]
                dataEp = aEntry[2]
                pdata = 'mod=xfield_ajaxs&name=' + dataName + '&hash=' + dataHash + '&episode=' + dataEp
                # pdata = {'mod': 'xfield_ajax', 'hash': dataHash, 'episode': dataEp, 'name' :  dataName}
                pdata = str(pdata)
            else:
                dataId = aEntry[0]
                dataName = aEntry[1]
                dataHash = aEntry[2]
                # pdata = 'mod=xfield_ajax&hash=' + dataHash + '&id=' + dataId + '&name=' + dataName
                pdata = {'mod': 'xfield_ajax', 'hash': dataHash, 'id': dataId, 'name': dataName}
                pdata = str(pdata)

            sHost = aEntry[3].strip()
            if not cHosterGui().checkHoster(sHost):
                continue

            sLang = aEntry[4]
            if sLang:
                sLang = sLang.split('/')[-1:][0]

            sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang.upper(), sHost.capitalize())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oGui.addLink(SITE_IDENTIFIER, 'hostersLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def hostersLink():
    oGui = Gui()
    oParser = cParser()
    oInputParameterHandler = InputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    referer = oInputParameterHandler.getValue('referer')
    pdata = oInputParameterHandler.getValue('pdata')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    # Fonctionnement différent entre film et serie
    if 'episode' in pdata:
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
    else:
        # import string
        # boundary = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        # oRequest.addHeaderEntry('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundary%s' % boundary)
        import ast
        pdata = ast.literal_eval(pdata)
        oRequest.addMultipartFiled(pdata)

    sHtmlContent = oRequest.request()

    sPattern = '(http[^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
