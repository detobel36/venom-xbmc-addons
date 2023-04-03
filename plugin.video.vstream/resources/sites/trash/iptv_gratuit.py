# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress, VSlog
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.parser import Parser
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
import re
return False


SITE_IDENTIFIER = 'iptv_gratuit'
SITE_NAME = 'IptvGratuit'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://iptvgratuit.com/'

IPTV_WORLD = URL_MAIN + 'iptv-world/'
IPTV_FRANCE = URL_MAIN + 'france/'
IPTV_AFRIQUE = URL_MAIN + 'iptv-afrique/'
IPTV_ALLEMAGNE = URL_MAIN + 'iptv-allemagne/'
IPTV_ANGLETERRE = URL_MAIN + 'iptv-uk/'
IPTV_ARABIC = URL_MAIN + 'iptv-arabic/'
# IPTV_AUTRICHE = URL_MAIN + 'iptv-autriche/'
IPTV_BELGIQUE = URL_MAIN + 'iptv-belgique/'
IPTV_BRESIL = URL_MAIN + 'iptv-bresil/'
IPTV_CANADA = URL_MAIN + 'iptv-canada/'
IPTV_CHINE = URL_MAIN + 'iptv-chine/'
IPTV_ESPAGNE = URL_MAIN + 'iptv-espagne/'
IPTV_HOLLANDE = URL_MAIN + 'iptv-hollande/'
IPTV_ITALIE = URL_MAIN + 'iptv-italie/'
IPTV_PORTUGAL = URL_MAIN + 'iptv-portugal/'
IPTV_SUISSE = URL_MAIN + 'iptv-suisse/'
IPTV_RUSSIE = URL_MAIN + 'iptv-russie/'
IPTV_TURK = URL_MAIN + 'iptv-turk/'
IPTV_USA = URL_MAIN + 'iptv-usa/'
IPTV_SPORT = URL_MAIN + 'iptv-sport/'
IPTV_VOD = URL_MAIN + 'iptv-vod/'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernieres listes',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_WORLD)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'Dernieres listes mondial',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_FRANCE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes France',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_AFRIQUE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Afrique',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_ALLEMAGNE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Allemande',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_ANGLETERRE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Anglaise',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_ARABIC)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Arabe',
        'tv.png',
        output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', IPTV_AUTRICHE)
    # gui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Autriche', 'tv.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_BELGIQUE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Belgique',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_BRESIL)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Brésil',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_CANADA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Canada',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_CHINE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Chine',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_ESPAGNE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Espagne',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_HOLLANDE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Hollande',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_ITALIE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Italie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_PORTUGAL)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Portugal',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_SUISSE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Suisse',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_SUISSE)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Russie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_TURK)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes Turque',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_USA)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes USA',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_SPORT)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes SPORT',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', IPTV_VOD)
    gui.addDir(
        SITE_IDENTIFIER,
        'showDailyList',
        'listes VOD',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showDailyList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
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
            sNumPage = re.search('pages/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showDailyList',
                'Page ' + sNumPage,
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class="next page-numbers" href="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')

    parser = Parser()
    html_content = getHtml(url)
    pattern = '<a class="more-link" title="(.+?)".+?href="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        sTitleTest = ''
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = entry[0]
            url2 = entry[1]

            if (title == sTitleTest):
                continue
            else:
                sTitleTest = title

            output_parameter_handler = OutputParameterHandler()
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


def showAllPlaylist2():  # On recupere les differentes playlist si il y en a
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')

    html_content = getHtml(url)
    url2 = getDownloadLink(html_content)

    for url in url2:

        if 'download' in url:
            VSlog('Redirect')
            url = getRealLink(url)
            gui.addText(SITE_IDENTIFIER, url)
        else:
            gui.addText(SITE_IDENTIFIER, 'rien')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)

        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()
