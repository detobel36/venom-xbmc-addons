# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import ast
import base64
import json
import re
import time
from datetime import datetime, timedelta

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser
from resources.lib.util import Quote

try:  # Python 2
    from urlparse import urlparse
except ImportError:  # Python 3
    from urllib.parse import urlparse

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'streamonsport'
SITE_NAME = 'Streamonsport'
SITE_DESC = 'Site pour regarder du sport en direct'

SPORT_SPORTS = ('/', 'load')
TV_TV = ('/', 'load')
SPORT_TV = (
    '31-foot-rugby-tennis-basket-f1-moto-hand-en-streaming-direct.html',
    'showMovies')
# CHAINE_CINE = ('2370162-chaines-tv-streaming-tf1-france-2-canal-plus.html', 'showMovies')
SPORT_LIVE = ('/', 'showMovies')
SPORT_GENRES = ('/', 'showGenres')


URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = ''


def GetUrlMain():
    global URL_MAIN
    if URL_MAIN != '':
        return URL_MAIN

    request_handler = RequestHandler(
        SiteManager().getUrlMain(SITE_IDENTIFIER))
    html_content = request_handler.request()

    pattern = '<a href="(.+?)"'
    parser = Parser()
    URL_MAIN = parser.parse(html_content, pattern)[1][0]
    return URL_MAIN


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', SPORT_LIVE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_LIVE[1],
        'Sports (En direct)',
        'replay.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SPORT_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', output_parameter_handler)
    #
    output_parameter_handler.addParameter('site_url', SPORT_TV[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_TV[1],
        'Chaines TV Sports',
        'sport.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', CHAINE_CINE[0])
    # gui.addDir(SITE_IDENTIFIER, CHAINE_CINE[1], 'Chaines TV Ciné', 'tv.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    urlMain = GetUrlMain()

    genreURL = '-foot-rugby-tennis-basket-f1-moto-hand-en-streaming-direct.html'
    genres = [('Basket', '3'), ('Football', '1'), ('Rugby', '2'),
              ('Tennis', '5'), ('Fomule1', '4'), ('Handball', '6'), ('Moto', '7')]

    output_parameter_handler = OutputParameterHandler()
    for title, url in genres:
        url = urlMain + url + genreURL
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', title)
        gui.addMisc(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            '',
            title,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    urlMain = GetUrlMain()
    if 'http' not in url:
        url = urlMain + url

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # THUMB ref title desc1 desc2
    pattern = '<img class=".+?src="([^"]+)".+?href="([^"]+).+?<span>([^<]+)<.+?data-time="(?:([^<]+)|)".+?>([^<]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        # total = len(results[1])
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            thumb = entry[0]
            url2 = entry[1]
            title = entry[2].replace(
                ' streaming gratuit',
                '').replace(
                ' foot',
                '').replace(
                '🆚',
                '/')
            sDate = entry[3]
            sDesc1 = entry[4]

            # bChaine = False
            # if url != CHAINE_CINE[0] and url != SPORT_TV[0]:
            if url != SPORT_TV[0]:
                display_title = title
                if sDesc1 and 'chaîne' not in sDesc1 and 'chaine' not in sDesc1:
                    display_title += ' (' + sDesc1.replace(' · ', '') + ')'
                if sDate:
                    try:
                        d = datetime(
                            *(time.strptime(sDate, '%Y-%m-%dT%H:%M:%S+01:00')[0:6]))
                        sDate = d.strftime("%d/%m/%y %H:%M")
                    except Exception:
                        pass
                    display_title = sDate + ' - ' + display_title
            else:
                # bChaine = True
                title = title.upper()
                display_title = title

            if 'http' not in url2:
                url2 = urlMain[:-1] + url2

            if 'http' not in thumb:
                thumb = urlMain[:-1] + thumb

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addLink(
                SITE_IDENTIFIER,
                'showLive',
                display_title,
                thumb,
                display_title,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showLive():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    # liens visibles
    pattern = r"btn btn-(success|warning) *btn-sm.+?src='([^\']*).+?img src=\".+?lang\/([^\"]*)\.gif.+?this\.src='.+?lang\/([^\']*)\.gif"
    results = parser.parse(html_content, pattern)

    i = 0
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        if results[1]:
            for entry in results[1]:
                i += 1
                url2 = entry[1]
                sLang1 = entry[2].upper()
                sLang2 = entry[3].upper()
                display_title = '%s - Lien %d (%s)' % (movie_title, i, sLang1 if len(
                    sLang1) == 2 else sLang2 if len(sLang2) == 2 else '')

                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('siterefer', url)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)


<< << << < HEAD
# # 1 seul liens tv telerium
# pattern = 'iframe id="video" src.+?id=([^"]+)'
# results = parser.parse(html_content, pattern)
# if results[0] is True:
#     url2 = GetUrlMain() + 'go/' + results[1][0]
#     display_title = movie_title
#     output_parameter_handler = OutputParameterHandler()
#     output_parameter_handler.addParameter('site_url', url2)
#     output_parameter_handler.addParameter('movie_title', movie_title)
#     output_parameter_handler.addParameter('thumb', thumb)
#     output_parameter_handler.addParameter('siterefer', url)
#     gui.addLink(SITE_IDENTIFIER, 'showLink', display_title, thumb, desc, output_parameter_handler)
== == == =
# 1 seul liens tv telerium
pattern = 'iframe id="video".src.+?id=([^"]+)'

results = parser.parse(html_content, pattern)
if results[0] is True:
    url2 = results[1][0]
    request_handler = RequestHandler(url2)
    html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0] is True:

        url2 = results[1][0]  # https://telerium.tv/embed/35001.html
        display_title = movie_title

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url2)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('siterefer', url)
        gui.addLink(
            SITE_IDENTIFIER,
            'showlink',
            display_title,
            thumb,
            desc,
            output_parameter_handler,
            input_parameter_handler)
