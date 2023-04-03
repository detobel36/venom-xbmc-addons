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
    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernière liste',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_WORLDWiDE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernière liste mondial',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPORT_LISTE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste Sport',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SMART_IPTV)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Smart Iptv',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
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
    output_parameter_handler.addParameter('site_url', IPTV_AMERICAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Américaine',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_ARABE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Arabe',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_BELGE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Belgique',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_CANADA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Canada',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_FRENCH)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines France',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_PAYSBAS)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Pays-bas',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_POLOGNE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Pologne',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_PORTUGAl)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Portugal',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_ROUMANIE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Liste chaines Roumanie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', IPTV_TURC)
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
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<div class="td-module-thumb"><a href="([^"]+)" rel="bookmark".+?title="([^"]+)">'
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
                'listes.png',
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
    pattern = ' class="last".+?href="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')

    html_content = getHtml(url)

    url = re.search(
        '<a href="([^"]+)".+class="da-download-link da-download-attachment',
        html_content).group(1)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)

    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        title,
        '',
        output_parameter_handler)

    gui.setEndOfDirectory()
