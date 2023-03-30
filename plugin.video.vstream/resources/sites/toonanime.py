# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import urlEncode

try:
    xrange
except NameError:
    xrange = range

SITE_IDENTIFIER = 'toonanime'
SITE_NAME = 'Toon Anime'
SITE_DESC = 'anime en VF/VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_VFS = (URL_MAIN + 'anime-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-vostfr/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'films/', 'showMovies')
ANIM_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        "Recherche d'animés",
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_FILM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_FILM[1],
        "Film d'animation japonais (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Dernier ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

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
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'Action'], [
            'Animation', 'Action'], [
                'Aventure', 'Aventure'], [
                    'Comédie', 'Comédie'], [
                        'Tranche de Vie', 'Tranche de vie'], [
                            'Drame', 'Drame'], [
                                'Fantasy', 'Fantasy'], [
                                    'Surnaturel', 'Surnaturel'], [
                                        'Mystère', 'Mystère'], [
                                            'Shonen', 'Shonen'], [
                                                'Psychologique', 'Psychologique'], [
                                                    'Romance', 'Romance'], [
                                                        'Science-Fiction', 'Sci-Fi']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'xfsearch/genre/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(xrange(1982, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'xfsearch/year/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    bGlobal_Search = False
    if sSearch:
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        query_args = (('do', 'search'), ('subaction', 'search'),
                      ('story', sSearch), ('titleonly', '0'), ('full_search', '1'))
        data = urlEncode(query_args)

        oRequestHandler = RequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_SEARCH[0])
        oRequestHandler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addHeaderEntry('Content-Length', str(len(data)))
        sHtmlContent = oRequestHandler.request()
    else:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    if "/films/" in sUrl:
        sPattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" alt="([^"]+).+?pg">([^<]+).+?text">([^<]+)'
    else:
        sPattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" alt="([^"]+).+?pg">([^<]+).+?cat">([^<]+).+?text">([^<]+)'

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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            if "/films/" in sUrl:
                title = aEntry[2]
                sQual = aEntry[3]
                desc = aEntry[4]
                sLang = ""
            else:
                sLang = aEntry[2].split(" ")[-1]
                title = re.sub('Saison \\d+',
                                '',
                                aEntry[2][:aEntry[2].rfind('')].replace(sLang,
                                                                        "")) + " " + aEntry[4]
                sQual = aEntry[3]
                desc = aEntry[5]

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sLang.upper())

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addAnime(
                SITE_IDENTIFIER,
                'ShowSxE',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href="([^"]+)"><span class="md__icon md-arrowr"></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def ShowSxE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    # sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    # sMovieTitle = re.sub('Episode \d+', '', sMovieTitle)

    sID = sUrl.split('/')[3].split('-')[0]

    oRequestHandler = RequestHandler(
        URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']

    sPattern = 'href="(.+?)".+?title="(.+?)">'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = aEntry[1]
            sUrl2 = aEntry[0]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('id', sID)

            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                title,
                'animes.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sID = input_parameter_handler.getValue('id')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-class="(.+?) ".+?data-server-id="(.+?)"'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oRequestHandler = RequestHandler(
        URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sPattern = '<div id="content_player_' + aEntry[1] + '".+?>(.+?)<'
            aResult1 = oParser.parse(sHtmlContent, sPattern)
            hostClass = aEntry[0]

            for aEntry1 in aResult1[1]:
                # title = sMovieTitle  + " [COLOR coral]" + hostClass.capitalize() + "[/COLOR]"

                if "https" in aEntry1[0]:
                    sHosterUrl = aEntry1[0]
                elif hostClass == "cdnt":
                    sHosterUrl = "https://lb.toonanime.xyz/playlist/" + \
                        aEntry1 + "/" + str(round(time.time() * 1000))
                else:
                    oRequestHandler = RequestHandler(
                        URL_MAIN + "/templates/toonanime/js/anime.js")
                    sHtmlContent1 = oRequestHandler.request()

                    sPattern = 'player_type=="toonanimeplayer_' + \
                        hostClass + '".+?src=\\\\"([^\\\\]+)\\\\"'
                    urlBase = oParser.parse(sHtmlContent1, sPattern)[1][0]
                    sHosterUrl = urlBase.replace('"+player_content+"', aEntry1)

                if "toonanime" in sHosterUrl:
                    oHoster = HosterGui().checkHoster(".mp4")
                else:
                    oHoster = HosterGui().checkHoster(sHosterUrl)

                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
