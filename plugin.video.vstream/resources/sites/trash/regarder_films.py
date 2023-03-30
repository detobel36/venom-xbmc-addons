# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'regarder_films'
SITE_NAME = 'Regarder-films-gratuit'
SITE_DESC = 'Série streaming gratuit illimité vf et vostfr.'

URL_MAIN = 'http://regarder-film-gratuit.online/'

SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_SERIES = (URL_MAIN, 'load')
SERIE_LIST = (URL_MAIN + 'liste-de-series/', 'showAlpha')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showAlpha():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler(SERIE_LIST[0])
    sHtmlContent = oRequestHandler.request()

    sPattern = '<font color="red".+?>(.+?)<\\/font>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLetter = str(aEntry).replace('=', '')
            dAZ = str(aEntry)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('dAZ', dAZ)
            gui.addDir(
                SITE_IDENTIFIER,
                'showList',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'az.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    oRequestHandler = RequestHandler(SERIE_LIST[0])
    dAZ = input_parameter_handler.getValue('dAZ')
    sHtmlContent = oRequestHandler.request()

    # Decoupage pour cibler la partie selectionnée
    sPattern = '<font color="red".+?>' + dAZ + '</font>(.+?)<p><strong>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # regex pour listage series sur la partie decoupée
    sPattern = '<a href="([^"]+)".+?>(.+?)<\\/a>'
    aResult = oParser.parse(aResult, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = str(aEntry[0])
            # on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in sUrl:
                continue
            title = str(aEntry[1]).decode("unicode_escape").encode(
                "latin-1").replace('&#8217;', '\'').replace('&#8212;', '-')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'az.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Dessin animés', URL_MAIN + 'category/dessins-animes/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['News', URL_MAIN + 'category/news/'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="post".+?<h2><a class="title" href="(.+?)" rel="bookmark">(.+?)</a>.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(
                        sSearch.replace(
                            URL_SEARCH[0],
                            ''),
                        aEntry[1]) == 0:
                    continue

            sUrl = str(aEntry[0])
            title = str(aEntry[1]).replace(
                '&#8212;', '-').replace('&#8217;', '\'')
            sThumb = str(aEntry[2])
            # on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in sThumb:
                continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(SITE_IDENTIFIER, 'serieHosters', title,
                      '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">..<'
    aResult = re.findall(sPattern, sHtmlContent, re.UNICODE)
    if (aResult):
        return aResult[0]

    return False


def serieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    # recuperation thumb
    sThumb = ''
    sPattern = '<p><img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumb = aResult[1][0]

    # if 'streamzz' in sUrl:
        # sPattern = '<div class="boton reloading"><a href="([^"]+)">'
    # else:
    sPattern = '<center><.+?<stron.+?((?:VF|VOSTFR|VO)).+?trong>|<p><a href="([^"]+)".+?target="_blank">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].replace('&#8230;', '').replace(':', '')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    sLang +
                    '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                oHoster = HosterGui().checkHoster(sHosterUrl)

                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
