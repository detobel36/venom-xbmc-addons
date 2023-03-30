# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.comaddon import progress, addon
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'tfarjo'
SITE_NAME = 'Tfarjo'
SITE_DESC = 'Films & Séries en streaming VO | VF | VOSTFR'

# URL_MAIN = 'https://www5.tfarjo.ws/'
# URL_MAIN = 'https://www.filmz.cc/'
URL_MAIN = 'https://www.tfarjo.cc/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series', 'showSeries')
# SERIE_VFS = (URL_MAIN + 'series/vf', 'showSeries')
# SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr', 'showSeries')  # pas fiable et pareil que dernier ajouts

URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'


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
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sText = sSearchText
        showMovies(sText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'films/genre/action'])
    liste.append(['Animation', URL_MAIN + 'films/genre/animation'])
    liste.append(['Arts Martiaux', URL_MAIN + 'films/genre/arts-Martiaux'])
    liste.append(['Aventure', URL_MAIN + 'films/genre/aventure'])
    liste.append(['Biopic', URL_MAIN + 'films/genre/biopic'])
    liste.append(['Comédie', URL_MAIN + 'films/genre/comédie'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'films/genre/comédie-dramatique'])
    liste.append(['Comédie Musicale', URL_MAIN + 'films/genre/comédie-musicale'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/crime'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/dance'])
    liste.append(['Documentaire', URL_MAIN + 'films/genre/documentaire'])
    liste.append(['Drame', URL_MAIN + 'films/genre/drame'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'films/genre/epouvante-horreur'])
    liste.append(['Erotique', URL_MAIN + 'films/genre/erotique'])
    liste.append(['Espionnage', URL_MAIN + 'films/genre/espionnage'])
    liste.append(['Famille', URL_MAIN + 'films/genre/famille'])
    liste.append(['Fantastique', URL_MAIN + 'films/genre/fantastique'])
    liste.append(['Guerre', URL_MAIN + 'films/genre/guerre'])
    liste.append(['Historique', URL_MAIN + 'films/genre/historique'])
    liste.append(['Musical', URL_MAIN + 'films/genre/musical'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/mystere'])
    liste.append(['Policier', URL_MAIN + 'films/genre/policier'])
    liste.append(['Romance', URL_MAIN + 'films/genre/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'films/genre/science-fiction'])
    liste.append(['Divers', URL_MAIN + 'films/genre/sport'])
    liste.append(['Thriller', URL_MAIN + 'films/genre/thriller'])
    liste.append(['Western', URL_MAIN + 'films/genre/western'])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def getcode(sHtmlContent):
    sPattern1 = '<input type="hidden" name="csrf_test_name" id="csrf_test_name" value="([^"]+)">'
    sCode = re.search(sPattern1, sHtmlContent)
    if sCode:
        return sCode.group(1)
    else:
        return ''


def showMovies(sSearch=''):
    oGui = Gui()
    oParser = cParser()

    if sSearch:
        oRequest = RequestHandler(URL_MAIN)
        sHtmlContent = oRequest.request()
        cook = oRequest.GetCookies()

        sCode = getcode(sHtmlContent)

        sText = sSearch
        oRequest = RequestHandler(URL_MAIN + 'search')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Cookie', cook)
        oRequest.addParametersLine('search=' + sText + '&csrf_test_name=' + sCode)

        sHtmlContent = oRequest.request()
        sHtmlContent = re.sub(
            '<h2></h2>',
            '<span class="Langue..."></span><span class="qalite">Qualité...</span>',
            sHtmlContent)  # recherche pas de qualité,langue

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        # parfois pas de qualité,langue,liens >> BA
        sHtmlContent = re.sub(
            '<span class="bientot"></span>',
            '<span class="nothing"></span><span class="qalite">nothing</span>',
            sHtmlContent)

    sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">.+?<span class="([^"]+)"></span><span class="qalite">([^<]+)</span>'

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

            if aEntry[3] == 'nothing' and aEntry[4] == 'nothing':  # pas de qualité,langue,liens >> BA
                continue

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sLang = aEntry[3]
            sQual = aEntry[4]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', output_parameter_handler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="active">\\d+</span>.+?<a href="([^"]+)" data-ci'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSeries():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">'

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
            sTitle = aEntry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSaisons():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sHtmlContent = oParser.abParse(sHtmlContent, 'begin seasons', 'end seasons')
    # pas encore d'épisode >> timer avant sortie
    sHtmlContent = re.sub('<kbd><span', '<kbd>nothing</span>', sHtmlContent)

    sPattern = '<h3 class="panel-title"><a href=".+?">(saison *\\d+)<\\/a>|<div class="panel-body">.+?href="([^"]+)">.+?<\\/span>([^"]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[1]

                sDisplayTitle = "%s %s" % (sMovieTitle, aEntry[2].replace(',', ''))

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = cParser()
    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    cook = oRequest.GetCookies()
    sCode = getcode(sHtmlContent)

    sPattern2 = "<button *class=\"players(?:(vf|vo|vostfr))\" *onclick=\"getIframe\\('([^']+)'\\).+?<\\/span> *([^<]+)<"
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if aResult[0]:
        for aEntry in aResult[1]:

            sLang = aEntry[0].upper()
            sHost = aEntry[2].capitalize()
            sCode2 = aEntry[1]

            sDisplayTitle = ('%s (%s) [COLOR %s]%s[/COLOR]') % (sMovieTitle, sLang, sColor, sHost)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sCode', sCode)
            output_parameter_handler.addParameter('sCode2', sCode2)
            output_parameter_handler.addParameter('sCook', cook)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sCode = input_parameter_handler.getValue('sCode')
    sCode2 = input_parameter_handler.getValue('sCode2')
    sCook = input_parameter_handler.getValue('sCook')

    oParser = cParser()

    # VSlog(URL_MAIN + 'getlinke')
    # VSlog(sCook)

    if '/serie' in sUrl:
        oRequest = RequestHandler(URL_MAIN + 'getlinke')
        oRequest.addParametersLine('csrf_test_name=' + sCode + '&episode=' + sCode2)
    else:
        oRequest = RequestHandler(URL_MAIN + 'getlink')
        oRequest.addParametersLine('csrf_test_name=' + sCode + '&movie=' + sCode2)

    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Cookie', sCook)

    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:

        sHosterUrl = aResult[1][0]

        oHoster = HosterGui().checkHoster(sHosterUrl)

        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
