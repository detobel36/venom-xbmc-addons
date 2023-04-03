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

    output_parameter_handler.addParameter('site_url', SPORT_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_GENRES[1],
        'Sports (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPORT_TV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_TV[1],
        'Chaines TV Sports',
        'sport.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showTV():
    gui = Gui()

    url = URL_MAIN + '/cast/stream-%d.php'
    chaines = [116, 117, 118, 119, 120, 121, 122]

    output_parameter_handler = OutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        display_title = channel[0]
        thumb = channel[1]
        output_parameter_handler.addParameter('site_url', url % iChannel)
        output_parameter_handler.addParameter('movie_title', display_title)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addLink(
            SITE_IDENTIFIER,
            'showLink',
            display_title,
            thumb,
            display_title,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    url = URL_MAIN
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<h2 style="background-color:cyan">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        sportGenre = {}
        output_parameter_handler = OutputParameterHandler()
        for title in results[1]:
            if 'Schedule' in title:
                break
            if 'Tv Show' in title:
                continue

            display_title = title.replace('Soccer', 'Football')
            display_title = display_title.replace('Darts', 'Flechettes')
            display_title = display_title.replace('Boxing', 'Boxe')
            display_title = display_title.replace('Cycling', 'Cyclisme')
            display_title = display_title.replace(
                'Horse Racing', 'Course de chevaux')
            display_title = display_title.replace(
                'Ice Hockey', 'Hockey sur glace')
            display_title = display_title.replace('Alpine Ski', 'Ski')
            display_title = display_title.replace('Rugby Union', 'Rugby à XV')
            display_title = display_title.replace('Sailing / Boating', 'Voile')
            sportGenre[display_title] = title

        for display_title, title in sorted(sportGenre.items()):
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                display_title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()
    url = URL_MAIN

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<h2 style="background-color:cyan">%s</h2>' % title
    html_content = parser.abParse(
        html_content,
        pattern,
        '<h2 style="background-color:cyan">')

    pattern = '<hr>(<strong>|)(\\d+:\\d+) (.+?)<'  # span.+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sDate = entry[1]
            title = entry[2]
            display_title = sDate + ' - ' + title.strip()
            title = sDate + ' ' + title

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showHoster',
                display_title,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()
    parser = Parser()
    urlMain = URL_MAIN

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(urlMain)
    html_content = request_handler.request()

    # enlève les accents qui gènent
    title2 = re.sub('[^a-zA-Z0-9:. ]', '#', title)
    if title2 != title:
        title2 = title[:title2.index('#')]
    pattern = '>%s' % title2

    html_content = parser.abParse(html_content, pattern, '<br')

    pattern = 'href="([^"]+).+?rel=".+?>([^\\(]+)'
    html_content = parser.abParse(html_content, pattern, '</p>')
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        # total = len(results[1])
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0].replace('/stream/', '/embed/')
            display_title = title + ' (' + entry[1].strip() + ')'

            if 'http' not in url:
                url = urlMain[:-1] + url

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)

            gui.addDir(
                SITE_IDENTIFIER,
                'showLink',
                display_title,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    siterefer = input_parameter_handler.getValue('siterefer')
    hoster_url = ''

    bvalid, shosterurl = getHosterIframe(url, siterefer)
    if bvalid:
        hoster_url = shosterurl

    if hoster_url:
        hoster_url = hoster_url.strip()
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


# Traitement générique
def getHosterIframe(url, referer):

    if not url.startswith('http'):
        url = URL_MAIN + url

    request_handler = RequestHandler(url)
    if referer:
        request_handler.addHeaderEntry('Referer', referer)
    html_content = str(request_handler.request())
    if not html_content:
        return False, False

    pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    results = re.findall(pattern, html_content)
    if results:
        from resources.lib.packer import cPacker
        sstr = results[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        html_content = cPacker().unpack(sstr)

    pattern = '.atob\\("(.+?)"'
    results = re.findall(pattern, html_content)
    if results:
        import base64
        code = results[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return True, code + '|Referer=' + url
        except Exception as e:
            pass

    pattern = '<iframe src=["\']([^"\']+)["\']'
    results = re.findall(pattern, html_content)
    if results:
        referer = url
        for url in results:
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

    pattern = ';var.+?src=["\']([^"\']+)["\']'
    results = re.findall(pattern, html_content)
    if results:
        url = results[0]
        if '.m3u8' in url:
            return True, url

    pattern = '[^/]source.+?["\'](https.+?)["\']'
    results = re.findall(pattern, html_content)
    if results:
        request_handler = RequestHandler(results[0])
        request_handler.request()
        hoster_url = request_handler.getRealUrl()
        hoster_url = hoster_url.replace('index', 'mono')
        return True, hoster_url + '|referer=' + url

    return False, False
