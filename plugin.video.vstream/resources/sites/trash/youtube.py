# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress, addon, VSlog, dialog
from resources.lib.epg import cePg
from resources.lib.enregistrement import Enregistremement
from resources.lib.jsunfuck import unFuckFirst
from resources.lib.gui.hoster import HosterGui
from resources.lib.config import GestionCookie
from resources.lib.player import Player
from resources.lib.util import urlEncode, Unquote, Quote, QuotePlus
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.gui import Gui
import ssl
import re
import sys
import requests
import random
import json
import string
import xbmcplugin
import xbmcvfs
import xbmc

return False

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2


SITE_IDENTIFIER = 'youtube'
SITE_NAME = '[COLOR orange]Youtube[/COLOR]'
SITE_DESC = 'Youtube'

URL_MAIN = 'https://www.googleapis.com/youtube/v3/'
API_KEY = ''
URL_VIEW = 'https://youtube.com/watch?v=%s'

icon = 'tv.png'
# /home/lordvenom/.kodi/
# sRootArt = cConfig().getRootArt()

# https://developers.google.com/youtube/v3/guides/implementation/pagination

ADDON = addon()


class youtube:
    def __init__(self, ctype='videos', params=''):
        self.result = ''
        self.next = ''

        params = urlEncode(params)

        req = urllib2.Request(URL_MAIN + ctype + '?' + params)
        try:
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            response = urllib2.urlopen(req, context=gcontext)
        except BaseException:
            response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        sHtmlContent = sHtmlContent.decode('utf-8')
        self.result = json.loads(sHtmlContent)
        response.close()
        if self.result:
            self.load_result()
        return

    def load_result(self):
        if self.result.has_key('nextPageToken'):
            self.next = self.result.get('nextPageToken', [])

        videos, channels, playlists = [], [], []
        for search_result in self.result.get('items', []):
            if search_result['kind'] == 'youtube#video':
                videos.append(
                    {
                        'title': search_result['snippet']['title'],
                        'id': search_result['id'],
                        'channelId': search_result['snippet']['channelId'],
                        'channelTitle': search_result['snippet']['channelTitle'],
                        'thumbnails': search_result['snippet']['thumbnails']['high']['url'],
                        'description': search_result['snippet']['description']})
            elif search_result['kind'] == 'youtube#channel':
                channels.append(
                    {'title': search_result['snippet']['title'], 'id': search_result['id']})
            elif search_result['kind'] == 'youtube#playlist':
                playlists.append(
                    {'title': search_result['snippet']['title'], 'id': search_result['id']})

        self.videos = videos
        self.channels = channels
        self.playlists = playlists
        return

    def getVideos(self):
        return self.videos

    def getNext(self):
        return self.next

    def getChannels(self):
        return self.channels

    def getPlaylists(self):
        return self.playlists


