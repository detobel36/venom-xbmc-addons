# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import urlEncode
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Films en Streaming complet VF HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'exclu/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Top exclu)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
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

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

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


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    nextPageSearch = input_parameter_handler.getValue('nextPageSearch')
    sUrl = input_parameter_handler.getValue('siteUrl')

    if nextPageSearch:
        sSearch = sUrl

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        if nextPageSearch:
            query_args = (('do', 'search'), ('subaction', 'search'),
                          ('search_start', nextPageSearch), ('story', sSearch))
        else:
            query_args = (
                ('do', 'search'), ('subaction', 'search'), ('story', sSearch))

        data = urlEncode(query_args)

        oRequestHandler = RequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addParameters('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

    else:
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    if sSearch:
        sPattern = '<div class="fullstream fullstreaming">.+?<img src="([^"]+)".+?<h3 class="mov-title"><a href="([^"]+)" >([^<]+)</a>.+?<strong>(?:Qualit|Version).+?">(.+?)</a>.+?</*strong>'
    else:
        sPattern = 'class="fullstream fullstreaming".+?src="([^"]+).+?alt="([^"]+).+?<strong>(?:Qualit|Version).+?>(.+?)</a>.+?</*strong>.+?xfsearch.+?>([^<]+).+?itemprop="description".+?;">([^<]+).+?<a href="([^"]+)'

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

            sYear = ''
            if sSearch:
                sThumb = aEntry[0]
                if sThumb.startswith('/'):
                    sThumb = URL_MAIN[:-1] + sThumb

                siteUrl = re.sub('www\\.', '', aEntry[1])
                title = aEntry[2]
                sQual = aEntry[3]
                sQual = sQual.replace(
                    ':',
                    '').replace(
                    ' ',
                    '').replace(
                    ',',
                    '/')
                desc = ''

            else:
                sThumb = aEntry[0]
                if sThumb.startswith('/'):
                    sThumb = "https:" + sThumb

                title = aEntry[1]
                sQual = aEntry[2]
                sQual = sQual.replace(
                    ':',
                    '').replace(
                    ' ',
                    '').replace(
                    ',',
                    '/')

                # Certain film n'ont pas de date.
                try:
                    sYear = re.search('(\\d{4})', aEntry[3]).group(1)
                except BaseException:
                    pass

                desc = aEntry[4]
                siteUrl = re.sub('www\\.', '', aEntry[5])

            sDisplayTitle = '%s [%s]' % (title, sQual)

            output_parameter_handler.addParameter('siteUrl', siteUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                'films.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = 'nextlink" id="nextlink" onclick="javascript:list_submit\\(([0-9]+)\\); return\\(false\\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sSearch)
                output_parameter_handler.addParameter(
                    'nextPageSearch', aResult[1][0])
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sNextPage)
                number = re.search('/page/([0-9]+)', sNextPage).group(1)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + number,
                    output_parameter_handler)

    if nextPageSearch:
        gui.setEndOfDirectory()

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)">Suivant &#8594;'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return re.sub('www\\.', '', aResult[1][0])

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<i class="fa fa-play-circle-o"></i>([^<]+)</div>|<a href="([^"]+)" title="([^"]+)" target="seriePlayer"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sethost = set()

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]')
                continue

            sHosterUrl = aEntry[1]
            if sHosterUrl not in sethost:
                sethost.add(sHosterUrl)
            else:
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
