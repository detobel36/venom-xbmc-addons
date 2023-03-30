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
return False

SITE_IDENTIFIER = 'videobuzzy_com'
SITE_NAME = 'Videobuzzy'
SITE_DESC = 'Sélection des vidéos les plus populaires de Videobuzzy'

URL_MAIN = 'https://www.videobuzzy.com/'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenres')

# URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler.addParameter('siteUrl', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos du net',
        'buzz.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos du net (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_MAIN + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Galerie', URL_MAIN + 'galerie.htm'])
    liste.append(['Football', URL_MAIN + 'football.htm'])
    liste.append(['Humour', URL_MAIN + 'humour.htm'])
    liste.append(['Animaux', URL_MAIN + 'animaux.htm'])
    liste.append(['Insolite', URL_MAIN + 'insolite.htm'])
    liste.append(['Télévision', URL_MAIN + 'television.htm'])
    liste.append(['Musique', URL_MAIN + 'musique.htm'])
    liste.append(['Sport', URL_MAIN + 'sport.htm'])
    liste.append(['Cinéma', URL_MAIN + 'cinema.htm'])
    # liste.append(['Bref.', URL_MAIN + 'BREF-tous-les-episodes-de-la-serie-de-canal-+-4902.news'])
    liste.append(['Top Vidéo', URL_MAIN + 'top-video.php'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
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
    sPattern = "class='titre_news_index' href='(.+?)' title='(.+?)'.+?class=\"thumbnail\" src='(.+?)'.+?class='corps_news_p2'>(.+?)</span>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1]
            sThumb = aEntry[2]
            desc = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('/page-([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?</span><a href="(.+?)" title=\'.+?\'>.+?</a>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'file: "(.+?)", label: "(.+?)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            title = sMovieTitle + ' | ' + aEntry[1]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(title)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
