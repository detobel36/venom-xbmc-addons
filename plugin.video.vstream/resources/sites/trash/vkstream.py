# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # 0212020 Site HS depuis plus de 1 moi

SITE_IDENTIFIER = 'vkstream'
SITE_NAME = 'Vkstream'
SITE_DESC = 'Series en streaming, streaming HD, streaming VF, séries, récent'

# URL_MAIN = 'https://wvv.vkstream.org/' # sous cloudfare
# ajout 09/10/2020 nom : VoirSeries ,clone sans CF avec  même code html
URL_MAIN = 'https://wvw.voirseries1.co/'

SERIE_SERIES = (URL_MAIN + 'series/page/1', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_VIEWS = (URL_MAIN + 'top-series/page/1', 'showSeries')
SERIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'search?search=', 'showSeries')
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'series/genre/action_1'])
    liste.append(['Animation', URL_MAIN + 'series/genre/animation_1'])
    liste.append(['Aventure', URL_MAIN + 'series/genre/aventure_1'])
    liste.append(['Biopic', URL_MAIN + 'series/genre/biopic_1'])
    liste.append(['Comédie', URL_MAIN + 'series/genre/comaedie_1'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 'series/genre/comaedie-musicale_1'])
    liste.append(['Documentaire', URL_MAIN + 'series/genre/documentaire_1'])
    liste.append(['Drame', URL_MAIN + 'series/genre/drame_1'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 'series/genre/epouvante-horreur_1'])
    liste.append(['Famille', URL_MAIN + 'series/genre/famille_1'])
    liste.append(['Fantastique', URL_MAIN + 'series/genre/fantastique_1'])
    liste.append(['Guerre', URL_MAIN + '/series/genre/guerre_1'])
    liste.append(['Policier', URL_MAIN + 'series/genre/policier_1'])
    liste.append(['Romance', URL_MAIN + 'series/genre/romance_1'])
    liste.append(['Science Fiction', URL_MAIN +
                 'series/genre/science-fiction_1'])
    liste.append(['Thriller', URL_MAIN + 'series/genre/thriller_1'])
    liste.append(['Western', URL_MAIN + 'series/genre/western_1'])
    liste.append(['Divers', URL_MAIN + 'series/genre/divers_1'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    for i in reversed(range(1997, 2021)):  # avant 1997 peu de results
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'series/annee/' + Year + '_1')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="item_larg">\\s*<a href="([^"]+)".+?"([^"]+)">.+?<img src="([^"]+)"'
    oParser = Parser()
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
            title = aEntry[1]
            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('([0-9]+)$', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Page ' +
                str(number) +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'href="([^"]+)"\\s*rel="next"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return False


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # description
    sPattern = 'colo_cont">.+?>([^<]*)</p>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        desc = aResult[1][0]
        desc = ('[COLOR coral]%s[/COLOR] %s') % (' SYNOPSIS : \r\n\r\n', desc)
    else:
        desc = ''

    sPattern = 'class="item">.+?href="([^"]+)".+?<h2>([^<]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            title = sMovieTitle + ' ' + aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
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

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"" href="([^"]*)".+?ep_ar.+?span>([^<]*)<'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            title = sMovieTitle + ' E' + aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'seriesHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href=\'([^"]*)\'.+?alt="([^"]*)".+?icon.([^"]*).png'
    # g1 url g2 host g3 vostfr vf

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        for aEntry in aResult[1]:

            if (str(aEntry[0]).find('streaming-video.html') >= 0):  # Fake
                continue

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sHoster = re.sub('\\.\\w+', '', aEntry[1]).capitalize()
            sLang = str(aEntry[2]).upper()
            sDisplayTitle = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHoster)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
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

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
