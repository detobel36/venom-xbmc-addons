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
    output_parameter_handler.addParameter('site_url', FREE_M3U)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Derniere liste',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
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
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+)"(?:>([^<]+)</a>|([^<]+)includes)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if str(entry[1]) != '':
                title = entry[1]
            else:
                title = entry[2].replace('"', '')
            url2 = entry[0].replace(' title=', '')

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
    pattern = '<div class="news-thumb col-md-6">\\s*<a href=([^"]+) title="([^"]+)".+?\\s*<img src=.+?uploads/.+?/.+?/([^"]+)\\..+?'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = entry[1]
            url2 = entry[0]
            if 'extinf' in url:
                flag = entry[2]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)

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
    pattern = '<a class="next page-numbers" href=([^>]+)>Next</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showDailyIptvList():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    html_content = getHtml(url)
    clearHtml = re.search('null>([\\s*\\S*]+)</pre>', html_content).group(1)
    line = re.compile('http(.+?)\n').findall(clearHtml)

    for url2 in line:
        if '/cdn-cgi/l/email-protection' in str(url2):
            url2 = 'http' + \
                decodeEmail(url2).replace('<', '').replace('&amp;', '&')
        else:
            url2 = 'http' + url2.replace('&amp;', '&')

        title = 'Lien: ' + url2.replace('&amp;', '&')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url2)
        output_parameter_handler.addParameter('movie_title', title)

        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            'tv.png',
            output_parameter_handler)

    gui.setEndOfDirectory()
