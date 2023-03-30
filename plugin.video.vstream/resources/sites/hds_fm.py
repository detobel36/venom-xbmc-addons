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


SITE_IDENTIFIER = 'hds_fm'
SITE_NAME = 'Hds-fm'
SITE_DESC = 'Films et Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/VOSTFR/', 'showMovies')
MOVIE_VF = (URL_MAIN + 'film/French/', 'showMovies')

MOVIE_HDLIGHT = (URL_MAIN + 'qualit/HDLight/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'serie-tv-streaming/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

SERIE_VFS = (URL_MAIN + 'serie/VF/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/VOSTFR/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on n'utilise pas le globale
MY_SEARCH_MOVIES = (True, 'myShowSearchMovie')
MY_SEARCH_SERIES = (True, 'myShowSearchSerie')

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

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF[1],
        'Films (VF)',
        'vf.png',
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VF[1],
        'Films (VF)',
        'vf.png',
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
        'series.png',
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


def myShowSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def myShowSearchMovie():
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

    # genre enlevés tous les films hs : Walt-Disney, Super_héros
    # arts-martiaux 4 films marche sur 150

    liste = []
    listegenre = [
        'action',
        'animation',
        'arts-martiaux',
        'aventure',
        'biopic',
        'comédie',
        'comédie-dramatique',
        'comédie-musicale',
        'drame',
        'documentaire',
        'epouvante_horreur',
        'espionnage',
        'famille',
        'fantastique',
        'musical',
        'guerre',
        'historique',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    # https://www1.hds.fm/film-genre/action
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'film-genre/' + igenre])

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
    liste = []
    listegenre = [
        'Action',
        'Animation',
        'Arts-martiaux',
        'Aventure',
        'Biopic',
        'Comédie',
        'Drame',
        'Epouvante_horreur',
        'Famille',
        'Historique',
        'Judiciaire',
        'Médical',
        'Policier',
        'Romance',
        'Science-fiction',
        'Sport-event',
        'Thriller',
        'Western']

    # https://www1.hds.fm/serie-genre/Drame/
    for igenre in listegenre:
        urlgenre = igenre
        if igenre == 'judiciaire':
            urlgenre = 'judiciare'
        liste.append([igenre.capitalize(), URL_MAIN +
                     'serie-genre/' + urlgenre + '/'])

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

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sSearch = sSearch.replace('%20', ' ')
        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)
        sSearch2 = sSearch.replace('-', '').strip().lower()
        sUrl = URL_SEARCH[0] + sSearch2
        oRequest = RequestHandler(sUrl)
        sHtmlContent = oRequest.request()

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # ref thumb title
    sPattern = 'class="TPostMv">.+?href="([^"]*).+?src="([^"]*).+?class="Qlty".+?class="Qlty.+?>([^<]*).+?center">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # itemss = 0

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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sLang = aEntry[2]
            title = aEntry[3]

            if bSearchMovie:
                if ' saison ' in title.lower():
                    continue
            if bSearchSerie:
                if ' saison ' not in title.lower():
                    continue

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue  # Filtre de recherche

            sDisplayTitle = ('%s (%s)') % (
                title.replace('- Saison', ' Saison'), sLang)
            if sSearch and not bSearchMovie and not bSearchSerie:
                if '/serie' in sUrl or '- saison ' in title.lower():
                    sDisplayTitle = sDisplayTitle + ' [Série]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [Film]'

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            # pour le debugage source avec bcpdechance d'etre hs
            # films didfficile a obtenir apres id= 18729
            # if not ('/serie' in sUrl or ' saison ' in title.lower()):
                # idmovie = get_id_int_Movie(sUrl2)
                # if idmovie  <= 18729:
                # sDisplayTitle = sDisplayTitle + ' *'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl or '- saison ' in title.lower():
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
                    'showHosters',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        bNextPage, sNextPage, sNumPage = __checkForNextPage(sHtmlContent)
        if bNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sNumberNext = ''
    sNumberMax = ''
    sNumPage = ''

    if '<a class="next"' not in sHtmlContent:
        return False, 'none', 'none'

    if 'class="end"' in sHtmlContent:
        sPattern = 'class="end".+?">(\\d+)'
    else:
        sPattern = '(\\d+)<.a>\\s*<a\\sclass="next"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0]

    sPattern = 'class="next.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0]  # minimum requis
        if 'htpp' not in sNextPage:
            sNextPage = URL_MAIN[:-1] + sNextPage
            if '/31/32/' in sNextPage:  # bug page 31
                sNextPage = re.sub('/31', '', sNextPage)
        try:
            sNumberNext = re.search('/(\\d+)/', sNextPage).group(1)
        except BaseException:
            pass

        if sNumberNext:
            sNumPage = sNumberNext
            if sNumberMax:
                sNumPage = sNumPage + '/' + sNumberMax

        if sNextPage:
            return True, sNextPage, sNumPage

    return False, 'none', 'none'


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

    sPattern = '<div class="Description">.*?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    desc = 'Hds Film'
    if aResult[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :',
                                                        cleanDesc(aResult[1][0]))

    sPattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\\d+)"\\s*href="([^"]+).+?title="([^"]+).+?data-rel="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    bFind = ''
    validEntry = ''
    sLang = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and aEntry[1]:
                validEntry = True
                sFirst_Url = aEntry[1]
                sEpisode = aEntry[2]
                sRel_Episode = aEntry[3]

                title = sMovieTitle.replace(
                    '- Saison', ' Saison') + ' ' + sEpisode
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
                    'showSeriesHosters',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    if not validEntry:
        gui.addText(SITE_IDENTIFIER, '# Aucune vidéo trouvée #')

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sRel_Episode = input_parameter_handler.getValue('sRel_Episode')
    sFirst_Url = input_parameter_handler.getValue('sFirst_Url')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sRel_Episode + \
        '" class="fullsfeature".*?<a (id="singh.*?<div style="height)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        # cas ou il n'y a qu'un seul lien  pas de référence  dans <div id="episodexx" class="fullsfeature">
        # le pattern est normalement hs
        if sFirst_Url:
            sUrl2 = sFirst_Url
            # sHost = '[COLOR coral]' + getHostName(sUrl2) + '[/COLOR]'

            # sDisplayTitle = sMovieTitle + ' ' + sHost
            sHosterUrl = sUrl2
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
                sUrl2 = aEntry
                # sHost = getHostName(sUrl2)
                if len(aResult[1]) == 1 and 'openload' in sUrl2:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue

                if isBlackHost(sUrl2):
                    continue

                # if 'hqq.tv' in sUrl2:
                    # continue

                # if 'www' in sHost.lower():
                    # sHost = getHostName(sUrl2)

                # sHost = '[COLOR coral]' + sHost + '[/COLOR]'
                # sDisplayTitle = sMovieTitle + ' ' + sHost

                sHosterUrl = sUrl2
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<a style=".+?cid="([^"]+).+?fa-play.+?i>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sHost = aEntry[1].strip().capitalize()
            if len(aResult[1]) == 1:
                if 'openload' in sHost.lower():
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue
                if 'oload' in sHost.lower():
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue] oload : site non sécurisé [/COLOR]')
                    continue

            if isBlackHost(sUrl2):
                continue

            # if 'hqq.tv' in sUrl2:
                # continue

            sHosterUrl = sUrl2
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(title)
                oHoster.setFileName(title)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


# teste id movie
def get_id_int_Movie(url):

    try:
        number = re.search('https.+?\\/(\\d+)', url).group(1)
        return int(number)
    except BaseException:
        return 20000
        pass
    return 20000


def getHostName(url):

    try:
        if 'opsktp' in url:
            sHost = re.search('http.+?opsktp.+?\\/([^\\/]+)', url).group(1)

        elif 'www' not in url:
            sHost = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        sHost = url

    return sHost.capitalize()


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


def isBlackHost(url):
    black_host = [
        'youflix',
        'verystream',
        'javascript',
        '4k-pl',
        'ffsplayer',
        'french-stream.ga',
        'oload.stream',
        'french-player.ga',
        'streamango.com',
        'hqq.tv']

    urllower = url.lower()
    for host in black_host:
        if host.lower() in urllower:
            return True
    return False
