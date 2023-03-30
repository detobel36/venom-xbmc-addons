# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import SiteManager
from resources.lib.parser import Parser
from resources.lib.util import QuotePlus, cUtil

SITE_IDENTIFIER = 'mesfilms'
SITE_NAME = 'Mes Films'
SITE_DESC = 'Mes Films - Films en streaming HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'

URL_SEARCH = (URL_MAIN + '?s=', 'showSearchResult')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/?get=movies', 'showMovies')
MOVIE_CLASS = (URL_MAIN + 'films-classiques/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
# MOVIE_LIST = (True, 'showList')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_CLASS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_CLASS[1],
        'Films (Classiques)',
        'star.png',
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

    # ne fonctionne plus sur le site
    # output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + QuotePlus(sSearchText)
        showSearchResult(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Action & aventure', 'action-adventure'], ['Animation', 'animation'],
             ['Aventure', 'aventure'], ['Comédie', 'comedie'], ['Crime', 'crime'], ['Documentaire', 'documentaire'],
             ['Drame', 'drame'], ['Etranger', 'etranger'], ['Familial', 'familial'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['News', 'news'], ['Policier', 'policier'], ['Reality', 'reality'],
             ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Science Fiction & Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Talk', 'talk'],
             ['Téléfilm', 'telefilm'], ['Thriller', 'thriller'], ['War & Politics', 'war-politics'],
             ['Western', 'western']]

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


def showList():
    gui = Gui()

    liste = [['09', '09'], ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'],
             ['H', 'h'], ['I', 'i'], ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'],
             ['Q', 'q'], ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'],
             ['Z', 'z']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + '?letter=true&s=title-' + sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1963, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchResult(sSearch=''):
    gui = Gui()
    oParser = Parser()
    sUrl = sSearch

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'animation-2".+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?(?:|year">([^<]*)<.+?)<p>(.*?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = re.sub(
                '/w\\d+/',
                '/w342/',
                aEntry[1],
                1)  # meilleure qualité
            title = aEntry[2].replace(': Season', ' Saison')
            sYear = aEntry[3]
            if sYear != '':  # on ne récupere que l'année
                sYear = re.search('(\\d{4})', sYear).group(1)
            desc = aEntry[4]

            # on ne recherche que des films même si séries et animés disponible
            if '/film/' not in sUrl:
                continue

            # Filtrer les résultats
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            # permet à addMovie d'afficher l'année en Meta
            output_parameter_handler.addParameter('sYear', sYear)

            gui.addMovie(SITE_IDENTIFIER, 'showLinks', title, '',
                         sThumb, desc, output_parameter_handler)


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
    sPattern = 'poster">\n*<[^<>]+src="([^"]+)" alt="([^"]+).+?(?:|quality">([^<]+).+?)href="([^"]+).+?<span>([^<]+).+?(texto">(.*?)<|<\\/article)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = re.sub(
                '/w\\d+/',
                '/w342/',
                aEntry[0],
                1)  # ameliore la qualité
            title = aEntry[1]
            sQual = aEntry[2]
            sUrl2 = aEntry[3]
            sYear = aEntry[4]
            desc = ''  # cas ou la sdesc n'est pas presente
            if aEntry[6]:
                desc = aEntry[6]
            sDisplayTitle = ('%s [%s]') % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = 'class="pagination"><span>Page.+?de ([^<]+).+?href="([^"]+)"><i id=.nextpagination'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    try:
        sPattern = 'og:description" content="(.+?)" /><meta'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = "type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+)</span>\\s*<span class='server'>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sType = aEntry[0]
            sPost = aEntry[1]
            sNume = aEntry[2]
            sQual = aEntry[3]
            sHost = re.sub('\\.\\w+', '', aEntry[4]).capitalize()
            if 'Youtube' in sHost:
                continue

            title = (
                '%s [%s] [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sType', sType)
            output_parameter_handler.addParameter('sPost', sPost)
            output_parameter_handler.addParameter('sNume', sNume)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sType = input_parameter_handler.getValue('sType')
    sPost = input_parameter_handler.getValue('sPost')
    sNume = input_parameter_handler.getValue('sNume')

    # trouve la vraie url
    oRequestHandler = RequestHandler(URL_MAIN)
    oRequestHandler.request()
    sUrl2 = oRequestHandler.getRealUrl() + 'wp-admin/admin-ajax.php'

    oRequestHandler = RequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addParameters('action', 'doo_player_ajax')
    oRequestHandler.addParameters('type', sType)
    oRequestHandler.addParameters('post', sPost)
    oRequestHandler.addParameters('nume', sNume)
    sHtmlContent = oRequestHandler.request()
    sPattern = "(http[^'\"]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
