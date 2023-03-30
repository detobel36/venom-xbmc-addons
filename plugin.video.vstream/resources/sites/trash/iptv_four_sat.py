# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.parser import Parser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'iptv_four_sat'
SITE_NAME = 'Iptv4Sat'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.iptv4sat.com/'
IPTV_WORLDWiDE = URL_MAIN + 'category/m3u-list-world-iptv/iptv-worldwide-m3u/'
SPORT_LISTE = URL_MAIN + 'category/m3u-list-world-iptv/free-iptv-sports/'
SMART_IPTV = URL_MAIN + 'category/m3u-list-world-iptv/smart-free-iptv/'

IPTV_AMERICAIN = URL_MAIN + 'category/m3u-list-world-iptv/america-m3u-iptv/'
IPTV_ARABE = URL_MAIN + 'category/m3u-list-world-iptv/free-iptv-arabic/'
IPTV_BELGE = URL_MAIN + 'category/european-iptv/belgique-iptv/'
IPTV_CANADA = URL_MAIN + 'category/m3u-list-world-iptv/canada-iptv-m3u/'
IPTV_FRENCH = URL_MAIN + 'category/european-iptv-iptv/france-m3u-iptv/'
IPTV_PAYSBAS = URL_MAIN + 'category/european-iptv/netherland-iptv/'
IPTV_POLOGNE = URL_MAIN + 'category/european-iptv/poland-iptv/'
IPTV_PORTUGAl = URL_MAIN + 'category/european-iptv/portugal-iptv-m3u/'
IPTV_ROUMANIE = URL_MAIN + 'category/european-iptv/iptv-romania/'
IPTV_TURC = URL_MAIN + 'category/european-iptv/m3u-turkey-iptv/'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernière liste',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_WORLDWiDE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernière liste mondial',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SPORT_LISTE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste Sport',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SMART_IPTV)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Smart Iptv',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'listePerContry',
        'Liste par Pays',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def listePerContry():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', IPTV_AMERICAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Américaine',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_ARABE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Arabe',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_BELGE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Belgique',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_CANADA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Canada',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_FRENCH)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines France',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_PAYSBAS)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Pays-bas',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_POLOGNE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Pologne',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_PORTUGAl)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Portugal',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_ROUMANIE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Roumanie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', IPTV_TURC)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Turc',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showDailyList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<div class="td-module-thumb"><a href="([^"]+)" rel="bookmark".+?title="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showAllPlaylist',
                title,
                'listes.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showDailyList',
                'Page ' + sNumPage,
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = ' class="last".+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')

    sHtmlContent = getHtml(sUrl)

    url = re.search(
        '<a href="([^"]+)".+class="da-download-link da-download-attachment',
        sHtmlContent).group(1)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', url)

    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        title,
        '',
        output_parameter_handler)

    gui.setEndOfDirectory()