def load():
    gui = Gui()
    addons = addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        addons.VSlang(30332),
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenres',
        'Catégorie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        'radio',
        'showAZ',
        addons.VSlang(30203) +
        ' (A-Z)',
        'music.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        'radio',
        'showWeb',
        addons.VSlang(30203),
        'music.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        'lsdb',
        'load',
        'Liveset Database',
        'music.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():

    gui = Gui()

    liste = []
    liste.append(['1', 'Film & Animation'])
    liste.append(['2', 'Autos & Vehicles'])
    liste.append(['10', 'Music'])
    liste.append(['15', 'Pets & Animals'])
    liste.append(['17', 'Sports'])
    liste.append(['18', 'Short Movies'])
    liste.append(['19', 'Travel & Events'])
    liste.append(['20', 'Gaming'])
    liste.append(['21', 'Videoblogging'])
    liste.append(['22', 'People & Blogs'])
    liste.append(['23', 'Comedy'])
    liste.append(['24', 'Entertainment'])
    liste.append(['25', 'News & Politics'])
    liste.append(['26', 'Howto & Style'])
    liste.append(['27', 'Education'])
    liste.append(['28', 'Science & Technology'])
    liste.append(['29', 'Nonprofits & Activism'])
    liste.append(['30', 'Movies'])
    liste.append(['31', 'Anime/Animation'])
    liste.append(['32', 'Action/Adventure'])
    liste.append(['33', 'Classics'])
    liste.append(['34', 'Comedy'])
    liste.append(['35', 'Documentary'])
    liste.append(['36', 'Drama'])
    liste.append(['37', 'Family'])
    liste.append(['38', 'Foreign'])
    liste.append(['39', 'Horror'])
    liste.append(['40', 'Sci-Fi/Fantasy'])
    liste.append(['41', 'Thriller'])
    liste.append(['42', 'Shorts'])
    liste.append(['43', 'Shows'])
    liste.append(['44', 'Trailers'])

    for sCatID, title in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('videoCategoryId', sCatID)
        gui.addDir(
            SITE_IDENTIFIER,
            'showLinks',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sCatID = input_parameter_handler.getValue('videoCategoryId')
    sNext = input_parameter_handler.getValue('pageToken')

    params = {
        'part': 'snippet',
                'maxResults': 20,
                'key': API_KEY,
                'chart': 'mostPopular',
                'regionCode': 'FR',
                'videoCategoryId': sCatID
    }

    if sNext:
        params['pageToken'] = sNext

    ytb = youtube('videos', params)
    videos = ytb.getVideos()
    # channel = result.getChannels()

    if (videos):
        total = len(videos)

        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in videos:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry['thumbnails']
            sID = aEntry['id']
            title = aEntry['title'].encode('utf-8')
            desc = aEntry['description'].encode('utf-8')
            sUrl = URL_VIEW % sID

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sID', sID)

            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'ytb.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        _next = ytb.getNext()
        if _next:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('videoCategoryId', sCatID)
            output_parameter_handler.addParameter('pageToken', _next)
            gui.addNext(
                SITE_IDENTIFIER,
                'showLinks',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):  # Affiche les page suivant si il y en a
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'myfree-tivi' in sUrl:
        sPattern = '<li class="page-item"><a class="page-link waves-effect" href="(.+?)" data-page=".+.?">.+?<div class="clearfix"></div></nav></div>'
    elif 'https://www.iptvsource.com/' in sUrl:
        sPattern = 'class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
    else:
        sPattern = '<a class="next page-numbers" href="(.+?)">'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        if 'myfree-tivi' in sUrl:
            return 'https://www.myfree-tivi.com' + aResult[1][0]
        else:
            return aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oHoster = HosterGui().checkHoster(sUrl)
    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sUrl, sThumb)

    gui.setEndOfDirectory()


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('thumbnail')
    desc = input_parameter_handler.getValue('sDescription')
    # VSlog(str(sUrl))
    if 'firstonetv' and 'Register-Login' in sUrl:

        session = requests.Session()
        url = 'https://www.firstonetv.net/Register-Login'
        data = {'usrmail': ADDON.getSetting('hoster_firstonetv_username'),
                'password': ADDON.getSetting('hoster_firstonetv_password'),
                'login': 'Login+Now'}

        headers = {'user-agent': UA,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'https://www.firstonetv.net/Index',
                   'Content-Length': str(len(data))}

        session.post(url, data=data, headers=headers)
        cookiesDict = requests.utils.dict_from_cookiejar(session.cookies)
        getUser = re.match("{'(.+?)': '(.+?)',", str(cookiesDict))
        # VSlog(cookiesDict)
        cookies = str(getUser.group(1)) + '=' + str(getUser.group(2))
        GestionCookie().SaveCookie('firstonetv', cookies)
        dialog().VSinfo('Authentification réussie merci de recharger la page', 'FirstOneTv', 15)
        return

    sHtmlContent = getHtml(sUrl)

    if 'myfree-tivi' in sUrl:
        aResult = re.findall(
            '<meta name="csrf-token" content="(.+?)">',
            sHtmlContent)
        if aResult:
            token = aResult[0]
            # VSlog(token)
            sHtmlContent = getHtml(sUrl, token)

    if 'firstonetv' in sUrl:
        sPattern = '(?:"surl":"{\".+?|,.+?)"([^"]+)\".+?"http([^"]+).m3u8'
    elif 'myfree-tivi' in sUrl:
        sPattern = 'url".+?"(.+?)".+?title.+?"(.+?)".+?thumb".+?"(.+?)"'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<h4><a class="more-link" title="(.+?)" href="(.+?)" target="_blank" rel="noopener"><button>.+?</button></a></h4>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '<p></br><br /><strong>2. Click on link to download .+? iptv channels list</strong></p>\\s*.+?<a href="(.+?)">Download (.+?)</a>'
    elif 'iptvsource.com':
        sPattern = '<a href="([^"]+)">Download as([^"]+)</a>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'firstonetv' in sUrl:
                title = title + aEntry[0]
                desc = desc
                sThumb = sThumb
                sUrl2 = 'http' + aEntry[1].replace('\\\\/', '/').replace('\\/', '/') + '.m3u8|Referer=' + sUrl + \
                    '&User-Agent=' + UA + '&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net'
            elif 'myfree-tivi' in sUrl:
                title = str(aEntry[1])
                sUrl2 = aEntry[0].replace('\\\\/', '/').replace("\\/", "/")
                sThumb = 'https:' + \
                    str(aEntry[2]).replace('\\\\/', '/').replace('\\/', '/')
                desc = ''
            elif 'iptvgratuit.com' in sUrl:
                title = aEntry[0]
                sUrl2 = aEntry[1]
                sThumb = ''
                desc = ''
            else:
                title = aEntry[1]
                sUrl2 = aEntry[0]
                sThumb = ''
                desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            if 'myfree-tivi' or 'firstonetv' in sUrl:
                output_parameter_handler.addParameter('thumbnail', sThumb)

            if 'iptvgratuit' and 'world-iptv-links' in sUrl:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showWorldIptvGratuit',
                    title,
                    '',
                    output_parameter_handler)
            elif 'firstonetv' in sUrl or 'myfree-tivi' in sUrl:
                oGuiElement = GuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('play__')
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon(sThumb)
                oGuiElement.setMeta(0)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setDirectTvFanart()
                oGuiElement.setCat(6)

                gui.CreateSimpleMenu(
                    oGuiElement,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'direct_epg',
                    'Guide tv Direct')
                gui.CreateSimpleMenu(
                    oGuiElement,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'soir_epg',
                    'Guide tv Soir')
                gui.CreateSimpleMenu(
                    oGuiElement,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'enregistrement',
                    'Enregistrement')
                gui.createContexMenuBookmark(
                    oGuiElement, output_parameter_handler)
                gui.addFolder(oGuiElement, output_parameter_handler)
            else:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showWeb',
                    title,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showWorldIptvGratuit():  # On recupere les liens qui sont dans les playlist 'World' de IptvGratuit
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    line = re.compile('http(.+?)\n').findall(sHtmlContent)

    for sUrl2 in line:
        sUrl2 = 'http' + sUrl2
        title = 'Lien: ' + sUrl2
        # cConfig().log(str(sHtmlContent))

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl2)
        output_parameter_handler.addParameter('sMovieTitle', title)

        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            'tv.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def getHtml(sUrl, data=None):  # S'occupe des requetes
    if 'firstonetv' in sUrl:
        cookies = GestionCookie().Readcookie('firstonetv')
    if 'myfree-tivi' and 'watch' in sUrl and data is not None:
        # VSlog(data)
        cookies = GestionCookie().Readcookie('myfree_tivi')
        headers = {
            'Host': 'www.myfree-tivi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': sUrl,
            'X-CSRF-Token': data.replace(
                '\n',
                '').replace(
                '\r',
                ''),
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Content-Length': '0',
            'TE': 'Trailers'}

        r = requests.post(
            'https://www.myfree-tivi.com/getdata',
            headers=headers)

    elif 'firstonetv' and '/France/' in sUrl:  # On passe les redirection
        aResult = re.findall('Live/.+?/*[^<>]+(?:-)([^"]+)', sUrl)
        idChannel = aResult[0]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'hiro')
        oRequestHandler.addParameters('result', 'get')
        data = oRequestHandler.request()
        hiro = unFuckFirst(data)  # On decode Hiro

        sPattern = '"hiro":(.+?),"hash":"(.+?)","time":(.+?),'

        oParser = Parser()
        aResult = oParser.parse(hiro, sPattern)

        for aEntry in aResult[1]:
            hiro = aEntry[0]
            Hash = aEntry[1]
            time = aEntry[2]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'hiro')
        oRequestHandler.addParameters('result', hiro)
        oRequestHandler.addParameters('time', time)
        oRequestHandler.addParameters('hash', Hash)
        data = oRequestHandler.request()

        aResult = re.findall('"ctoken":"(.+?)"}', data)
        cToken = aResult[0]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'channel')
        oRequestHandler.addParameters('ctoken', cToken)
        oRequestHandler.addParameters('c', 'fr')
        oRequestHandler.addParameters('id', idChannel)
        oRequestHandler.addParameters('native_hls', '0')
        oRequestHandler.addParameters('unsecure_hls', '0')
        data = oRequestHandler.request()
        return data
    elif 'firstonetv' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Host', 'www.firstonetv.net')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        data = oRequestHandler.request()
        return data

    if data is None and 'watch' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        data = oRequestHandler.request()
        cookies = oRequestHandler.GetCookies()
        GestionCookie().SaveCookie('myfree_tivi', cookies)
        return data

    else:
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)

    if data is not None and 'watch' in sUrl:
        data = r.text
        VSlog(data)
    else:
        data = oRequestHandler.request()
    # VSlog(data)
    return data


