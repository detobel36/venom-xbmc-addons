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
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'otakufr_com'
SITE_NAME = 'OtakuFR'
SITE_DESC = 'OtakuFR animés en streaming et téléchargement'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = (URL_MAIN, 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'film', 'showMovies')
ANIM_GENRES = (True, 'ShowGenre')
ANIM_LIST = (URL_MAIN + 'liste-anime/', 'showAlpha')

URL_SEARCH = (URL_MAIN + 'toute-la-liste-affiches/?q=', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'siteUrl')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIES[1],
        'Animés (Film)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
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

    if sSearch or '/genre/' in sUrl or '/film' in sUrl:  # news
        sPattern = '<figure class="m-0">.+?ref="([^"]+).+?(?:src="(.+?)"|\\.?) class.+?</i>([^<]+).+?Synopsis:.+?>([^<]+)'
    else:  # populaire et search
        sPattern = '<article class=".+?ref="([^"]+).+?src="([^"]+).+?title="([^"]+)'

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
            title = aEntry[2]
            sLang = ''
            if 'Vostfr' in title:
                sLang = 'VOSTFR'
                title = title.replace('Vostfr', '')
            desc = ''
            if sSearch or '/genre/' in sUrl or '/film' in sUrl:
                desc = aEntry[3]

            sDisplayTitle = title + ' (' + sLang + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if sSearch or '/genre/' in sUrl or '/film' in sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    'animes.png',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    'animes.png',
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
    sPattern = '>([^<]+)</a></li><li class="page-item"> <a class="next page-link" href="([^"]+)">Next'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def ShowGenre():
    gui = Gui()

    liste = [
        'action',
        'aventure',
        'comedie',
        'crime',
        'demons',
        'drame',
        'Ecchi',
        'espace',
        'fantastique',
        'gore',
        'harem',
        'historique',
        'horreur',
        'jeu',
        'lecole',
        'magie',
        'martial-arts',
        'mecha',
        'militaire',
        'musique',
        'mysterieux',
        'Parodie',
        'police',
        'psychologique',
        'romance',
        'samurai',
        'sci-fi',
        'seinen',
        'shoujo',
        'shoujo-ai',
        'shounen',
        'shounen-ai',
        'sport',
        'super-power',
        'surnaturel',
        'suspense',
        'thriller',
        'tranche-de-vie']

    output_parameter_handler = OutputParameterHandler()
    for igenre in liste:
        title = igenre.capitalize().replace('-', ' ')
        if 'Jeu' in igenre:
            title = 'Jeux'
        sUrl = URL_MAIN + 'genre/' + igenre + '/'
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
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
    sPattern = '<a href="([^<]+)">([A-Z#])</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sLetter = aEntry[1]
            Link = aEntry[0]

            output_parameter_handler.addParameter('siteUrl', URL_MAIN + Link)
            output_parameter_handler.addParameter('AZ', sLetter)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAZ',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'animes.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAZ():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    dAZ = input_parameter_handler.getValue('AZ')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'has-large-font-size.+?<strong>([^<]+)|<li><a href="([^"]+).+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    bValid = False
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                bValid = False
                if dAZ in aEntry[0]:
                    bValid = True
                    continue
            if bValid:
                sUrl = aEntry[1]
                title = aEntry[2]
                sDisplayTitle = title + ' (' + 'VOSTFR' + ')'
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    'animes.png',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    desc = ''
    sPattern = 'Synopsis:(.*?)(?:<ul|class="|Autre Nom)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = aResult[1][0]
        desc = cleanDesc(desc)

    sThumb = ''
    sPattern = 'ImageObject.*?primaryimage.+?"(https.*?jpg)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumb = aResult[1][0]

    sPattern = '(?:right">|<\\/a>)\\s*<a href="(https.+?\\/episode\\/.+?)".+?list-group-item.+?item-action">([^<]+)(?:Vostfr|Vf)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            Ep = aEntry[1].split(' ')[-2]
            title = aEntry[1].replace(Ep, '') + ' E' + Ep

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'animes.png',
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

    list_hostname = []
    sPattern = 'aria-selected="true">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            list_hostname.append(aEntry)

    # list_host = []
    # normalement on devrait correler le valeur de l'id avec list_hostname
    sPattern = 'iframe.+?src="([^"]*).+?id="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    i = 0
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            if 'https:' not in sUrl2:
                sUrl2 = 'https:' + sUrl2

            if len(aResult[1]) == len(list_hostname):
                sHost = list_hostname[i]
            else:
                sHost = GetHostname(sUrl2)
            i = i + 1
            sFilter = sHost.lower()
            if 'brightcove' in sFilter or 'purevid' in sFilter or 'videomega' in sFilter:
                continue

            sDisplayTitle = '%s [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteRefer', sUrl)
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
    siteRefer = input_parameter_handler.getValue('siteRefer')

    sHosterUrl = sUrl
    if 'parisanime' in sUrl:

        sHtmlContent = unCap(sUrl, siteRefer)

        sPattern = "data-url='([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def unCap(sHosterUrl, sUrl):

    oRequest = RequestHandler(sHosterUrl)
    oRequest.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    # Requete pour récupérer le cookie
    oRequest.request()
    Cookie = oRequest.GetCookies()

    xbmc.sleep(1000)

    oRequest = RequestHandler(sHosterUrl)
    oRequest.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
    oRequest.addHeaderEntry('Host', 'parisanime.com')
    oRequest.addHeaderEntry('Referer', sHosterUrl)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Cookie', Cookie)
    oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequest.addHeaderEntry('Connection', 'keep-alive')
    sHtmlContent = oRequest.request()
    return sHtmlContent


def GetHostname(url):
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
