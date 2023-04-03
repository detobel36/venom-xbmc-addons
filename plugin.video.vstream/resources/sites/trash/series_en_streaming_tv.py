# -*- coding: utf-8 -*-
# Venom.
# Pas top ce site
import unicodedata
import re
import urllib
import urllib2
from resources.lib.packer import cPacker
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.config import cConfig
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False
# https://github.com/Kodi-vStream/venom-xbmc-addons

SITE_IDENTIFIER = 'series_en_streaming_tv'
SITE_NAME = 'Séries-en-Streaming'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = 'http://www.seriefr.eu/'

SERIE_NEWS = (URL_MAIN + 'ajouts/', 'showLasts')
SERIE_SERIES = (URL_MAIN + 'search/', 'AlphaSearch')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')

URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def CleanTitle(title):
    title = cUtil().unescape(title)
    title = cUtil().removeHtmlTags(title)
    try:
        # title = unicode(title, 'utf-8')
        title = unicode(title, 'iso-8859-1')
    except BaseException:
        pass
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore')

    return title.encode("utf-8")


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries (Liste complète)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def AlphaSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0, 27):
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break

        if (i < 1):
            title = '[0-9]'
        else:
            title = chr(64 + i)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
        output_parameter_handler.addParameter('sLetter', title)
        output_parameter_handler.addParameter('movie_title', title)
        gui.addDir(
            SITE_IDENTIFIER,
            'AlphaDisplay',
            '[COLOR teal] Lettre [COLOR red]' +
            title +
            '[/COLOR][/COLOR]',
            'az.png',
            output_parameter_handler)

    cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def AlphaDisplay():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    sLetter = input_parameter_handler.getValue('sLetter')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a href=\'\\.\\.\\/(serie\\/[^\']+?)\'>(' + \
        sLetter + '[^<>]+?)<\\/a><br>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = CleanTitle(entry[1])
            url2 = URL_MAIN + entry[0]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)

            gui.addTV(
                SITE_IDENTIFIER,
                'ShowSaisons',
                title,
                'series.png',
                '',
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

        gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()

    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = "<a class='host-a wrap'.+?href='([^']+)'.+?src='([^']+)'.+?<h3.+?>(.+?)</h3>"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in list(set(results[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            thumb = entry[1].replace('=200', '=360')
            title = CleanTitle(entry[2])

            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb[1:]

            if not url.startswith('http'):
                url = URL_MAIN + url[1:]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'ShowSaisons',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    if not search:
        gui.setEndOfDirectory()


def showLasts():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    pattern = '<a class="host-a wrap".+?href="([^"]+)".+?src="([^"]+)".+?<span.+?>(.+?)</span><br><span.+?>(.+?)</span><br><span.+?>(.+?)</span>'
    results = parser.parse(html_content, pattern)

    if results[0]:

        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in list(set(results[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            thumb = entry[1].replace('=110', '=360')  # qualité image
            sSXXEXX = str(entry[3]).replace('-', '').split('x')
            movie_title = sSXXEXX[0] + ' ' + entry[2]
            display_title = ('%s %s') % (movie_title, entry[4])

            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb[1:]

            if not url.startswith('http'):
                url = URL_MAIN + url[1:]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def ShowSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    img = ''
    pattern = '<img.+?src="([^"]+)" alt=".+?" width=".+?">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        img = URL_MAIN[:-1] + results[1][0]

    pattern = '<a href="([^<>]+?)" class="seasonLink">([^<>]+?)<\\/a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = movie_title + ' Saison ' + entry[1]
            display_title = cUtil().DecoTitle(title)

            if img:
                thumb = img

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[0])
            output_parameter_handler.addParameter('movie_title', title)
            gui.addTV(SITE_IDENTIFIER, 'showEpisode', display_title,
                      '', str(thumb), '', output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    # pattern = "<a class='various' data-fancybox-type='iframe' href='(.+?)' > *(.+?)<\/a>\t*<\/h3>\t*(.+?)<br>"
    # pattern = ';" src="([^"]+)" class="img-responsive">.+?<a class="various" data-fancybox-type="iframe" href="(.+?)" *> *(.+?)<\/a> *<\/h3>([^<>]+)<'
    pattern = '<a class="host-a wrap".+?href="([^<"]+)".+?<img.+?src="/images/\\?src=(.+?)" class="img-responsive".+?<h3 style=.+?>(.+?)</h3>([^<"]+)<br'
    results = parser.parse(html_content, pattern)

    if results[0]:

        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            if not url.startswith('http'):
                url = URL_MAIN[:-1] + url

            title = movie_title + ' ' + entry[2]
            thumb = URL_MAIN + 'images/?src=' + entry[1]

            sCom = entry[3]
            display_title = cUtil().DecoTitle(title)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                sCom,
                output_parameter_handler)

        cConfig().finishDialog(dialog)
    else:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR coral]Aucun episode disponible[/COLOR]')

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    cConfig().log(url)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = "<a class=\"host-a wrap\" onclick=\"image\\('([^']+)'\\).+?<span>([^\\.<>]+)\\..{1,3}<\\/span> *<span style='color: #[0-9A-Z]+'>\\[(.+?)\\]<\\/span>"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url2 = URL_MAIN + 'cale/' + entry[0]

            display_title = ('%s [%s] (%s)') % (title, entry[2], entry[1])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumbnail)

            gui.addTV(
                SITE_IDENTIFIER,
                'GetLink',
                display_title,
                '',
                thumbnail,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def GetLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')

    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    results = parser.parse(html_content, pattern)
    if results[0]:
        hoster_url = cPacker().unpack(results[1][0])

        hoster_url = hoster_url.replace('"+window.innerWidth+"', '1680')

        sPattern2 = "src=\\\\\'(.+?)\\\\"
        results = parser.parse(hoster_url, sPattern2)
        if results[0]:
            hoster = HosterGui().checkHoster(results[1][0])
            hoster_url = results[1][0]
        else:
            hoster = False

        if (hoster):
            display_title = cUtil().DecoTitle(title)
            hoster.setDisplayName(display_title)
            hoster.setFileName(title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()
