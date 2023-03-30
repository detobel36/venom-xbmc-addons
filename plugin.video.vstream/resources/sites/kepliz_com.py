# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import SiteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# On garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

# Source compatible avec les clones : toblek, bofiaz, nimvon
# mais pas compatible avec les clones, qui ont une redirection directe :
# sajbo, trozam, radego
URL_HOST = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_HOST = dans sites.json
URL_MAIN = 'URL_MAIN'

# pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'c/poblom/29/0', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

DOC_NEWS = (URL_MAIN + 'c/poblom/26/0', 'showMovies')
SHOW_SHOWS = (URL_MAIN + 'c/poblom/3/0', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_MISC = ('', 'showMovies')
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films (A l\'affiche)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SHOW_SHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SHOW_SHOWS[1],
        'Spectacles',
        'doc.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['A l\'affiche', 29])
    liste.append(['Action', 1])
    liste.append(['Animation', 2])
    liste.append(['Aventure', 4])
    # liste.append(['Biographie', 5])  # aucun
    liste.append(['Comédie', 6])
    liste.append(['Documentaires', 26])
    liste.append(['Drame', 7])
    liste.append(['Epouvante Horreur', 9])
    liste.append(['Fantastique', 8])
    liste.append(['Policier', 10])
    liste.append(['Science Fiction', 11])
    liste.append(['Spectacle', 3])
    liste.append(['Thriller', 12])

    output_parameter_handler = OutputParameterHandler()
    for title, iGenre in liste:
        sUrl = URL_MAIN + 'c/poblom/%d/0' % iGenre
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

    # L'url change tres souvent donc faut la retrouver
    oRequestHandler = RequestHandler(URL_HOST)
    data = oRequestHandler.request()
    # Compatible avec plusieurs clones
    aResult = oParser.parse(data, '<a.+?href="(/*[0-9a-zA-Z]+)"')
    if not aResult[0]:
        return   # Si ca ne marche pas, pas la peine de continuer

    # memorisation pour la suite
    sMainUrl = URL_HOST + aResult[1][0] + '/'
    # correction de l'url

    # En cas de recherche direct OU lors de la navigation dans les differentes
    # pages de résultats d'une recherche
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_MISC[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        sSearch = sSearch[:20]  # limite de caractere sinon bug de la recherche
        oRequestHandler = RequestHandler(sMainUrl + 'home/poblom/')
        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('searchword', sSearch.replace(' ', '+'))
        sABPattern = '<div class="column24"'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        if sUrl == URL_MAIN:  # page d'accueil
            sABPattern = '<div class="column1"'
        else:
            sABPattern = '<div class="column20"'
        sUrl = sUrl.replace(URL_MAIN, sMainUrl)
        oRequestHandler = RequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(
        sHtmlContent, sABPattern, '<div class="column2"')
    sPattern = '<span style="list-style-type:none;".+? href="\\/[0-9a-zA-Z]+\\/([^"]+)">(.+?)\\((.+?)\\).+?>(<i>(.+?)</i>|)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            title = aEntry[1].strip()
            sYear = aEntry[2]
            sQual = aEntry[4]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue    # Filtre de recherche

            sDisplayTitle = ("%s (%s) [%s]") % (title, sYear, sQual)
            output_parameter_handler.addParameter('siteUrl', sMainUrl + sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sMainUrl', sMainUrl)
            output_parameter_handler.addParameter('sYear', sYear)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                'films.png',
                '',
                '',
                output_parameter_handler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter(
                'siteUrl', URL_HOST[:-1] + sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Suivant',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'a><a style="position: relative;top: 3px;margin-right: 6px;" href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    # sMainUrl = input_parameter_handler.getValue('sMainUrl')
    # sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<br/>', '')  # traitement de desc

    # Recuperation info film, com et image
    sThumb = ''
    desc = ''
    sPattern = '<img src="([^"]+).+?<p.+?>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sThumb = aResult[1][0][0]
        desc = aResult[1][0][1]

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sLink = aResult[1][0]
        if sLink.startswith('/'):
            sLink = URL_HOST[:-1] + sLink

        oRequestHandler = RequestHandler(sLink)
        data = oRequestHandler.request()

        sPattern = 'file: "(.+?)"'
        aResult = oParser.parse(data, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:

                sLink2 = aEntry
                oHoster = HosterGui().checkHoster(sLink2)

                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sLink2, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
