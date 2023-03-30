# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.parser import Parser
from resources.sites.freebox import getHtml, showWeb, play__, decodeEmail
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'iptv'
SITE_NAME = 'Iptv'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.extinf.com/'
FREE_M3U = URL_MAIN + 'home-passion-for-iptv-free-m3u-links-working-and-updated/'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', FREE_M3U)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Derniere liste',
        'tv.png',
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
    sPattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+)"(?:>([^<]+)</a>|([^<]+)includes)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if str(aEntry[1]) != '':
                title = aEntry[1]
            else:
                title = aEntry[2].replace('"', '')
            sUrl2 = aEntry[0].replace(' title=', '')

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
    sPattern = '<div class="news-thumb col-md-6">\\s*<a href=([^"]+) title="([^"]+)".+?\\s*<img src=.+?uploads/.+?/.+?/([^"]+)\\..+?'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = aEntry[1]
            sUrl2 = aEntry[0]
            if 'extinf' in sUrl:
                flag = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)

            if str(flag) == 'm3u-playlist-720x405':
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showDailyIptvList',
                    title,
                    'listes.png',
                    output_parameter_handler)
            else:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showWeb',
                    title,
                    'tv.png',
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
    sPattern = '<a class="next page-numbers" href=([^>]+)>Next</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showDailyIptvList():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    clearHtml = re.search('null>([\\s*\\S*]+)</pre>', sHtmlContent).group(1)
    line = re.compile('http(.+?)\n').findall(clearHtml)

    for sUrl2 in line:
        if '/cdn-cgi/l/email-protection' in str(sUrl2):
            sUrl2 = 'http' + \
                decodeEmail(sUrl2).replace('<', '').replace('&amp;', '&')
        else:
            sUrl2 = 'http' + sUrl2.replace('&amp;', '&')

        title = 'Lien: ' + sUrl2.replace('&amp;', '&')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl2)
        output_parameter_handler.addParameter('sMovieTitle', title)

        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            'tv.png',
            output_parameter_handler)

    gui.setEndOfDirectory()
