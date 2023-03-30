# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'french_stream_lol'
SITE_NAME = 'French-stream-lol'
SITE_DESC = 'Films & séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'xfsearch/qualit/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/film-sous-titre/', 'showMovies')
MOVIE_VF_FRENCH = (URL_MAIN + 'xfsearch/version-film/French/', 'showMovies')
MOVIE_VF_TRUEFRENCH = (
    URL_MAIN +
    'xfsearch/version-film/TrueFrench/',
    'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'xfsearch/qualit/HDLight/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + 'film/film-netflix/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'xfsearch/version-serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VFS = (URL_MAIN + 'serie/serie-en-vf-streaming/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/serie-en-vostfr-streaming/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
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

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films',
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF_FRENCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_FRENCH[1],
        'Films (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_FRENCH[1],
        'Films (Netflix)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF_TRUEFRENCH[1],
        'Films (True French)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HDLIGHT[1],
        'Films (HD Light)',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

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

    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

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

    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_movies + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = []
    listegenre = [
        'action',
        'animation',
        'arts-martiaux',
        'aventure',
        'biopic',
        'comedie',
        'drame',
        'documentaire',
        'epouvante-horreur',
        'espionnage',
        'famille',
        'fantastique',
        'guerre',
        'historique',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + igenre + '/'])

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


def showSerieGenres():
    gui = Gui()

    liste = [['Action', 'serie-action'], ['Animation', 'animation-serie'], ['Aventure', 'aventure-serie'],
             ['Biopic', 'biopic-serie'], ['Comédie', 'serie-comedie'], ['Drame', 'drame-serie'],
             ['Famille', 'familles-serie'], ['Fantastique', 'serie-fantastique'], ['Historique', 'serie-historique'],
             ['Horreur', 'serie-horreur'], ['Judiciaire', 'serie-judiciare'], ['Médical', 'serie-medical'],
             ['Policier', 'serie-policier'], ['Romance', 'serie-romance'], ['Science-fiction', 'serie-science-fiction'],
             ['Thriller', 'serie-thriller'], ['Western', 'serie-western'], ['K-Drama', 'serie/k-drama']]

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
    sUrl = input_parameter_handler.getValue('siteUrl')

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        # sUrl = URL_SEARCH[0]  # sert a rien
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')

        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        sUrl = URL_MAIN + 'index.php?story=' + sSearch + '&do=search&subaction=search'
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        # la méthode suivante fonctionne mais pas à 100%
        # pdata = 'do=search&subaction=search&search_start=1&full_search=0&result_from=1&story=' + sSearch
        # oRequest = RequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        # oRequest.addHeaderEntry('Referer', URL_MAIN)
        # oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        # oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        # oRequest.addParametersLine(pdata)
        # sHtmlContent = oRequest.request()

    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]*)'
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
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            title = aEntry[2]

            if bSearchMovie:  # il n'y a jamais '/serie' dans sUrl2
                if '- Saison' in aEntry[2]:
                    continue
            if bSearchSerie:
                if '- Saison' not in aEntry[2]:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sDisplayTitle = title

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl2 or 'serie/' in sUrl or '/serie' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif bSearchSerie is True or '- Saison' in aEntry[2]:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovieLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
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
    oParser = Parser()
    sPattern = '(\\d+)</a>\\s*</span><span class="pnext"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'saison' not in sMovieTitle.lower():
        sPattern = 'saison-(\\d+)'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            sMovieTitle = sMovieTitle + ' Saison ' + aResult[1][0]

    sPattern = 'id="s-desc">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'french stream lol'
    if aResult[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                        cleanDesc(aResult[1][0]))

    sPattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\\d+)"\\s*href="([^"]+).+?data-rel="([^"]+).+?</i>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sLang = ''
    bFind = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and aEntry[1]:
                sFirst_Url = aEntry[1]
                sRel_Episode = aEntry[2]
                if sRel_Episode == "ABCDE":
                    sEpisode = 'Episode 2'
                else:
                    sEpisode = aEntry[3]

                title = sMovieTitle + ' ' + sEpisode
                sDisplayTitle = title + ' (' + sLang + ')'

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sLang', sLang)
                output_parameter_handler.addParameter(
                    'sRel_Episode', sRel_Episode)
                output_parameter_handler.addParameter('sFirst_Url', sFirst_Url)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSerieLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sLang = input_parameter_handler.getValue('sLang')
    sFirst_Url = input_parameter_handler.getValue('sFirst_Url')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sRel_Episode = input_parameter_handler.getValue('sRel_Episode')
    if not sRel_Episode:
        numEpisode = input_parameter_handler.getValue(
            'sEpisode')  # Gestion Up_Next
        if numEpisode:
            numEpisode = int(numEpisode)
            if 'VO' in sLang:
                numEpisode += 32
            if numEpisode == 2:
                sRel_Episode = 'ABCDE'
            else:
                sRel_Episode = 'episode%d' % numEpisode

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sRel_Episode + \
        '" class="fullsfeature".*?<li><a (id="singh.*?<div style="height)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        # dans cas ou il n'y a qu'un seul lien il n'y a pas de reference  dans <div id="episodexx" class="fullsfeature">
        # le pattern devient alors normalement hs
        if sFirst_Url:
            sHosterUrl = sFirst_Url
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    if aResult[0]:
        html = aResult[1][0]
        sPattern = 'href="([^"]+).*?aria-hidden'
        aResultUrl = oParser.parse(html, sPattern)
        if aResultUrl[0] is True:
            for aEntry in aResultUrl[1]:
                sHosterUrl = aEntry

                if 'http' not in sHosterUrl:  # liens naze du site url
                    continue

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showMovieLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    sPattern = '<li>\\s*<a.*?href="([^"]+).+?<\\/i>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sHosterName = ''

    if aResult[0]:
        for aEntry in aResult[1]:

            if 'FRENCH' not in aEntry[1] and 'VOSTFR' not in aEntry[1]:
                sHosterName = aEntry[1].strip()
                continue
            sLang = aEntry[1].strip()
            sDisplayTitle = '%s [%s] (%s)' % (sMovieTitle, sLang, sHosterName)

            sHosterUrl = aEntry[0]
            if 'http' not in sHosterUrl:  # liens nazes du site url
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def cleanDesc(desc):
    oParser = Parser()
    sPattern = '(Résumé.+?streaming Complet)'
    aResult = oParser.parse(desc, sPattern)

    if aResult[0]:
        desc = desc.replace(aResult[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        desc = desc.replace(s, '')

    return desc
