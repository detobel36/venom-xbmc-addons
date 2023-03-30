# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import requests

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, addon

SITE_IDENTIFIER = 'alldebrid'
SITE_NAME = '[COLOR violet]Alldebrid[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

ITEM_PAR_PAGE = 20


def load():
    gui = Gui()
    oAddon = addon()

    URL_HOST = oAddon.getSetting('urlmain_alldebrid')
    ALL_ALL = (URL_HOST + 'links/', 'showLiens')
    ALL_MAGNETS = (URL_HOST + 'magnets/', 'showMagnets')
    ALL_INFORMATION = ('https://alldebrid.fr', 'showInfo')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ALL_ALL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_ALL[1],
        'Liens',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ALL_MAGNETS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_MAGNETS[1],
        'Magnets',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ALL_INFORMATION[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_INFORMATION[1],
        'Information sur les hébergeurs ',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showLiens(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        '</h1><hr><pre><a href="../">../</a>', '')
    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        nbItem = 0
        index = 0
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = aEntry[1]
            sUrl2 = sUrl + aEntry[0]
            sThumb = ''
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)
            progress_.VSclose(progress_)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', sUrl)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

        gui.setEndOfDirectory()


def showMagnets(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        '</h1><hr><pre><a href="../">../</a>', '')
    # Pattern servant à retrouver les éléments dans la page
    sPattern = '<a href="(.+?)">([^<]+)</a>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        nbItem = 0
        index = 0

        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = aEntry[0]
            sUrl2 = sUrl + aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', sUrl)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

            if 'mp4' in sUrl2 or 'avi' in sUrl2 or 'mkv' in sUrl2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'series.png',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showseriesHoster',
                    title,
                    'movies.png',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showseriesHoster(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    try:  # Dans le cas ou le mot mp4/avi/mkv n'est pas présent quand c'est un seul fichier
        s = requests.Session()
        resp = s.head(sUrl)
        result = resp.headers['location']
        sHosterUrl = result
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sMovieTitle,
                                   input_parameter_handler=input_parameter_handler)
            gui.setEndOfDirectory()
    except BaseException:
        pass

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        '</h1><hr><pre><a href="../">../</a>', '')

    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        nbItem = 0
        index = 0
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue
            numItem += 1
            nbItem += 1

            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = aEntry[1]
            sUrl2 = sUrl + aEntry[0]
            sThumb = ''
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('referer', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', sUrl)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

            progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    sHosterUrl = sUrl
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sMovieTitle,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showInfo():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<li class="([^"]+)">.+?<i alt=".+?" title="([^"]+)".+?</li>'

    oParser = Parser()
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

            sDisponible = aEntry[0].replace(
                'downloaders_available',
                'Disponible') .replace(
                'downloaders_unavailable',
                'Non Disponible')
            sHebergeur = aEntry[1]

            sDisplayTitle = ('%s (%s)') % (sHebergeur, sDisponible)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)

            gui.addText(SITE_IDENTIFIER, sDisplayTitle)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()
