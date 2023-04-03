# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import base64
import re
import xbmc

from resources.lib.comaddon import Progress, isMatrix, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import Parser
from resources.lib.util import cUtil, Unquote

try:
    import json
except BaseException:
    import simplejson as json

SITE_IDENTIFIER = 'livetv'
SITE_NAME = 'Live TV'
SITE_DESC = 'Evénements sportifs en direct'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

SPORT_GENRES = (URL_MAIN + '/frx/allupcoming/',
                'showMovies')  # Liste de diffusion des sports
SPORT_LIVE = (URL_MAIN + '/frx/', 'showLive')  # streaming Actif
SPORT_SPORTS = (True, 'load')


def load():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', SPORT_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_GENRES[1],
        'Les sports (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SPORT_LIVE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_LIVE[1],
        'Les sports (En direct)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showLive():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a class="live" href="([^"]+)">([^<]+)<.a>\\s*<br>\\s*<a\\s*class="live.+?span class="evdesc">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl3 = URL_MAIN + entry[0]
            title2 = entry[1] + ' ' + entry[2]

            try:
                title2 = title2.decode("iso-8859-1", 'ignore')
            except BaseException:
                pass
            title2 = cUtil().unescape(title2)
            try:
                title2 = title2.encode("utf-8", 'ignore')
                title2 = str(title2, encoding="utf-8", errors='ignore')
            except BaseException:
                pass

            output_parameter_handler.addParameter('siteUrl3', sUrl3)
            output_parameter_handler.addParameter('sMovieTitle2', title2)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies3',
                title2,
                'sport.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies():  # affiche les catégories qui ont des lives'
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a class="main" href="([^"]+)"><b>([^<]+)</b>.+?\\s*</td>\\s*<td width=.+?>\\s*<a class="small" href=".+?"><b>([^<]+)</b></a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = URL_MAIN + entry[0]
            title = entry[1]

            try:
                title = title.decode("iso-8859-1", 'ignore')
            except BaseException:
                pass

            title = cUtil().unescape(title)
            try:
                title = title.encode("utf-8", 'ignore')
                title = str(title, encoding="utf-8", errors='ignore')
            except BaseException:
                pass

            output_parameter_handler.addParameter('siteUrl2', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies2',
                title,
                'genres.png',
                output_parameter_handler)

        gui.setEndOfDirectory()


