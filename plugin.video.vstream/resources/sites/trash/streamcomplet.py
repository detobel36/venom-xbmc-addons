# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # 06/02/2021
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress  # , VSlog
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamcomplet'
SITE_NAME = 'StreamComplet'
SITE_DESC = 'Les meilleurs films en version française'

URL_MAIN = 'https://www2.stream-complet.me/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_MOVIE = ('http://', 'load')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['Drame', 'drame'], ['Fiction', 'fiction'], ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Horreur', 'horreur'], ['Musique', 'musical'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for sTitle, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'films/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)".+?<div class="(movies">(.+?)<|moviefilm">)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if (aEntry[0] == '/'):
                continue

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[4]

            # tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('/([0-9]+)/', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, output_parameter_handler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?<a class="page larger" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False


def showLinks():
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="player link" data-player="([^"]+)">.+?<span class="p-name">([^"]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sDisplayName = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, aEntry[1])

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayName, sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    # vimple redirect to ok or openload
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = 'url=([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

#
#
# Ancien code du site .xyz
# si retour en arriere
#
#

#    sPattern = '<iframe.+?src="(http(?:|s):\/\/media\.vimple\.me.+?f=([^"]+))"'
#    aResult = oParser.parse(sHtmlContent, sPattern)
#    if aResult[0]:

#        sUrl2 = aResult[1][0][0]
#
#        oRequestHandler = RequestHandler(sUrl2)
#        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0')
#        oRequestHandler.addHeaderEntry('Referer', sUrl)
#        sHtmlContent = oRequestHandler.request()
#
#        sPattern = '<iframe src="([^"]+)"'
#        aResult = oParser.parse(sHtmlContent, sPattern)
#
#        if aResult[0]:
#            sHosterUrl = 'https:' + aResult[1][0]
#            #VSlog(sHosterUrl)
#            oHoster = HosterGui().checkHoster(sHosterUrl)
#            if (oHoster):
#                oHoster.setDisplayName(sMovieTitle)
#                oHoster.setFileName(sMovieTitle)
#                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
#        else:
#            sHtmlContent = oParser.abParse(sHtmlContent, "<script>", "</script><script>")
#
#            sPattern = 'eval\s*\(\s*function(?:.|\s)+?{}\)\)'
#            aResult = oParser.parse(sHtmlContent, sPattern)
#            if aResult[0]:
#                sHtmlContent = cPacker().unpack(aResult[1][0])
#                sHtmlContent = sHtmlContent.replace('\\', '')
#                #VSlog(sHtmlContent)
#                code = re.search('(https://openload.+?embed\/.+?\/)', sHtmlContent)
#                if code:
#                    sHosterUrl = code.group(1)
#                   #VSlog(sHosterUrl)
#                   oHoster = HosterGui().checkHoster(sHosterUrl)
#                   if (oHoster):
#                       oHoster.setDisplayName(sMovieTitle)
#                       oHoster.setFileName(sMovieTitle)
#                       HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
