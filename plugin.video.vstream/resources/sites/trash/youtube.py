# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress, Addon, VSlog, dialog
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

ADDON = Addon()


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
        html_content = response.read()
        html_content = html_content.decode('utf-8')
        self.result = json.loads(html_content)
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
    addons = Addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        addons.VSlang(30332),
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenres',
        'Catégorie',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        'radio',
        'showAZ',
        addons.VSlang(30203) +
        ' (A-Z)',
        'music.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        'radio',
        'showWeb',
        addons.VSlang(30203),
        'music.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://')
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

        for entry in videos:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry['thumbnails']
            sID = entry['id']
            title = entry['title'].encode('utf-8')
            desc = entry['description'].encode('utf-8')
            url = URL_VIEW % sID

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('sID', sID)

            output_parameter_handler.addParameter('movie_title', title)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'ytb.png',
                thumb,
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


def __checkForNextPage(html_content):  # Affiche les page suivant si il y en a
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'myfree-tivi' in url:
        pattern = '<li class="page-item"><a class="page-link waves-effect" href="(.+?)" data-page=".+.?">.+?<div class="clearfix"></div></nav></div>'
    elif 'https://www.iptvsource.com/' in url:
        pattern = 'class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
    else:
        pattern = '<a class="next page-numbers" href="(.+?)">'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        if 'myfree-tivi' in url:
            return 'https://www.myfree-tivi.com' + results[1][0]
        else:
            return results[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    hoster = HosterGui().checkHoster(url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, url, thumb)

    gui.setEndOfDirectory()


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumbnail')
    desc = input_parameter_handler.getValue('description')
    # VSlog(str(url))
    if 'firstonetv' and 'Register-Login' in url:

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

    html_content = getHtml(url)

    if 'myfree-tivi' in url:
        results = re.findall(
            '<meta name="csrf-token" content="(.+?)">',
            html_content)
        if results:
            token = results[0]
            # VSlog(token)
            html_content = getHtml(url, token)

    if 'firstonetv' in url:
        pattern = '(?:"surl":"{\".+?|,.+?)"([^"]+)\".+?"http([^"]+).m3u8'
    elif 'myfree-tivi' in url:
        pattern = 'url".+?"(.+?)".+?title.+?"(.+?)".+?thumb".+?"(.+?)"'
    elif 'iptvgratuit.com' in url:
        pattern = '<h4><a class="more-link" title="(.+?)" href="(.+?)" target="_blank" rel="noopener"><button>.+?</button></a></h4>'
    elif 'dailyiptvlist.com' in url:
        pattern = '<p></br><br /><strong>2. Click on link to download .+? iptv channels list</strong></p>\\s*.+?<a href="(.+?)">Download (.+?)</a>'
    elif 'iptvsource.com':
        pattern = '<a href="([^"]+)">Download as([^"]+)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'firstonetv' in url:
                title = title + entry[0]
                desc = desc
                thumb = thumb
                url2 = 'http' + entry[1].replace('\\\\/', '/').replace('\\/', '/') + '.m3u8|Referer=' + url + \
                    '&User-Agent=' + UA + '&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net'
            elif 'myfree-tivi' in url:
                title = str(entry[1])
                url2 = entry[0].replace('\\\\/', '/').replace("\\/", "/")
                thumb = 'https:' + \
                    str(entry[2]).replace('\\\\/', '/').replace('\\/', '/')
                desc = ''
            elif 'iptvgratuit.com' in url:
                title = entry[0]
                url2 = entry[1]
                thumb = ''
                desc = ''
            else:
                title = entry[1]
                url2 = entry[0]
                thumb = ''
                desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            if 'myfree-tivi' or 'firstonetv' in url:
                output_parameter_handler.addParameter('thumbnail', thumb)

            if 'iptvgratuit' and 'world-iptv-links' in url:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showWorldIptvGratuit',
                    title,
                    '',
                    output_parameter_handler)
            elif 'firstonetv' in url or 'myfree-tivi' in url:
                gui_element = GuiElement()
                gui_element.setSiteName(SITE_IDENTIFIER)
                gui_element.setFunction('play__')
                gui_element.setTitle(title)
                gui_element.setFileName(title)
                gui_element.setIcon(thumb)
                gui_element.setMeta(0)
                gui_element.setThumbnail(thumb)
                gui_element.setDirectTvFanart()
                gui_element.setCat(6)

                gui.CreateSimpleMenu(
                    gui_element,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'direct_epg',
                    'Guide tv Direct')
                gui.CreateSimpleMenu(
                    gui_element,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'soir_epg',
                    'Guide tv Soir')
                gui.CreateSimpleMenu(
                    gui_element,
                    output_parameter_handler,
                    SITE_IDENTIFIER,
                    SITE_IDENTIFIER,
                    'enregistrement',
                    'Enregistrement')
                gui.createContexMenuBookmark(
                    gui_element, output_parameter_handler)
                gui.addFolder(gui_element, output_parameter_handler)
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
    url = input_parameter_handler.getValue('site_url')

    html_content = getHtml(url)
    line = re.compile('http(.+?)\n').findall(html_content)

    for url2 in line:
        url2 = 'http' + url2
        title = 'Lien: ' + url2
        # cConfig().log(str(html_content))

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url2)
        output_parameter_handler.addParameter('movie_title', title)

        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            'tv.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def getHtml(url, data=None):  # S'occupe des requetes
    if 'firstonetv' in url:
        cookies = GestionCookie().Readcookie('firstonetv')
    if 'myfree-tivi' and 'watch' in url and data is not None:
        # VSlog(data)
        cookies = GestionCookie().Readcookie('myfree_tivi')
        headers = {
            'Host': 'www.myfree-tivi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': url,
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

    elif 'firstonetv' and '/France/' in url:  # On passe les redirection
        results = re.findall('Live/.+?/*[^<>]+(?:-)([^"]+)', url)
        idChannel = results[0]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addParameters('action', 'hiro')
        request_handler.addParameters('result', 'get')
        data = request_handler.request()
        hiro = unFuckFirst(data)  # On decode Hiro

        pattern = '"hiro":(.+?),"hash":"(.+?)","time":(.+?),'

        parser = Parser()
        results = parser.parse(hiro, pattern)

        for entry in results[1]:
            hiro = entry[0]
            Hash = entry[1]
            time = entry[2]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addParameters('action', 'hiro')
        request_handler.addParameters('result', hiro)
        request_handler.addParameters('time', time)
        request_handler.addParameters('hash', Hash)
        data = request_handler.request()

        results = re.findall('"ctoken":"(.+?)"}', data)
        cToken = results[0]

        apiNumber = random.uniform(0.0000000000000000, 0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addParameters('action', 'channel')
        request_handler.addParameters('ctoken', cToken)
        request_handler.addParameters('c', 'fr')
        request_handler.addParameters('id', idChannel)
        request_handler.addParameters('native_hls', '0')
        request_handler.addParameters('unsecure_hls', '0')
        data = request_handler.request()
        return data
    elif 'firstonetv' in url:
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Host', 'www.firstonetv.net')
        request_handler.addHeaderEntry('Cookie', cookies)
        data = request_handler.request()
        return data

    if data is None and 'watch' in url:
        request_handler = RequestHandler(url)
        data = request_handler.request()
        cookies = request_handler.GetCookies()
        GestionCookie().SaveCookie('myfree_tivi', cookies)
        return data

    else:
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)

    if data is not None and 'watch' in url:
        data = r.text
        VSlog(data)
    else:
        data = request_handler.request()
    # VSlog(data)
    return data


def parseM3U(infile):  # Traite les m3u local
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'iptv4sat' in url or '.zip' in url:
        html_content = getHtml(url)
        from zipfile import ZipFile
        import io
        zip_file = ZipFile(io.BytesIO(html_content))
        files = zip_file.namelist()
        with zip_file.open(files[0]) as f:
            html_content = []
            for line in f:
                html_content.append(line)
            inf = html_content

    elif '#EXTM3U' not in url:
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
    url = input_parameter_handler.getValue('site_url')

    playlist = parseM3U(url)

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
        output_parameter_handler.addParameter('site_url', 'http://')
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
            thumb = track.icon
            if not thumb:
                thumb = 'tv.png'

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')
            if not '[' in url2 and not ']' in url2 and '.m3u8' not in url2:
                url2 = 'plugin://plugin.video.f4mTester/?url=' + \
                    QuotePlus(url2) + '&amp;streamtype=TSDOWNLOADER&name=' + Quote(track.title)

            thumb = '/'.join([sRootArt, thumb])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', track.title)
            output_parameter_handler.addParameter('thumbnail', thumb)

            # gui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + thumb, output_parameter_handler)

            gui_element = GuiElement()
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setFunction('play__')
            gui_element.setTitle(track.title)
            gui_element.setFileName(track.title)
            gui_element.setIcon('tv.png')
            gui_element.setMeta(0)
            gui_element.setThumbnail(thumb)
            gui_element.setDirectTvFanart()
            gui_element.setCat(6)

            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'enregistrement',
                'Enregistrement')
            gui.createContexMenuBookmark(gui_element, output_parameter_handler)
            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)
    gui.setEndOfDirectory()


