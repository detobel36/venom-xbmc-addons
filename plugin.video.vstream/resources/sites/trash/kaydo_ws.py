# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Il faut faire le code pour le nouvel hoster.
from resources.lib.util import Noredirection
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import time
import base64
import re
return False


# copie du site http://www.kaydo.ws/
# copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hdss.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'mieux-notes/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showMovieGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tv-series-z/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'

UA = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'


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

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films et Séries (Genres)',
        'genres.png',
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
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par lettre)',
        'az.png',
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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Film',
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
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par lettre)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()

    liste = []
    liste.append(['#', URL_MAIN + 'letter/0-9/'])
    liste.append(['A', URL_MAIN + 'letter/a/'])
    liste.append(['B', URL_MAIN + 'letter/b/'])
    liste.append(['C', URL_MAIN + 'letter/c/'])
    liste.append(['D', URL_MAIN + 'letter/d/'])
    liste.append(['E', URL_MAIN + 'letter/e/'])
    liste.append(['F', URL_MAIN + 'letter/f/'])
    liste.append(['G', URL_MAIN + 'letter/g/'])
    liste.append(['H', URL_MAIN + 'letter/h/'])
    liste.append(['I', URL_MAIN + 'letter/i/'])
    liste.append(['J', URL_MAIN + 'letter/j/'])
    liste.append(['K', URL_MAIN + 'letter/k/'])
    liste.append(['L', URL_MAIN + 'letter/l/'])
    liste.append(['M', URL_MAIN + 'letter/m/'])
    liste.append(['N', URL_MAIN + 'letter/n/'])
    liste.append(['O', URL_MAIN + 'letter/o/'])
    liste.append(['P', URL_MAIN + 'letter/p/'])
    liste.append(['Q', URL_MAIN + 'letter/q/'])
    liste.append(['R', URL_MAIN + 'letter/r/'])
    liste.append(['S', URL_MAIN + 'letter/s/'])
    liste.append(['T', URL_MAIN + 'letter/t/'])
    liste.append(['U', URL_MAIN + 'letter/u/'])
    liste.append(['V', URL_MAIN + 'letter/v/'])
    liste.append(['W', URL_MAIN + 'letter/w/'])
    liste.append(['X', URL_MAIN + 'letter/x/'])
    liste.append(['Y', URL_MAIN + 'letter/y/'])
    liste.append(['Z', URL_MAIN + 'letter/z/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
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

    input_parameter_handler = InputParameterHandler()
    siteUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(siteUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sHtmlContent = oParser.abParse(
        sHtmlContent,
        '"AAIco-movie_creation">Genres</label>',
        '</div>')
    sPattern = 'data-val="([^"]+)" data-value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sGenre = aEntry[0]
            if sGenre in ('random', 'Uncategorized'):
                continue
            sFilter = aEntry[1]
            sUrl = siteUrl + '?s=trfilter&trfilter=1&geners%5B%5D=' + sFilter

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                sGenre,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    if URL_MAIN + 'letter/' in sUrl:
        sPattern = '<td class="MvTbImg">.+?href="([^"]+).+?src="([^"]*).+?class="MvTbTtl.+?<strong>([^<]*).+?<td>([^<]*).+?Qlty">([^<]+).+?<td>([^<]*)'
    else:
        sPattern = 'class="TPost C".+?href="([^"]+).+?src="([^"]*).+?Title">([^<]+).+?(?:|Year">([^<]*).+?)(?:|Qlty">([^<]*).+?)Description"><p>([^<]+)'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()
    # réécriture pour prendre les séries dans le menu des genres
    # sHtmlContent = sHtmlContent.replace('<span class="Qlty">TV</span></div><h3', '</div><h3')

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

            siteUrl = aEntry[0]
            sThumb = re.sub('/w\\d+', '/w342', aEntry[1])
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
            title = aEntry[2]
            sYear = aEntry[3]
            sQual = aEntry[4]
            desc = aEntry[5]
            if sYear.lower() == 'unknown':
                sYear = ''
            if sQual.lower() == 'unknown':
                sQual = ''

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sYear)

            output_parameter_handler.addParameter('siteUrl', siteUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sQual', sQual)

            if '/serie/' in siteUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'ShowSaisonEpisodes',
                    sDisplayTitle,
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

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
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
    sPattern = '>([^<]+?)</a><a class="next page-numbers" href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def ShowSaisonEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="Title AA-Season.+?>Season <span>([^<]+)</span>|class="MvTbImg">.+?img src.+?["|;]([^\"]+?)["|;].+?href="([^"]+)">([^<]+)<'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]Saison: ' +
                    aEntry[0] +
                    '[/COLOR]')
            else:
                sThumb = re.sub('/w\\d+', '/w342', aEntry[1], 1)
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sUrl2 = aEntry[2]
                title = aEntry[3]

                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)

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
    # UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    gui = Gui()
    oParser = Parser()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Recuperer variable pour url de base
    sPattern = 'trembed=(\\d+).+?trid=(\\d+).+?trtype=(\\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        list_site_film = []
        for aEntry in aResult[1]:

            site = URL_MAIN + "?trembed=" + \
                aEntry[0] + "&trid=" + aEntry[1] + "&trtype=" + aEntry[2]
            if aEntry[2] == '1':
                if site not in list_site_film:
                    list_site_film.append(site)
                else:
                    continue  # inutile de faire des requetes identiques pour les films

            oRequestHandler = RequestHandler(site)
            sHtmlContent = oRequestHandler.request()

            slug = re.search(
                '"Video".+?src=".+?v=(.+?)"',
                sHtmlContent).group(1)

            sHosterUrl = "https://geoip.redirect-ads.com/?v=" + slug

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def decode(t):
    a = len(t) - 1
    trde = ''
    while a >= 0:
        trde = trde + t[a]
        a -= 1

    return trde
