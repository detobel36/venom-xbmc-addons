# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser


SITE_IDENTIFIER = 'daddyhd'
SITE_NAME = 'DaddyHD'
SITE_DESC = 'Chaines de Sport et de Divertissement'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showTV')

# chaines
channels = {
    116: ['bein Sports 1', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    117: ['bein Sports 2', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    118: ['bein Sports 3', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    119: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    120: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    121: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    122: ['Canal+ sport', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG']
}


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('siteUrl', SPORT_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_GENRES[1],
        'Sports (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SPORT_TV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_TV[1],
        'Chaines TV Sports',
        'sport.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showTV():
    gui = Gui()

    sUrl = URL_MAIN + '/cast/stream-%d.php'
    chaines = [116, 117, 118, 119, 120, 121, 122]

    output_parameter_handler = OutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        sDisplayTitle = channel[0]
        sThumb = channel[1]
        output_parameter_handler.addParameter('siteUrl', sUrl % iChannel)
        output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        gui.addLink(
            SITE_IDENTIFIER,
            'showLink',
            sDisplayTitle,
            sThumb,
            sDisplayTitle,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    sUrl = URL_MAIN
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<h2 style="background-color:cyan">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        sportGenre = {}
        output_parameter_handler = OutputParameterHandler()
        for title in aResult[1]:
            if 'Schedule' in title:
                break
            if 'Tv Show' in title:
                continue

            sDisplayTitle = title.replace('Soccer', 'Football')
            sDisplayTitle = sDisplayTitle.replace('Darts', 'Flechettes')
            sDisplayTitle = sDisplayTitle.replace('Boxing', 'Boxe')
            sDisplayTitle = sDisplayTitle.replace('Cycling', 'Cyclisme')
            sDisplayTitle = sDisplayTitle.replace(
                'Horse Racing', 'Course de chevaux')
            sDisplayTitle = sDisplayTitle.replace(
                'Ice Hockey', 'Hockey sur glace')
            sDisplayTitle = sDisplayTitle.replace('Alpine Ski', 'Ski')
            sDisplayTitle = sDisplayTitle.replace('Rugby Union', 'Rugby à XV')
            sDisplayTitle = sDisplayTitle.replace('Sailing / Boating', 'Voile')
            sportGenre[sDisplayTitle] = title

        for sDisplayTitle, title in sorted(sportGenre.items()):
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', sDisplayTitle)

            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                sDisplayTitle,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    oParser = Parser()
    sUrl = URL_MAIN

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<h2 style="background-color:cyan">%s</h2>' % title
    sHtmlContent = oParser.abParse(
        sHtmlContent,
        sPattern,
        '<h2 style="background-color:cyan">')

    sPattern = '<hr>(<strong>|)(\\d+:\\d+) (.+?)<'  # span.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sDate = aEntry[1]
            title = aEntry[2]
            sDisplayTitle = sDate + ' - ' + title.strip()
            title = sDate + ' ' + title

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', sDisplayTitle)

            gui.addDir(
                SITE_IDENTIFIER,
                'showHoster',
                sDisplayTitle,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    oParser = Parser()
    urlMain = URL_MAIN

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(urlMain)
    sHtmlContent = oRequestHandler.request()

    # enlève les accents qui gènent
    sTitle2 = re.sub('[^a-zA-Z0-9:. ]', '#', title)
    if sTitle2 != title:
        sTitle2 = title[:sTitle2.index('#')]
    sPattern = '>%s' % sTitle2

    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '<br')

    sPattern = 'href="([^"]+).+?rel=".+?>([^\\(]+)'
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '</p>')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        # total = len(aResult[1])
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0].replace('/stream/', '/embed/')
            sDisplayTitle = title + ' (' + aEntry[1].strip() + ')'

            if 'http' not in sUrl:
                sUrl = urlMain[:-1] + sUrl

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('desc', sDisplayTitle)

            gui.addDir(
                SITE_IDENTIFIER,
                'showLink',
                sDisplayTitle,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    siterefer = input_parameter_handler.getValue('siterefer')
    sHosterUrl = ''

    bvalid, shosterurl = getHosterIframe(sUrl, siterefer)
    if bvalid:
        sHosterUrl = shosterurl

    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()


# Traitement générique
def getHosterIframe(url, referer):

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = RequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False, False

    sPattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        from resources.lib.packer import cPacker
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return True, code + '|Referer=' + url
        except Exception as e:
            pass

    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        referer = url
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    # ajout du nom de domaine
                    url = '//' + referer.split('/')[2] + url
                url = "https:" + url
            b, url = getHosterIframe(url, referer)
            if b:
                return True, url

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return True, url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = RequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        sHosterUrl = sHosterUrl.replace('index', 'mono')
        return True, sHosterUrl + '|referer=' + url

    return False, False
