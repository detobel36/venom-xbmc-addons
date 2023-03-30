# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import dialog, SiteManager


SITE_IDENTIFIER = 'streaming_series'
SITE_NAME = 'Streaming-Séries'
SITE_DESC = 'Regarder toutes vos séries en Streaming Gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSerieSearch',
        'Recherche',
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

    gui.setEndOfDirectory()


def showSerieSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
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
                        'Documentaire', 'documentaire'], [
                            'Drame', 'drame'], [
                                'Epouvante Horreur', 'epouvante-horreur'], [
                                    'Espionnage', 'espionnage'], [
                                        'Famille', 'famille'], [
                                            'Fantastique', 'fantastique'], [
                                                'Guerre', 'guerre'], [
                                                    'Historique', 'historique'], [
                                                        'Judiciaire', 'judiciaire'], [
                                                            'Medical', 'medical'], [
                                                                'Musical', 'musical'], [
                                                                    'Policier', 'policier'], [
                                                                        'Romance', 'romance'], [
                                                                            'Science Fiction', 'science-fiction'], [
                                                                                'Soap', 'soap'], [
                                                                                    'Thriller', 'thriller'], [
                                                                                        'Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'category/series/' + sUrl + '/')
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
        oUtil = cUtil()
        sUrl = sSearch.replace(' ', '+')
        sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH[0], ''))
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="post-thumbnail">.+?href="([^"]+)" *title="([^"]+).+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[2]
            title = aEntry[1]

            if sSearch:
                if not oUtil.CheckOccurence(sSearch, title):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

    if not sSearch:  # une seule page par recherche
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
    sPattern = '>([^<]+)</a></li><li class="pg-item"><a class="next page-numbers" href="([^"]+)">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    desc = ''
    try:
        sPattern = 'style="text-align:justify">(.+?)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
            desc = desc.replace('&#8220;', '\"').replace('&#8221;', '\"')
    except BaseException:
        pass

    # filtre pour ne prendre que sur une partie
    sStart = '<span>Informations</span>'
    sEnd = '<div class="content ">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?<span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' Episode ' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oParser = Parser()
    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = '<span class="lg">([^<]+)<|<span class="myLecteur">.+?<b>([^<]+)</b>.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sLang = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            # langue
            if aEntry[0]:
                sLang = aEntry[0].replace('(', '').replace(')', '')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    sLang +
                    '[/COLOR]')
            # hote
            else:
                sHost = aEntry[1]
                sUrl = URL_MAIN[:-1] + aEntry[2]
                title = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sLang', sLang)
                output_parameter_handler.addParameter('sHost', sHost)

                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    sThumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    sHosterUrl = protectStreamByPass(sUrl)

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def protectStreamByPass(url):

    # lien commencant par VID_
    Codedurl = url
    oRequestHandler = RequestHandler(Codedurl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        postdata = 'k=' + aResult[1][0]

        dialog().VSinfo('Décodage en cours', 'Patientez', 5)
        xbmc.sleep(5000)

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

        oRequest = RequestHandler(URL_MAIN + 'embed_secur.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Host', 'www.protect-stream.com')
        oRequest.addHeaderEntry('Referer', Codedurl)
        oRequest.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        oRequest.addParametersLine(postdata)
        sHtmlContent = oRequest.request()

        # Test de fonctionnement
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            dialog().VSinfo('Lien encore protégé', "Erreur", 5)
            return ''

        # recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0]

        # recherche d'un lien redirige
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0]

    return ''
