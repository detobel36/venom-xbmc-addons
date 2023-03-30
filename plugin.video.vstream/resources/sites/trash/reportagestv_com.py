# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'reportagestv_com'
SITE_NAME = 'Reportages TV'
SITE_DESC = 'Reportages TV - Replay des reportages télé français en streaming.'

URL_MAIN = 'http://www.reportagestv.com/'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['TF1', URL_MAIN + 'category/tf1/'])
    liste.append(['TF1 - Appels d\'Urgence',
                  URL_MAIN + 'category/tf1/appels-durgence/'])
    liste.append(['TF1 - Sept à Huit', URL_MAIN + 'category/tf1/sept-a-huit/'])
    liste.append(['France 2', URL_MAIN + 'category/france-2/'])
    liste.append(['France 2 - Apocalypse la 1ère guerre mondiale',
                  URL_MAIN + 'category/france-2/apocalypse-la-1-ere-guerre-mondiale/'])
    liste.append(['France 2 - Envoyé Spécial', URL_MAIN +
                 'category/france-2/envoye-special/'])
    liste.append(['Canal+', URL_MAIN + 'category/canal-plus/'])
    liste.append(['Canal+ - Nouvelle Vie', URL_MAIN +
                 'category/canal-plus/nouvelle-vie/'])
    liste.append(['Canal+ - Spécial Investigation', URL_MAIN +
                 'category/canal-plus/special-investigation/'])
    liste.append(['D8 - Au coeur de l\'Enquête',
                  URL_MAIN + 'category/d8/au-coeur-de-lenquete/'])
    liste.append(['D8 - En quête d\'Actualité',
                  URL_MAIN + 'category/d8/en-quete-dactualite/'])
    liste.append(['D8', URL_MAIN + 'category/d8/'])
    liste.append(['TMC', URL_MAIN + 'category/tmc/'])
    liste.append(['TMC - 90 Enquêtes', URL_MAIN + 'category/tmc/90-enquetes/'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'doc.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        '&#039;',
        '\'').replace(
        '&#8217;',
        '\'').replace(
            '&laquo;',
            '<<').replace(
                '&raquo;',
                '>>').replace(
                    '&nbsp;',
        '')

    sPattern = 'class="mh-loop-thumb".+?src="([^"]+)" class="attachment.+?href="([^"]+)" rel="bookmark">([^<]+)</a>.+?<div class="mh-excerpt"><p>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            title = aEntry[2]
            # .replace('&laquo;', '<<').replace('&raquo;', '>>')
            desc = aEntry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                sThumb,
                desc,
                output_parameter_handler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^"]+)">'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def __checkForRealUrl(sHtmlContent):
    sPattern = '<a href="([^"]+)" target="_blank".+?class="btns btn-lancement">Lancer La Video</a>'
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

    sRealUrl = __checkForRealUrl(sHtmlContent)

    if (sRealUrl):
        oRequestHandler = RequestHandler(sRealUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'https:' + sHosterUrl

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
