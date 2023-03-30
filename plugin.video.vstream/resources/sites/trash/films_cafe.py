# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import Progress  # , VSlog
import re
import base64

SITE_IDENTIFIER = 'films_cafe'
SITE_NAME = 'Films Cafe'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = 'https://ww1.films.cafe/'

MOVIE_NEWS = (URL_MAIN + 'tous-les-films/?sort=date', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'tous-les-films/', 'load')
MOVIE_VIEWS = (URL_MAIN + 'tous-les-films/?sort=views', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'tous-les-films/?sort=comments', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'tous-les-films/?sort=imdb', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'


def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except BaseException:
        return chain


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
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    # gui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_COMMENTS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/action/'])
    liste.append(['Animation', URL_MAIN + 'category/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'category/arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'category/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'category/biopic/'])
    liste.append(['Bollywood', URL_MAIN + 'category/bollywood/'])
    liste.append(['Comédie', URL_MAIN + 'category/comedie/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'category/drame/'])
    liste.append(['Espionnage', URL_MAIN + 'category/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'category/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'category/fantastique/'])
    liste.append(['Fiction', URL_MAIN + 'category/science-fiction/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre/'])
    liste.append(['Historique', URL_MAIN + 'category/historique/'])
    liste.append(['Horreur', URL_MAIN + 'category/horreur/'])
    liste.append(['Musical', URL_MAIN + 'category/musical/'])
    liste.append(['Péplum', URL_MAIN + 'category/peplum/'])
    liste.append(['Policier', URL_MAIN + 'category/policier/'])
    liste.append(['Romance', URL_MAIN + 'category/romance/'])
    liste.append(['Thriller', URL_MAIN + 'category/thriller/'])
    liste.append(['Western', URL_MAIN + 'category/western/'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    sUrl = URL_MAIN + 'tous-les-films/?release-year='

    liste = []
    liste.append(['2018', sUrl + '2018'])
    liste.append(['2017', sUrl + '2017'])
    liste.append(['2016', sUrl + '2016'])
    liste.append(['2015', sUrl + '2015'])
    liste.append(['2014', sUrl + '2014'])
    liste.append(['2013', sUrl + '2013'])
    liste.append(['2012', sUrl + '2012'])
    liste.append(['2011', sUrl + '2011'])
    liste.append(['<2010', sUrl + '2010'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
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
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="movie-preview-content".+?src="([^"]+)".+?href="([^"]+)" title="([^"]+)".+?<p class=.story.>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            title = aEntry[2]
            desc = aEntry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'films.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if not sSearch:
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
    oParser = Parser()
    sPattern = 'class="current".+?<a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<a  id="([^"]+)".+?>► (.+?)<'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sPost = aEntry[0].split("_")
            sHost = aEntry[1].capitalize()
            title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sPostId', sPost[0])
            output_parameter_handler.addParameter('sTabId', sPost[1])
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sPostId = input_parameter_handler.getValue('sPostId')
    sTabId = input_parameter_handler.getValue('sTabId')

    # trouve la vrais url
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sUrl2 = oRequestHandler.getRealUrl() + 'wp-admin/admin-ajax.php'

    oRequestHandler = RequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry(
        'User-Agent',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addParameters('action', 'fetch_iframes_from_post')
    oRequestHandler.addParameters('post_id', sPostId)
    oRequestHandler.addParameters('tab_id', sTabId)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            # https://drive.google.com/file/d/' + sId + '/view' #?pli=1
            # https://docs.google.com/file/d/1Li4nfkHuLPYkZ7JxAIYVoQBBxHy4l6Up/preview

            sHosterUrl = aEntry

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, '')

    gui.setEndOfDirectory()
