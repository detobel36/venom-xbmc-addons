# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # NPAI 04/02/2022

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = "https://www.film-streamingk.biz/"

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
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


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'views.png',
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

    # Inutilisable
    # output_parameter_handler.addParameter('siteUrl', SERIE_EPISODES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_EPISODES[1], 'Séries (Episodes)', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NETFLIX[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_AMAZON[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_CANAL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_DISNEY[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_APPLE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (Youtube Originals)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'action'], [
            'Animation', 'animation'], [
                'Aventure', 'aventure'], [
                    'Comédie', 'comedie'], [
                        'Crime', 'crime'], [
                            'Drame', 'drame'], [
                                'Familial', 'familial'], [
                                    'Fantastique', 'fantastique'], [
                                        'Guerre', 'guerre'], [
                                            'Horreur', 'horreur'], [
                                                'Histoire', 'histoire'], [
                                                    'Romance', 'romance'], [
                                                        'Thriller', 'thriller'], [
                                                            'Science-Fiction', 'science-fiction'], [
                                                                'Western', 'western']]

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


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch
        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH[0], ''))
        sPattern = 'class="image">.*?<a href="([^"]+)">\\s*<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)'
    elif 'episodes' in sUrl:
        sPattern = 'class="poster">.*?<img src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)'
    else:
        sPattern = 'class="poster"> *<img src="([^"]+)".+?<a href="([^"]+)" *title="([^"]+)".+?class="texto">([^<]*)'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # for the first sThumb in the movies "featured movies"
    if 'class="archive_post">' in sHtmlContent:
        sHtmlContent = oParser.abParse(
            sHtmlContent, 'class="archive_post">', '')
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

            # Si recherche et trop de resultat, on filtre
            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, aEntry[2]):
                    continue

            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                title = aEntry[2]
                desc = aEntry[3]
            elif 'episodes' in sUrl:
                sThumb = aEntry[0]
                title = aEntry[1]
                sUrl = aEntry[2]
                desc = ''
            else:
                sThumb = aEntry[0]
                sUrl = aEntry[1]
                title = aEntry[2].replace('streaming', ' ')
                desc = aEntry[3]

            # si utile il faut retirer output_parameter_handler.addParameter(desc)
            # if desc:  # désactivé le 17/06/2020,
                # try:
                # desc = cUtil().unescape(desc.decode('utf8'))
                # except AttributeError:
                # desc = cUtil().unescape(desc)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            if 'series' in sUrl:
                gui.addTV(SITE_IDENTIFIER, 'showSxE', title, '',
                          sThumb, desc, output_parameter_handler)
            elif 'episodes' in sUrl:
                gui.addTV(SITE_IDENTIFIER, 'showLinks', title, '',
                          sThumb, desc, output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
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
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'Page \\d+ de ([^<]+).+?arrow_pag\' *href="([^"]+)"><i id=\'nextpagination'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<span class="title">(.+?)<|class="numerando">([^"]+)</div><div class="episodiotitle"><a href="([^"]+)">'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    aEntry[0] +
                    '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub(
                    '(\\d+) - (\\d+)',
                    'saison \\g<1> Episode \\g<2>',
                    aEntry[1])
                title = sMovieTitle + ' ' + SxE

                # "MARQUER LU" à besoin de la saison et de l'épisode # sMovieTitle + ' ' + re.sub('saison \d+ ', '', SxE)
                sDisplaytitle = title

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplaytitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if 'episodes' in sUrl:
        sPattern = 'dooplay_player_option.+?data-post="(\\d+)".+?data-nume="([^"]+).+?title">([^<]+)'
    else:
        sPattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='([^']+).+?title'>([^<]+)"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if ('trailer' in aEntry[1]):
                continue
            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            if 'episodes' in sUrl:
                dtype = 'tv'
            else:
                dtype = 'movie'
            dpost = aEntry[0]
            dnum = aEntry[1]
            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype

            # trie des hosters
            sHoster = aEntry[2].capitalize()
            oHoster = HosterGui().checkHoster(sHoster)
            if not oHoster:
                continue

            sDisplaytitle = '%s [COLOR coral]%s[/COLOR]' % (
                sMovieTitle, sHoster)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('pdata', pdata)
            output_parameter_handler.addParameter('sHost', sHoster)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplaytitle,
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
    oRequest.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
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
    sPattern = "<iframe.+?src='(.+?)'"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        for aEntry in aResult:
            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
