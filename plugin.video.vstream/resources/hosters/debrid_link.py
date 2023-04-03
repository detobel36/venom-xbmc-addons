# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.handler.requestHandler import RequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import Addon, dialog

URL_HOST = "https://debrid-link.fr"


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'debrid_link', 'Debrid Link', 'violet')

    def _getMediaLinkForGuest(self, auto_play=False):
        token_debrid_link = "Bearer " + Addon().getSetting('hoster_debridlink_token')

        request_handler = RequestHandler(URL_HOST + '/api/downloader/add')
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Accept', 'application/json')
        request_handler.addHeaderEntry('Authorization', token_debrid_link)
        request_handler.addHeaderEntry(
            'Content-Type', "application/x-www-form-urlencoded")
        request_handler.addParameters("link", self._url)
        text = json.loads(request_handler.request())

        if text["result"] == "KO":
            if text["ERR"] == 'badToken':
                new_token = renewToken()

                request_handler = RequestHandler(
                    URL_HOST + '/api/downloader/add')
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry('Accept', 'application/json')
                request_handler.addHeaderEntry('Authorization', new_token)
                request_handler.addHeaderEntry(
                    'Content-Type', "application/x-www-form-urlencoded")
                request_handler.addParameters("link", self._url)
                text = json.loads(request_handler.request())

        api_call = text["value"]["downloadLink"]

        if text:
            return True, api_call

        return False, False


def renewToken():
    refreshTok = Addon().getSetting('hoster_debridlink_tokenrefresh')
    if refreshTok == "":
        request_handler = RequestHandler(URL_HOST + "/api/oauth/device/code")
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addParameters(
            'client_id', Addon().getSetting('hoster_debridlink_ID'))
        r = json.loads(request_handler.request())

        dialog().VSok('Allez sur la page : https://debrid-link.fr/device\n' +
                      'et rentrer le code ' + r["user_code"] + ' pour autorisez la connection')

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