def parseM3U(infile):  # Traite les m3u local
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'iptv4sat' in sUrl or '.zip' in sUrl:
        sHtmlContent = getHtml(sUrl)
        from zipfile import ZipFile
        import io
        zip_file = ZipFile(io.BytesIO(sHtmlContent))
        files = zip_file.namelist()
        with zip_file.open(files[0]) as f:
            sHtmlContent = []
            for line in f:
                sHtmlContent.append(line)
            inf = sHtmlContent

    elif '#EXTM3U' not in sUrl:
        site = infile
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(site, headers=headers)
        inf = urllib2.urlopen(req)
    else:
        inf = infile

    try:
        line = inf.readline()
    except BaseException:
        pass

    # cConfig().log(str(line))
    # if not line.startswith('#EXTM3U'):
        # return

    playlist = []
    song = track(None, None, None, None)
    ValidEntry = False

    for line in inf:

        line = line.strip()
        if line.startswith('#EXTINF:'):
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except BaseException:
                icon = 'tv.png'
            ValidEntry = True

            song = track(length, title, None, icon)
        elif (len(line) != 0):
            if (ValidEntry) and (
                    not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                # VSlog(playlist)
                song = track(None, None, None, None)

    try:
        inf.close()
    except BaseException:
        pass

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    playlist = parseM3U(sUrl)

    if (input_parameter_handler.exist('AZ')):
        sAZ = input_parameter_handler.getValue('AZ')
        string = filter(
            lambda t: t.title.strip().capitalize().startswith(sAZ),
            playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    else:
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://')
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red] Problème de lecture avec la playlist[/COLOR]")

    else:
        total = len(playlist)
        progress_ = Progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')
            if not '[' in url2 and not ']' in url2 and '.m3u8' not in url2:
                url2 = 'plugin://plugin.video.f4mTester/?url=' + \
                    QuotePlus(url2) + '&amp;streamtype=TSDOWNLOADER&name=' + Quote(track.title)

            thumb = '/'.join([sRootArt, sThumb])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', url2)
            output_parameter_handler.addParameter('sMovieTitle', track.title)
            output_parameter_handler.addParameter('thumbnail', thumb)

            # gui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, output_parameter_handler)

            oGuiElement = GuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'enregistrement',
                'Enregistrement')
            gui.createContexMenuBookmark(oGuiElement, output_parameter_handler)
            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)
    gui.setEndOfDirectory()


