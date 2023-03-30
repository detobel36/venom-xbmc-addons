# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Progress, SiteManager
import re
return False  # l'adresse a changé mais plus du tout le meme site, le 06/06/22


SITE_IDENTIFIER = 'zustream'
SITE_NAME = 'ZuStream'
SITE_DESC = 'Retrouvez un énorme répertoire de films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuFilms')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/mangas/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (True, 'showYearsSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche films',
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


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche séries',
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

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Mangas)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/' + sUrl])
    liste.append(['Animation', URL_MAIN + 'genre/animation/' + sUrl])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/' + sUrl])
    liste.append(['Biopic', URL_MAIN + 'genre/biographie/' + sUrl])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/' + sUrl])
    liste.append(['Comédie musicale', URL_MAIN + 'genre/musique/' + sUrl])
    liste.append(['Comédie romantique', URL_MAIN + 'genre/romance/' + sUrl])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/' + sUrl])
    liste.append(['Drame', URL_MAIN + 'genre/drame/' + sUrl])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/' + sUrl])
    liste.append(['Famille', URL_MAIN + 'genre/familial/' + sUrl])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/' + sUrl])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/' + sUrl])
    liste.append(['Historique', URL_MAIN + 'genre/histoire/' + sUrl])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/' + sUrl])
    liste.append(['Noël', URL_MAIN + 'genre/noel/' + sUrl])
    liste.append(['Science Fiction', URL_MAIN +
                 'genre/science-fiction/' + sUrl])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/' + sUrl])
    liste.append(['Western', URL_MAIN + 'genre/western/' + sUrl])

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


def showNetwork():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NETFLIX[0])
    output_parameter_handler.addParameter('sTmdbId', 213)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_CANAL[0])
    output_parameter_handler.addParameter('sTmdbId', 285)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_AMAZON[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 1024)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_DISNEY[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 2739)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_APPLE[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 2552)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    output_parameter_handler.addParameter(
        'sTmdbId', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (YouTube Originals)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1995, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'sortie/' + Year + '/?post_types=movies')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYearsSeries():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1997, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'sortie/' + Year + '/?post_types=tvshows')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()
    oUtil = cUtil()

    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
        sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)</p>'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sPattern = 'article id="post-\\d+".+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)href="([^"]+).+?class="texto">(.*?)</div>'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
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

            sLang = ''
            sYear = ''
            desc = ''
            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                title = aEntry[2]
                desc = aEntry[3]

                # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue
            else:
                sThumb = aEntry[0]
                title = aEntry[1]
                if aEntry[2]:
                    sLang = aEntry[2]
                if aEntry[3]:
                    sYear = aEntry[3]
                sUrl = aEntry[4]
                if aEntry[5]:
                    desc = aEntry[5]

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = oUtil.unescape(desc).encode(
                    'utf-8')    # retire les balises HTML
            except BaseException:
                pass

            sDisplayTitle = ('%s (%s) (%s)') % (title, sLang, sYear)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            if '/serie' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
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
    oParser = Parser()
    sPattern = '<span>Page.+?de ([^<]+)</span.+?href="([^"]+)(?:"><i id=\'nextpaginat|" ><span class="icon-chevron-rig)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaison():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<span class='title'>Saisons (.+?) *<i>"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sNumSaison = aEntry[0].strip()
            title = sMovieTitle + ' saison ' + sNumSaison
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            output_parameter_handler.addParameter('siteUrl', sUrlSaison)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(SITE_IDENTIFIER, 'showSxE', title, '',
                          sThumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')
    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "class='numerando'>(\\d+) - (\\d+)</div><div class='episodiotitle'><a href='([^']+)'"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            s = aEntry[0]
            if s != sNumSaison:
                continue
            e = aEntry[1]
            sUrl = aEntry[2]
#            SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', aEntry[0])
            title = sMovieTitle + ' Saison %s Episode %s' % (s, e)

            output_parameter_handler.addParameter('siteUrl', sUrl)
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


def showLink(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            # fonctionne pour Film ou Série (pour info : série -> dtype = 'tv')
            dtype = 'movie'
            dpost = aEntry[0]
            dnum = aEntry[1]
            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype
            sLang = aEntry[2].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '').replace(
                ')',
                '')

            if 'VIP - ' in sLang:  # Les liens VIP ne fonctionnent pas
                continue

            title = ('%s [%s]') % (sMovieTitle, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('pdata', pdata)
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
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    oRequest = RequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    # 1
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=[\'|"]([^\'"|]+)'
    aResult1 = re.findall(sPattern, sHtmlContent)

    # 2
    sPattern = '<a href="([^"]+)">'
    aResult2 = re.findall(sPattern, sHtmlContent)

    # fusion
    aResult = aResult1 + aResult2

    if aResult:
        for aEntry in aResult:

            sHosterUrl = aEntry
            if 'zustreamv2/viplayer' in sHosterUrl:
                return

            if 're.zu-lien.com' in sHosterUrl:
                oRequestHandler = RequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry(
                    'Referer', 'https://re.zu-lien.com')
                oRequestHandler.request()
                sUrl1 = oRequestHandler.getRealUrl()
                if not sUrl1 or sUrl1 == sHosterUrl:
                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.disableRedirect()
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry(
                        'Referer', 'https://re.zu-lien.com')
                    oRequestHandler.request()

                    getreal = sHosterUrl

                    if oRequestHandler.statusCode() == 302:
                        redirection_target = reponse.getResponseHeader()[
                            'Location']
                else:
                    sHosterUrl = sUrl1

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
