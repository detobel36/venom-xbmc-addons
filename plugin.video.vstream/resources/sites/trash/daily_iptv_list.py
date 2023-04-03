# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.parser import Parser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import Progress

SITE_IDENTIFIER = 'daily_iptv_list'
SITE_NAME = 'Daily Iptv List'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.dailyiptvlist.com/'
URL_EUROPE = URL_MAIN + 'europe-m3u-iptv/'
URL_AMERICA = URL_MAIN + 'iptv-american/'
URL_ASIA = URL_MAIN + 'asia/'
URL_SPORT = URL_MAIN + 'sport-iptv-m3u/'
URL_WORLDWIDE = URL_MAIN + 'iptv-world-wide/'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernière liste',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showPays',
        'Choix du pays',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_EUROPE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste iptv Europe',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_AMERICA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste iptv America',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_ASIA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste iptv Asia',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SPORT)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste iptv Sport',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_WORLDWIDE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste iptv Worldwide',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showPays():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+)".+?>([^<]+)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
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
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '</a><h2 class="post-title"><a href="([^"]+)">([^<]+)</a></h2><div class="excerpt"><p>.+?</p>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showAllPlaylist',
                title,
                'tv.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showDailyList',
                'Page ' + sNumPage,
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a class="next page-numbers" href="([^"]+)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showAllPlaylist():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<p></br><br /><strong>2. Click on link to download .+? iptv channels list</strong></p>|<a href="([^"]+)">Download ([^<]+)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showWeb',
                title,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
