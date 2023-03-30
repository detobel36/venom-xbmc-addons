# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import progress, siteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.multihost import cMultiup
from resources.lib.util import cUtil
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'asia_insane'
SITE_NAME = 'Asia Insane'
SITE_DESC = 'Regarder Films et Séries Asiatique en Streaming gratuit'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DRAMA_DRAMAS = (True, 'load')
DRAMA_MOVIES = (URL_MAIN + 'films-asiatiques-affichage-grid/', 'showMovies')
DRAMA_GENRES = (True, 'showGenres')
DRAMA_ANNEES = (True, 'showYears')
DRAMA_LIST = (True, 'showAlpha')
DRAMA_SERIES = (URL_MAIN + 'liste-des-dramas-vostfr-ddl/', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'wp-admin/admin-ajax.php', 'showMovies')
URL_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_MOVIES[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_GENRES[1], 'Dramas (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_ANNEES[1], 'Dramas (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_SERIES[1], 'Séries (Dramas)', 'dramas.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    liste = [['Action', 'action'], ['Arts Martiaux', 'arts-martiaux'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Drame', 'drame'], ['Ecole', 'ecole'], ['Expérimental', 'experimental'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Gastronomie', 'gastronomie'],
             ['Guerre', 'guerre'], ['Histoire vraie', 'histoire-vraie'], ['Historique', 'historique'],
             ['Horreur', 'horreur'], ['Maladie', 'maladie'], ['Médecine', 'medecine'], ['Mélodrame', 'melodrame'],
             ['Musical', 'musical'], ['Mystère', 'mystere'], ['Policier', 'policier'], ['Psycologique', 'psycologique'],
             ['Romance', 'romance'], ['Science Fiction', 'science-fiction'], ['Sport', 'sport'],
             ['Suspense', 'suspense'], ['Travail', 'travail'], ['Tranche de vie', 'tranche-de-vie'],
             ['Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for sTitle, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'amy_genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = Gui()

    from itertools import chain
    generator = chain([1966, 1972, 1987, 1988, 1990, 1991, 1992], range(1994, 2023))

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(list(generator)):
        Year = str(i)
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'date/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = Gui()
    oParser = cParser()

    sUrl = URL_MAIN + 'films-asiatiques-vostfr-affichage-alphanumerique/'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+)d{2}.+?.+?field-desc"><p>([^<]+)'
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

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/dramas/' in sUrl:
                oGui.addDrama(SITE_IDENTIFIER, 'showSerieEpisodes', sTitle, '', sThumb, '', output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, output_parameter_handler)

        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)

        sPattern = '<a class=\'asp_res_image_url\' href=\'([^>]+)\'.+?url\\("([^"]+)"\\).+?\'>([^.]+)d{2}.+?<span.+?class="asp_res_text">([^<]+)'

        oRequestHandler = RequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN + "recherche-avancee-asia-insane/")
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')

        oRequestHandler.addParameters('action', "ajaxsearchpro_search")
        oRequestHandler.addParameters('asid', "1")
        oRequestHandler.addParameters('aspp', sSearch)
        oRequestHandler.addParameters('asp_inst_id', "1_1")
        oRequestHandler.addParameters(
            'options',
            "current_page_id=413&qtranslate_lang=0&asp_gen%5B%5D=title&customset%5B%5D=amy_movie&customset%5B%5D=amy_tvshow&termset%5Bamy_director%5D%5B%5D=-1&termset%5Bamy_actor%5D%5B%5D=-1")
        sHtmlContent = oRequestHandler.request()

    elif '/amy_genre/' in sUrl or '/date/' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'item-poster">.+?src="(http[^"]+).+?href="([^"]+)">([^<]+)d{2}.+?desc"><p>([^<]+)'

    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+)d{2}.+?field-desc"><p>([^<]+).+?(?:|/version/([^/]+).+?)(?:|/date/([^/]+).+?)Genre:'

    oParser = cParser()
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

            if sSearch:
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]

                sDisplayTitle = '%s' % sTitle

            elif '/amy_genre/' in sUrl or '/date/' in sUrl:
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]

                sDisplayTitle = '%s' % sTitle

            else:
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
                sQual = aEntry[4].upper()
                sYear = aEntry[5]

                sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/dramas/' in sUrl2:
                oGui.addDrama(
                    SITE_IDENTIFIER,
                    'showSerieEpisodes',
                    sDisplayTitle,
                    '',
                    sThumb,
                    sDesc,
                    output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a><a class="next page-numbers" href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)/', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSerieEpisodes():
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="entry-content e-content" itemprop="description articleBody">'
    sEnd = '<div class="entry-comment">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = sMovieTitle + " E" + aEntry[1]
            sUrl2 = aEntry[0]
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('HostUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sUrl2 = input_parameter_handler.getValue('HostUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    if '/dramas/' in sUrl:
        if 'multiup' in sUrl2:
            aResult = cMultiup().GetUrls(sUrl2)

            if aResult:
                for aEntry in aResult:
                    sHosterUrl = aEntry

                    oHoster = HosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        else:
            sHosterUrl = sUrl2

            oHoster = HosterGui().checkHoster(sUrl2)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sStart = '<pre>'
        sEnd = '</pre>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '>.+?href="([^"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle = sMovieTitle
                sHosterUrl = aEntry

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
