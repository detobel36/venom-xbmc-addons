# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager


SITE_IDENTIFIER = 'neko_sama'
SITE_NAME = 'Neko Sama'
SITE_DESC = 'Animés en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showLastEp')
ANIM_VFS = (URL_MAIN + 'anime-vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime', 'showMovies')

URL_SEARCH = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_ANIMS = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_VF = (ANIM_VFS[0], 'showSearchResult')

FUNCTION_SEARCH = 'showSearchResult'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VOSTFR)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VF)',
        'search.png',
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showSearchResult(sSearchText)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchResult(sSearch):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    searchURL = URL_MAIN[:-1] + \
        re.search('var urlsearch = "([^"]+)";', sHtmlContent).group(1)

    bGlobal_Search = False
    if sSearch:
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch = sSearch.replace(URL_SEARCH[0], '')
    sSearch = sSearch.lower()

    oRequestHandler = RequestHandler(searchURL)
    data = oRequestHandler.request(jsonDecode=True)

    output_parameter_handler = OutputParameterHandler()
    for dicts in data:
        if sSearch in dicts['title'].lower() or sSearch in dicts['title_english'].lower(
        ) or sSearch in dicts['others'].lower():
            title = dicts['title']
            sUrl2 = URL_MAIN[:-1] + dicts['url']
            sThumb = dicts['url_image']
            desc = ''

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addAnime(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def showLastEp():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '"episode":"([^"]+)".+?","title":"([^"]+)".+?"lang":"([^"]+)".+?"anime_url":"([^"]+)".+?"url_bg":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[3]
            sThumb = aEntry[4]
            sLang = aEntry[2].upper()
            title = '%s %s [%s]' % (aEntry[1], aEntry[0], sLang)
            desc = ''

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)">.+?src="([^"]+)" alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2]
            desc = ''

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addAnime(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

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
    sPattern = '>([^<]+)</a><a href="([^"]+)" class=""><svg'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisonEpisodes():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    if sUrl.endswith("vostfr"):
        oRequestHandler = RequestHandler(sUrl.replace('vostfr', 'vf'))
        sHtmlContent = oRequestHandler.request()
        if "404 Not Found" not in sHtmlContent:
            output_parameter_handler = OutputParameterHandler()
            title = "[COLOR red]Cliquez ici pour accéder à la version VF[/COLOR]"
            output_parameter_handler.addParameter(
                'siteUrl', sUrl.replace('vostfr', 'vf'))
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                output_parameter_handler)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    try:
        sPattern = '<p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = '"episode":"([^"]+)".+?"url":"([^"]+)","url_image":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = sMovieTitle + ' ' + aEntry[0].replace('Ep. ', 'E')
            sUrl2 = URL_MAIN[:-1] + aEntry[1].replace('\\/', '/')
            sThumb = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "video\\[\\d+\\] = \'([^']+)\'"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Enlève les faux liens
            # if 'openload' in aEntry or '.mp4' not in aEntry:
            if 'openload' in aEntry or 'mystream.to' in aEntry or "streamtape" in aEntry:
                continue

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
