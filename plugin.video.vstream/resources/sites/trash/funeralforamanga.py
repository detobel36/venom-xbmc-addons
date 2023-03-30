# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 44 https://funeralforamanga.fr/
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress


SITE_IDENTIFIER = 'funeralforamanga'
SITE_NAME = 'Funeral for a manga'
SITE_DESC = 'animés en streaming'

URL_MAIN = 'https://funeralforamanga.fr/'

ANIM_ANIMS = ('http://', 'load')

ANIM_NEWS = (URL_MAIN + 'videos?sk=c&unlicenced=1&p=1', 'showMovies')
ANIM_POPULAR = (URL_MAIN + 'videos?sk=b&unlicenced=1&p=1&', 'showMovies')
ANIM_ANNEES = (True, 'showAllYears')
ANIM_ALPHA = (True, 'showAllAlpha')
ANIM_GENRES = (True, 'showAllGenre')
ANIM_VFS = (URL_MAIN + 'videos?sk=c&unlicenced=1&lang=vf&p=1', 'showMovies')
ANIM_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&unlicenced=1&lang=vostfr&p=1',
    'showMovies')

ANIM_SERIE_NEWS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&p=1',
    'showMovies')
ANIM_SERIE_POPULAR = (
    URL_MAIN +
    'videos?sk=b&filter=serie&unlicenced=1&p=1',
    'showMovies')
ANIM_SERIE_ANNEES = (True, 'showSerieYears')
ANIM_SERIE_ALPHA = (True, 'showSerieAlpha')
ANIM_SERIE_GENRES = (True, 'showSerieGenre')
ANIM_SERIE_VFS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&lang=vf&p=1',
    'showMovies')
ANIM_SERIE_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&filter=serie&unlicenced=1&lang=vostfr&p=1',
    'showMovies')

ANIM_MOVIE_NEWS = (
    URL_MAIN +
    '/videos?sk=c&filter=movie&unlicenced=1&p=1',
    'showMovies')
ANIM_MOVIE_POPULAR = (
    URL_MAIN +
    '/videos?sk=b&filter=movie&unlicenced=1&p=1',
    'showMovies')
ANIM_MOVIE_ANNEES = (True, 'showMovieYears')
ANIM_MOVIE_ALPHA = (True, 'showMovieAlpha')
ANIM_MOVIE_GENRES = (True, 'showMovieGenre')
ANIM_MOVIE_VFS = (
    URL_MAIN +
    'videos?sk=c&filter=movie&unlicenced=1&lang=vf&p=1',
    'showMovies')
ANIM_MOVIE_VOSTFRS = (
    URL_MAIN +
    'videos?sk=c&filter=movie&unlicenced=1&lang=vostfrp=1',
    'showMovies')

URL_SEARCH_ANIMS = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_INTERNALSEARCH_SERIES = (
    URL_MAIN +
    'videos?filter=serie&unlicenced=1&q=',
    'showMovies')
URL_INTERNALSEARCH_MOVIES = (
    URL_MAIN +
    'videos?filter=movie&unlicenced=1&q=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_POPULAR[1],
        'Animés (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ALPHA[1],
        'Animés (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_NEWS[1],
        'Animés Séries (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_POPULAR[1],
        'Animés Séries (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_ANNEES[1],
        'Animés Séries (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_ALPHA[1],
        'Animés Séries (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_GENRES[1],
        'Animés Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_VOSTFRS[1],
        'Animés Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_SERIE_VFS[1],
        'Animés Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_NEWS[1],
        'Animés Films (Récents)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_POPULAR[1],
        'Animés Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_ANNEES[1],
        'Animés Films (Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_ALPHA[1],
        'Animés Films (Alpha)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_GENRES[1],
        'Animés Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_VOSTFRS[1],
        'Animés Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE_VFS[1],
        'Animés Films (VF)',
        'vf.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieAlpha():
    showAllAlpha('movie')


def showSerieAlpha():
    showAllAlpha('serie')


def showAllAlpha(sfilter=''):
    gui = Gui()
    import string
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)

    url1 = 'videos?sk=a&alpha='
    url2 = '&filter=' + sfilter + '&unlicenced=1&p=1'

    output_parameter_handler = OutputParameterHandler()
    for alpha in listalpha:
        title = str(alpha).upper()
        sUrl = URL_MAIN + url1 + alpha + url2
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


