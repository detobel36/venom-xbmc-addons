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
    sUrl = 'http://www.worldtimeserver.com/current_time_in_CA-ON.aspx'
    oRequestHandler = RequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sPattern = '<span id="theTime" class="fontTS">\\s*(.+?)\\s*</span>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    timeError = ''
    return timeError


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
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/nba-replays/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'NBA Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showFinals',
        'NBA Finals Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/all-star-weekend/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'NBA All Star Weekend Replay',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenres',
        'NBA Replay (Par États/Équipes)',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', REDDIT)
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Live NBA Games (bêta)',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showFinals():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl',
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
        'siteUrl', URL_MAIN + 'category/2016-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2016 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2015-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2015 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2014-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2014 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2011-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2011 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2010-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2010 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2009-nba-finals/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Replay NBA 2009 PlayOffs',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'siteUrl', URL_MAIN + 'category/2008-nba-finals/')
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

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'reddit' in sUrl:
        TimeUTC = TimeET()
        sPattern = 'utm_name=nbastreams".+?>Game Thread:(.+?)</a>.+?<ul class=".+?"><li class=".+?"><a href="(.+?)"'
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

    elif 'category/20' in sUrl:
        sPattern = '<a href="([^"]+)">([^<]+)</a></h2>'
    elif sSearch:
        sPattern = '<div class="col-sm-4 col-xs-6 item responsive-height">\\s*<a title="([^"]+)" href="([^"]+)".+?src="([^"]+)"'
    else:
        sPattern = '<div id="post-.+?<a href="([^"]+)"><img.+?src="([^"]+)".+?<h.+?>([^"]+)–([^"]+)</a>'

    sDateReplay = ''
    sDate = ''

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])

        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # listage game thread via reddit
            if 'reddit' in sUrl:
                try:
                    sUrl2 = aEntry[1]
                    title = aEntry[0]
                    sThumb = base64.b64decode(Logo_Reddit)
                    sTitle2 = title.split('(')
                    title = sTitle2[0]
                    sTimeLive = sTitle2[1]
                    sTimeLive = sTimeLive.replace(')', '')
                    title = '[COLOR teal]' + sTimeLive + '[/COLOR]' + title

                finally:
                    # erreur parse
                    sThumb = ' '
                    title = 'Erreur parse'
                    sUrl2 = ''

            # listage replay&search
            else:

                if 'category/20' in sUrl:

                    sUrl2 = aEntry[0]
                    title = aEntry[1]
                    sThumb = ' '
                elif '?s=' in sUrl:
                    title = aEntry[0]
                    sUrl2 = aEntry[1]
                    sThumb = aEntry[2]
                else:
                    sUrl2 = aEntry[0]
                    sThumb = aEntry[1]
                    title = aEntry[2]

            try:
                if 'category/nba' in sUrl:

                    sTitle2 = title.split(' – ')
                    title = sTitle2[0]
                    sDateReplay = sTitle2[1]

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
                if ('category/20' in sUrl) or ('?s=' in sUrl) or ('search/' in sUrl):

                    if 'Game' in title:
                        sTitle2 = title.split(":")
                        sGame = sTitle2[0] + ':'
                        sTitle3 = sTitle2[1]
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
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sDateReplay', sDateReplay)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters4',
                title,
                '',
                sThumb,
                sUrl2,
                output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    else:
        if 'reddit' in sUrl:
            gui.addText(
                SITE_IDENTIFIER,
                '(Aucun Match disponible via Reddit pour le moment)')
        else:
            gui.addText(SITE_IDENTIFIER, '(Erreur - Replay non disponible)')

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, sUrl):
    oParser = Parser()
    if '?s=' in sUrl:
        sPattern = '<span class=\'current\'>.+?</span><a href=\'(.+?)\''
    else:
        sPattern = '<a href="([^"]+)"> <li class="next">Newer.+?</ul>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]
    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sDateReplay = input_parameter_handler.getValue('sDateReplay')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(' rel="nofollow"', '')

    if sDateReplay:
        sMovieTitle = sMovieTitle + \
            '[COLOR teal]' + ' / ' + sDateReplay + '[/COLOR]'

    sLink = []

    if 'reddit' in sUrl:  # Live

        sPattern = '(?:<td>|)<a href="(http.+?(?:nbastreams|eplstream|yoursportsinhd|247hd).+?)">(?:<strong>.+?</strong>|)([^<]+)</a>(?:.+?Chrome.+?|)</td>'

        sLink = re.findall(sPattern, sHtmlContent)

        sDisplay = '[COLOR olive]Streaming disponibles:[/COLOR]'

    else:  # Replay

        sPattern = '<a href="(https?://(?:wstream|youwa|openlo)[^"]+)" target="_blank">(?:([^<]+)</a>|)'
        sPattern2 = '(?:data\\-lazy\\-src|src)="(http.+?(?:openload|raptu)\\.co[^"]+)"'

        aResult1 = re.findall(sPattern, sHtmlContent)
        aResult2 = re.findall(sPattern2, sHtmlContent)
        sLink = aResult1 + aResult2

        # Test si lien video non embed (raptu/openload)
        sPattern3 = 'document.getElementById\\(\'frame\'\\).src=\'([^"]+)\'">(.+?)<span'
        aResult3 = re.findall(sPattern3, sHtmlContent)

        # recup lien video non embed
        if (aResult3):

            for aEntry in aResult3:

                sUrl = str(aEntry)

                oRequestHandler = RequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request()
                sHtmlContent = sHtmlContent.replace(' rel="nofollow"', '')

                aResult4 = re.findall(sPattern2, sHtmlContent)
                sLink = sLink + aResult4

        sDisplay = '[COLOR olive]Qualités disponibles:[/COLOR]'

    gui.addText(SITE_IDENTIFIER, sMovieTitle)
    gui.addText(SITE_IDENTIFIER, sDisplay)

    # affichage final des liens
    if (sLink):

        for aEntry in sLink:

            if 'reddit' in sUrl:  # Live

                sThumb = base64.b64decode(Logo_Nba)
                sHosterUrl = aEntry[0].replace('&amp;', '&')

                if 'yoursport' in aEntry[0]:
                    title = ('[%s] %s') % ('YourSportsinHD', aEntry[1])
                elif 'nbastream' in aEntry[0]:
                    title = ('[%s] %s') % ('NBAstreamspw', aEntry[1])
                elif 'eplstream' in aEntry[0]:
                    title = ('[%s] %s') % ('EPLstreams', aEntry[1])
                elif '247hd' in aEntry[0]:
                    title = ('[%s] %s') % ('247HD', aEntry[1])

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sHosterUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)

                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLiveHosters',
                    title,
                    '',
                    sThumb,
                    sHosterUrl,
                    output_parameter_handler)

            else:  # Replay

                if aEntry[0]:
                    sHosterUrl = aEntry[0]

                if 'openload' in aEntry:
                    title = ('[%s]') % ('720p')
                    sHosterUrl = str(aEntry)

                elif 'raptu' in aEntry:
                    title = ('[%s]') % ('720p')
                    sHosterUrl = str(aEntry)

                elif 'youwatch' in aEntry[0]:
                    title = ('[%s]') % ('540p')

                elif 'wstream' in aEntry[0]:
                    title = ('[%s]') % ('720p')

                else:
                    title = ('[%s]') % (aEntry[1])

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(title)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    else:
        gui.addText(SITE_IDENTIFIER, '(Live/Replay non disponible)')

    gui.setEndOfDirectory()


