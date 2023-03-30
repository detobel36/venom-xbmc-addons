# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 27 https://cinemey.com/
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import re
return False  # HS voir https://cinemay.cc/ memes films et series


SITE_IDENTIFIER = 'cinemey'
SITE_NAME = 'Cinemey'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = 'https://cinemey.com/'
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VIEWS = (URL_MAIN + 'classement-box-office-film', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'les-series-en-streaming', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')


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
        'Films (Les plus vus)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
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
        'Recherche',
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
        'Films (les plus vus)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
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

    liste = []
    # https://cinemey.com/categorie/romance
    # Aucun résultats war-politics, soap, kids, talk, news,
    # science-fiction-fantastique, reality, action-adventure
    listegenre = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'crime',
        'documentaire',
        'drame',
        'familial',
        'fantastique',
        'guerre',
        'histoire',
        'horreur',
        'musique',
        'Musical',
        'mystere',
        'romance',
        'science-fiction',
        'telefilm',
        'thriller',
        'western']

    url1g = URL_MAIN + 'categorie/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    # https://cinemey.com/annee/2020
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2001, 2023)):  # pas grand chose 32 - 90
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'annee/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:

        bvalid, stoken, scookie = GetTokens()
        if bvalid:
            pdata = '_token=' + stoken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            oRequestHandler = RequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry(
                'Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)
            oRequestHandler.request()

            # constatation : on est oblige de faire 2 requetes
            # dans le cas ou le mot recherché est composé ?
            xbmc.sleep(500)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)

            sHtmlContent = oRequestHandler.request()

        else:
            gui.addText(SITE_IDENTIFIER)
            return

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # title img year surl
    sPattern = '<article class.+?data-url.+?title="([^"]*).+?img src=([^\\s]*).+?year">([^<]+).+?href="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            desc = ''
            title = aEntry[0]
            sThumb = aEntry[1]
            sYear = aEntry[2]
            sUrl2 = aEntry[3]
            sDisplayTitle = title + '(' + sYear + ')'

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)

            if sSearch:
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showSelectType',
                    sDisplayTitle,
                    sThumb,
                    desc,
                    output_parameter_handler)
            elif SERIE_NEWS[0] in sUrl:
                sDisplayTitle = title
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSXE',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
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
    sPattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-numbers'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSelectType():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    desc = ''
    oParser = Parser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sUrl)
    output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
    output_parameter_handler.addParameter('sThumb', sThumb)
    output_parameter_handler.addParameter('desc', desc)
    output_parameter_handler.addParameter('sYear', sYear)

    if 'class="num-epi">' in sHtmlContent:

        gui.addTV(
            SITE_IDENTIFIER,
            'showSXE',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)
    else:
        gui.addMovie(
            SITE_IDENTIFIER,
            'showLink',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = 'class="num-epi">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    list_saison = []

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if 'x' in aEntry[0]:
                # class="numep">1x13<
                saison, episode = aEntry[0].split('x')
                if saison not in list_saison:
                    list_saison.append(saison)
                    sSaison = 'Saison ' + saison
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue]' +
                        sSaison +
                        '[/COLOR]')

                sUrl2 = aEntry[1]
                title = sMovieTitle + ' ' + sSaison + ' Episode' + episode

                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('desc', desc)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLink',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = Parser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if False and 'class="num-epi">' in sHtmlContent and 'episode' not in sUrl:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('desc', desc)
        gui.addTV(
            SITE_IDENTIFIER,
            'showSXE',
            sMovieTitle,
            '',
            sThumb,
            desc,
            output_parameter_handler)

        gui.setEndOfDirectory()
        return

    sPattern = 'data-url="([^"]+).+?server.+?alt="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oHosterGui = HosterGui()
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sKey = aEntry[0]
            sHost = aEntry[1].replace(
                'www.', '').replace(
                'embed.mystream.to', 'mystream')
            sHost = re.sub('\\.\\w+', '', sHost).capitalize()

            oHoster = oHosterGui.checkHoster(sHost)
            if not oHoster:
                continue

            sLang = aEntry[2].upper()
            sUrl2 = URL_MAIN + 'll/captcha?hash=' + sKey

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.*?src=([^\\s]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]

        oHoster = HosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


def GetTokens():
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = '<nav id="menu.+?name=_token.+?value="([^"]+).+?<div class="typeahead'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?cinemay_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; cinemay_session=' + site_session + ';'
    return True, token, cook


def cleanDesc(desc):
    list_comment = ['Voir film ', 'en streaming', 'Voir Serie ']
    for s in list_comment:
        desc = desc.replace(s, '')

    return desc
