# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import Unquote
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import re
return False  # Sous Cloudflare 14/10/2021


SITE_IDENTIFIER = 'enstream'
SITE_NAME = 'Enstream'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = "https://www.enstream.club/"

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (True, 'showAlpha')


def load():
    gui = Gui()

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

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Ordre alphabétique)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        showMovies(sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Comédie Dramatique', 'comedie-dramatique'],
             ['Comédie Musicale', 'comedie-musical'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'],
             ['Historique', 'historique'], ['Judiciaire', 'judiciaire'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'genre/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1942, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'Annee/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = [['0-9', ''], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F'], ['G', 'G'],
             ['H', 'H'], ['I', 'I'], ['J', 'J'], ['K', 'K'], ['L', 'L'], ['M', 'M'], ['N', 'N'], ['O', 'O'],
             ['P', 'P'], ['Q', 'Q'], ['R', 'R'], ['S', 'S'], ['T', 'T'], ['U', 'U'], ['V', 'V'], ['W', 'W'],
             ['X', 'X'], ['Y', 'Y'], ['Z', 'Z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'ABC/' + sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        sUrl = URL_MAIN + 'search.php'
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('q', Unquote(sSearch))
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)

    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if sSearch:
        sPattern = '<a href="([^"]+).+?url\\((.+?)\\).+?<div class="title"> (.+?) </div>'
    elif 'Annee/' in sUrl or '/ABC' in sUrl:
        sPattern = '<div class="table-movies-content.+?href="([^"]+).+?url\\((.+?)\\).+?<.i>.([^<]+)'
    elif 'genre/' in sUrl:
        sPattern = 'film-uno.+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+)'
    else:
        sPattern = 'class="film-uno".+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+).+?min.+?·([^<]+).+?short-story">([^<]*)'

    oParser = Parser()
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
            title = aEntry[2]
            desc = ''
            if len(aEntry) > 3:
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sQual = aEntry[3].split('·')[1].replace('Â', '').strip()
                    sLang = aEntry[3].split('·')[2].strip()
                else:
                    sQual = aEntry[3].split('·')[1].strip()
                    sLang = aEntry[3].split('·')[2].strip()

                desc = aEntry[4]

                sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang)
                output_parameter_handler.addParameter('sQual', sQual)

            else:
                sDisplayTitle = title

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHoster',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            # sNumPage = re.search('(page|genre).*?[-=\/]([0-9]+)',
            # sNextPage).group(2)  # ou replace'.html',''; '([0-9]+)$'
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'class=\'Paginaactual\'.+?a href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search(
            '(page|genre).*?[-=\\/]([0-9]+)',
            sNextPage).group(2)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    sPattern = '<span>\\d+</span>.+?href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search(
            '(page|genre).*?[-=\\/]([0-9]+)',
            sNextPage).group(2)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHoster(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-url="([^"]+)".+?data-code="([^"]+)".+?mobile">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sDataUrl = aEntry[0]
            sDataCode = aEntry[1]
            sHost = aEntry[2].capitalize()

            # filtrage des hosters
            oHoster = HosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            lien = URL_MAIN + 'video/' + sDataCode + '/recaptcha/' + sDataUrl

            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', lien)
            output_parameter_handler.addParameter('referer', sUrl)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersLinks',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    sPattern = "class=.download.+?href='/([^']*).+?mobile.>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            lien = URL_MAIN + aEntry[0]
            sHost = aEntry[1].capitalize()
            oHoster = HosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteUrl', lien)
            output_parameter_handler.addParameter('referer', sUrl)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersLinks',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHostersLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', referer)

    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = HosterGui().checkHoster(sHosterUrl)

    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
