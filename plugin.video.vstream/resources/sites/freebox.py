# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import string

from resources.lib.comaddon import Progress, addon, dialog, SiteManager
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
ADDON = addon()


class track:
    def __init__(self, length, title, path, icon, data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data


def load():
    gui = Gui()
    addons = addon()

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
    addons = addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_WEB)
    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        addons.VSlang(30332),
        'tv.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showMenuMusic():
    gui = Gui()
    addons = addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_RADIO)
    gui.addDir(
        'radio',
        'showWeb',
        addons.VSlang(30203),
        'music.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        'radio',
        'showGenres',
        addons.VSlang(30203) +
        ' (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_RADIO)
    gui.addDir(
        'radio',
        'showAZ',
        addons.VSlang(30203) +
        ' (Alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def parseM3U(sUrl=None):  # Traite les m3u local

    if not sUrl:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    inf = oRequestHandler.request().split('\n')

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
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB
    elif sUrl == 'RADIO':
        sUrl = URL_RADIO

    playlist = parseM3U(sUrl=sUrl)

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
        output_parameter_handler.addParameter('siteUrl', 'http://')
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
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            channelName = track.title.replace(
                'sport', 'sports').replace(
                '(en clair)', '')
            desc = cEpg.getChannelEpg(EPG, channelName)

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')

            thumb = '/'.join([sRootArt, sThumb])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', url2)
            output_parameter_handler.addParameter('sMovieTitle', track.title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('EpgData', EPG)

            oGuiElement = GuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setDescription(desc)
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)

            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            gui.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            # gui.createSimpleMenu(oGuiElement, output_parameter_handler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def direct_epg():  # Code qui gerent l'epg
    # oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()
    # aParams = input_parameter_handler.getAllParameter()
    title = input_parameter_handler.getValue('sMovieTitle')
    text = input_parameter_handler.getValue('EpgData')
    cePg().view_epg(title, 'direct', text=text)


def soir_epg():  # Code qui gerent l'epg
    # oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()
    title = input_parameter_handler.getValue('sMovieTitle')
    cePg().view_epg(title, 'soir')


def enregistrement():  # Code qui gerent l'enregistrement
    # oGuiElement = GuiElement()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = getRealUrl(sUrl)

    if 'plugin' in sUrl:
        url = re.findall('url=(.+?)&amp', ''.join(sUrl))
        sUrl = Unquote(url[0])
    Enregistremement().programmation_enregistrement(sUrl)


def showAZ():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    output_parameter_handler = OutputParameterHandler()
    for i in string.digits:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showTV',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
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
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    output_parameter_handler = OutputParameterHandler()
    for i in string.digits:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('AZ', i)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    for i in string.ascii_uppercase:
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
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        progress_ = Progress().VScreate(SITE_NAME)

        # affiche par
        if input_parameter_handler.exist('AZ'):
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
        output_parameter_handler = OutputParameterHandler()
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

            gui.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'direct_epg',
                'Guide tv Direct')
            gui.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                SITE_IDENTIFIER,
                'soir_epg',
                'Guide tv Soir')
            # gui.createSimpleMenu(oGuiElement, output_parameter_handler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
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
    desc = input_parameter_handler.getValue('desc')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = getRealUrl(sUrl)

    # Bug specifique au flux france TV
    # eof detectedL
    if 'ftven.fr' in sUrl:
        oGuiElement = GuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(title)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(thumbnail)
        oGuiElement.setDescription(desc)

        from resources.lib.player import Player
        oPlayer = Player()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()

    else:
        oHoster = HosterGui().checkHoster(sUrl)

        if oHoster:
            oHoster.setDisplayName(title)
            oHoster.setFileName(title)
            HosterGui().showHoster(gui, oHoster, sUrl, thumbnail,
                                   input_parameter_handler=input_parameter_handler)

        gui.setEndOfDirectory()


"""
Fonction diverse:
#   - getRealUrl = Regex pour Iptv(Officiel)
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def getRealUrl(chain):
    oParser = Parser()

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

    oRequestHandler = RequestHandler(url)
    if param:
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
    if head:
        import json
        head = json.loads(head)
        for a in head:
            oRequestHandler.addHeaderEntry(a, head[a])
    sHtmlContent = oRequestHandler.request()

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def decodeNrj(d):
    oRequestHandler = RequestHandler(d)
    sHtmlContent = oRequestHandler.request()

    title = re.search('data-program_title="([^"]+)"', sHtmlContent).group(1)
    ids = re.search('data-ref="([^"]+)"', sHtmlContent).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + \
        d.split('/')[3] + '&channel=' + d.split('/')[3] + '&title='
    url += title + '&channel=' + \
        d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    oRequestHandler = RequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    dataUrl = re.search(
        '"contentUrl" content="([^"]+)"',
        sHtmlContent).group(1)

    return dataUrl


def getBrightcoveKey(sUrl):
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "rmcdecouverte" in sUrl:
        url = re.search(
            '<script type="application/javascript" src="([^"]+)"></script>',
            sHtmlContent).group(1)

        oRequestHandler = RequestHandler(
            "https://" + sUrl.split('/')[2] + url)
        sHtmlContent = oRequestHandler.request()
        result = re.search('N="([^"]+)",y="([^"]+)"\\)', sHtmlContent)
        player = result.group(1)
        video = result.group(2)

        oRequestHandler = RequestHandler(
            "https://static.bfmtv.com/ressources/next-player/cleo-player/playerBridge.js")
        sHtmlContent = oRequestHandler.request().lower()

        ID = sUrl.split('/')[2].split('.')[0]
        account = re.search(
            "\n(.+?): '" + ID + "'",
            sHtmlContent).group(1).replace(
            '            ',
            '')

    else:
        result = re.search(
            '<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"',
            sHtmlContent)

        account = result.group(1)
        player = result.group(2)
        video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (
        account, player)
    oRequestHandler = RequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    policyKey = re.search('policyKey:"(.+?)"', sHtmlContent).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (
        account, video)
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry(
        'Accept', "application/json;pk=" + policyKey)
    sHtmlContent = oRequestHandler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', sHtmlContent).group(1)

    return url
