# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'voirseries_best'
SITE_NAME = 'VoirSeries'
SITE_DESC = 'Séries en streaming VF et VOSTFR '

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_NEWS = (URL_MAIN + 'series/', 'showSeries')
SERIE_NEWS_SAISONS = (URL_MAIN, 'showSaisonsEpisodesNews')
tagnewsepidodes = '#tagnewsepidodes'
SERIE_NEWS_EPISODES = (URL_MAIN + tagnewsepidodes, 'showSaisonsEpisodesNews')
SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showAlpha')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_SERIES = (True, 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS_SAISONS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_SAISONS[1],
        'Séries (Dernières saisons)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS_EPISODES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_EPISODES[1],
        'Séries (Derniers épisodes)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Adventure', 'adventure'],
             ['Arts-Martiaux', 'arts-martiaux'], ['Biopic', 'biopic'], ['Biographie', 'biographie'],
             ['Biography', 'biography'], ['Comédie', 'comedie'], ['Comédie dramatique', 'comedie-dramatique'],
             ['Comédie musicale', 'comedie-musicale'], ['Crime', 'crime'], ['Documentaire', 'documentaire'],
             ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Horreur', 'horreur'], ['Policier', 'policier'],
             ['Romance', 'romance'], ['Thriller', 'thriller'], ['Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'genres/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'],
             ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'], ['H', 'h'], ['I', 'i'],
             ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'], ['Q', 'q'], ['R', 'r'],
             ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'], ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:

        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'liste/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'Année</div>'
    sEnd = 'class="Genres Séries">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href=([^ ]+) rel=nofollow><i class=material-icons>date_range</i><br>([0-9]{4})'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl = aEntry[0]
            Year = aEntry[1]
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                Year,
                'annees.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSaisonsEpisodesNews():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sStart = 'Derniers épisodes Séries-TV ajoutés'
    sEnd = 'more_horiz'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    if sUrl == SERIE_NEWS_EPISODES[0]:  # ne pas réduire les regex
        sPattern = '<li>\\s*<a href=([^ ]+) title=".+?>([^<]+)<span> <i class="langue ([^"]+)'
    else:
        sPattern = '<li>\\s*<a href=([^ ]+) title="([^"]+)">[^<]+<span class'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = ''
            sUrl2 = aEntry[0]
            title = aEntry[1].replace('  - S', '').title()
            if sUrl == SERIE_NEWS_EPISODES[0]:
                sLang = aEntry[2]
                if 'vf' in sLang:
                    sThumb = URL_MAIN + 'storage/icon/vf.png'
                if 'vostfr' in sLang:
                    sThumb = URL_MAIN + 'storage/icon/vostfr.png'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if sUrl == SERIE_NEWS_EPISODES[0]:
                gui.addTV(SITE_IDENTIFIER, 'showHosters', title,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                          '', sThumb, '', output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20', '+') + '&submit='
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class=shortstory>.+?href=([^ ]+).+?data-src=([^ ]+).+?>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            if sSearch:
                gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                          '', sThumb, '', output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showSaisons', title,
                          '', sThumb, '', output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>(\\d+)</a> <a class="next page-numbers" href=([^ ]+) >Suivant'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging
    return False, 'none'


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    sPattern = 'fsynopsis>\\s*<p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResult[1][0])

    sPattern = 'class="shortstory">.+?href="([^"]+).+?data-src="([^"]+).+?<figcaption>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = sMovieTitle + ' ' + aEntry[2]

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
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if not sThumb:
        sPattern = 'fstory-poster.+?data-src=([^ ]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sThumb = aResult[1][0]

    if not desc:
        sPattern = 'fsynopsis>\\s*<p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = (
                '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResult[1][0])

    sPattern = 'class=saision_LI2>\\s*<a href=([^ ]+).+?span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' ' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if 'storage/icon/' in sThumb:
        sPattern = 'poster image">\\s*<img src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sThumb = aResult[1][0]

    if not desc:
        sPattern = 'fsynopsis>\\s*<p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = (
                '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResult[1][0])

    sPattern = '<div data-url=([^ ]+).+?id=player_v_DIV_5.*?(?:class="download-server"|)>([^<]+).+?langue ([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]

            if HosterGui().checkHoster(sUrl2) is False:
                continue

            sHostName = aEntry[1]
            sLang = aEntry[2].upper()
            if 'HD VIP' in sHostName or 'STREAMANGO' in sHostName or 'OPENLOAD' in sHostName or 'VERYSTREAM' in sHostName:
                continue

            sHostName = sHostName.capitalize()
            sDisplayTitle = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHostName)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sHost', sHostName)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
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

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-url=([^ ]+).+?langue ([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'https:' + sHosterUrl
            sLang = aEntry[1].upper()

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle + ' (' + sLang + ')')
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