def showMovieYears():
    showAllYears('movie')


def showSerieYears():
    showAllYears('serie')


def showAllYears(sfilter=''):
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1983, 2023)):
        sYear = str(i)
        url1 = 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&aired-min=' + \
            sYear + '&aired-max=' + sYear + '&p=1'
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + url1)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            sYear,
            'annees.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showMovieGenre():
    showAllGenre('movie')


def showSerieGenre():
    showAllGenre('serie')


def showAllGenre(sfilter=''):
    gui = Gui()

    listegenre = [
        'action',
        'aventure',
        'comedie',
        'drame',
        'fantastique',
        'horreur',
        'policier',
        'romance',
        'science-fiction',
        'sexy',
        'sport']

    url1 = URL_MAIN + 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&genres='
    url2 = '&p=1'
    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:
        title = igenre.capitalize()
        sUrl = url1 + igenre + url2
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
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


def showSearchMovie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_INTERNALSEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_INTERNALSEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):

    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = "col-sm-4 col-md-3\">.+?href=\"([^\"]+).+?url\\(\'([^']+).+?<span class=.anime-label.+?uppercase.>([^<]+).+?anime-header.>([^<]+)"

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

            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sType = aEntry[2]
            title = aEntry[3]
            sDisplayTitle = title + ' [' + sType + ']'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addAnime(
                SITE_IDENTIFIER,
                'showEpisodesxMovies',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent, sUrl)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, sUrl):
    sNumberMax = ''
    sPattern = '"text-muted">page.+?sur\\s*(\\d+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0]

    sPattern = '&p=(\\d+)'
    aResult = oParser.parse(sUrl, sPattern)
    if aResult[0]:
        sNumberCurrent = aResult[1][0]
        iNumberCurrent = int(sNumberCurrent)
        iNumberNext = iNumberCurrent + 1
        sNumberNext = str(iNumberNext)
        sNextPage = sUrl.replace('&p=' + sNumberCurrent, '&p=' + sNumberNext)
        if sNumberMax:
            if int(sNumberMax) >= iNumberNext:
                return sNextPage, sNumberNext + '/' + sNumberMax
        else:
            return sNextPage, sNumberNext
    return False, False


def showEpisodesxMovies():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    sPattern = '<h4>Intrigue<.h4>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                        cleanDesc(aResult[1][0]))

    if 'aucune vidéo disponible' in sHtmlContent:
        gui.addText(SITE_IDENTIFIER, 'Aucune video disponible')
        gui.setEndOfDirectory()
        return

    sHtmlContent1 = oParser.abParse(
        sHtmlContent,
        '<h4 class="list-group-item-heading">',
        '<div id="footer')

    sPattern = '<h4 class="list-group-item-heading">([^<]+)<.h4>|<a href="([^"]+).+?(?:group-item-text">|>)([^<]+)(?:<.p>|<.a>)'
    sPattern = sPattern
    aResult = oParser.parse(sHtmlContent1, sPattern)

    sLang = ''
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0]
                continue

            if sLang:
                sUrl = URL_MAIN[:-1] + aEntry[1]
                title = sMovieTitle + ' ' + \
                    aEntry[2].replace('Épisode', 'Episode')

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sLang', sLang)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="subsection">.+?label-default">\\D*(\\d+)([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1].replace(' ', '').replace('-', '')
            sHost = re.sub('\\.\\w+', '', sHost)
            pdata = 'id=' + sId
            sMovieTitle = re.sub('\\[.+?\\]', '', sMovieTitle)
            sDisplayTitle = (
                '%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            sUrl2 = URL_MAIN + 'remote/ajax-load_video'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('siteRefer', sUrl)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    pdata = input_parameter_handler.getValue('pdata')
    siteRefer = input_parameter_handler.getValue('siteRefer')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', siteRefer)
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequestHandler.addParametersLine(pdata)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'frame.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sHosterUrl = aResult[1][0]
        if 'https:' not in sHosterUrl:
            sHosterUrl = 'https:' + sHosterUrl
        # VSlog(sHosterUrl)
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def cleanDesc(desc):
    oParser = Parser()
    sPattern = '(<.+?>)'
    aResult = oParser.parse(desc, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            desc = desc.replace(aEntry, '')
    return desc