def direct_epg():  # Code qui gere l'epg
    oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()
    # aParams = input_parameter_handler.getAllParameter()
    title = input_parameter_handler.getValue('sMovieTitle')
    sCom = cePg().view_epg(title, 'direct')


def soir_epg():  # Code qui gere l'epg
    oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()

    title = input_parameter_handler.getValue('sMovieTitle')
    sCom = cePg().view_epg(title, 'soir')


def enregistrement():  # Code qui gere l'epg
    oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        oDialog = dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'plugin' in sUrl:
        url = re.findall('url=(.+?)&amp', ''.join(sUrl))
        sUrl = Unquote(url[0])
    shebdule = Enregistremement().programmation_enregistrement(sUrl)


def showAZ():

    import string
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    for i in string.digits:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showTV',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showTV',
            i,
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAZRadio():

    import string
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    for i in string.digits:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showTV():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    # sPattern = '<url>([^<>]+?)</url><title>([^<>]+?)</title><order>' + sOrder + '</order><icon>(.+?)</icon>'
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        progress_ = Progress().VScreate(SITE_NAME)

        # affiche par
        if (input_parameter_handler.exist('AZ')):
            sAZ = input_parameter_handler.getValue('AZ')
            string = filter(
                lambda t: t[0].strip().capitalize().startswith(sAZ),
                aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else:
            string = sorted(
                aResult[1],
                key=lambda t: t[0].strip().capitalize())

        total = len(string)
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', aEntry[1])
            output_parameter_handler.addParameter('sMovieTitle', aEntry[0])
            output_parameter_handler.addParameter('thumbnail', 'tv.png')

            oGuiElement = GuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(aEntry[0])
            oGuiElement.setFileName(aEntry[0])
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            # oGuiElement.setThumbnail('tv.png')
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            gui.CreateSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'enregistrement',
                'Enregistrement')
            gui.createContexMenuBookmark(oGuiElement, output_parameter_handler)
            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def play__():  # Lancer les liens
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace('P_L_U_S', '+')
    title = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    playmode = ''

    if playmode == 0:
        stype = ''
        if '.ts' in sUrl:
            stype = 'TSDOWNLOADER'
        elif '.m3u' in sUrl:
            stype = 'HLS'
        if stype:
            from F4mProxy import f4mProxyHelper
            f4mp = f4mProxyHelper()
            xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
            f4mp.playF4mLink(
                sUrl,
                title,
                proxy=None,
                use_proxy_for_chunks=False,
                maxbitrate=0,
                simpleDownloader=False,
                auth=None,
                streamtype=stype,
                setResolved=False,
                swf=None,
                callbackpath="",
                callbackparam="",
                iconImage=thumbnail)
            return

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin(' + sUrl + ')')
        return
    else:
        oGuiElement = GuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(title)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(thumbnail)

        oPlayer = Player()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        # tout repetter
        # xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

        oPlayer.startPlayer()
        return


def openwindows():
    xbmc.executebuiltin("ActivateWindow(%d, return)" % (10601))
    return
