# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Progress
import urllib2
import re
import base64
return false  # désactivé le 29/08/2020


# from resources.lib.config import GestionCookie
# tester le 30/10 ne fonctionne pas

SITE_IDENTIFIER = 'tvrex_net'
SITE_NAME = 'Tvrex'
SITE_DESC = 'NBA Live/Replay'

URL_MAIN = 'http://tvrex.net/'
REDDIT = 'https://www.reddit.com/r/nbastreams/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SPORT_SPORTS = ('http://', 'load')

Logo_Reddit = 'aHR0cHM6Ly9iLnRodW1icy5yZWRkaXRtZWRpYS5jb20va1c5ZFNqRFlzUDhGbEJYeUUyemJaaEFCaXM5eS0zVHViSWtic0JfUDlBay5wbmc='
Logo_Nba = 'aHR0cDovL3d3dy5vZmZpY2lhbHBzZHMuY29tL2ltYWdlcy90aHVtYnMvSS1sb3ZlLXRoaXMtZ2FtZS1uYmEtbG9nby1wc2Q2MDQwNy5wbmc='


def TimeET():
    url = 'http://www.worldtimeserver.com/current_time_in_CA-ON.aspx'
    request_handler = RequestHandler(url)

    html_content = request_handler.request()
    pattern = '<span id="theTime" class="fontTS">\\s*(.+?)\\s*</span>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    timeError = ''
    return timeError


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
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/nba-replays/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'NBA Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showFinals',
        'NBA Finals Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/all-star-weekend/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'NBA All Star Weekend Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenres',
        'NBA Replay (Par États/Équipes)',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', REDDIT)
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Live NBA Games (bêta)',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showFinals():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url',
        URL_MAIN +
        'category/2017-nba-playoffs/2017-nba-finals-nba-finals-2/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2017 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2016-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2016 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2015-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2015 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2014-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2014 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2011-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2011 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2010-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2010 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2009-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2009 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/2008-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2008 PlayOffs',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    liste = []
    liste.append(['Atlanta (Hawks)', URL_MAIN + 'category/nba/atlanta-hawks/'])
    liste.append(['Boston (Celtics)', URL_MAIN +
                 'category/nba/boston-celtics/'])
    liste.append(['Brooklyn (Nets)', URL_MAIN + 'category/nba/brooklyn-nets/'])
    liste.append(['Charlotte (Hornets)', URL_MAIN +
                 'category/nba/charlotte-hornets/'])
    liste.append(['Chicago (Bulls)', URL_MAIN + 'category/nba/chicago-bulls/'])
    liste.append(['Cleveland (Cavaliers)', URL_MAIN +
                 'category/nba/cleveland-cavaliers/'])
    liste.append(['Dallas (Mavericks)', URL_MAIN +
                 'category/nba/dallas-mavericks/'])
    liste.append(['Denver (Nuggets)', URL_MAIN +
                 'category/nba/denver-nuggets/'])
    liste.append(['Détroit (Pistons)', URL_MAIN +
                 'category/nba/detroit-pistons/'])
    liste.append(['Golden-state (Warriors)', URL_MAIN +
                 'category/nba/golden-state-warriors/'])
    liste.append(['Houston (Rockets)', URL_MAIN +
                 'category/nba/houston-rockets/'])
    liste.append(['Indiana (Pacers)', URL_MAIN +
                 'category/nba/indiana-pacers/'])
    liste.append(['Los Angeles (Clippers)', URL_MAIN +
                 'category/nba/los-angeles-clippers/'])
    liste.append(['Los Angeles (Lakers)', URL_MAIN +
                 'category/nba/los-angeles-lakers/'])
    liste.append(['Memphis (Grizzlies)', URL_MAIN +
                 'category/nba/memphis-grizzlies/'])
    liste.append(['Miami (Heat)', URL_MAIN + 'category/nba/miami-heat/'])
    liste.append(['Milwaukee (Bucks)', URL_MAIN +
                 'category/nba/milwaukee-bucks/'])
    liste.append(['Minnesota (Timberwolves)', URL_MAIN +
                 'category/nba/minnesota-timberwolves/'])
    liste.append(['New-Orléans (Pelicans)', URL_MAIN +
                 'category/nba/new-orleans-pelicans/'])
    liste.append(['New-York (Knicks)', URL_MAIN +
                 'category/nba/new-york-knicks/'])
    liste.append(['Oklahoma City (Thunder)', URL_MAIN +
                 'category/nba/oklahoma-city-thunder/'])
    liste.append(['Orlando (Magic)', URL_MAIN + 'category/nba/orlando-magic/'])
    liste.append(['Philadelphia (79ers)', URL_MAIN +
                 'category/nba/philadelphia-76ers/'])
    liste.append(['Phoenix (Suns)', URL_MAIN + 'category/nba/phoenix-suns/'])
    liste.append(['Portland (Blazers)', URL_MAIN +
                  'category/nba/portland-trail-blazers/'])
    liste.append(['Sacramento (Kings)', URL_MAIN +
                 'category/nba/sacramento-kings/'])
    liste.append(['San Antonio (Spurs)', URL_MAIN +
                 'category/nba/san-antonio-spurs/'])
    liste.append(['Toronto (Raptors)', URL_MAIN +
                 'category/nba/toronto-raptors/'])
    liste.append(['Utah (Jazz)', URL_MAIN + 'category/nba/utah-jazz/'])
    liste.append(['Washington (Wizards)', URL_MAIN +
                 'category/nba/washington-wizards/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        url = search

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if 'reddit' in url:
        TimeUTC = TimeET()
        pattern = 'utm_name=nbastreams".+?>Game Thread:(.+?)</a>.+?<ul class=".+?"><li class=".+?"><a href="(.+?)"'
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Live NBA Game (@Reddit)[/COLOR]' +
            '[COLOR gray]' +
            ' [ Heure Locale ET : ' +
            '[/COLOR]' +
            TimeUTC +
            '[COLOR gray]' +
            ']' +
            '[/COLOR]')

    elif 'category/20' in url:
        pattern = '<a href="([^"]+)">([^<]+)</a></h2>'
    elif search:
        pattern = '<div class="col-sm-4 col-xs-6 item responsive-height">\\s*<a title="([^"]+)" href="([^"]+)".+?src="([^"]+)"'
    else:
        pattern = '<div id="post-.+?<a href="([^"]+)"><img.+?src="([^"]+)".+?<h.+?>([^"]+)–([^"]+)</a>'

    sDateReplay = ''
    sDate = ''

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])

        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # listage game thread via reddit
            if 'reddit' in url:
                try:
                    url2 = entry[1]
                    title = entry[0]
                    thumb = base64.b64decode(Logo_Reddit)
                    title2 = title.split('(')
                    title = title2[0]
                    sTimeLive = title2[1]
                    sTimeLive = sTimeLive.replace(')', '')
                    title = '[COLOR teal]' + sTimeLive + '[/COLOR]' + title

                finally:
                    # erreur parse
                    thumb = ' '
                    title = 'Erreur parse'
                    url2 = ''

            # listage replay&search
            else:

                if 'category/20' in url:

                    url2 = entry[0]
                    title = entry[1]
                    thumb = ' '
                elif '?s=' in url:
                    title = entry[0]
                    url2 = entry[1]
                    thumb = entry[2]
                else:
                    url2 = entry[0]
                    thumb = entry[1]
                    title = entry[2]

            try:
                if 'category/nba' in url:

                    title2 = title.split(' – ')
                    title = title2[0]
                    sDateReplay = title2[1]

                    if (sDate != sDateReplay):
                        gui.addText(
                            SITE_IDENTIFIER,
                            '[COLOR olive]Replay[/COLOR]' +
                            '[COLOR teal]' +
                            ' / ' +
                            sDateReplay +
                            '[/COLOR]')
                        sDate = sDateReplay

            finally:
                pass

            try:
                if ('category/20' in url) or ('?s=' in url) or ('search/' in url):

                    if 'Game' in title:
                        title2 = title.split(":")
                        sGame = title2[0] + ':'
                        sTitle3 = title2[1]
                    else:
                        sGame = 'Game: '
                        sTitle3 = title

                    sTitle3 = sTitle3.replace('\xe2\x80\x93', '-')
                    title = sTitle3.split('-')
                    sTeam = title[0]
                    if title[1]:
                        sDatePlayoff = title[1]
                    else:
                        sDatePlayoff = ''

                    title = '[COLOR olive]' + sGame + '[/COLOR]' + sTeam + \
                        '[COLOR teal]' + '/' + sDatePlayoff + '[/COLOR]'

            finally:
                pass

            try:
                title = title.replace(' vs ',
                                      '[COLOR gray] vs [/COLOR]').replace('@',
                                                                          '[COLOR gray] vs [/COLOR]')
            except AttributeError:
                title = ''.join(title)
                title = title.replace(' vs ',
                                      '[COLOR gray] vs [/COLOR]').replace('@',
                                                                          '[COLOR gray] vs [/COLOR]')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('sDateReplay', sDateReplay)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters4',
                title,
                '',
                thumb,
                url2,
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content, url)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    else:
        if 'reddit' in url:
            gui.addText(
                SITE_IDENTIFIER,
                '(Aucun Match disponible via Reddit pour le moment)')
        else:
            gui.addText(SITE_IDENTIFIER, '(Erreur - Replay non disponible)')

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content, url):
    parser = Parser()
    if '?s=' in url:
        pattern = '<span class=\'current\'>.+?</span><a href=\'(.+?)\''
    else:
        pattern = '<a href="([^"]+)"> <li class="next">Newer.+?</ul>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]
    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sDateReplay = input_parameter_handler.getValue('sDateReplay')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(' rel="nofollow"', '')

    if sDateReplay:
        movie_title = movie_title + \
            '[COLOR teal]' + ' / ' + sDateReplay + '[/COLOR]'

    sLink = []

    if 'reddit' in url:  # Live

        pattern = '(?:<td>|)<a href="(http.+?(?:nbastreams|eplstream|yoursportsinhd|247hd).+?)">(?:<strong>.+?</strong>|)([^<]+)</a>(?:.+?Chrome.+?|)</td>'

        sLink = re.findall(pattern, html_content)

        sDisplay = '[COLOR olive]Streaming disponibles:[/COLOR]'

    else:  # Replay

        pattern = '<a href="(https?://(?:wstream|youwa|openlo)[^"]+)" target="_blank">(?:([^<]+)</a>|)'
        sPattern2 = '(?:data\\-lazy\\-src|src)="(http.+?(?:openload|raptu)\\.co[^"]+)"'

        aResult1 = re.findall(pattern, html_content)
        aResult2 = re.findall(sPattern2, html_content)
        sLink = aResult1 + aResult2

        # Test si lien video non embed (raptu/openload)
        sPattern3 = 'document.getElementById\\(\'frame\'\\).src=\'([^"]+)\'">(.+?)<span'
        aResult3 = re.findall(sPattern3, html_content)

        # recup lien video non embed
        if (aResult3):

            for entry in aResult3:

                url = str(entry)

                request_handler = RequestHandler(url)
                html_content = request_handler.request()
                html_content = html_content.replace(' rel="nofollow"', '')

                aResult4 = re.findall(sPattern2, html_content)
                sLink = sLink + aResult4

        sDisplay = '[COLOR olive]Qualités disponibles:[/COLOR]'

    gui.addText(SITE_IDENTIFIER, movie_title)
    gui.addText(SITE_IDENTIFIER, sDisplay)

    # affichage final des liens
    if (sLink):

        for entry in sLink:

            if 'reddit' in url:  # Live

                thumb = base64.b64decode(Logo_Nba)
                hoster_url = entry[0].replace('&amp;', '&')

                if 'yoursport' in entry[0]:
                    title = ('[%s] %s') % ('YourSportsinHD', entry[1])
                elif 'nbastream' in entry[0]:
                    title = ('[%s] %s') % ('NBAstreamspw', entry[1])
                elif 'eplstream' in entry[0]:
                    title = ('[%s] %s') % ('EPLstreams', entry[1])
                elif '247hd' in entry[0]:
                    title = ('[%s] %s') % ('247HD', entry[1])

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', hoster_url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)

                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLiveHosters',
                    title,
                    '',
                    thumb,
                    hoster_url,
                    output_parameter_handler)

            else:  # Replay

                if entry[0]:
                    hoster_url = entry[0]

                if 'openload' in entry:
                    title = ('[%s]') % ('720p')
                    hoster_url = str(entry)

                elif 'raptu' in entry:
                    title = ('[%s]') % ('720p')
                    hoster_url = str(entry)

                elif 'youwatch' in entry[0]:
                    title = ('[%s]') % ('540p')

                elif 'wstream' in entry[0]:
                    title = ('[%s]') % ('720p')

                else:
                    title = ('[%s]') % (entry[1])

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    else:
        gui.addText(SITE_IDENTIFIER, '(Live/Replay non disponible)')

    gui.setEndOfDirectory()


