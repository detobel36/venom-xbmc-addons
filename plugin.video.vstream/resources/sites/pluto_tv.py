# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import string
import uuid

from resources.lib.comaddon import Progress, Addon, isMatrix, SiteManager
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
    if Addon().getSetting("PlutoTV_sid"):
        deviceID = Addon().getSetting("PlutoTV_deviceID")
        clientID = Addon().getSetting("PlutoTV_clientID")
        sid = Addon().getSetting("PlutoTV_sid")

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

        Addon().setSetting("PlutoTV_deviceID", deviceID)
        Addon().setSetting("PlutoTV_clientID", clientID)
        Addon().setSetting("PlutoTV_sid", sid)

    return clientID, deviceID, sid


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', CHAINE_DIRECT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        CHAINE_DIRECT[1],
        'Chaines en direct',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', VOD[0])
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
    url = input_parameter_handler.getValue('site_url')

    clientID, deviceID, sid = getData()

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request(json_decode=True)

    if html_content:
        output_parameter_handler = OutputParameterHandler()
        for entry in html_content:
            thumb = entry["featuredImage"]["path"]
            title = entry["name"]
            if not isMatrix():
                title = title.encode('utf8')

            url2 = "https://boot.pluto.tv/v4/start?deviceId=" + deviceID
            url2 += "&deviceMake=Firefox&deviceType=web&deviceVersion=87.0&deviceModel=web&DNT=0&appName=web"
            url2 += "&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&serverSideAds=true&channelSlug="
            url2 += entry["slug"] + "&episodeSlugs=&clientID=" + \
                clientID + "&clientModelNumber=na"

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'tv.png',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenre():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request(json_decode=True)

    sID = 1
    if html_content:
        output_parameter_handler = OutputParameterHandler()
        for entry in html_content["categories"]:
            title = entry["name"]
            if not isMatrix():
                title = title.encode('utf8')

            output_parameter_handler.addParameter('site_url', url)
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
    url = input_parameter_handler.getValue('site_url')
    sID = input_parameter_handler.getValue('sID')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request(json_decode=True)

    if html_content:
        items = html_content["categories"][int(sID) - 1]["items"]
        total = len(items)
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in items:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry["featuredImage"]["path"]
            title = entry["name"]
            # /!\ ces replace sont différents
            title = title.replace(
                ' : Saison',
                ' saison').replace(
                ' : Saison',
                ' saison')
            ids = entry["_id"]
            desc = entry["description"]
            if not isMatrix():
                title = title.encode('utf8')
                desc = desc.encode('utf8')

            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            VOD_SERIES = "https://service-vod.clusters.pluto.tv/v3/vod/series/"
            if entry["type"] == "series":
                url = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                output_parameter_handler.addParameter('site_url', url)
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSerieSxE',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif entry["type"] == "Anime":
                url = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                output_parameter_handler.addParameter('site_url', url)
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSerieSxE',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                site_url = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + \
                    ids + "/master.m3u8"
                output_parameter_handler.addParameter('site_url', site_url)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showSerieSxE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request(json_decode=True)

    if html_content:
        output_parameter_handler = OutputParameterHandler()
        for entry in html_content["seasons"]:
            for a in entry["episodes"]:
                title = movie_title + " S" + \
                    str(a["season"]) + " E" + str(a["number"])
                sID = a["_id"]

                site_url = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + \
                    sID + "/master.m3u8"
                output_parameter_handler.addParameter('site_url', site_url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    title,
                    'series.png',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request(json_decode=True)

    hoster_url = "https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/"
    hoster_url += html_content["startingChannel"]["id"] + \
        "/master.m3u8?" + html_content["stitcherParams"]

    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    clientID, deviceID, sid = getData()

    hoster_url = url
    hoster_url += "?appName=web&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&deviceDNT=false"
    hoster_url += "&deviceId=" + deviceID + \
        "&deviceMake=Firefox&deviceModel=web&deviceType=web&deviceVersion=87.0"
    hoster_url += "&includeExtendedEvents=false&marketingRegion=FR&sid=" + \
        sid + "&serverSideAds=true"

    hoster = HosterGui().checkHoster(url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
