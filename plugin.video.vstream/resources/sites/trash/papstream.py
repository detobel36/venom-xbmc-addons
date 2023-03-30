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
return False  # 06/02/2021


SITE_IDENTIFIER = 'papstream'
SITE_NAME = 'PapStream'
SITE_DESC = 'Films, Séries'

URL_MAIN = 'https://www.papstream.in/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche/', 'showMovies')

# recherche globale MOVIE/TVSHOWS
key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

MOVIE_MOVIE = (URL_MAIN + 'films.html', 'showMoviesMenu')
MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (URL_MAIN + 'series.html', 'showSeriesMenu')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (URL_MAIN + 'animes.html', 'showAnimesMenu')
ANIM_NEWS = (URL_MAIN + 'animes.html', 'showMovies')
# ANIM_GENRES = (URL_MAIN + 'animes/', 'showGenres')
ANIM_ANNEES = (True, 'showAnimeYears')

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

    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesMenu():
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimesMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
        'annees.png',
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
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Animation', sUrl + 'animation/'])
    liste.append(['Aventure', sUrl + 'aventure/'])
    liste.append(['Biopic', sUrl + 'biopic/'])
    liste.append(['Comédie', sUrl + 'comedie/'])
    liste.append(['Comédie Dramatique', sUrl + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', sUrl + 'comedie-musicale/'])
    liste.append(['Documentaire', sUrl + 'documentaire/'])
    liste.append(['Drame', sUrl + 'drame/'])
    liste.append(['Epouvante Horreur', sUrl + 'epouvante-horreur/'])
    liste.append(['Famille', sUrl + 'famille/'])
    liste.append(['Fantastique', sUrl + 'fantastique/'])
    liste.append(['Guerre', sUrl + 'guerre/'])
    liste.append(['Policier', sUrl + 'policier/'])
    liste.append(['Romance', sUrl + 'romance/'])
    liste.append(['Science Fiction', sUrl + 'science-fiction/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

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


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1918, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films/annee-' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'series/annee-' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimeYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1965, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'animes/annee/' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        KeySearch = sSearch
        if key_search_movies in KeySearch:
            KeySearch = str(KeySearch).replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in KeySearch:
            KeySearch = str(KeySearch).replace(key_search_series, '')
            bSearchSerie = True
        sUrl = URL_SEARCH[0] + KeySearch
        oRequestHandler = RequestHandler(sUrl)

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="short-images-link".+?img src="([^"]+)".+?<a.+?>([^<]+).+?.+?<a.+?>([^<]+).+?short-link">\\s*<a href="([^"]+)".+?>([^<]+)<\\/a>'
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

            sThumb = URL_MAIN[:-1] + aEntry[0]
            sUrl2 = URL_MAIN[:-1] + aEntry[3].replace(
                '/animes/films/', '/films/').replace('/animes/series/', '/series/')
            title = aEntry[4]
            sQual = aEntry[1]
            sLang = aEntry[2].replace('French', 'VF')

            if bSearchMovie:
                if '/series/' in sUrl2:
                    continue
            if bSearchSerie:
                if '/films/' in sUrl2:
                    continue
            sDisplayTitle = ('%s (%s) [%s]') % (title, sQual, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/animes/' in sUrl2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    'animes.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif '/series/' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    'series.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    sDisplayTitle,
                    'films.png',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('-([0-9]+).html', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<div class="pages-numbers".+?<span>.+?</span><a href=["\']([^"\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return URL_MAIN[:-1] + aResult[1][0]

    return False


def showSaisons():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    sPattern = '</a>\\s*:\\s*</h2>\\s*(.+?)<div'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = aResult[1][0]

    # Decoupage pour cibler la partie des saisons
    sPattern = '<div id="full-video">(.+?)<div class="fstory'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult

    sPattern = '<a href="([^"]+)" title=".+?(saison\\s\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2
            sSaison = aEntry[1]
            title = ("%s %s") % (sMovieTitle, sSaison)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    desc = input_parameter_handler.getValue('desc')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="saision_LI2">\\s*<a title="(.+?)"\\s*href=["\']([^"\']+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry[0].replace(' en streaming', '')
            sUrl2 = URL_MAIN[:-1] + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if (not desc):
        sPattern = '</a>\\s*:\\s*</h2>\\s*(.+?)<div'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0].replace(' en Streaming Complet ', ': ')

    sPattern = '"#"\\srel="([^"]+).+?class="server.+?<img src="([^"]+).+?<span style=".+?">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sLang = aEntry[1].replace(
                '/Public/images/',
                '').replace(
                '.png',
                '')
            sQual = aEntry[2].replace('(', '').replace(')', '')

            if 'alliance4creativity' in sUrl2:
                continue

            oHoster = HosterGui().checkHoster(sUrl2)
            if (oHoster):
                sHost = oHoster.getDisplayName()
            else:
                sHost = GetHostname(sUrl2)

            title = '%s [%s] (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle,
                                                               sQual, sLang.upper(), sHost)

            output_parameter_handler.addParameter('refUrl', sUrl)
            output_parameter_handler.addParameter('sUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    refUrl = input_parameter_handler.getValue('refUrl')
    sUrl = input_parameter_handler.getValue('sUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    if sUrl.startswith('/'):
        sUrl = URL_MAIN[:-1] + sUrl

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', refUrl)
    oRequestHandler.request()
    vUrl = oRequestHandler.getRealUrl()

    if vUrl:
        sHosterUrl = vUrl
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


def GetHostname(url):

    try:
        if 'www' not in url:
            sHost = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        sHost = url

    return sHost.capitalize()
