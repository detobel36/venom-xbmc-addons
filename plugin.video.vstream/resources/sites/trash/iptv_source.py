# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.parser import Parser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'iptv_source'
SITE_NAME = 'IptvSource'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.iptvsource.com/'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernières listes',
        'listes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showPays',
        'Choix du pays',
        'lang.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showPays():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+).+?>([^<]+)</a>'
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
                'showDailyList',
                title,
                'tv.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showDailyList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<h3 class="entry-title td-module-title"><a href="([^"]+)" rel="bookmark" title="([^"]+)"'
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
                'tv.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showDailyList',
                'Page ' + sNumPage,
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = ' class="last".+?href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showAllPlaylist():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<a href="([^"]+)">Download ([^<]+)</a>'
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
                'showWeb',
                title,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