>>>>>> > c8d3996be(Try to make auto play)

gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    siterefer = input_parameter_handler.getValue('siterefer')
    hoster_url = ''

    if 'yahoo' in url:  # redirection
        urlMain = GetUrlMain()
        url = urlMain + url

    if 'allfoot' in url or 'streamonsport' in url:
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        # request_handler.addHeaderEntry('Referer', siterefer) # a verifier
        html_content = request_handler.request()

        siterefer = url
        parser = Parser()
        if "pkcast123.me" in html_content:
            pattern = 'fid="([^"]+)"'
            results = parser.parse(html_content, pattern)
            url = "https://www.pkcast123.me/footy.php?player=desktop&live=" + \
                results[1][0] + "&vw=649&vh=460"
        else:
            pattern = '<iframe.+?src="([^"]+)'
            results = parser.parse(html_content, pattern)
            if results[0]:
                url = results[1][0]

    shosterurl = ''
    if 'hola.php' in url:
        urlMain = GetUrlMain()
        url = urlMain + url

    if 'pkcast123' in url:
        bvalid, shosterurl = Hoster_Pkcast(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if "leet365.cc" in url or 'casadelfutbol' in url:
        bvalid, shosterurl = Hoster_Leet365(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if 'telerium' in url:
        bvalid, shosterurl = Hoster_Telerium(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if 'andrhino' in url:
        bvalid, shosterurl = Hoster_Andrhino(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if 'wigistream' in url or 'cloudstream' in url:
        bvalid, shosterurl = Hoster_Wigistream(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    # a verifier
    if 'laylow' in url:
        bvalid, shosterurl = Hoster_Laylow(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if not hoster_url:
        bvalid, shosterurl = getHosterIframe(url, siterefer)
        if bvalid:
            hoster_url = shosterurl

    if hoster_url:
        hoster_url = hoster_url.strip()
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def Hoster_Pkcast(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Referer', '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(referer)))
    html_content = request_handler.request()

    parser = Parser()
    pattern = r'play\(\).+?return\((.+?)\.join'
    results = parser.parse(html_content, pattern)

    if results:
        return True, ''.join(
            ast.literal_eval(
                results[1][0])) + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Telerium(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    urlrederict = request_handler.getRealUrl()
    # ex https://telerium.club
    urlmain = 'https://' + urlrederict.split('/')[2]

    pattern = r'var\s+cid[^\'"]+[\'"]{1}([0-9]+)'
    results = re.findall(pattern, html_content)

    if results:
        str2 = results[0]
        datetoken = int(getTimer()) * 1000

        jsonUrl = urlmain + '/streams/' + str2 + '/' + str(datetoken) + '.json'
        tokens = getRealTokenJson(jsonUrl, urlrederict)
        m3url = tokens['url']
        nxturl = urlmain + tokens['tokenurl']
        realtoken = getRealTokenJson(nxturl, urlrederict)[10][::-1]
        try:
            m3url = m3url.decode("utf-8")
        except Exception:
            pass

        hoster_url = 'https:' + m3url + realtoken
        hoster_url += '|User-Agent=' + UA + \
            '&Referer=' + Quote(urlrederict)  # + '&Sec-F'

        return True, hoster_url

    return False, False


def Hoster_Leet365(url, referer):
    parser = Parser()
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        hostUrl = results[1][0]
        if 'dailymotion' in hostUrl:
            return True, hostUrl
        return Hoster_Wigistream(hostUrl, url)

    pattern = r'<script>fid="(.+?)".+?src="\/\/fclecteur\.com\/footy\.js">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        referer = url
        url = 'https://fclecteur.com/footy.php?player=desktop&live=%s' % results[1][0]
        return Hoster_Laylow(url, referer)

    return False, False


def Hoster_Andrhino(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = r"atob\('([^']+)"
    results = re.findall(pattern, html_content)

    if results:
        url2 = base64.b64decode(results[0])
        return True, url2.strip() + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    # fichier vu mais ne sait plus dans quel cas
    pattern = r"source:\s'(https.+?m3u8)"
    results = re.findall(pattern, html_content)

    if results:
        return True, results[0] + '|User-Agent=' + \
            UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Wigistream(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = r'(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    results = re.findall(pattern, html_content)

    if results:
        sstr = results[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sUnpack = cPacker().unpack(sstr)
        pattern = 'src="(.+?)"'
        results = re.findall(pattern, sUnpack)
        if results:
            return True, results[0] + '|User-Agent=' + \
                UA + '&Referer=' + Quote(url)

    pattern = '<iframe.+?src="([^"]+)'  # iframe imbriqué
    results = re.findall(pattern, html_content)
    if results:
        return Hoster_Wigistream(results[0], url)

    return False, False


def Hoster_Laylow(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = "source:.+?'(https.+?m3u8)"
    results = re.findall(pattern, html_content)

    if results:
        return True, results[0] + '|User-Agent=' + \
            UA + '&Referer=' + Quote(url)

    return Hoster_Pkcast(url, referer)


def getRealTokenJson(link, referer):

    realResp = ''
    request_handler = RequestHandler(link)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept-Language',
        'pl,en-US;q=0.7,en;q=0.3')
    request_handler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    request_handler.addHeaderEntry('Referer', referer)
    request_handler.addCookieEntry('elVolumen', '100')
    request_handler.addCookieEntry('__ga', '100')

    try:
        realResp = request_handler.request()
    except Exception:
        pass

    if not realResp:
        request_handler = RequestHandler(link)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Accept', 'application/json')
        request_handler.addHeaderEntry(
            'Accept-Language', 'pl,en-US;q=0.7,en;q=0.3')
        request_handler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        request_handler.addHeaderEntry('Referer', referer)
        request_handler.addCookieEntry('elVolumen', '100')
        request_handler.addCookieEntry('__ga', '100')
        realResp = request_handler.request()

    return json.loads(realResp)


def getTimer():
    datenow = datetime.utcnow().replace(second=0, microsecond=0)
    datenow = datenow + timedelta(days=1)
    epoch = datetime(1970, 1, 1)
    return (datenow - epoch).total_seconds() // 1


# Traitement générique
def getHosterIframe(url, referer):

    if not url.startswith('http'):
        url = GetUrlMain() + url

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = str(request_handler.request())
    if not html_content:
        return False, False

    pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
    results = re.findall(pattern, html_content)
    if results:
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

    pattern = '<iframe.+?src=["\']([^"\']+)["\']'
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
            return True, url  # + '|User-Agent=' + UA + '&Referer=' + referer

    pattern = '[^/]source.+?["\'](https.+?)["\']'
    results = re.findall(pattern, html_content)
    if results:
        return True, results[0] + '|referer=' + url

    return False, False
