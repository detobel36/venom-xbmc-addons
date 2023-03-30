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
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
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
    sUrl = input_parameter_handler.getValue('siteUrl')

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
        output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
        output_parameter_handler.addParameter('sLetter', title)
        output_parameter_handler.addParameter('sMovieTitle', title)
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
    sUrl = input_parameter_handler.getValue('siteUrl')
    sLetter = input_parameter_handler.getValue('sLetter')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<a href=\'\\.\\.\\/(serie\\/[^\']+?)\'>(' + \
        sLetter + '[^<>]+?)<\\/a><br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = CleanTitle(aEntry[1])
            sUrl2 = URL_MAIN + aEntry[0]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)

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

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = "<a class='host-a wrap'.+?href='([^']+)'.+?src='([^']+)'.+?<h3.+?>(.+?)</h3>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in list(set(aResult[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1].replace('=200', '=360')
            title = CleanTitle(aEntry[2])

            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb[1:]

            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl[1:]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('thumbnail', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'ShowSaisons',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    if not sSearch:
        gui.setEndOfDirectory()


def showLasts():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    sPattern = '<a class="host-a wrap".+?href="([^"]+)".+?src="([^"]+)".+?<span.+?>(.+?)</span><br><span.+?>(.+?)</span><br><span.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in list(set(aResult[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1].replace('=110', '=360')  # qualité image
            sSXXEXX = str(aEntry[3]).replace('-', '').split('x')
            sMovieTitle = sSXXEXX[0] + ' ' + aEntry[2]
            sDisplayTitle = ('%s %s') % (sMovieTitle, aEntry[4])

            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb[1:]

            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl[1:]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('thumbnail', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def ShowSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('thumbnail')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()

    img = ''
    sPattern = '<img.+?src="([^"]+)" alt=".+?" width=".+?">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        img = URL_MAIN[:-1] + aResult[1][0]

    sPattern = '<a href="([^<>]+?)" class="seasonLink">([^<>]+?)<\\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = sMovieTitle + ' Saison ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(title)

            if img:
                sThumb = img

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', aEntry[0])
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,
                      '', str(sThumb), '', output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    # sPattern = "<a class='various' data-fancybox-type='iframe' href='(.+?)' > *(.+?)<\/a>\t*<\/h3>\t*(.+?)<br>"
    # sPattern = ';" src="([^"]+)" class="img-responsive">.+?<a class="various" data-fancybox-type="iframe" href="(.+?)" *> *(.+?)<\/a> *<\/h3>([^<>]+)<'
    sPattern = '<a class="host-a wrap".+?href="([^<"]+)".+?<img.+?src="/images/\\?src=(.+?)" class="img-responsive".+?<h3 style=.+?>(.+?)</h3>([^<"]+)<br'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = URL_MAIN[:-1] + sUrl

            title = sMovieTitle + ' ' + aEntry[2]
            sThumb = URL_MAIN + 'images/?src=' + aEntry[1]

            sCom = aEntry[3]
            sDisplayTitle = cUtil().DecoTitle(title)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('thumbnail', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTitle,
                '',
                sThumb,
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
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    cConfig().log(sUrl)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<a class=\"host-a wrap\" onclick=\"image\\('([^']+)'\\).+?<span>([^\\.<>]+)\\..{1,3}<\\/span> *<span style='color: #[0-9A-Z]+'>\\[(.+?)\\]<\\/span>"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl2 = URL_MAIN + 'cale/' + aEntry[0]

            sDisplayTitle = ('%s [%s] (%s)') % (title, aEntry[2], aEntry[1])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('thumbnail', thumbnail)

            gui.addTV(
                SITE_IDENTIFIER,
                'GetLink',
                sDisplayTitle,
                '',
                thumbnail,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def GetLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')

    thumbnail = input_parameter_handler.getValue('thumbnail')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = cPacker().unpack(aResult[1][0])

        sHosterUrl = sHosterUrl.replace('"+window.innerWidth+"', '1680')

        sPattern2 = "src=\\\\\'(.+?)\\\\"
        aResult = oParser.parse(sHosterUrl, sPattern2)
        if aResult[0]:
            oHoster = HosterGui().checkHoster(aResult[1][0])
            sHosterUrl = aResult[1][0]
        else:
            oHoster = False

        if (oHoster):
            sDisplayTitle = cUtil().DecoTitle(title)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(title)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)

    gui.setEndOfDirectory()
