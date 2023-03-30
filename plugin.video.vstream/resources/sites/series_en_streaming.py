# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

"""
Pour rappel.
Problème avec les DNS en ipv6 il faut utiliser les suivantes
CloudFlare DNS:
Préféré : 2606:4700:4700::1111
Auxiliaire : 2606:4700:4700::1001
Ou:
Google DNS:
Préféré : 2001:4860:4860::8888
Auxiliaire : 2001:4860:4860::8844
"""

import re
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, dialog, SiteManager
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'series_en_streaming'
SITE_NAME = 'Series-en-Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'category/series/?orderby=date', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
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


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(URL_SEARCH[0] + sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Classique', 'classique'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'],
             ['Dessin animés', 'dessin-anime'], ['Divers', 'divers'], ['Documentaire', 'documentaire'],
             ['Drama', 'drama'], ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'],
             ['Historique', 'historique'], ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'],
             ['Péplum', 'peplum'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science-fiction', 'science-fiction'], ['Soap', 'soap'], ['Thriller', 'thriller'],
             ['Webséries', 'webserie'], ['Western', 'western']]

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

    sPattern = '<div class="video\\s.+?href="([^"]+).+?class="izimg".+?src="([^"]+).+?title="([^"]+)'
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

            sUrl = aEntry[0]
            title = aEntry[2].replace(' Streaming', '')

            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            # tris search
            if sSearch and total > 3:
                if not oUtil.CheckOccurence(sSearch, title):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', sThumb, '', output_parameter_handler)

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
    sPattern = '>([^<]+)</a></div><span class="son bg"><a href="([^"]+)" *>Suivante'
    oParser = Parser()
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
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération des Synopsis
    desc = ''
    try:
        sPattern = '<b>Synopsis :</b>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
            desc = desc.replace('\\', '')
    except BaseException:
        pass

    sPattern = '<a href="([^"]+)" class="post-page-numbers".+?<span>([^<>]+)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' episode ' + aEntry[1]

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

    sPattern = '<span class="lg">(.+?)</span>|myLecteur">Lecteur (?:<b>)*([a-z]+)(?:</b>)* *:</span> <a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sLang = ''

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                # sLang = aEntry[0].replace('Langue(', 'Langue -')
                sLang = aEntry[0].replace('(', '- ').replace(')', '').strip()
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    sLang +
                    '[/COLOR]')
            else:
                sHost = aEntry[1].capitalize()
                sUrl = aEntry[2]
                if sUrl.startswith('/'):
                    sUrl = URL_MAIN[:-1] + sUrl

                sDisplayTitle = (
                    '%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sLang', sLang)
                output_parameter_handler.addParameter('sHost', sHost)
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

    # lien commençant par VID_
    Codedurl = url
    oRequestHandler = RequestHandler(Codedurl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        postdata = 'k=' + aResult[1][0]

        dialog().VSinfo('Décodage en cours', "Patientez", 5)
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

        # recherche d'un lien redirigé
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0]

    return ''
