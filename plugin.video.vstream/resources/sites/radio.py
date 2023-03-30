# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom
import re
import string
import xbmc
import xbmcvfs

from resources.lib.comaddon import addon
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.player import Player

SITE_IDENTIFIER = 'radio'
SITE_NAME = '[COLOR orange]Radio[/COLOR]'
SITE_DESC = 'Radio'

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {
    'User-Agent': USER_AGENT,
    'Accept': '*/*',
    'Connection': 'keep-alive'}

icon = 'tv.png'
# sRootArt = cConfig().getRootArt()
sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/tv'


class track:
    def __init__(self, location, title, image, ident):
        self.location = location
        self.title = title
        self.image = image
        self.ident = ident


def load():
    gui = Gui()
    addons = addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showWeb',
        addons.VSlang(30203),
        'music.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenres',
        addons.VSlang(30203) +
        ' (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showAZ',
        addons.VSlang(30203) +
        ' (Alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [
        [
            '70', '70'], [
            '80', '80'], [
                '90', '90'], [
                    'Clubbing', 'Clubbing'], [
                        'Dance', 'Dance'], [
                            'Electronic', 'Electronic'], [
                                'Funk', 'Funk'], [
                                    'Hip-Hop', 'Hip-hop'], [
                                        'Hits', 'Hits'], [
                                            'Jazz', 'Jazz'], [
                                                'Lounge', 'Lounge'], [
                                                    'Metal', 'Metal'], [
                                                        'News', 'News'], [
                                                            'Pop', 'Pop'], [
                                                                'Rock', 'Rock'], [
                                                                    'Slow', 'Slow'], [
                                                                        'Trance', 'Trance']]

    output_parameter_handler = OutputParameterHandler()
    for title, sIdent in liste:
        output_parameter_handler.addParameter('siteUrl', '')
        output_parameter_handler.addParameter('ident', sIdent)
        gui.addDir(
            SITE_IDENTIFIER,
            'showWeb',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def parseWebM3U():  # Traite les m3u
    playlist = []
    # song = track(None, None, None, None)
    sFile = 'special://home/addons/plugin.video.vstream/resources/extra/radio.xspf'

    if not xbmcvfs.exists(sFile):
        return

    f = xbmcvfs.File(sFile, 'rb')
    sHtmlContent = f.read()
    f.close()

    line = re.compile(
        '<location>([^<]+).+?title>([^<]+).+?image>([^<]+).+?identifier>([^<]+)',
        re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(sHtmlContent)

    if line:
        # total = len(line)

        for result in line:
            # sUrl2 = result[0].replace('\r', '')
            song = track(result[0], result[1], result[2], result[3])
            playlist.append(song)

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    playlist = parseWebM3U()

    if input_parameter_handler.exist('AZ'):
        sAZ = input_parameter_handler.getValue('AZ')
        string = filter(
            lambda t: t.title.strip().capitalize().startswith(sAZ),
            playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    elif input_parameter_handler.exist('ident'):
        sIdent = input_parameter_handler.getValue('ident')
        string = filter(
            lambda t: t.ident.strip().capitalize().startswith(sIdent),
            playlist)
        playlist = sorted(string, key=lambda t: t.ident.strip().capitalize())
    else:
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://')
        gui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat[/COLOR] ')
    else:
        output_parameter_handler = OutputParameterHandler()
        for track in playlist:
            sThumb = track.image
            if not sThumb:
                sThumb = 'music.png'

            output_parameter_handler.addParameter('siteUrl', track.location)
            output_parameter_handler.addParameter('sMovieTitle', track.title)
            output_parameter_handler.addParameter('thumbnail', sThumb)

            oGuiElement = GuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('music.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            gui.createContexMenuBookmark(oGuiElement, output_parameter_handler)
            gui.addFolder(oGuiElement, output_parameter_handler)

    gui.setEndOfDirectory()


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
            'showWeb',
            i,
            'az.png',
            output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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


def play__():  # Lancer les liens
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace('P_L_U_S', '+')
    title = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

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
        # tout répéter
        xbmc.executebuiltin('xbmc.playercontrol(RepeatAll)')

        oPlayer.startPlayer()
        return


def GetRealUrl(chain):  # Récupère les liens des regex

    UA2 = UA
    url = chain
    regex = ''
    sHtmlContent = ''

    r = re.search('\\[[REGEX]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\\[[UA]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\\[[URL]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        url = r.group(1)

    # post methode ?
    r = re.search('\\[[POSTFORM]+\\](.+?)(?:(?:\\[[A-Z]+\\])|$)', chain)
    if r:
        param = r.group(1)
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
        sHtmlContent = oRequestHandler.request()

    else:
        if url:
            oRequestHandler = RequestHandler(url)
            sHtmlContent = oRequestHandler.request()

    if regex:
        oParser = Parser()
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url
