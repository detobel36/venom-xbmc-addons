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

"""
Pour rappel.
Problème avec les DNS en ipv6 il faut utiliser les suivantes
CloudFlare DNS:
Préféré : 2606:4700:4700::1111
Auxiliaire : 2606:4700:4700::1001
Ou:
Google DNS:
Préféré : 2001:4860:4860::8888
Auxiliaire : 2001:4860:4860::8844
"""


# from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamdivx'
SITE_NAME = 'StreamDivx'
SITE_DESC = 'Regarder, Voir Films En Streaming VF 100% Gratuit.'

# ou 'https://www.voustreaming.com/' < recherche hs
URL_MAIN = 'https://wvvw.streamdivx.net/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'tags/', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Musicale', 'comedie-musicale'], ['Drame', 'drame'], ['Documentaire', 'documentaire'],
             ['Epouvante Horreur', 'epouvante-horreur'], ['Erotique', 'erotique'], ['Espionnage', 'espionnage'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Judiciaire', 'judiciaire'], ['Musical', 'musical'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1985, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'tags/' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch
        oRequest = RequestHandler(sUrl)
        sHtmlContent = oRequest.request()
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        if '<h2 class="side-title nop">film du moment</h2>' in sHtmlContent:
            sStart = '<div class="films-group small'
            sEnd = '<div class="side-title">films par Genres'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        else:
            sHtmlContent = sHtmlContent

    sPattern = 'class="film-uno *">.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+).+?class="quality ">([^<]+).+?class="nop short-story *">(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2]  # .decode("unicode_escape").encode("latin-1")
            sQual = aEntry[3]
            desc = aEntry[4]
            sDisplayTitle = ('%s [%s]') % (title, sQual)

            # Nettoie le titre, la premiere phrase est souvent doublée
            desc = desc.replace('SYNOPSIS ET DÉTAILS', '').lstrip()
            if len(desc) > 180:
                idx = desc.find(desc[:15], 30, 180)
                if idx > 0:
                    desc = desc[idx:]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sQual', sQual)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href="([^"]+)">Last page</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    # sPost = input_parameter_handler.getValue('sPost')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe src="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
