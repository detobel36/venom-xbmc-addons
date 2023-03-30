# -*- coding: utf-8 -*-
# Venom.
from resources.lib.config import cConfig
from resources.lib.db import Db
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler

import urllib
import re
import xbmc
import md5
import unicodedata

try:
    import json
except BaseException:
    import simplejson as json

SITE_IDENTIFIER = 'cBseries'
SITE_NAME = 'Betaseries'

API_KEY = '56ab1fd1ef57'
API_VERS = '2.4'
API_URL = 'https://api.betaseries.com'


class cBseries:

    def __init__(self):
        # self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        # self.__sFunctionName = ''

    def getToken(self):

        sUrl = 'https://api.betaseries.com/members/auth'
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)

        oRequestHandler.addParameters('login', cConfig().getSetting('bs_login'))

        passw = md5.new(cConfig().getSetting('bs_pass')).hexdigest()
        oRequestHandler.addParameters('password', passw)

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)

        total = len(sHtmlContent)

        if (total > 0):
            # self.__Token  = result['token']
            cConfig().setSetting('bstoken', str(result['token']))
            xbmc.executebuiltin("Container.Refresh")
            return
        return False

    def delFavourites(self):

        input_parameter_handler = InputParameterHandler()
        siteUrl = input_parameter_handler.getValue('siteUrl')
        sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

        meta = {}
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['siteurl'] = siteUrl
        try:
            Db().del_favorite(meta)
        except BaseException:
            pass

        return

    def getLoad(self):

        # self.getToken()
        oGui = Gui()

        if cConfig().getSetting("bstoken") == '':
            self.getToken()
        else:
            oRequestHandler = RequestHandler('https://api.betaseries.com/members/infos')
            oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
            oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
            oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
            # n'affiche pas les infos des films
            oRequestHandler.addParameters('summary', 'false')

            sHtmlContent = oRequestHandler.request()
            result = json.loads(sHtmlContent)

            # xbmc.log(str(result))

            total = len(sHtmlContent)

            if (total > 0):

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', 'https://')
                oGui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR khaki]Bonjour, ' +
                    result['member']['login'] +
                    '[/COLOR]',
                    output_parameter_handler)

                # for i in result['shows']:
                # sId, sTitle = i['id'], i['name']
                if (result['member']['stats']['shows'] > 0):
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/members/infos')
                    output_parameter_handler.addParameter('param', 'shows')
                    oGui.addDir(SITE_IDENTIFIER,
                                'getBseries',
                                'Series (' + str(result['member']['stats']['shows']) + ')',
                                'mark.png',
                                output_parameter_handler)

                if (result['member']['stats']['movies'] > 0):
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/members/infos')
                    output_parameter_handler.addParameter('param', 'movies')
                    oGui.addDir(SITE_IDENTIFIER,
                                'getBseries',
                                'Films (' + str(result['member']['stats']['movies']) + ')',
                                'mark.png',
                                output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/movies/member')
        oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Films (favories)', 'mark.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/shows/member')
        oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Series (favories)', 'mark.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/timeline/member')
        oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Testt (favories)', 'mark.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://')
        output_parameter_handler.addParameter('userID', result['member']['id'])
        oGui.addDir(SITE_IDENTIFIER, 'getBtimeline', 'Timeline', 'mark.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'https://api.betaseries.com/members/destroy')
        oGui.addDir(SITE_IDENTIFIER, 'getBsout', 'Deconnection', 'mark.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def getBtimeline(self):

        import datetime
        import time
        # self.getToken()
        oGui = Gui()

        input_parameter_handler = InputParameterHandler()
        userID = input_parameter_handler.getValue('userID')

        # timeline
        oRequestHandler = RequestHandler('https://api.betaseries.com/timeline/member')
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        oRequestHandler.addParameters('id', userID)

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)

        # xbmc.log(str(result))

        total = len(sHtmlContent)
        if (total > 0):
            for i in result['events']:
                sHtml = unicodedata.normalize('NFD', i['html']).encode('ascii', 'ignore').decode("unicode_escape")
                sHtml.encode("utf-8")  # on repasse en utf-8
                titre = re.sub('<a href(.+?)>|<\\/a>', '', sHtml)

                xbmc.log(str(i['date']))
                # 2016-11-14 09:50:35
                # date = datetime.datetime.strptime("2016-11-14", "%Y-%m-%d")
                date = datetime.datetime(
                    *(time.strptime(i['date'], "%Y-%m-%d %H:%M:%S")[0:6])).strftime('%d-%m-%Y %H:%M')

                sTitle = ('%s - %s') % (date, titre)
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', 'http://')
                oGui.addText(SITE_IDENTIFIER, sTitle, output_parameter_handler)

        oGui.setEndOfDirectory()

    def getBsout(self):

        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oGui = Gui()

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        # api buguer normalement ça affiche que les films et series
        oRequestHandler.addParameters('token', cConfig().getSetting("bstoken"))

        oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)
        total = len(sHtmlContent)
        if (total > 0):
            cConfig().setSetting('bstoken', '')
            oGui.showNofication('Vous avez ?t? d?connect? avec succ?s')
            xbmc.executebuiltin("Container.Refresh")

        return

    def getBseries(self):

        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sParam = input_parameter_handler.getValue('param')

        oGui = Gui()

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        # api buguer normalement ça affiche que les films et series
        # oRequestHandler.addParameters('only', 'true')

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)

        xbmc.log(str(result))

        total = len(sHtmlContent)

        if (total > 0):
            for i in result['member'][sParam]:
                if sParam == 'shows':
                    sId, sImdb_id, sTitle, sDesc, sSeasons, sEpisodes, sThumb, sRemaining, sLast = i['id'], i['imdb_id'], i['title'], i[
                        'description'], i['seasons'], i['episodes'], i['images']['show'], i['user']['remaining'], i['user']['last']

                    sTitle = ('%s - Saisons (%s) / Episodes (%s/%s) / Dernier %s') % (sTitle.encode("utf-8"),
                                                                                      sSeasons, sRemaining, sEpisodes, sLast)
                else:
                    sId, sImdb_id, sTitle, sDesc, sYear, sThumb, sStatus = i['id'], i['imdb_id'], i['title'], i['synopsis'], i['production_year'], i['poster'], str(
                        i['user']['status'])

                    sStatus = sStatus.replace('0', 'Non vue').replace('1', 'Vue').replace('2', 'Ne pas voir')

                    sTitle = ('%s - (%s) / %s') % (sTitle.encode("utf-8"), int(sYear), sStatus)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', 'http://')

                oGuiElement = GuiElement()

                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('load')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setIcon("mark.png")
                oGuiElement.setMeta(0)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setTmdbId(sImdb_id)
                oGuiElement.setDescription(sDesc)
                # oGuiElement.setFanart(fanart)

                # oGui.createContexMenuDelFav(oGuiElement, output_parameter_handler)

                # oGui.addHost(oGuiElement, output_parameter_handler)
                oGui.addFolder(oGuiElement, output_parameter_handler)
                # oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', output_parameter_handler)

            oGui.setEndOfDirectory()
        return

    def getBseries2(self):
        oGui = Gui()

        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        # aParams = input_parameter_handler.getAllParameter()

        iPage = 1
        if (input_parameter_handler.exist('page')):
            iPage = input_parameter_handler.getValue('page')

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        # oRequestHandler.addParameters('start', iPage)

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)

        xbmc.log(str(result))

        total = len(sHtmlContent)

        try:
            row = Db().get_favorite()

            for data in row:

                title = data[1]
                siteurl = urllib.unquote_plus(data[2])
                site = data[3]
                function = data[4]
                cat = data[5]
                thumbnail = data[6]
                fanart = data[7]

                if thumbnail == '':
                    thumbnail = 'False'

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', siteurl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumbnail', thumbnail)

                if (function == 'play'):
                    oHoster = HosterGui().checkHoster(siteurl)
                    output_parameter_handler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    output_parameter_handler.addParameter('sFileName', oHoster.getFileName())
                    output_parameter_handler.addParameter('sMediaUrl', siteurl)

                if (cat == sCat):
                    oGuiElement = GuiElement()

                    oGuiElement.setSiteName(site)
                    oGuiElement.setFunction(function)
                    oGuiElement.setTitle(title)
                    oGuiElement.setIcon("mark.png")
                    oGuiElement.setMeta(0)
                    oGuiElement.setThumbnail(thumbnail)
                    oGuiElement.setFanart(fanart)

                    oGui.createContexMenuDelFav(oGuiElement, output_parameter_handler)

                    if (function == 'play'):
                        oGui.addHost(oGuiElement, output_parameter_handler)
                    else:
                        oGui.addFolder(oGuiElement, output_parameter_handler)

                    # oGui.addFav(site, function, title, "mark.png", thumbnail, fanart, output_parameter_handler)

            oGui.setEndOfDirectory()
        except BaseException:
            pass
        return

    def setFavorite(self):
        input_parameter_handler = InputParameterHandler()
        # xbmc.log(str(input_parameter_handler.getAllParameter()))

        if int(input_parameter_handler.getValue('sCat')) < 1:
            cConfig().showInfo('Error', 'Mise en Favoris non possible pour ce lien')
            return

        meta = {}
        meta['siteurl'] = input_parameter_handler.getValue('siteUrl')
        meta['site'] = input_parameter_handler.getValue('sId')
        meta['fav'] = input_parameter_handler.getValue('sFav')
        meta['cat'] = input_parameter_handler.getValue('sCat')

        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            Db().insert_favorite(meta)
        except BaseException:
            pass
