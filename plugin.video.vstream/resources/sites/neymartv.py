# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import SiteManager, isMatrix
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser


SITE_IDENTIFIER = 'neymartv'
SITE_NAME = 'NeymarTV'
SITE_DESC = 'Toutes les chaines de Sport'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = ('p/all-sports-tv-schedule-full-hd.html', 'showGenres')

TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showTV')


# chaines
channels = {

    'bein Sports 1': ['2023/01/bein-sports-1-full-hd-france.html', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],

    'Canal+': ['2023/01/canal-france-full-hd.html', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    #    'Canal+ sport': ['2022/03/canal-sport-full-hd.html', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG'],
    'Foot+': ['2022/03/foot-full-hd.html', 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png'],
    #    'GOLF+': ['2022/06/golf-full-hd.html', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],

    'RMC Sport 1': ['2023/01/rmc-sport-1-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    'RMC Sport 2': ['2023/01/rmc-sport-2-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],

    'eurosport 1': ['2022/03/eurosport-1-full-hd-france.html', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg'],
    'eurosport 2': ['2022/03/eurosport-2-full-hd-france.html', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg'],

    'L\'equipe TV': ['2022/05/lequipe-tv-full-hd.html', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png'],

    'bein Sports 2': ['2023/01/bein-sports-2-full-hd-france.html', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    'bein Sports 3': ['2023/01/bein-sports-3-full-hd-france.html', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    'bein Sports MAX 4': ['2022/03/bein-sports-max-4-full-hd-france.html', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    'bein Sports MAX 5': ['2022/03/bein-sports-max-5-full-hd-france.html', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    'bein Sports MAX 6': ['2022/03/bein-sports-max-6-full-hd-france.html', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    'bein Sports MAX 7': ['2022/03/bein-sports-max-7-full-hd-france.html', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    'bein Sports MAX 8': ['2022/03/bein-sports-max-8-full-hd-france.html', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    'bein Sports MAX 9': ['2022/03/bein-sports-max-9-full-hd-france.html', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    'bein Sports MAX 10': ['2022/03/bein-sports-max-10-full-hd-france.html', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png'],

    'RMC SPORT 3': ['2022/03/rmc-sport-3-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT3_PNG_500x500px.png?w=500&ssl=1'],
    'RMC SPORT 4': ['2022/03/rmc-sport-4-full-hd.html', 'https://w0rld.tv/wp-content/uploads/2020/09/rmc-sport-4.png'],
    'RMC SPORT LIVE 5': ['2022/03/rmc-sport-live-5-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],
    'RMC SPORT LIVE 6': ['2022/03/rmc-sport-live-6-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],
    'RMC SPORT LIVE 7': ['2022/03/rmc-sport-live-7-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],
    'RMC SPORT LIVE 8': ['2022/03/rmc-sport-live-8-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],
    'RMC SPORT LIVE 9': ['2022/03/rmc-sport-live-9-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],
    'RMC SPORT LIVE 10': ['2022/03/rmc-sport-live-10-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png'],

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
    output_parameter_handler = OutputParameterHandler()

    for display_title in channels:
        value = channels.get(display_title)
        url = value[0]
        thumb = value[1]
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', display_title)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addLink(
            SITE_IDENTIFIER,
            'showHoster',
            display_title,
            thumb,
            display_title,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(URL_MAIN + url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<h3> (.+?) <\\/h3>.+?&#9989;'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        sportGenre = {}
        output_parameter_handler = OutputParameterHandler()
        for title in results[1]:
            display_title = title
            display_title = display_title.replace('ALPINE SKI', 'SKI')
            display_title = display_title.replace('BOXING', 'BOXE')
            display_title = display_title.replace('CLIMBING', 'ESCALADE')
            display_title = display_title.replace('CYCLING', 'CYCLISME')
            display_title = display_title.replace('DARTS', 'FLECHETTES')
            display_title = display_title.replace(
                'HORSE RACING', 'COURSES DE CHEVAUX')
            display_title = display_title.replace(
                'ICE HOCKEY', 'HOCKEY SUR GLACE')
            display_title = display_title.replace('RUGBY UNION', 'RUGBY')
            display_title = display_title.replace('SAILING/BOATING', 'VOILE')
            display_title = display_title.replace('SOCCER', 'FOOTBALL')
            display_title = display_title.replace(
                'TABLE TENNIS', 'TENNIS DE TABLE')
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

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')
    url = URL_MAIN + input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<h3> %s <' % title
    html_content = parser.abParse(html_content, pattern, '<h3>')

    pattern = '(\\d+:\\d+) (.+?)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sDate = entry[0]
            title = entry[1].strip()
            display_title = sDate + ' - ' + title.strip()
            title = sDate + ' ' + title

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMoviesLinks',
                display_title,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesLinks():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '%s' % title
    html_content = parser.abParse(html_content, pattern, '<br ')

    pattern = 'href="(.+?)" target="_blank" rel="noopener">(.+?)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            display_title = title = entry[1].strip()

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


def showHoster():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    url = URL_MAIN + input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<li movieurl=["\']([^"]+)["\']><a>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        blackList = (
            '.tutele.sx',
            'leet365',
            'casadelfutbol.net',
            'yrsport.top',
            'cdn.sportcast.life',
            '.ustreamix.su',
            'sportzonline.to',
            'sportkart1.xyz',
            'olasports.xyz',
            'cricplay2.xyz')
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            hoster = entry[1]
            for out in blackList:
                if out in url:
                    url = None
                    break

            if not url:
                continue

            display_title = title + ' (' + hoster.strip() + ')'

            if 'http' not in url:
                url = URL_MAIN[:-1] + url

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLink',
                display_title,
                thumb,
                display_title,
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

# TODO
# url = "https://stream.crichd.vip/update/euro1.php"
# url = "https://www.tutelehd.com/online.php?a=3112"

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
#    request_handler.disableSSL()
    html_content = str(request_handler.request())
#    cook = request_handler.GetCookies()

    if not html_content or html_content == 'False':
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
        request_handler = RequestHandler(hoster_url)
        h = request_handler.request()
        return True, hoster_url + '|referer=' + url
    return False, False
