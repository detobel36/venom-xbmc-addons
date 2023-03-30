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

SITE_IDENTIFIER = 'kstreamingserie'
SITE_NAME = 'K Streaming Série'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

SERIE_SERIE = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
# SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showList')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Afro', 'afro'], ['Animation', 'animation'], ['Arts Martiaux', 'art-martiaux'],
             ['Aventure', 'aventure'], ['Biographique', 'biographique'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Divers', 'divers'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Epouvante-horreur', 'epouvante-horreur'], ['Erotique', 'erotique'], ['Espionnage', 'espionnage'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Film-musical', 'film-musical'],
             ['Guerre', 'guerre'], ['Historique', 'historique'], ['Horreur', 'horreur'], ['Judiciaire', 'judiciaire'],
             ['Musical', 'musique'], ['Mystère', 'mystere'], ['Non classé', 'non-classe'], ['Policier', 'policier'],
             ['Romance', 'romance'], ['Science fiction', 'science-fiction'], ['Slasher', 'slasher'],
             ['Sport', 'sport-event'], ['Terreur', 'thriller/terreur'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    # sHtmlContent = oParser.abParse(sHtmlContent, '<h1>Listes des séries:</h1>', 'Copyright')

    sPattern = 'class="cat-item cat-item-.+?"><a href="([^"]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        # series = []

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = aEntry[1]
            # series.append((title, sUrl))

        # Trie des séries par ordre alphabétique
        # series = sorted(series, key=lambda serie: serie[0])

        # for title, sUrl:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    if 'Récemment ajoutées' in sHtmlContent:
        sStart = 'Récemment ajoutées'
        sEnd = 'Séries streaming les plus populaires'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+).+?(?:|story\'>([^<]+).+?)movie-cast'
    if sSearch:
        sPattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+)'

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

            sThumb = aEntry[0]
            title = re.sub('\\(\\d{4}\\)', '', aEntry[1])
            sUrl = aEntry[2]

            if sSearch:     # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            desc = ''  # absente pour la recherche
            if len(aEntry) > 3:
                desc = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addTV(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
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
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a></div><div class="naviright"><a href="([^"]+?)" >Suivant'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'movie-poster.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2].replace(' Streaming', '')

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

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    try:
        sPattern = 'line-clamp line-hide">(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0].replace('<br />', '').replace('</div>', '')
    except BaseException:
        pass

    # recuperation du hoster de base
    sPattern = '<div class="keremiya_part"> <span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ListeUrl = []
    if aResult[0]:
        ListeUrl = [(sUrl, aResult[1][0])]

    # Recuperation des suivants
    sPattern = '<a href="([^"]+)" class="post-page-numbers"><span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in ListeUrl:
            sUrl = aEntry[0]
            title = sMovieTitle + ' Episode' + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
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

    # si un seul episode
    else:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter(
            'sMovieTitle', sMovieTitle + ' episode 1')
        output_parameter_handler.addParameter('sThumb', sThumb)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            sMovieTitle +
            ' episode 1',
            '',
            sThumb,
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h3>.+?(VF|VOSTFR)\\s*<\\/h3>\\s*<p><\\/p>|<iframe.+?src="([^"]+)"'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            # langue
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]')
            # hote
            else:
                sHosterUrl = aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
