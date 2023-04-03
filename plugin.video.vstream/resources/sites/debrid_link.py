# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json
import re

from resources.lib.comaddon import Progress, Addon, dialog
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'debrid_link'
SITE_NAME = '[COLOR violet]Debrid Link[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

URL_HOST = "https://debrid-link.fr"


def load():
    gui = Gui()
    addon = Addon()

    URL_HOST = "https://debrid-link.fr"
    ALL_ALL = (
        URL_HOST +
        '/api/v2/downloader/list?page=0&perPage=20',
        'showLiens')
    ALL_MAGNETS = (
        URL_HOST +
        '/api/v2/seedbox/list?page=0&perPage=20',
        'showLiens')
    ALL_INFORMATION = (URL_HOST + '/infos/downloader', 'showInfo')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ALL_ALL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_ALL[1],
        'Liens',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ALL_MAGNETS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_MAGNETS[1],
        'Magnets',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ALL_INFORMATION[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_INFORMATION[1],
        'Information sur les hébergeurs ',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showLiens(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    numPage = input_parameter_handler.getValue('numPage')
    if not numPage:
        numPage = 0
    numPage = int(numPage)

    Token_debrid_link = "Bearer " + Addon().getSetting('hoster_debridlink_token')
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('Accept', 'application/json')
    request_handler.addHeaderEntry('Authorization', Token_debrid_link)
    r = json.loads(request_handler.request())

    if (r["success"] == False):
        gui.addText(SITE_IDENTIFIER)
        if (r["error"] == 'badToken'):
            New_token = RenewToken()

            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('Accept', 'application/json')
            request_handler.addHeaderEntry('Authorization', New_token)
            r = json.loads(request_handler.request())

    if (r["success"]):
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in r["value"]:

            progress_.VSupdate(progress_, len(entry["name"]))
            if progress_.iscanceled():
                break

            if 'seedbox' in url:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry["name"] +
                    '[/COLOR]')

                title = entry["files"][0]["name"]
                url2 = entry["files"][0]["downloadUrl"]

            else:
                title = entry["name"]
                url2 = entry["downloadUrl"]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                '',
                '',
                output_parameter_handler)
            progress_.VSclose(progress_)

        if not search:
            numPage += 1
            url = re.sub('page=([0-9])', 'page=' + str(numPage), url)
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('numPage', numPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showLiens',
                'Page ' + str(numPage),
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    hoster_url = url
    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, movie_title,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showInfo():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<i class="sprite sprite-.+?"></i>.+?<li tooltip="([^"]+)" class="([^"]+)">'

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

            sDisponible = entry[1].replace('on', 'Disponible')\
                                   .replace('off', 'Non Disponible')
            sHebergeur = entry[0]

            display_title = ('%s (%s)') % (sHebergeur, sDisponible)

            output_parameter_handler.addParameter('movie_title', display_title)

            gui.addText(SITE_IDENTIFIER, display_title)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()


def RenewToken():
    refreshTok = Addon().getSetting('hoster_debridlink_tokenrefresh')
    if refreshTok == "":
        request_handler = RequestHandler(URL_HOST + "/api/oauth/device/code")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addParameters(
            'client_id', Addon().getSetting('hoster_debridlink_ID'))
        r = json.loads(request_handler.request())

        dialog().VSok(
            'Allez sur la page : https://debrid-link.fr/device\n et rentrer le code ' +
            r["user_code"] +
            ' pour autorisez la connection')

        request_handler = RequestHandler(URL_HOST + "/api/oauth/token")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addParameters(
            'client_id', Addon().getSetting('hoster_debridlink_ID'))
        request_handler.addParameters("code", r["device_code"])
        request_handler.addParameters(
            "grant_type", "http://oauth.net/grant_type/device/1.0")
        r = json.loads(request_handler.request())

        Addon().setSetting(
            'hoster_debridlink_tokenrefresh',
            r["refresh_token"])
        Addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]

    else:
        request_handler = RequestHandler(URL_HOST + "/api/oauth/token")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addParameters(
            'client_id', Addon().getSetting('hoster_debridlink_ID'))
        request_handler.addParameters("refresh_token", refreshTok)
        request_handler.addParameters("grant_type", "refresh_token")
        r = json.loads(request_handler.request())

        Addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]