# Live 24/24 chaine nbatv
def showLiveNbatv():
    gui = Gui()

    thumb = base64.b64decode(Logo_Nba)
    url = [
        ('aHR0cDovL3d3dy4yNDdoZC5wdy9uYmEucGhwP2V4dGlkPTEmdmlldz1OQkFUVg=='),
        ('aHR0cDovL3lzaWhkLm1lL25iYXR2Lw==')]

    for entry in url:

        url = base64.b64decode(entry)
        if '247hd' in url:
            title = ('[%s] %s') % ('247HD', 'NBA TV')
        else:
            title = ('[%s] %s') % ('YourSportsinHD', 'NBA TV')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('thumb', thumb)

        gui.addMovie(SITE_IDENTIFIER, 'showLiveHosters', title,
                     '', thumb, url, output_parameter_handler)

    gui.setEndOfDirectory()


# recuperation lecture m3u8 nba livestream - ok sauf si geoIP (USA) ou
# lien secu ou regex a maj
def showLiveHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

    try:
        request = urllib2.Request(url)
        request.add_header('User-agent', UA)
        response = urllib2.urlopen(request)
        html_content = response.read()
        response.close()
    except urllib2.HTTPError:
        html_content = ''
        pass

    pattern = '(?:\"|\')(.+?m3u8.+?)(?:\"|\')'
    results = re.findall(pattern, html_content)

    if (results):
        for entry in results:

            # si streamer utilise chrome extension
            if '#http' in entry:
                url2 = entry.split('#')
                hoster_url = url2[1]
            else:
                hoster_url = entry

            # live ok avec UA ipad sauf si geoIP usa
            hoster_url = hoster_url + \
                '|User-Agent=Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.1'

            hoster = HosterGui().checkHoster('.m3u8')
            hoster.setDisplayName(title)
            hoster.setFileName(title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    else:
        gui.addText(
            SITE_IDENTIFIER,
            '(Erreur connection ou stream non disponible : UA pas bon/Lien protégé/code soluce à trouver)')

    gui.setEndOfDirectory()


def showHosters4():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'onClick=.+?src=\'([^"]+)\''
    sPattern2 = '<iframe src="([^"]+)".+?</iframe></p>'

    aResult1 = re.findall(pattern, html_content)
    aResult2 = re.findall(sPattern2, html_content)
    results = aResult1 + aResult2

    if results:
        for entry in results:
            hoster_url = entry
            if not hoster_url.startswith('http'):
                hoster_url = 'http:' + hoster_url

            if 'fembed' in hoster_url:
                videoID = re.findall('v/([^"]+)', hoster_url)
                request_handler = RequestHandler(url)
                request_handler.request()
                cookies = request_handler.GetCookies()

                apiUrl = 'https://www.fembed.com/api/source/' + videoID[0]
                request_handler = RequestHandler(apiUrl)
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry(
                    'User-Agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
                request_handler.addHeaderEntry('Referer', hoster_url)
                request_handler.addHeaderEntry('Cookie', cookies)
                request_handler.addParameters('r', '')
                request_handler.addParameters('d', 'www.fembed.com')
                html_content = request_handler.request()

                results = re.findall('"file":"(.+?)"', html_content)
                if (results):
                    hoster_url = entry.replace('\\/', '\\')
                    if not hoster_url.startswith('http'):
                        hoster_url = 'https://www.fembed.com' + hoster_url

                    hoster = HosterGui().checkHoster(hoster_url)
                    if (hoster):
                        hoster.setDisplayName(movie_title)
                        hoster.setFileName(movie_title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

            else:
                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()
