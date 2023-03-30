# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import string
import uuid

from resources.lib.comaddon import Progress, addon, isMatrix, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.util import Quote

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"

SITE_IDENTIFIER = 'pluto_tv'
SITE_NAME = 'Pluto TV'
SITE_DESC = 'Chaine gratuite légal, VOD de programme divers'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

CHAINE_DIRECT = (URL_MAIN + '/v2/channels.json?', 'showTV')
VOD = (
    URL_MAIN +
    '/v3/vod/categories?includeItems=true&deviceType=web',
    'showGenre')


def getData():
    if addon().getSetting("PlutoTV_sid"):
        deviceID = addon().getSetting("PlutoTV_deviceID")
        clientID = addon().getSetting("PlutoTV_clientID")
        sid = addon().getSetting("PlutoTV_sid")

    else:
        sid = str(uuid.uuid1().hex)
        deviceID = str(uuid.uuid4().hex)
        clientID = Quote(
            ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.ascii_lowercase +
                    string.digits +
                    '=+') for _ in range(24)))

        addon().setSetting("PlutoTV_deviceID", deviceID)
        addon().setSetting("PlutoTV_clientID", clientID)
        addon().setSetting("PlutoTV_sid", sid)

    return clientID, deviceID, sid


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', CHAINE_DIRECT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        CHAINE_DIRECT[1],
        'Chaines en direct',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', VOD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        VOD[1],
        'Programmes disponibles en VOD',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showTV():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    clientID, deviceID, sid = getData()

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sHtmlContent:
            sThumb = aEntry["featuredImage"]["path"]
            title = aEntry["name"]
            if not isMatrix():
                title = title.encode('utf8')

            sUrl2 = "https://boot.pluto.tv/v4/start?deviceId=" + deviceID
            sUrl2 += "&deviceMake=Firefox&deviceType=web&deviceVersion=87.0&deviceModel=web&DNT=0&appName=web"
            sUrl2 += "&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&serverSideAds=true&channelSlug="
            sUrl2 += aEntry["slug"] + "&episodeSlugs=&clientID=" + \
                clientID + "&clientModelNumber=na"

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'tv.png',
                sThumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenre():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sID = 1
    if sHtmlContent:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sHtmlContent["categories"]:
            title = aEntry["name"]
            if not isMatrix():
                title = title.encode('utf8')

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sID', int(sID))
            sID = sID + 1

            gui.addDir(
                SITE_IDENTIFIER,
                'showVOD',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showVOD():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sID = input_parameter_handler.getValue('sID')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        items = sHtmlContent["categories"][int(sID) - 1]["items"]
        total = len(items)
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in items:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry["featuredImage"]["path"]
            title = aEntry["name"]
            # /!\ ces replace sont différents
            title = title.replace(
                ' : Saison',
                ' saison').replace(
                ' : Saison',
                ' saison')
            ids = aEntry["_id"]
            desc = aEntry["description"]
            if not isMatrix():
                title = title.encode('utf8')
                desc = desc.encode('utf8')

            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            VOD_SERIES = "https://service-vod.clusters.pluto.tv/v3/vod/series/"
            if aEntry["type"] == "series":
                sUrl = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                output_parameter_handler.addParameter('siteUrl', sUrl)
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSerieSxE',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            elif aEntry["type"] == "Anime":
                sUrl = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                output_parameter_handler.addParameter('siteUrl', sUrl)
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSerieSxE',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                siteUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + \
                    ids + "/master.m3u8"
                output_parameter_handler.addParameter('siteUrl', siteUrl)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSerieSxE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sHtmlContent["seasons"]:
            for a in aEntry["episodes"]:
                title = sMovieTitle + " S" + \
                    str(a["season"]) + " E" + str(a["number"])
                sID = a["_id"]

                siteUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + \
                    sID + "/master.m3u8"
                output_parameter_handler.addParameter('siteUrl', siteUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    title,
                    'series.png',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sHosterUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/"
    sHosterUrl += sHtmlContent["startingChannel"]["id"] + \
        "/master.m3u8?" + sHtmlContent["stitcherParams"]

    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    clientID, deviceID, sid = getData()

    sHosterUrl = sUrl
    sHosterUrl += "?appName=web&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&deviceDNT=false"
    sHosterUrl += "&deviceId=" + deviceID + \
        "&deviceMake=Firefox&deviceModel=web&deviceType=web&deviceVersion=87.0"
    sHosterUrl += "&includeExtendedEvents=false&marketingRegion=FR&sid=" + \
        sid + "&serverSideAds=true"

    oHoster = HosterGui().checkHoster(sUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