def showMovies2():  # affiche les matchs en direct depuis la section showMovie

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url2 = input_parameter_handler.getValue('siteUrl2')

    request_handler = RequestHandler(url2)
    html_content = request_handler.request()

    pattern = '<a class="live" href="([^"]+)">([^<]+)</a>\\s*(<br><img src=".+?/img/live.gif"><br>|<br>)\\s*<span class="evdesc">([^<]+)\\s*<br>\\s*([^<]+)</span>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        mois = [
            'filler',
            'janvier',
            'février',
            'mars',
            'avril',
            'mai',
            'juin',
            'juillet',
            'aout',
            'septembre',
            'octobre',
            'novembre',
            'décembre']
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME, large=True)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = ''
            taglive = ''
            title2 = entry[1].replace('<br>', ' ')
            sUrl3 = URL_MAIN + entry[0]

            if 'live.gif' in entry[2]:
                taglive = ' [COLOR limegreen] Online[/COLOR]'

            sDate = entry[3]
            qual = entry[4]

            if not isMatrix():
                try:
                    title2 = title2.decode("iso-8859-1", 'ignore')
                    qual = qual.decode("iso-8859-1", 'ignore')
                    sDate = sDate.decode("iso-8859-1", 'ignore')
                except BaseException:
                    pass

                title2 = cUtil().unescape(title2)
                title2 = title2.encode("utf-8", 'ignore')

                qual = cUtil().unescape(qual)
                qual = str(qual.encode("utf-8", 'ignore'))

                sDate = sDate.encode('utf-8')

            if sDate:
                try:
                    sDateTime = re.findall(
                        '(\\d+) ([\\S]+).+?(\\d+)(:\\d+)', str(sDate))
                    if sDateTime:
                        sMonth = mois.index(sDateTime[0][1])
                        sDate = '%02d/%02d %02d%s' % (
                            int(sDateTime[0][0]), sMonth, int(sDateTime[0][2]), sDateTime[0][3])
                except Exception as e:
                    pass

            title2 = (
                '%s - %s [COLOR yellow]%s[/COLOR]') % (sDate, title2, qual)
            display_title = title2 + taglive

            output_parameter_handler.addParameter('siteUrl3', sUrl3)
            output_parameter_handler.addParameter('sMovieTitle2', title2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies3',
                display_title,
                'sport.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies3():  # affiche les videos disponible du live
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl3 = input_parameter_handler.getValue('siteUrl3')

    request_handler = RequestHandler(sUrl3)
    html_content = request_handler.request()
    sMovieTitle2 = input_parameter_handler.getValue('sMovieTitle2')

    pattern = '<td width=16><img title="(.*?)".+?<a title=".+?" *href="(.+?)"'
    parser = Parser()

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            lang = entry[0]
            lang = cUtil().unescape(lang)
            try:
                lang = lang.encode("utf-8", 'ignore')
                lang = str(lang, encoding="utf-8", errors='ignore')
            except BaseException:
                pass

            sUrl4 = entry[1]
            if not (sUrl4.startswith("http")):
                sUrl4 = "http:" + sUrl4
            title = ('%s (%s)') % (sMovieTitle2, lang[:4])
            thumb = ''

            output_parameter_handler.addParameter('siteUrl4', sUrl4)
            output_parameter_handler.addParameter('sMovieTitle2', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addDir(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'sport.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():  # affiche les videos disponible du live
    gui = Gui()
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    input_parameter_handler = InputParameterHandler()
    sUrl4 = input_parameter_handler.getValue('siteUrl4')
    sMovieTitle2 = input_parameter_handler.getValue('sMovieTitle2')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(sUrl4)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<iframe.+?(?:allowFullScreen=|width).+?src="([^"]+)".+?</iframe>'
    results = parser.parse(html_content, pattern)

    if results[0]:

        hoster_url = ''
        Referer = ''
        url = results[1][0]
        if not (url.startswith("http")):
            url = "http:" + url

        if 'popofthestream' in url:
            request_handler = RequestHandler(url)
            html_content = request_handler.request()
            pattern = 'src="([^"]+)'
            results = re.findall(pattern, html_content)
            if results:
                url2 = url.replace('-', '/')
                urlChannel = url2.replace('html', 'json')
                request_handler = RequestHandler(urlChannel)
                html_content = request_handler.request()

                if not html_content.startswith('<!'):   # ce n'est pas du json
                    result = json.loads(html_content)
                    if 'id' in result:
                        idChannel = result['id']
                        request_handler = RequestHandler(url2)
                        sHtmlContent2 = request_handler.request()
                        pattern = '<iframe.+?src="([^\']+)'
                        results = re.findall(pattern, sHtmlContent2)
                        if results:
                            url = results[0] + idChannel

        if 'sportlevel' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = "manifestUrl: '(.+?)',"
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = 'http://d.sportlevel.com' + results[0]
            else:
                sPattern2 = '(http:\\/\\/embedded.+?)"'
                results = parser.parse(sHtmlContent2, sPattern2)
                if results[0]:
                    url2 = results[1][0]
                    request_handler = RequestHandler(url2)
                    sHtmlContent3 = request_handler.request()
                    pattern = "RESOLUTION=(\\w+)\\s*(http.+?)(#|$)"
                    aResult2 = parser.parse(sHtmlContent3, pattern)
                    if aResult2[0] is True:
                        for results in aResult2[1]:
                            q = results[0]
                            hoster_url = results[1]
                            display_title = sMovieTitle2 + ' [' + q + '] '

                            hoster = HosterGui().checkHoster(hoster_url)
                            if hoster:
                                hoster.setDisplayName(display_title)
                                hoster.setFileName(sMovieTitle2)
                                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                                       input_parameter_handler=input_parameter_handler)
                        gui.setEndOfDirectory()
                        return

        if 'tv.rushandball' in url:
            pattern = '\\/(\\d+)'
            results = re.findall(pattern, url)
            if results:
                videoId = results[0]
                url2 = 'https://tv.rushandball.ru/api/v2/content/' + videoId + '/access'

                request_handler = RequestHandler(url2)
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry('Referer', url)
                html_content = request_handler.request()
                pattern = 'stream.+?"(https.+?)"'
                results = parser.parse(html_content, pattern)
                if results[0]:
                    hoster_url = results[1][0]

        if 'seenow.tv' in url:
            pattern = 'api.(.+?)$'
            results = re.findall(pattern, url)
            if results:
                data = 'url=' + results[0] + '&type=tv'  # url=itv-4&type=tv]
                request_handler = RequestHandler(url)
                request_handler.addHeaderEntry('Referer', url)
                request_handler.addHeaderEntry(
                    'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                html_content = request_handler.request()
                cook = request_handler.GetCookies()
                xbmc.sleep(200)
                request_handler = RequestHandler(url)
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry('Content-Length', len(data))
                request_handler.addHeaderEntry('Referer', url)
                request_handler.addHeaderEntry(
                    'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                request_handler.addHeaderEntry(
                    'X-Requested-With', 'XMLHttpRequest')
                # request_handler.addHeaderEntry('Content-Type', 'application/json; charset=utf-8')
                request_handler.addHeaderEntry('Cookie', cook)
                # request_handler.addHeaderEntry('Connection', 'keep-alive')
                request_handler.addParametersLine(data)
                sHtmlContent2 = request_handler.request()  # json

                pattern = 'stream_id.+?(\\d+)'
                results = re.findall(pattern, sHtmlContent2)
                if results:
                    stream_id = results[0]
                    url2 = 'https://www.filmon.com/api-v2/channel/' + stream_id + '?protocol=hls'
                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry(
                        'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                    sHtmlContent2 = request_handler.request()
                    pattern = 'quality"."(\\w+)".*?url.*?"(https.+?)"'
                    results = re.findall(pattern, sHtmlContent2)
                    if results:
                        for Result in results:
                            q = Result[0]
                            hoster_url = Result[1]
                            display_title = sMovieTitle2 + ' [' + q + '] '

                            hoster = HosterGui().checkHoster(hoster_url)
                            if hoster:
                                hoster.setDisplayName(display_title)
                                hoster.setFileName(sMovieTitle2)
                                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                                       input_parameter_handler=input_parameter_handler)

                        gui.setEndOfDirectory()
                        return

        if 'faraoni1' in url:
            # type de chaine : eurosport
            # plusieurs suivi  de liens  possibles 5 max vus
            # ex :
            # http://faraoni1.ru/1/10.html ,20.html 5 requetes
            # LiveTV/live2/1.html 3 requetes
            # etc

            nextlink = url
            for x in range(
                    0, 6):  # 6 reqs max pour trouver lhost (normalement 5 )
                request_handler = RequestHandler(nextlink)
                html_content = request_handler.request()
                pattern = 'url.+?(http.+?m3u8)'
                results = re.findall(pattern, html_content)
                if results:
                    hoster_url = str(results[0])
                    break
                else:
                    pattern = '<iframe.+?src="([^"]+)'
                    results = re.findall(pattern, html_content)
                    if results:
                        nextlink = 'http://faraoni1.ru' + results[0]

        if 'embed.tvcom.cz' in url:
            request_handler = RequestHandler(url)
            html_content = request_handler.request()
            pattern = "source.+?hls.+?'(https.+?m3u8)"
            results = re.findall(pattern, html_content)
            if results:
                hoster_url = results[0]

        if 'allsports.icu' in url:
            pattern = 'ch(\\d+).php'
            results = re.findall(pattern, url)
            if results:
                videoId = results[0]
                url2 = 'http://allsports.icu/stream/ch' + videoId + '.html'
                hoster_url = getHosterIframe(url2, url2)

        # old host
        if 'espn-live.stream' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            results = re.findall(pattern, sHtmlContent2)
            if results:
                url = results[0]  # redirection vers un autre site ci-dessous

        if 'footballreal.xyz' in url or 'cdnz.one' in url:  # or 'sports247' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern1 = '<iframe src=["\'](.+?)["\']'
            results = re.findall(sPattern1, sHtmlContent2)
            if results:
                Referer = url
                url = results[0]  # redirection vers un autre site

        if 'dailydeports.pw' in url:
            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', sUrl4)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src="([^"]+)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                if 'cdnz.one' in results[0]:
                    url = results[0]  # redirection vers un autre site
            else:
                sPattern2 = "str='([^']+)'"
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    for entry in results:
                        entry = entry.replace('@', '')
                        data = bytearray.fromhex(entry).decode()
                        sPattern3 = '<iframe src="([^"]+)"'
                        aResult1 = re.findall(sPattern3, data)
                        if aResult1:
                            url = aResult1[0]  # redirection vers un autre site
                            break

        if 'emb.apl' in url:  # Terminé - Supporte emb.aplayer et emb.apl3
            if url.startswith('//'):
                url = 'http:' + url
            Referer = url
            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('User-Agent', UA)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'source: *\'(.+?)\''

            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0] + '|User-Agent=' + \
                    UA + '&referer=' + Referer
            else:
                sPattern2 = "pl\\.init\\('([^']+)'\\);"
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    hoster_url = results[0] + '|User-Agent=' + \
                        UA + '&referer=' + Referer

        if 'sport7.pw' in url or 'vip7stream' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0] + \
                    '|User-Agent=' + UA + '&referer=' + url

        if 'totalsport.me' in url or 'airhdx' in url or 'givemenbastreams' in url:  # Terminé
            request_handler = RequestHandler(url)
            if Referer:
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'source: ["\'](.+?)["\']'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'sportsbar.pw' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'livesoccers.pw' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = results[0]
                request_handler = RequestHandler(sHosterUrl2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', sHosterUrl2)
                sHtmlContent3 = request_handler.request()
                sPattern3 = '<source src="([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    hoster_url = aResult1[0]

        if 'assia' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'file:"([^"]+)"|source: \'([^\']+)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0][1] + \
                    '|User-Agent=' + UA + '&referer=' + url
            else:
                sPattern2 = '<source src=\'([^\']+)\''
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    hoster_url = results[0] + \
                        '|User-Agent=' + UA + '&referer=' + url

        if 'sawlive' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'src="([^"]+)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl3 = results[0]
                request_handler = RequestHandler(sHosterUrl3)
                sHtmlContent3 = request_handler.request()
                sPattern3 = 'var .+? = "([^;]+);([^\"]+)";'
                results = re.findall(sPattern3, sHtmlContent3)
                if results:
                    sHosterUrl3 = "http://www.sawlive.tv/embedm/stream/" + \
                        results[0][1] + '/' + results[0][0]
                    request_handler = RequestHandler(sHosterUrl3)
                    sHtmlContent4 = request_handler.request()

                    sPattern4 = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
                    results = re.findall(sPattern4, sHtmlContent4)
                    if results:
                        str2 = results[0]
                        if not str2.endswith(';'):
                            str2 = str2 + ';'

                        strs = cPacker().unpack(str2)
                        sPattern5 = 'var .+?=([^;]+);'
                        aResult1 = re.findall(sPattern5, strs)
                        if aResult1:
                            jameiei = eval(aResult1[0])
                            data = ''
                            for c in jameiei:
                                data += chr(c)
                            hoster_url = data

        if 'sportlive.site' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src="(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = results[0]
                request_handler = RequestHandler(sHosterUrl2)
                sHtmlContent3 = request_handler.request()
                sPattern3 = '<script type=\'text/javascript\'>id=\'(.+?)\''
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    sHosterUrl3 = aResult2[0]
                    sHosterUrl3 = "http://hdcast.pw/stream_jw2.php?id=" + sHosterUrl3
                    request_handler = RequestHandler(sHosterUrl3)
                    sHtmlContent4 = request_handler.request()
                    sPattern4 = 'curl = "([^"]+)";'
                    aResult3 = re.findall(sPattern4, sHtmlContent4)
                    if aResult3:
                        hoster_url = aResult3[0]
                        hoster_url = base64.b64decode(hoster_url)

        if 'stream365' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'var a[ 0-9]+="(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                gameId = int(results[2]) + int(results[0]) - \
                    int(results[1]) - int(results[2])
                hoster_url = 'http://91.192.80.210/edge0/xrecord/' + \
                    str(gameId) + '/prog_index.m3u8'

        if 'youtube' in url:  # Je sais pas
            sPattern2 = 'youtube.com/embed/(.+?)[?]autoplay=1'
            results = re.findall(sPattern2, url)

            if results:
                video_id = results[0]
                url2 = url.replace(
                    '/embed/', '/watch?v=').replace('?autoplay=1', '')
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                sHtmlContent3 = Unquote(str(request_handler.request()))

                sPattern3 = 'hlsManifestUrl":"(.+?)"'
                results = re.findall(sPattern3, sHtmlContent3)

                if results:
                    hoster_url = results[0] + '|User-Agent=' + \
                        UA + '&Host=manifest.googlevideo.com'
                else:
                    url2 = 'https://youtube.com/get_video_info?video_id=' + video_id + '&sts=17488&hl=fr'

                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent3 = Unquote(str(request_handler.request()))

                    sPattern3 = 'hlsManifestUrl":"(.+?)"'
                    results = re.findall(sPattern3, sHtmlContent3)

                    if results:
                        hoster_url = results[0] + '|User-Agent=' + \
                            UA + '&Host=manifest.googlevideo.com'

        if 'streamup.me' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src="([^"]+)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = results[0]
                request_handler = RequestHandler(sHosterUrl2)
                sHtmlContent3 = request_handler.request()
                sHtmlContent3 = Unquote(sHtmlContent3)
                sPattern3 = 'src: "\\/\\/(.+?)"'
                results = re.findall(sPattern3, sHtmlContent3)
                if results:
                    hoster_url = 'http://' + results[0]

        if 'livestream' in url:  # fixé
            sPattern2 = '<td bgcolor=".+?" *align="center".+?\\s*<iframe.+?src="https://([^"]+)/player?.+?</iframe>'
            results = re.findall(sPattern2, html_content)
            if results:
                accountid = results[0]
                jsonUrl = 'https://player-api.new.' + accountid + '?format=short'
                request_handler = RequestHandler(jsonUrl)
                html_content = request_handler.request()
                sPattern3 = '"m3u8_url":"(.+?)"'
                results = re.findall(sPattern3, html_content)
            if results:
                hoster_url = results[0]

        if 'forbet.tv' in url:  # Probleme ssl
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'file: "([^"]+)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'p.hd24.watch' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'data-channel="([^"]+)">'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                Host = '190-2-146-56.livesports24.online'
                hoster_url = 'https://' + Host + '/' + results[0] + '.m3u8'

        if 'hdsoccerstreams.net' in url:  # Pas terminer
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<script>fid="(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                fid = results[0]
                url2 = 'http://webtv.ws/embed.php?live=spstream' + fid + '&vw=700&vh=440'
                Referer = url
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = request_handler.request()

        if 'lato.sx' in url:  # Pas terminer
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<script>fid=["\'](.+?)["\']'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                fid = results[0]
                url2 = 'https://yourjustajoo.com/embedred.php?player=desktop&live=' + fid
                Referer = url
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = request_handler.request()

                sPattern2 = 'player.load\\({source: (.+?)\\('
                results = re.findall(sPattern2, sHtmlContent3)
                if results:
                    func = results[0]

                    # sPattern2 = 'function %s\(\) +{ +return\(\[(.+?)\]' % func
                    # sPattern2 = 'function %s\(\) +{ +return\(\[([^\[]+)\]' % func
                    sPattern2 = 'function %s\\(\\) +{\n + return\\(\\[([^\\]]+)' % func
                    results = re.findall(sPattern2, sHtmlContent3)

                    if results:
                        hoster_url = results[0].replace(
                            '"', '').replace(',', '')

        if 'thesports4u.net' in url or 'soccerstreams' in url or 'all.ive' in url:  # Fini
            if 'all.ive' in url:
                request_handler = RequestHandler(url)
                sHtmlContent2 = request_handler.request()
                sPattern2 = "<script>fid='(.+?)'"
                results = re.findall(sPattern2, sHtmlContent2)

                if results:
                    Referer = 'https://ragnaru.net/'
                    url2 = 'https://ragnaru.net/embed.php?player=desktop&live=' + \
                        results[0]
                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry(
                        'Referer', 'https://all.ive.zone/')
                    sHtmlContent3 = request_handler.request()

            if 'thesports4u' in url:
                request_handler = RequestHandler(url)
                sHtmlContent2 = request_handler.request()
                sPattern2 = '<script>fid="(.+?)"'
                results = re.findall(sPattern2, sHtmlContent2)

                if results:
                    url2 = 'http://wlive.tv/embed.php?player=desktop&live=' + \
                        results[0] + '&vw=700&vh=440'
                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry(
                        'Referer', 'http://thesports4u.net/')
                    request_handler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = request_handler.request()

            if 'soccerstreams' in url:
                url = url.replace('/hds', '/hdss/ch')

                request_handler = RequestHandler(url)
                sHtmlContent1 = request_handler.request()
                sPattern2 = '<script>fid="(.+?)"'
                results = re.findall(sPattern2, sHtmlContent1)

                if results:
                    url2 = 'http://wlive.tv/embedra.php?player=desktop&live=' + \
                        results[0] + '&vw=700&vh=440'
                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = request_handler.request()

            if sHtmlContent3:
                m = re.search(
                    'return.*?\\[(.*?)\\].*?\\+\\s+(.*)\\.join.*document.*?"(.*?)"',
                    sHtmlContent3)
                if m:
                    timeVar = m.group(2)
                    hashVar = m.group(3)

                    # http://tv.wlive.tv/tv/lu2mIWw6KZ20180321/playlist.m3u8?hlsendtime=1542297480&hlsstarttime=0&hlshash=jhTrgemr-kGm9E01YIVfqkZ9VPobibqbDRiov2psf_A=
                    url3 = ''.join(m.group(1).split(','))
                    url3 = url3.replace('"', '').replace('\\/', '/')
                    if not url3.startswith('http'):
                        url3 = 'http:' + url3

                    m = re.search(timeVar + '.*?\\[(.*?)\\]', sHtmlContent3)
                    if m:
                        timeStr = ''.join(
                            m.group(1).split(',')).replace(
                            '"', '')
                        url3 += timeStr

                    m = re.search(hashVar + '>(.*?)<', sHtmlContent3)
                    if m:
                        hashStr = ''.join(
                            m.group(1).split(',')).replace(
                            '"', '')
                        url3 += hashStr
                        hoster_url = url3
                        if Referer:
                            hoster_url += '|referer=' + Referer

        if 'sports-stream.net' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                fid = results[0]
                url2 = 'http://webtv.ws/embeds.php?live=spstream' + fid + '&vw=700&vh=440'
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Referer', 'http://www.sports-stream.net/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = request_handler.request()

                sPattern3 = 'source src="(.+?)".+?">'
                results = re.findall(sPattern3, sHtmlContent2)
                if results:
                    hoster_url = results[0]

        if 'sports-stream.link' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                fid = results[0]
                url2 = 'https://www.airhdx.com/embedd.php?live=spstream' + fid + '&vw=700&vh=440'
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Referer', 'http://www.sports-stream.link/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = request_handler.request()

                sPattern3 = 'source: "(.+?)",'
                results = re.findall(sPattern3, sHtmlContent2)
                if results:
                    hoster_url = results[0] + '|referer=' + url2

        if 'foot.futbol' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = results[0]
                Referer = sHosterUrl2
                request_handler = RequestHandler(sHosterUrl2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = request_handler.request()
                sPattern3 = '<source src="([^"]+)"'
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    hoster_url = aResult2[0]

        if 'viewhd.me' in url:  # Pas terminer je sais pas comment on trouve le m3u dans hdstream
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<script>fid="([^"]+)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = 'http://www.hdstream.live/embed.php?player=desktop&live=' + \
                    results[0] + '&vw=620&vh=490'
                Referer = sHosterUrl2
                request_handler = RequestHandler(sHosterUrl2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = request_handler.request()

        if 'socolive.pro' in url:  # OK
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'channel=\'(.+?)\', g=\'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                for entry in results:
                    channel = entry[0]
                    g = entry[1]

            url2 = 'https://web.uctnew.com/hembedplayer/' + channel + '/' + g + '/700/480'
            request_handler = RequestHandler(url2)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry(
                'Referer', 'http://new.socolive.pro/')
            sHtmlContent2 = request_handler.request()

            sPatternUrl = 'hlsUrl = "https:\\/\\/" \\+ ea \\+ "([^"]+)"'
            sPatternPK = 'var pk = "([^"]+)"'
            sPatternEA = 'ea = "([^"]+)";'
            aResultUrl = re.findall(sPatternUrl, sHtmlContent2)
            aResultEA = re.findall(sPatternEA, sHtmlContent2)
            aResultPK = re.findall(sPatternPK, sHtmlContent2)
            if aResultUrl and aResultPK and aResultEA:
                # une lettre s'est glissé dans le code :D
                aResultPK = aResultPK[0][:53] + aResultPK[0][54:]
                url3 = aResultEA[0] + aResultUrl[0] + aResultPK
                hoster_url = 'https://' + url3

        if 'socolive.xyz' in url or 'sportsfix' in url or 'bartsim' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'iframe src="(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                url2 = results[0]
                if not url.startswith('http'):
                    url2 = "http:" + url2
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                sHtmlContent2 = request_handler.request()

                sPattern2 = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
                results = re.findall(sPattern2, sHtmlContent2)

                if results:
                    str2 = results[0]
                    if not str2.endswith(';'):
                        str2 = str2 + ';'

                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        hoster_url = aResult1[0] + \
                            '|User-Agent=' + UA + '&referer=' + url2
                    else:
                        sPattern3 = 'src="([^"]+)"'
                        aResult1 = re.findall(sPattern3, strs)
                        if aResult1:
                            hoster_url = aResult1[0] + \
                                '|User-Agent=' + UA + '&referer=' + url2

        if '1me.club' in url or 'sportz' in url or 'streamhd' in url or 'hdsportslive' in url or 'cricfree' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()

            if 'hdsportslive' in url or 'cricfree' in url:
                sPattern2 = 'document.write\\(unescape\\(\'(.+?)\'\\)\\)'
                results = re.findall(sPattern2, sHtmlContent2)
                unQuote = Unquote(results[0])

                sPattern2 = '<iframe.+?src="(.+?)"'
                results = re.findall(sPattern2, unQuote)

                url = results[0]
                if not url.startswith('http'):
                    url = 'https:' + url

                request_handler = RequestHandler(url)
                sHtmlContent2 = request_handler.request()

                sPattern2 = '<iframe.+?src=\'(.+?)\''
                results = re.findall(sPattern2, sHtmlContent2)

            else:
                sPattern2 = '<iframe src="(.+?)"'
                results = re.findall(sPattern2, sHtmlContent2)

            if results:

                if 'wstream.to' in results[0] or 'streamcdn' in results[0]:  # Terminé
                    embedUrl = results[0]

                    if embedUrl.startswith('//'):
                        embedUrl = 'https:' + embedUrl

                    if 'sportz' in url or 'hdsportslive' in url or 'cricfree' in url:
                        Referer = url
                    else:
                        Referer = 'http://1me.club'

                    request_handler = RequestHandler(embedUrl)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry('Referer', Referer)
                    sHtmlContent3 = request_handler.request()

                    sPattern2 = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
                    results = re.findall(sPattern2, sHtmlContent3)

                    if results:
                        str2 = results[0]
                        if not str2.endswith(';'):
                            str2 = str2 + ';'

                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        hoster_url = aResult1[0]

                if 'widestream.io' in results[0]:  # Terminé
                    request_handler = RequestHandler(results[0])
                    sHtmlContent3 = request_handler.request()
                    sPattern3 = 'file:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, sHtmlContent3)
                    if aResult1:
                        hoster_url = aResult1[0]

        if ('shd' in url) or ('hd' in url and 'streamhd' not in url and 'hdsportslive' not in url and 'airhdx'
                              not in url and 'wizhd' not in url):

            urlApi = 'https://api.livesports24.online/gethost'
            sHtmlContent2 = ''
            channel = url.split('/')[4]
            try:
                request_handler = RequestHandler(urlApi)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                request_handler.addHeaderEntry(
                    'Origin', 'https://' + url.split('/')[2])
                sHtmlContent2 = request_handler.request()
            except BaseException:
                pass
            if sHtmlContent2:

                sPattern1 = '([^"]+)'
                results = re.findall(sPattern1, sHtmlContent2)
                if results:
                    host = results[0]
            else:
                urlApi = 'https://api.livesports24.online:8443/gethost'
                channel = url.split('/')[4]
                request_handler = RequestHandler(urlApi)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                request_handler.addHeaderEntry(
                    'Origin', 'https://' + url.split('/')[2])
                sHtmlContent2 = request_handler.request()

                sPattern1 = '([^"]+)'
                results = re.findall(sPattern1, sHtmlContent2)
                if results:
                    host = results[0]

            hoster_url = 'https://' + host + '/' + channel + '.m3u8'

        if 'sportgol7' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern1 = '<source src="(.+?)"'
            results = re.findall(sPattern1, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'nowlive.pro' in url:
            request_handler = RequestHandler(url)
            sHtmlContent3 = request_handler.request()
            sPattern3 = 'src%3A%20%22//([^"]+)%3A([^"]+)m3u8'
            aResult1 = re.findall(sPattern3, sHtmlContent3)
            if aResult1:
                ip = aResult1[0][0]
                name = aResult1[0][1]
                hoster_url = 'http://' + ip + ':' + name + 'm3u8'

        if 'harleyquinn' in url or 'joker' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                fid = results[0][0]
                vw = results[0][1]
                vh = results[0][2]

                url2 = 'http://www.jokersplayer.xyz/embed.php?u=' + fid + '&vw=' + vw + '&vh=' + vh
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                sHtmlContent2 = request_handler.request()
                sPattern3 = 'src=http://(.+?)/(.+?) '
                results = re.findall(sPattern3, sHtmlContent2)
                if results:
                    ip = results[0][0]
                    url3 = 'http://' + ip + '/' + results[0][1]
                    request_handler = RequestHandler(url3)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry('Referer', url2)
                    request_handler.addHeaderEntry('Connection', 'keep-alive')
                    sHtmlContent2 = request_handler.request()
                    sPattern3 = 'src=.+?e=(.+?)&st=(.+?)&'
                    results = re.findall(sPattern3, sHtmlContent2)
                    if results:
                        e = results[0][0]
                        st = results[0][1]
                        hoster_url = 'http://' + ip + '/live/' + \
                            fid + '.m3u8' + '?e=' + e + '&st=' + st

                if hoster_url == '':
                    url2 = 'http://player.jokehd.com/one.php?u=' + fid + '&vw=' + vw + '&vh=' + vh
                    request_handler = RequestHandler(url2)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry('Referer', url)
                    sHtmlContent2 = request_handler.request()
                    sPattern3 = 'source: \'(.+?)\''
                    results = re.findall(sPattern3, sHtmlContent2)
                    if results:
                        hoster_url = results[0]

        if 'baltak.biz' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src="\\/blok.php\\?id=(.+?)"'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                url2 = results[0]
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Referer', 'http://baltak.biz/blok.php?id=' + url2)
                sHtmlContent2 = request_handler.request()

                sPattern2 = 'source: \'(.+?)\''
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    hoster_url = results[0]
            else:
                sPattern2 = 'source: \"(.+?)\"'
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    hoster_url = results[0]

        if 'footballstream' in url:  # Terminé
            url = url.replace('/streams', '/hdstreams')
            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                fid = results[0][0]
                vw = results[0][1]
                vh = results[0][2]

                embedded = "mobile"  # "desktop"

                url2 = 'http://www.b4ucast.me/embedra.php?player=' + \
                    embedded + '&live=' + fid + '&vw=' + vw + '&vh=' + vh
                request_handler = RequestHandler(url2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                sHtmlContent2 = request_handler.request()

                sPattern3 = 'source: *["\'](.+?)["\']'
                results = re.findall(sPattern3, sHtmlContent2)
                if results:
                    hoster_url = 'http:' + results[0]

        if 'tennistvgroup' in url:  # Terminé
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()

            sPattern2 = 'source: *["\'](.+?)["\']'
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'box-live.stream' in url:  # Terminé
            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry('Referer', sUrl4)

            sHtmlContent2 = request_handler.request()
            sPattern2 = 'source: \'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                hoster_url = results[0] + \
                    '|User-Agent=' + UA + '&referer=' + url
            else:
                sPattern2 = 'var source = \"(.+?)\"'
                results = re.findall(sPattern2, sHtmlContent2)
                if results:
                    hoster_url = results[0]
                else:
                    sPattern2 = '<iframe.+?src="(http.+?)".+?</iframe>'
                    results = re.findall(sPattern2, sHtmlContent2)
                    if results:
                        Referer = url
                        url = results[0]  # decryptage plus bas (telerium)

        if 'telerium.tv' in url:  # WIP
            request_handler = RequestHandler(url)
            if Referer:
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '(\\s*eval\\s*\\(\\s*function(?:.|\\s)+?{}\\)\\))'
            results = re.findall(sPattern2, sHtmlContent2)

            if results:
                str2 = results[0]
                if not str2.endswith(';'):
                    str2 = str2 + ';'

                strs = cPacker().unpack(str2)

                sPattern3 = '{url:window\\.atob\\((.+?)\\)\\.slice.+?\\+window\\.atob\\((.+?)\\)'
                aResult1 = re.findall(sPattern3, strs)
                if aResult1:
                    m3u = aResult1[0][0]
                    sPatternM3u = m3u + '="(.+?)"'
                    m3u = re.findall(sPatternM3u, strs)
                    m3u = base64.b64decode(m3u[0])[14:]

                    token = aResult1[0][1]
                    sPatterntoken = token + '="(.+?)"'
                    token = re.findall(sPatterntoken, strs)
                    token = base64.b64decode(token[0])

                    hoster_url = 'https://telerium.tv/' + m3u + token + '|referer=' + url

        # TODO A TESTER
        if 'usasports.live' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern1 = 'var sou = "  (.+?)"'
            results = re.findall(sPattern1, sHtmlContent2)
            if results:
                hoster_url = results[0]

        # TODO A TESTER
        if 'wiz1' in url:
            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern1 = '"iframe" src="(.+?)"'
            results = re.findall(sPattern1, sHtmlContent2)
            if results:
                hoster_url = results[0]

        if 'var16.ru' in url:
            hoster_url = getHosterVar16(url, url)

        # TODO A TESTER
        if 'livesportone' in url:
            url = url.replace('livesportone.com', 'sportes.pw')

            request_handler = RequestHandler(url)
            sHtmlContent2 = request_handler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            results = re.findall(sPattern2, sHtmlContent2)
            if results:
                sHosterUrl2 = results[0] + \
                    '|User-Agent=' + UA + '&referer=' + url
                request_handler = RequestHandler(sHosterUrl2)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry('Referer', url)
                sHtmlContent3 = request_handler.request()
                sPattern3 = 'source: "([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    hoster_url = aResult1[0] + \
                        '|User-Agent=' + UA + '&referer=' + url

        # Tentative avec les pattern les plus répendus
        if not hoster_url:
            hoster_url = getHosterIframe(url, url)

        if hoster_url:
            if hoster_url.startswith('//'):
                hoster_url = 'http:' + hoster_url

            hoster = HosterGui().checkHoster(".m3u8")
            if hoster:
                hoster.setDisplayName(sMovieTitle2)  # nom affiche
                hoster.setFileName(sMovieTitle2)  # idem
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

        gui.setEndOfDirectory()


def getHosterVar16(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = request_handler.request()

    pattern = 'file:\"([^"]+)\"'
    results = re.findall(pattern, html_content)
    if results:
        return results[0] + '|referer=' + url

    pattern = 'src=\"(.+?)\"'
    results = re.findall(pattern, html_content)
    if results:
        referer = url
        url = 'http://var16.ru/' + results[0]
        return getHosterVar16(url, referer)


# Traitement générique
def getHosterIframe(url, referer):
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Referer', referer)
    html_content = str(request_handler.request())
    if not html_content:
        return False

    referer = url

    # import xbmcvfs
    # f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
    # f.write(html_content)
    # f.close()

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
#            return code + '|User-Agent=' + UA + '&Referer=' + Quote(referer)
            return code + '|Referer=' + referer
        except Exception as e:
            pass

    pattern = '<iframe.+?src=["\']([^"\']+)["\']'
    results = re.findall(pattern, html_content)
    if results:
        for url in results:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    # ajout du nom de domaine
                    url = '//' + referer.split('/')[2] + url
                url = "https:" + url
            url = getHosterIframe(url, referer)
            if url:
                return url

    pattern = ';var.+?src=["\']([^"\']+)["\']'
    results = re.findall(pattern, html_content)
    if results:
        url = results[0]
        if '.m3u8' in url:
            return url

    pattern = '[^/]source.+?["\'](https.+?)["\']'
    results = re.findall(pattern, html_content)
    if results:
        return results[0] + '|referer=' + referer

    return False
