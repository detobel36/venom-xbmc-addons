# -*- coding: utf-8 -*-
# Venom.

# desactiver le 18/09
import xbmc
import re
from resources.lib.config import cConfig
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'filmstreamingv2'
SITE_NAME = '[COLOR violet]Films Streaming V2[/COLOR]'
SITE_DESC = 'Film streaming (Version 2) - Premier site de streaming film VF en HD'

URL_MAIN = 'http://www.filmstreamingv2.com/'

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_SAGAS = (URL_MAIN + 'les-sagas-de-films.html', 'showMoviesHtml')
MOVIE_MARVEL = (
    URL_MAIN +
    'telecharger-les-films-de-lunivers-marvel.html',
    'showMoviesHtml')
MOVIE_JAMESB = (
    URL_MAIN +
    'integrale-james-bond-films-collection-complete.html',
    'showMoviesHtml')
MOVIE_TOP = (URL_MAIN + 'top-250-imdb.html', 'showMoviesHtml')
MOVIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (
    URL_MAIN +
    'les-films-disney-en-streaming.html',
    'showMoviesHtml')

URL_SEARCH = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_SAGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SAGAS[1],
        'Films (Sagas)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MARVEL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MARVEL[1],
        'Films (Marvel)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_JAMESB[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_JAMESB[1],
        'Films (Saga James Bond)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Top 250 IMDB)',
        'star.png',
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
    output_parameter_handler.addParameter('siteUrl', ANIM_ENFANTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ENFANTS[1],
        'Les Walt Disney',
        'enfants.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'xfsearch/action'])
    liste.append(['Animation', URL_MAIN + 'xfsearch/animation'])
    liste.append(['Aventure', URL_MAIN + 'xfsearch/aventure'])
    liste.append(['Biopic', URL_MAIN + 'xfsearch/biopic'])
    liste.append(['Comédie', URL_MAIN + 'xfsearch/Comedie'])
    liste.append(['Documentaire', URL_MAIN + 'xfsearch/documentaire'])
    liste.append(['Drame', URL_MAIN + 'xfsearch/drame'])
    liste.append(['Famille', URL_MAIN + 'xfsearch/famille'])
    liste.append(['Fantastique', URL_MAIN + 'xfsearch/fantastique'])
    liste.append(['Historique', URL_MAIN + 'xfsearch/historique'])
    liste.append(['Horreur', URL_MAIN + 'xfsearch/horreur'])
    liste.append(['Musical', URL_MAIN + 'xfsearch/musical'])
    liste.append(['Policier', URL_MAIN + 'xfsearch/policier'])
    liste.append(['Romance', URL_MAIN + 'xfsearch/romance'])
    liste.append(['Science fiction', URL_MAIN + 'xfsearch/fiction'])
    liste.append(['Thriller', URL_MAIN + 'xfsearch/thriller'])
    liste.append(['Western', URL_MAIN + 'xfsearch/western'])

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


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sUrl = sSearch
        else:
            sUrl = URL_SEARCH[0] + sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="hover-special"></div><img src="([^"]+)" alt="([^"]+)"><div class="hd720p">([^<]+)</div>.+?<div class="pipay1"><a href="([^"]+)"'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sQual = ' (' + aEntry[2] + ')'
            title = str(aEntry[1]).replace('streaming', '')
            sUrl = aEntry[3]
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sDisplayTitle = title + sQual

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="([^"]+)">Suivant'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sUrl = aResult[1][0]
        # correction d'1 bug de leur site
        sUrl = sUrl.replace('xfsearch//page/2/', 'xfsearch/page/2/page/2/')
        return sUrl

    return False


def showMoviesHtml():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="tops-item"><a href="([^<]+)">.+?<img src="([^<]+)" alt="(.+?)"/>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            title = str(aEntry[2]).replace('streaming', '')
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/les-sagas-' in sUrl:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showSagas',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showSagas():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span style="color:.+?">([^<]+)</span>.+?<a href="([^<]+)">.+?<img src="(.+?)".+?>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            title = aEntry[0]
            sUrl = aEntry[1]
            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    # recherche des liens de streaming
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]' +
            'Liens Streaming :' +
            '[/COLOR]')
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            # print aEntry
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            sHosterUrl = sHosterUrl.replace('//ok.ru', 'https://ok.ru')
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, '')

    # recherche des liens de telechargement
    sUrl = sUrl + '#example'
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<div id="download-quality-([^"]+)">.+?<span class="download-filesize">([^<]+)</span>|<a class="download-torrent leta-[^"]+" target="_blank" href="([^"]+)" rel="external noopener noreferrer">([^>]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]' +
            'Liens Download :' +
            '[/COLOR]')
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            # print aEntry
            if dialog.iscanceled():
                break

            if aEntry[0]:  # affichage format et taille du fichier
                gui.addText(SITE_IDENTIFIER, '[COLOR olive]' + str(
                    aEntry[0]) + ' (' + str(aEntry[1]) + ')' + '[/COLOR]')

            else:
                sDisplayTitle = aEntry[3]

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', aEntry[2])
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def Display_protected_link():
    # xbmc.log('Display_protected_link')
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()

    # Est ce un lien ushort-links?
    if 'ushort-links' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        if sHtmlContent:
            sPattern = '<a id="download" href="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            sHosterUrl = aResult[1][0]
            # print sHosterUrl

            title = sMovieTitle

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                sDisplayTitle = cUtil().DecoTitle(title)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(title)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

        else:
            oDialog = cConfig().createDialogOK('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    gui.setEndOfDirectory()
