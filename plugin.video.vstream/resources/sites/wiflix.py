# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'wiflix'
SITE_NAME = 'Wiflix'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_EXCLU = (URL_MAIN + 'film-en-streaming/exclue', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
SERIE_NEWS = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN, 'showSearch')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showSearch'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://film')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://serie')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
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

    output_parameter_handler.addParameter('siteUrl', MOVIE_EXCLU[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLU[1],
        'Films et Séries (Exclus)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:

        if 'film' in sUrl:
            showMovies(sSearchText)
        else:
            showSeries(sSearchText)

        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()

    sUrl = URL_MAIN
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '</span><b>Films par genre</b></div>'
    sEnd = '<div class="side-b">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            title = aEntry[1].capitalize()
            TriAlpha.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, sUrl in TriAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
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
        sSearchText = oUtil.CleanName(sSearch.replace('%20', ' '))

        pdata = 'do=search&subaction=search&story=' + \
            sSearchText.replace(' ', '+') + '&titleonly=3&all_word_seach=1&catlist[]=1'

        oRequest = RequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Origin', URL_MAIN)
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

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:|bloc1">([^<]+).+?)(?:|bloc2">([^<]*).+?)'
    sPattern += 'ml-desc"> (?:([0-9]+)| )</div.+?Synopsis:.+?ml-desc">(.*?)</div'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]
            title = aEntry[1].replace(' wiflix', '')
            sUrl = aEntry[2]
            sLang = aEntry[3]
            sQual = aEntry[4]
            sYear = aEntry[5]
            if sYear in title:  # double affichage de l'année
                title = re.sub('\\(' + sYear + '\\)', '', title)

            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, title):
                continue

            # Nettoyage du synopsis
            desc = str(aEntry[6])
            desc = desc.replace('en streaming ', '')
            desc = desc.replace('Regarder film ' + title + ';', '')
            desc = desc.replace('Regarder film ' + title + ':', '')
            desc = desc.replace('Voir film ' + title + ';', '')
            desc = desc.replace('Voir film ' + title + ':', '')
            desc = desc.replace('Voir Film ' + title + ':', '')
            desc = desc.replace('Voir film ' + title + ' :', '')
            desc = desc.replace('Regarder ' + title + ';', '')
            desc = desc.replace('Regarder ' + title + ' :', '')
            desc = desc.replace('Regarder ' + title + ':', '')
            desc = desc.replace('voir ' + title + ';', '')
            desc = desc.replace('voir ' + title + ':', '')
            desc = desc.replace('Voir ' + title + ':', '')
            desc = desc.replace('Regarder film ', '')
            desc = desc.strip()

            sDisplayTitle = '%s [%s] (%s)' % (title, sQual, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            if 'serie-en-streaming' in sUrl:
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
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
    else:
        gui.addText(SITE_IDENTIFIER)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSeries(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch.replace('%20', ' '))
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + \
            '&titleonly=3&all_word_seach=1&catlist[]=31&catlist[]=35'

        oRequest = RequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
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

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]+)" *alt="([^"]+).+?data-link="([^"]+).+?block-sai">([^<]+).+?ml-desc">(.+?)</div>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]

            title = aEntry[1].replace(
                '- Saison',
                'saison').replace(
                ' wiflix',
                '')

            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, title):
                continue

            # sLang = re.sub('Saison \d+', '', aEntry[3]).replace(' ', '')
            sDisplayTitle = title
            sUrl = aEntry[2]
            desc = aEntry[4]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                sDisplayTitle,
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
                'showSeries',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="(ep.+?)"|<a href="([^"]+)"[^><]+target="x_player"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Afficher le numero de l episode et la saison dans le titre
    # permet de marquer vu avec trakt automatiquement.
    ep = 0
    sLang = ''

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:

                if 'vs' in aEntry[0]:
                    sLang = ' (VOSTFR)'
                elif 'vf' in aEntry[0]:
                    sLang = ' (VF)'

                if 'epblocks' in aEntry[0]:
                    continue

                ep = aEntry[0].replace(
                    'ep',
                    'Episode ').replace(
                    'vs',
                    '').replace(
                    'vf',
                    '')

            if aEntry[1]:
                title = sMovieTitle + ' ' + ep + sLang
                sHosterUrl = aEntry[1].replace('/vd.php?u=', '')
                if 'players.wiflix.' in sHosterUrl:
                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(title)
                    oHoster.setFileName(title)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a href="\\/vd.php\\?u=([^"]+)"[^<>]+target="x_player_wfx"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]  # .replace('/wiflix.cc/', '')
            if 'wiflix.' in sHosterUrl:
                oRequestHandler = RequestHandler(sHosterUrl)
                oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()
            else:
                sHosterUrl = aEntry[0].replace('/wiflix.cc/', '')
            sLang = aEntry[1].replace('2', '').replace('3', '')
            if 'Vost' in aEntry[1]:
                sDisplayTitle = ('%s (%s)') % (sMovieTitle, sLang)
            else:
                sDisplayTitle = sMovieTitle
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
