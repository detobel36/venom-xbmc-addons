# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import string

from resources.lib.comaddon import Progress, Addon, dialog, SiteManager
from resources.lib.enregistrement import Enregistremement
from resources.lib.epg import cePg
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import Unquote

SITE_IDENTIFIER = 'freebox'
SITE_NAME = 'Free Télévision/Radio'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_WEB = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/Beta/repo/resources/webtv2.m3u'
URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'

TV_TV = (True, 'showMenuTV')
CHAINE_TV = (URL_WEB, 'showWeb')


UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

icon = 'tv.png'
sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/tv'
ADDON = Addon()


class track:
    def __init__(self, length, title, path, icon, data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data


def load():
    gui = Gui()
    addons = Addon()

    output_parameter_handler = OutputParameterHandler()
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTV',
        addons.VSlang(30115),
        'tv.png',
        output_parameter_handler)
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMusic',
        addons.VSlang(30137),
        'music.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showMenuTV():
    gui = Gui()
    addons = Addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_WEB)
    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        addons.VSlang(30332),
        'tv.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showMenuMusic():
    gui = Gui()
    addons = Addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_RADIO)
    gui.addDir(
        'radio',
        'showWeb',
        addons.VSlang(30203),
        'music.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        'radio',
        'showGenres',
        addons.VSlang(30203) +
        ' (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_RADIO)
    gui.addDir(
        'radio',
        'showAZ',
        addons.VSlang(30203) +
        ' (Alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def parseM3U(url=None):  # Traite les m3u local

    if not url:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    inf = request_handler.request().split('\n')

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

        elif len(line) != 0:
            if ValidEntry and (
                    not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                song = track(None, None, None, None)

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if url == 'TV':
        url = URL_WEB
    elif url == 'RADIO':
        url = URL_RADIO

    playlist = parseM3U(url=url)

    if input_parameter_handler.exist('AZ'):
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
            '[COLOR red]Problème de lecture avec la playlist[/COLOR]')

    else:
        cEpg = cePg()
        EPG = cEpg.getEpg('', 'direct', noTextBox=True)

        total = len(playlist)
        progress_ = Progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            thumb = track.icon
            if not thumb:
                thumb = 'tv.png'

            channelName = track.title.replace(
                'sport', 'sports').replace(
                '(en clair)', '')
            desc = cEpg.getChannelEpg(EPG, channelName)

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')

            thumb = '/'.join([sRootArt, thumb])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', track.title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('EpgData', EPG)

            gui_element = GuiElement()
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setFunction('play__')
            gui_element.setDescription(desc)
            gui_element.setTitle(track.title)
            gui_element.setFileName(track.title)

            gui_element.setIcon('tv.png')
            gui_element.setMeta(0)
            gui_element.setThumbnail(thumb)
            gui_element.setDirectTvFanart()
            gui_element.setCat(6)

            gui.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            # gui.createSimpleMenu(gui_element, output_parameter_handler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def direct_epg():  # Code qui gerent l'epg
    # gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()
    # aParams = input_parameter_handler.getAllParameter()
    title = input_parameter_handler.getValue('movie_title')
    text = input_parameter_handler.getValue('EpgData')
    cePg().view_epg(title, 'direct', text=text)


def soir_epg():  # Code qui gerent l'epg
    # gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('movie_title')
    cePg().view_epg(title, 'soir')


def enregistrement():  # Code qui gerent l'enregistrement
    # gui_element = GuiElement()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in url and ']' in url:
        url = getRealUrl(url)

    if 'plugin' in url:
        url = re.findall('url=(.+?)&amp', ''.join(url))
        url = Unquote(url[0])
    Enregistremement().programmation_enregistrement(url)


def showAZ():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    output_parameter_handler = OutputParameterHandler()
    for i in string.digits:
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showTV',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
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
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    output_parameter_handler = OutputParameterHandler()
    for i in string.digits:
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
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
    pattern = '<title>(.+?)</title><link>(.+?)</link>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        progress_ = Progress().VScreate(SITE_NAME)

        # affiche par
        if input_parameter_handler.exist('AZ'):
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
        output_parameter_handler = OutputParameterHandler()
        for entry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

            gui.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            # gui.createSimpleMenu(gui_element, output_parameter_handler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
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
    desc = input_parameter_handler.getValue('desc')

    # Special url with tag
    if '[' in url and ']' in url:
        url = getRealUrl(url)

    # Bug specifique au flux france TV
    # eof detectedL
    if 'ftven.fr' in url:
        gui_element = GuiElement()
        gui_element.setSiteName(SITE_IDENTIFIER)
        gui_element.setTitle(title)
        url = url.replace(' ', '%20')
        gui_element.setMediaUrl(url)
        gui_element.setThumbnail(thumbnail)
        gui_element.setDescription(desc)

        from resources.lib.player import Player
        player = Player()
        player.clearPlayList()
        player.addItemToPlaylist(gui_element)
        player.startPlayer()

    else:
        hoster = HosterGui().checkHoster(url)

        if hoster:
            hoster.setDisplayName(title)
            hoster.setFileName(title)
            HosterGui().showHoster(gui, hoster, url, thumbnail,
                                   input_parameter_handler=input_parameter_handler)

        gui.setEndOfDirectory()


"""
Fonction diverse:
#   - getRealUrl = Regex pour Iptv(Officiel)
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def getRealUrl(chain):
    parser = Parser()

    UA2 = UA
    url = chain
    regex = ''
    param = ""
    head = None

    r = re.search('\\[[DECODENRJ]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        url = decodeNrj(r.group(1))

    r = re.search('\\[[BRIGHTCOVEKEY]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        url = getBrightcoveKey(r.group(1))

    r = re.search('\\[[REGEX]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\\[[UA]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\\[[URL]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        url = r.group(1)

    r = re.search('\\[[HEAD]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        head = r.group(1)

    # post metehod ?
    r = re.search('\\[[POSTFORM]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        param = r.group(1)

    request_handler = RequestHandler(url)
    if param:
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Accept-Encoding', 'identity')
        request_handler.addParametersLine(param)
    if head:
        import json
        head = json.loads(head)
        for a in head:
            request_handler.addHeaderEntry(a, head[a])
    html_content = request_handler.request()

    if regex:
        aResult2 = parser.parse(html_content, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def decodeNrj(d):
    request_handler = RequestHandler(d)
    html_content = request_handler.request()

    title = re.search('data-program_title="([^"]+)"', html_content).group(1)
    ids = re.search('data-ref="([^"]+)"', html_content).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + \
        d.split('/')[3] + '&channel=' + d.split('/')[3] + '&title='
    url += title + '&channel=' + \
        d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    dataUrl = re.search(
        '"contentUrl" content="([^"]+)"',
        html_content).group(1)

    return dataUrl


def getBrightcoveKey(url):
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if "rmcdecouverte" in url:
        url = re.search(
            '<script type="application/javascript" src="([^"]+)"></script>',
            html_content).group(1)

        request_handler = RequestHandler(
            "https://" + url.split('/')[2] + url)
        html_content = request_handler.request()
        result = re.search('N="([^"]+)",y="([^"]+)"\\)', html_content)
        player = result.group(1)
        video = result.group(2)

        request_handler = RequestHandler(
            "https://static.bfmtv.com/ressources/next-player/cleo-player/playerBridge.js")
        html_content = request_handler.request().lower()

        ID = url.split('/')[2].split('.')[0]
        account = re.search(
            "\n(.+?): '" + ID + "'",
            html_content).group(1).replace(
            '            ',
            '')

    else:
        result = re.search(
            '<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"',
            html_content)

        account = result.group(1)
        player = result.group(2)
        video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (
        account, player)
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    policyKey = re.search('policyKey:"(.+?)"', html_content).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (
        account, video)
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry(
        'Accept', "application/json;pk=" + policyKey)
    html_content = request_handler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', html_content).group(1)

    return url
