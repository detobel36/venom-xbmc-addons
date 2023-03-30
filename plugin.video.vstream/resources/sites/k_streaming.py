# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'k_streaming'
SITE_NAME = 'K-Streaming'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'film/serie-gratuit-1/', 'showMovies')


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    urlStart = input_parameter_handler.getValue('siteUrl')

    liste = [['Action', 'action-complet'], ['Animation', 'animation-gratuit'],
             ['Arts Martiaux', 'arts-martiaux-streaming-vf'], ['Aventure', 'aventure-streaming-vf'],
             ['Comédie', 'films-comedie-streaming'], ['Documentaire', 'documentaire-streaming'],
             ['Drame', 'film-drame-streaming-vf'], ['Epouvante Horreur', 'horreur-streaming-film'],
             ['Espionnage', 'film-espionnage-streaming'], ['Famille', 'famille'],
             ['Fantastique', 'film-fantastique-streaming'], ['Guerre', 'film-guerre-streaming'],
             ['Historique', 'film-historique-streaming'], ['Musical', 'film-musical-streaming'],
             ['Policier', 'film-policier-streaming'], ['Romance', 'film-romance-streaming'],
             ['Science Fiction', 'film-science-fiction-streaming'], ['Spectacle', 'film-spectacles-streaming'],
             ['Thriller', 'film-thriller-streaming']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', urlStart + 'film/' + sUrl + '/')
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
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '%20')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # parfois pas d'image et la qualité est une option pour la recherche
    sPattern = 'moviefilm".+?href="([^"]+).+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2].replace(
                'Streaming', '').replace(
                'Sasion', 'Saison')

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sDisplayTitle = title
            desc = ''

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '-saison-' in sUrl2 or '/series-' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
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
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    # &raquo; est réécris par vStream en >>
    sPattern = 'pages\'>.age.+?sur (\\d+).+?current\'>.+?href="([^"]+)">>>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    # Uniquement saison a chaque fois
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'Synopsis</span>:([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = '<div class="unepetitesaisons">\\s*<a href="([^"]+)" title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN + sUrl

            title = aEntry[1]
            # double affichage de la saison
            title = re.sub('- Saison \\d+', '', title)

            output_parameter_handler.addParameter('siteUrl', sUrl)
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
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    desc = ''
    try:
        sPattern = 'Synopsis</span>:([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    # recuperation du premier épisode
    sPattern = 'current" aria-current="page"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ListeUrl = []
    if aResult[0]:
        ListeUrl = [(sUrl, aResult[1][0])]

    # Recuperation des suivants
    sPattern = '<a href="([^<]+)" class="post-page-numbers"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if aResult[0]:
        for aEntry in ListeUrl:

            sUrl = aEntry[0]
            title = sMovieTitle.replace(
                ' - Saison', ' Saison') + ' ' + aEntry[1].replace('Part', 'Episode')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    # si un seul episode
    else:
        title = sMovieTitle + ' episode 1 '
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', title)
        output_parameter_handler.addParameter('sThumb', sThumb)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe (SRC|src)="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[1]
            if '//www.facebook.com/' in sHosterUrl:
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
