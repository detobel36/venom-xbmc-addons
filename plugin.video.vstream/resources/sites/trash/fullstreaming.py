# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

# site HS le 02/10/18
from resources.lib.comaddon import progress
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'fullstreaming'
SITE_NAME = 'Full Streaming'
SITE_DESC = 'Films et Séries en streaming HD'

URL_MAIN = 'https://one4streaming.cc/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN, '')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_NEWS = (URL_MAIN + 'serie-tv/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-tv/', 'showMovies')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries', 'news.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()
    oParser = cParser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-13.+?"><a href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace('-720p', ' [720p]').replace('-1080p', ' [1080p]')
            sUrl = URL_MAIN[:-1] + aEntry[0]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = Gui()

    for i in reversed(xrange(1964, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + '?filter-by=films&anne=' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="mt-.+?href="([^<]+)".+?src="([^<]+)" alt="([^<]+) Streaming.+?".+?class="calidad2">(.+?)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2].replace(' - Saison', ' Saison')
            sQual = aEntry[3]
            sDesc = ''

            # Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '-saison-' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^<]+)" >Suivant</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # réécriture des liens beclic pour recuperer les bons hosters
    sHtmlContent = sHtmlContent.replace('https://beclic.pw/op.php?s=', 'https://oload.site/embed/')
    sHtmlContent = sHtmlContent.replace('http://beclic.pw/op.php?s=', 'https://oload.site/embed/')
    sHtmlContent = sHtmlContent.replace('https://beclic.pw/jaja.php?s=', 'https://jawcloud.co/embed-')
    sHtmlContent = sHtmlContent.replace('https://beclic.pw/rapid.php?s=', 'https://www.rapidvideo.com/e/')

    sPattern = '<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if 'jawcloud' in sHosterUrl:
                sHosterUrl = sHosterUrl + '.html'
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(' class="selected"', '')
    # réécriture des liens beclic
    sHtmlContent = sHtmlContent.replace('https://beclic.pw/op.php?s=', 'https://oload.site/embed/')
    sHtmlContent = sHtmlContent.replace('http://beclic.pw/op.php?s=', 'https://oload.site/embed/')

    sEpisodesList = {}
    sPattern = '<a href="#(div[0-9]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for i in aResult[1]:
            sEpisodesList[i[0]] = i[1]

    sPattern = '<div id="(div[^"]+)">.+?<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            div = aEntry[0]
            sEpisodes = sEpisodesList.get(div, "Error")
            sEpisodes = sEpisodes.replace('Épisodes ', 'E')

            sMovieTitle2 = sMovieTitle + sEpisodes

            sHosterUrl = aEntry[1]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle2)
                oHoster.setFileName(sMovieTitle2)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
