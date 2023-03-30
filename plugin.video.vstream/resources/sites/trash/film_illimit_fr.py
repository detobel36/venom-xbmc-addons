# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil, QuotePlus, Noredirection
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimité'
SITE_DESC = 'Films, Séries HD en streaming'

URL_MAIN = 'https://www.official-film-illimite.to/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/streaming-720p-streaming-1080p/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD)',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
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


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Ultra-HD', URL_MAIN + 'ultra-hd/'])
    liste.append(['720p/1080p', URL_MAIN +
                  'films/streaming-720p-streaming-1080p/'])
    liste.append(['Action/Aventure', URL_MAIN + 'films/action-aventure/'])
    liste.append(['Animation', URL_MAIN + 'films/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'films/arts-martiaux/'])
    liste.append(['Biographie', URL_MAIN + 'films/biographique/'])
    liste.append(['Comédie', URL_MAIN + 'films/comedie/'])
    liste.append(['Crime/Gangster', URL_MAIN + 'films/crimegangster/'])
    liste.append(['Documentaire', URL_MAIN + 'films/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'films/drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'films/epouvante-horreur/'])
    liste.append(['Etranger', URL_MAIN + 'films/etranger/'])
    liste.append(['Famille', URL_MAIN + 'films/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'films/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'films/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'films/histoire/'])
    liste.append(['Musique/Danse', URL_MAIN + 'films/musiquedanse/'])
    liste.append(['Mystère', URL_MAIN + 'films/mystere/'])
    liste.append(['Policier', URL_MAIN + 'films/policier/'])
    liste.append(['Romance', URL_MAIN + 'films/romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'films/science-fiction/'])
    liste.append(['Spectacle (FR)', URL_MAIN +
                 'spectacle/francais-spectacle/'])
    liste.append(['Spectacle (VOSTFR)', URL_MAIN +
                 'spectacle/vostfr-spectacle/'])
    liste.append(['Sport', URL_MAIN + 'films/sport/'])
    liste.append(['Suspense/Thriller', URL_MAIN + 'films/thrillersuspense/'])
    liste.append(['Téléfilm', URL_MAIN + 'films/telefilm/'])
    liste.append(['VOSTFR', URL_MAIN + 'films/vostfr/'])
    liste.append(['Western', URL_MAIN + 'films/western/'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="filter-content-slider">'
    sEnd = '<div class="filter-slide filter-slide-down">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            title = aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('en illimité', 'en illimite')

    oParser = Parser()
    sPattern = 'class="item">.+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?ttx">([^<]+).+?(?:|class="year">([^<]+).+?)class="calidad2'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = aEntry[2].replace(
                ' Streaming Ultra-HD',
                '').replace(
                ' Streaming Full-HD',
                '') .replace(
                ' en Streaming HD',
                '').replace(
                ' Streaming HD',
                '') .replace(
                    ' streaming',
                    '').replace(
                        'HD',
                '')

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\\d+', '/w342', aEntry[1])
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb
            desc = aEntry[3].split('en illimite')[1].replace('&#160;', '')
            sYear = aEntry[4]

            # Si recherche et trop de resultat, on filtre
            if sSearch and total > 2:
                if cUtil().CheckOccurence(
                        sSearch.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)

            sPattern1 = '.+?saison [0-9]+'
            aResult1 = oParser.parse(title, sPattern1)

            if aResult1[0]:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                str(number) +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<a class=\'current.+?href=\'([^']+)\'"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="//www.youtube.com/', '')

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            if '//goo.gl' in sHosterUrl:
                try:
                    url8 = sHosterUrl.replace('https', 'http')

                    opener = Noredirection()
                    opener.addheaders.append(('User-Agent', UA))
                    opener.addheaders.append(('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https', 'http')
                except BaseException:
                    pass

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace(
        '<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<iframe.+?src="(http.+?)".+?>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        i = 1
        for aEntry in aResult[1]:

            sUrl = aEntry
            title = '%s episode %s' % (
                sMovieTitle.replace(' - Saison', ' Saison'), i)

            i = i + 1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowSpecialHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowSpecialHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    data = re.sub('(.+?f=)', '', sUrl)
    data = data.replace('&c=', '')
    pdata = 'data=' + QuotePlus(data)

    if 'fr-land.me' in sUrl:
        oRequest = RequestHandler('http://fr-land.me/Htplugins/Loader.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Host', 'official-film-illimite.to')
        oRequest.addHeaderEntry('Referer', sUrl)
        oRequest.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '')

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        sPattern = '\\[(.+?)\\]'

        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            listurl = aResult[1][0].replace('"', '').split(',http')
            listqual = aResult[1][1].replace('"', '').split(',')

            tab = zip(listurl, listqual)

            for url, qual in tab:
                sHosterUrl = url
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http' + sHosterUrl

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    sDisplayTitle = '[' + qual + '] ' + sMovieTitle
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    else:

        oHoster = HosterGui().checkHoster(sUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sUrl, sThumb)

    gui.setEndOfDirectory()
