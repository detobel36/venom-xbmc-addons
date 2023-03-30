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

SITE_IDENTIFIER = 'dbanimes'
SITE_NAME = 'DBanimes'
SITE_DESC = 'animés en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_VOSTFRS = (URL_MAIN + 'genre/anime-vostfr/', 'showAnimes')
ANIM_NEWS = (URL_MAIN + 'genre/anime-vostfr/', 'showAnimes')
ANIM_MOVIES = (URL_MAIN + 'films/', 'showAnimes')
# ANIM_LIST = (URL_MAIN + 'liste/a/', 'showAlpha')
ANIM_GENRES = (True, 'showGenres')
ANIM_LAST_EPISODES = (URL_MAIN, 'showAnimes')
key_serie = '?key_serie&s='
key_film = '?key_film&s='

URL_SEARCH = (URL_MAIN + '?s=', 'showAnimes')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showAnimes')
URL_INTERNALSEARCH_SERIES = (URL_MAIN + key_serie, 'showAnimes')
URL_INTERNALSEARCH_MOVIES = (URL_MAIN + key_film, 'showAnimes')
FUNCTION_SEARCH = 'showAnimes'


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

    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_LAST_EPISODES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LAST_EPISODES[1],
        'Animés (Derniers épisodes)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIES[1],
        'Animés (Films)',
        'animes.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', ANIM_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Ordre alphabétique)', 'az.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [['Action & aventure', 'action-adventure'], ['Aventure', 'aventure'],
             ['Comédie', 'comedie'], ['Crime', 'crime'], ['Drame', 'drame'], ['Fantasy', 'fantasy']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'genre/anime-' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'class=liste><a href=(\\S+).+?mb-2">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sLetter = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('AZ', sLetter)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAnimes',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'az.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchMovie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_INTERNALSEARCH_MOVIES[0] + sSearchText
        showAnimes(sUrl)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_INTERNALSEARCH_SERIES[0] + sSearchText
        showAnimes(sUrl)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showAnimes(sUrl)
        gui.setEndOfDirectory()
        return


def showAnimes(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+') + '&post_type=anime&submit='
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'movie-gride-agile1.+?href="([^"]+)" title="([^"]+).+?src="([^"]+)'
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

            desc = ''
            sUrl2 = aEntry[0]
            title = aEntry[1].replace('VOSTFR', '').replace('vostfr', '').replace(
                'Vostfr', '')  # à confirmer : tous vostr meme ceux  notés non vostfr
            title = title.replace(
                'Saision', 'Saison').replace(
                'Sasion', 'Saison')
            sDisplayTitle = title
            sThumb = aEntry[2]

            if key_serie in sUrl:
                if 'film' in title.lower():
                    continue
            if key_film in sUrl:
                if 'film' not in title.lower():
                    continue

            if 'film' in title.lower():
                title = title.replace(
                    'Film', '').replace(
                    'film', '')  # à reverifier .replace('Movie', '')
                sDisplayTitle = title + ' [Film]'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if URL_MAIN + 'films/' == sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisodes',
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
                'showAnimes',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>(\\d+)</a></li><li><a class="next page-numbers" href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, False


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    sPattern = 'Synopsis\\s*:(.*?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                        cleanDesc(aResult[1][0]))

    sYear = ''
    sPattern = 'Année de Production.+?(\\d{4}).+?/div'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sYear = aResult[1][0]

    sPattern = 'href="([^"]+)" class="btn btn-default mb-2" title=.+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME, large=total > 50)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0]
            sEpisode = aEntry[1]
            title = sMovieTitle + ' ' + sEpisode
            sDisplayTitle = title
            if sYear:
                sDisplayTitle = title + '(' + sYear + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # i = 0
    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry.strip()
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'https:' + sHosterUrl

            # sHost = getHostName(sHosterUrl)
            # i = i + 1
            # sDisplayTitle = '%s [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHost)

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getHostName(url):
    oHoster = HosterGui().checkHoster(url)
    if oHoster:
        return oHoster.getDisplayName()
    try:
        if 'www' not in url:
            sHost = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        sHost = url
    return sHost.capitalize()


def cleanDesc(desc):
    oParser = Parser()
    sPattern = '(<.+?>)'
    aResult = oParser.parse(desc, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            desc = desc.replace(aEntry, '')
    return desc