# Live 24/24 chaine nbatv
def showLiveNbatv():
    gui = Gui()

    sThumb = base64.b64decode(Logo_Nba)
    sUrl = [
        ('aHR0cDovL3d3dy4yNDdoZC5wdy9uYmEucGhwP2V4dGlkPTEmdmlldz1OQkFUVg=='),
        ('aHR0cDovL3lzaWhkLm1lL25iYXR2Lw==')]

    for aEntry in sUrl:

        sUrl = base64.b64decode(aEntry)
        if '247hd' in sUrl:
            title = ('[%s] %s') % ('247HD', 'NBA TV')
        else:
            title = ('[%s] %s') % ('YourSportsinHD', 'NBA TV')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', title)
        output_parameter_handler.addParameter('sThumb', sThumb)

        gui.addMovie(SITE_IDENTIFIER, 'showLiveHosters', title,
                     '', sThumb, sUrl, output_parameter_handler)

    gui.setEndOfDirectory()


# recuperation lecture m3u8 nba livestream - ok sauf si geoIP (USA) ou
# lien secu ou regex a maj
def showLiveHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

    try:
        request = urllib2.Request(sUrl)
        request.add_header('User-agent', UA)
        response = urllib2.urlopen(request)
        sHtmlContent = response.read()
        response.close()
    except urllib2.HTTPError:
        sHtmlContent = ''
        pass

    sPattern = '(?:\"|\')(.+?m3u8.+?)(?:\"|\')'
    aResult = re.findall(sPattern, sHtmlContent)

    if (aResult):
        for aEntry in aResult:

            # si streamer utilise chrome extension
            if '#http' in aEntry:
                sUrl2 = aEntry.split('#')
                sHosterUrl = sUrl2[1]
            else:
                sHosterUrl = aEntry

            # live ok avec UA ipad sauf si geoIP usa
            sHosterUrl = sHosterUrl + \
                '|User-Agent=Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.1'

            oHoster = HosterGui().checkHoster('.m3u8')
            oHoster.setDisplayName(title)
            oHoster.setFileName(title)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    else:
        gui.addText(
            SITE_IDENTIFIER,
            '(Erreur connection ou stream non disponible : UA pas bon/Lien protégé/code soluce à trouver)')

    gui.setEndOfDirectory()


def showHosters4():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'onClick=.+?src=\'([^"]+)\''
    sPattern2 = '<iframe src="([^"]+)".+?</iframe></p>'

    aResult1 = re.findall(sPattern, sHtmlContent)
    aResult2 = re.findall(sPattern2, sHtmlContent)
    aResult = aResult1 + aResult2

    if aResult:
        for aEntry in aResult:
            sHosterUrl = aEntry
            if not sHosterUrl.startswith('http'):
                sHosterUrl = 'http:' + sHosterUrl

            if 'fembed' in sHosterUrl:
                videoID = re.findall('v/([^"]+)', sHosterUrl)
                oRequestHandler = RequestHandler(sUrl)
                oRequestHandler.request()
                cookies = oRequestHandler.GetCookies()

                apiUrl = 'https://www.fembed.com/api/source/' + videoID[0]
                oRequestHandler = RequestHandler(apiUrl)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry(
                    'User-Agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
                oRequestHandler.addHeaderEntry('Referer', sHosterUrl)
                oRequestHandler.addHeaderEntry('Cookie', cookies)
                oRequestHandler.addParameters('r', '')
                oRequestHandler.addParameters('d', 'www.fembed.com')
                sHtmlContent = oRequestHandler.request()

                aResult = re.findall('"file":"(.+?)"', sHtmlContent)
                if (aResult):
                    sHosterUrl = aEntry.replace('\\/', '\\')
                    if not sHosterUrl.startswith('http'):
                        sHosterUrl = 'https://www.fembed.com' + sHosterUrl

                    oHoster = HosterGui().checkHoster(sHosterUrl)
                    if (oHoster):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)

            else:
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)

    gui.setEndOfDirectory()
