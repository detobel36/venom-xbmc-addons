# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'stream_complet'
SITE_NAME = 'Stream Complet'
SITE_DESC = 'Voir les meilleurs films en version française'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?keymovies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'series-streaming/?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SERIES_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche Films ', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche Séries', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIES_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearchSerie():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    # ajout: documentaire, fantastique, western
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'documentaire', 'drame', 'fantastique', 'guerre',
                  'historique', 'horreur', 'musical', 'policier', 'romance', 'science-fiction', 'thriller', 'western']

    url1g = URL_MAIN + 'film/'

    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:
        sUrl = url1g + igenre + '/'
        sTitle = igenre.capitalize()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="moviefilm">.+?href="([^"]+).+? src="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sTitle = sTitle.replace('streaming VF', '')

            if URL_SEARCH_MOVIES[0] in sUrl:
                if '/serie' in sUrl2:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, '', sThumb, '', output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPagination = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', sPagination, output_parameter_handler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="nextpostslink.+?href="([^"]+).+?class="last.+?href=.*?page.([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][1]
        sNextPage = aResult[1][0][0]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPagination = sNumberNext + '/' + sNumberMax
        return sNextPage, sPagination
    return False, False


def showSaison():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    oParser = cParser()
    sPattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = oParser.parse(sHtmlContent, sPattern)
    if aResultDesc[0] is True:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResultDesc[1][0])

    sPattern = '(\\d+)<\\/a><\\/h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sNumSaison = aEntry[0]
            sSaison = 'Saison ' + aEntry[0]
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison

            sTitle = sMovieTitle + sSaison
            sDisplayTitle = sTitle + '' + sSaison
            output_parameter_handler.addParameter('siteUrl', sUrlSaison)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showSXE', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

    oGui.setEndOfDirectory()


def showSXE():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = 'id="saison-' + sNumSaison
    sEnd = '<div id="alt">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">épisode (\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            Ep = aEntry[1]
            Saison = 'Saison ' + sNumSaison
            sTitle = sMovieTitle + Saison + ' Episode ' + Ep

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    oParser = cParser()
    sPattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = oParser.parse(sHtmlContent, sPattern)
    if aResultDesc[0] is True:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResultDesc[1][0])

    sPattern = 'class="player link" data-player="([^"]+).+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sLang = aEntry[1]
            sHostname = aEntry[2].capitalize()
            sDisplayName = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sTitle, sLang, sHostname)
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteReferer', sUrl)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHostname)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayName, sThumb, sDesc, output_parameter_handler)

    sPattern = '(?:class="players">|</a>)\\s*<a href="([^"]+).+?<li class="player".+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    # avec href="([^"]+)"; '"' à garder  pour éviter oublie avec test reg101
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sLang = aEntry[1]

            sHostname = aEntry[2].lower()
            sHostname = sHostname.capitalize()
            sDisplayTitle = '%s (%s) [COLOR coral]%s[/COLOR]' % (sTitle, sLang, sHostname)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteReferer', sUrl)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHostname)
            oGui.addLink(SITE_IDENTIFIER, 'showHostersDL', sDisplayTitle, sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    oHosterGui = HosterGui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    siteReferer = input_parameter_handler.getValue('siteReferer')

    if 'sstatic' in sUrl:
        sUrl1 = sUrl + '/ajax'
        oRequestHandler = RequestHandler(sUrl1)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'url":"([^"]+)'  # tjrs doodstream
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHosterUrl = aResult[1][0]
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Referer', siteReferer)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'url=([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                oHoster = oHosterGui.checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHostersDL():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sLang = input_parameter_handler.getValue('sLang')

    sDisplayName = ('%s (%s)') % (sMovieTitle, sLang)

    if 'shortn.co' in sUrl:
        bvalid, shost = Hoster_shortn(sUrl)
        if bvalid:
            sHosterUrl = shost
            oHoster = HosterGui().checkHoster(sHosterUrl)

            if oHoster:
                oHoster.setDisplayName(sDisplayName)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sHosterUrl = sUrl
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sDisplayName)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


def Hoster_shortn(url):
    shost = ''
    url = url.replace('%22', '')
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    sPattern = "type.*?name=.*?value='([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        token = aResult[0]
        data = '_token=' + token
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParametersLine(data)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'href="([^"]+).+?target="_blank'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            shost = aResult[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
