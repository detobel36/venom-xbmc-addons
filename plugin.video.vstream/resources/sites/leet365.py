# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import ast
import re

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

SITE_IDENTIFIER = 'leet365'
SITE_NAME = 'Leet365'
SITE_DESC = 'Tous les sports'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = (True, 'load')
TV_TV = (True, 'load')
SPORT_TV = ('sport', 'showTV')
CHAINE_CINE = ('cinema', 'showTV')
SPORT_LIVE = ('/', 'showMovies')
SPORT_GENRES = ('/', 'showGenres')

# chaines dans l'ordre d'affichage
channels = {
    1: ['bein Sports 1', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    4: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    21: ['prime video ligue 1', 'https://i.imgur.com/PvpkxgG.png'],
    20: ['prime video ligue 2', 'https://i.imgur.com/PvpkxgG.png'],
    5: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    6: ['Canal+ sport', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG'],
    17: ['Canal+ decale', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_257.PNG'],
    7: ['eurosport 1', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg'],
    8: ['eurosport 2', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg'],
    18: ['L\'equipe TV', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png'],
    19: ['Automoto', 'https://moto-station.com/wp-content/uploads/2021/05/05/Automoto-La-Chaine-logo_0.png.jpg'],
    9: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    2: ['bein Sports 2', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    3: ['bein Sports 3', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    10: ['bein Sports MAX 4', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    11: ['bein Sports MAX 5', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    12: ['bein Sports MAX 6', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    13: ['bein Sports MAX 7', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    14: ['bein Sports MAX 8', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    15: ['bein Sports MAX 9', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    16: ['bein Sports MAX 10', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png'],
    22: ['prime video ligue 1/2 (LDC4)', 'https://i.imgur.com/PvpkxgG.png'],
    23: ['prime video ligue 1/2 (LDC5)', 'https://i.imgur.com/PvpkxgG.png'],
    24: ['prime video ligue 1/2 (LDC6)', 'https://i.imgur.com/PvpkxgG.png'],
    25: ['prime video ligue 1/2 (LDC7)', 'https://i.imgur.com/PvpkxgG.png'],
    26: ['prime video ligue 1/2 (LDC8)', 'https://i.imgur.com/PvpkxgG.png'],
    27: ['prime video ligue 1/2 (LDC9)', 'https://i.imgur.com/PvpkxgG.png'],
    28: ['prime video ligue 1/2 (LDC10)', 'https://i.imgur.com/PvpkxgG.png'],
    37: ['foot+', 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png'],
    31: ['multisport+ 1', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    32: ['multisport+ 2', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    33: ['multisport+ 3', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    34: ['multisport+ 4', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    35: ['multisport+ 5', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    36: ['multisport+ 6', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    29: ['TF1', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/TF1_logo_2013.png/800px-TF1_logo_2013.png'],
    30: ['France 2', 'https://www.ffp.asso.fr/wp-content/uploads/2018/10/France-2.png'],
    38: ['France 3', 'https://static.wikia.nocookie.net/hdl-logopedia/images/0/0a/Logo-france-3.png/revision/latest/scale-to-width-down/220?cb=20180220171302&path-prefix=fr'],
    39: ['TMC', 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Tmc_2016.png']
}


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

    output_parameter_handler.addParameter('site_url', CHAINE_CINE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        CHAINE_CINE[1],
        'Chaines TV Ciné',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = URL_MAIN + input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Besoin des saut de ligne
    html_content = html_content.replace('\n', '@')
    pattern = '\\d+-\\d+-\\d+ \\(.+?\\) (.+?) : .+?@'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
        gui.setEndOfDirectory()
        return

    genres = set()
    for sGenre in results[1]:
        genres.add(sGenre)

    output_parameter_handler = OutputParameterHandler()
    for sGenre in sorted(genres):
        title = sGenre
        display_title = title

        output_parameter_handler.addParameter('site_url', 'genre=' + sGenre)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('desc', display_title)
        gui.addMisc(
            SITE_IDENTIFIER,
            'showMovies',
            display_title,
            'sport.png',
            '',
            display_title,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showTV():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'sport' in url:
        chaines = [
            1,
            4,
            21,
            20,
            5,
            6,
            7,
            8,
            18,
            19,
            9,
            2,
            3,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            37,
            31,
            32,
            33,
            34,
            35,
            36]
    else:  # Chaines ciné
        chaines = [29, 30, 38, 5, 17, 39]

    output_parameter_handler = OutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        display_title = channel[0]
        thumb = channel[1]
        output_parameter_handler.addParameter('site_url', iChannel)
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


def showMovies():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = URL_MAIN + input_parameter_handler.getValue('site_url')
    sGenre = ''

    if 'genre=' in url:
        url, sGenre = url.split('genre=')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Besoin des saut de ligne
    html_content = html_content.replace('\n', '@')
    pattern = '(\\d+-\\d+-\\d+ \\(.+?\\)) (.+?) : (.+?)\\(CH(.+?)@'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sDate = entry[0].replace(
                '-20', '/').replace('-', '/').replace('(', '').replace(')', '')
            sDesc1 = entry[1]
            if sGenre and sGenre != sDesc1:
                continue
            sDesc2 = entry[2]
            url2 = "('" + entry[3].replace(') (',
                                             "', '").replace('(CH', "('").replace(')', "')")
            title = '%s (%s)' % (sDesc2, sDesc1)
            display_title = sDate + ' - ' + title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', display_title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showLive',
                display_title,
                'sport.png',
                '',
                display_title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLive():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    desc = input_parameter_handler.getValue('desc')
    movie_title = input_parameter_handler.getValue('movie_title')

    links = []
    if ',' in url:
        links.extend(eval(url))
    else:
        links.append(eval(url))

    output_parameter_handler = OutputParameterHandler()
    for link in links:
        entry = re.findall('(\\d+)(.+)', link)
        iChannel = entry[0][0]
        lang = entry[0][1]
        channel = channels.get(int(iChannel))
        sChannel = thumb = ''
        if channel:
            sChannel = channel[0]
            thumb = channel[1]
        display_title = '%s - [%s] (%s)' % (movie_title, sChannel, lang)

        output_parameter_handler.addParameter('site_url', iChannel)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addMisc(
            SITE_IDENTIFIER,
            'showLink',
            display_title,
            'sport.png',
            thumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    if not thumb:
        thumb = ''

    hoster = 'https://leet365.cc/fr/%d/%s'
# alternative    hoster = 'https://1rowsports.com/player/%d/%s'

    output_parameter_handler = OutputParameterHandler()

    # jusqu'à 6 hosters, mais on vStream ne sait décoder que le 1 et le 5.
    hosters = [1, 5]
#    for numHost in range(1, 7):
    i = 0
    for numHost in hosters:
        i += 1
        display_title = '%s [Lien %d]' % (movie_title, i)
        hoster_url = hoster % (numHost, url)
        output_parameter_handler.addParameter('site_url', hoster_url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addMisc(
            SITE_IDENTIFIER,
            'showHoster',
            display_title,
            'sport.png',
            thumb,
            display_title,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHoster():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    if not thumb:
        thumb = ''

    bvalid, hoster_url = Hoster_Leet365(url, url)

    if hoster_url:
        hoster_url = hoster_url.strip()
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


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
        if 'fclecteur.com' in hostUrl:
            return Hoster_Laylow(hostUrl, url)
        return Hoster_Wigistream(hostUrl, url)

    pattern = '<script>fid="(.+?)".+?src="\\/\\/fclecteur\\.com\\/footy\\.js">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        referer = url
        url = 'https://fclecteur.com/footy.php?player=desktop&live=%s' % results[1][0]
        return Hoster_Laylow(url, referer)

    return False, False


def Hoster_Wigistream(url, referer):

    if not url.startswith('http'):
        url = 'https:' + url
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
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


def Hoster_Pkcast(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Referer', '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(referer)))
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'play\\(\\).+?return\\((.+?)\\.join'
    results = parser.parse(html_content, pattern)

    if results:
        return True, ''.join(
            ast.literal_eval(
                results[1][0])) + '|User-Agent=' + UA + '&Referer=' + Quote(url)

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