def direct_epg():  # Code qui gere l'epg
    gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()
    # aParams = input_parameter_handler.getAllParameter()
    title = input_parameter_handler.getValue('movie_title')
    sCom = cePg().view_epg(title, 'direct')


def soir_epg():  # Code qui gere l'epg
    gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()

    title = input_parameter_handler.getValue('movie_title')
    sCom = cePg().view_epg(title, 'soir')


def enregistrement():  # Code qui gere l'epg
    gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        oDialog = dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in url and ']' in url:
        url = GetRealUrl(url)

    if 'plugin' in url:
        url = re.findall('url=(.+?)&amp', ''.join(url))
        url = Unquote(url[0])
    shebdule = Enregistremement().programmation_enregistrement(url)


def showAZ():

    import string
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    for i in string.digits:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showTV',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
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
    url = input_parameter_handler.getValue('site_url')

    for i in string.digits:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
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
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    # pattern = '<url>([^<>]+?)</url><title>([^<>]+?)</title><order>' + sOrder + '</order><icon>(.+?)</icon>'
    pattern = '<title>(.+?)</title><link>(.+?)</link>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        progress_ = Progress().VScreate(SITE_NAME)

        # affiche par
        if (input_parameter_handler.exist('AZ')):
            sAZ = input_parameter_handler.getValue('AZ')
            string = filter(
                lambda t: t[0].strip().capitalize().startswith(sAZ),
                results[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else:
            string = sorted(
                results[1],
                key=lambda t: t[0].strip().capitalize())

        total = len(string)
        for entry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[1])
            output_parameter_handler.addParameter('movie_title', entry[0])
            output_parameter_handler.addParameter('thumbnail', 'tv.png')

            gui_element = GuiElement()
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setFunction('play__')
            gui_element.setTitle(entry[0])
            gui_element.setFileName(entry[0])
            gui_element.setIcon('tv.png')
            gui_element.setMeta(0)
            # gui_element.setThumbnail('tv.png')
            gui_element.setDirectTvFanart()
            gui_element.setCat(6)

            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            gui.CreateSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'enregistrement',
                'Enregistrement')
            gui.createContexMenuBookmark(gui_element, output_parameter_handler)
            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def play__():  # Lancer les liens
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace('P_L_U_S', '+')
    title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # Special url with tag
    if '[' in url and ']' in url:
        url = GetRealUrl(url)

    playmode = ''

    if playmode == 0:
        stype = ''
        if '.ts' in url:
            stype = 'TSDOWNLOADER'
        elif '.m3u' in url:
            stype = 'HLS'
        if stype:
            from F4mProxy import f4mProxyHelper
            f4mp = f4mProxyHelper()
            xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
            f4mp.playF4mLink(
                url,
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

    if 'f4mTester' in url:
        xbmc.executebuiltin('XBMC.RunPlugin(' + url + ')')
        return
    else:
        gui_element = GuiElement()
        gui_element.setSiteName(SITE_IDENTIFIER)
        gui_element.setTitle(title)
        url = url.replace(' ', '%20')
        gui_element.setMediaUrl(url)
        gui_element.setThumbnail(thumbnail)

        player = Player()
        player.clearPlayList()
        player.addItemToPlaylist(gui_element)
        # tout repetter
        # xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

        player.startPlayer()
        return


def openwindows():
    xbmc.executebuiltin("ActivateWindow(%d, return)" % (10601))
    return
