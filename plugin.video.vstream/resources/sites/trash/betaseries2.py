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

        url = 'https://api.betaseries.com/members/auth'
        request_handler = RequestHandler(url)
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)

        request_handler.addParameters(
            'login', cConfig().getSetting('bs_login'))

        passw = md5.new(cConfig().getSetting('bs_pass')).hexdigest()
        request_handler.addParameters('password', passw)

        html_content = request_handler.request()
        result = json.loads(html_content)

        total = len(html_content)

        if (total > 0):
            # self.__Token  = result['token']
            cConfig().setSetting('bstoken', str(result['token']))
            xbmc.executebuiltin("Container.Refresh")
            return
        return False

    def delFavourites(self):

        input_parameter_handler = InputParameterHandler()
        site_url = input_parameter_handler.getValue('site_url')
        movie_title = input_parameter_handler.getValue('movie_title')

        meta = {}
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['siteurl'] = site_url
        try:
            Db().del_favorite(meta)
        except BaseException:
            pass

        return

    def getLoad(self):

        # self.getToken()
        gui = Gui()

        if cConfig().getSetting("bstoken") == '':
            self.getToken()
        else:
            request_handler = RequestHandler(
                'https://api.betaseries.com/members/infos')
            request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
            request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
            request_handler.addHeaderEntry(
                'Authorization', cConfig().getSetting("bstoken"))
            # n'affiche pas les infos des films
            request_handler.addParameters('summary', 'false')

            html_content = request_handler.request()
            result = json.loads(html_content)

            # xbmc.log(str(result))

            total = len(html_content)

            if (total > 0):

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', 'https://')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR khaki]Bonjour, ' +
                    result['member']['login'] +
                    '[/COLOR]',
                    output_parameter_handler)

                # for i in result['shows']:
                # s_id, title = i['id'], i['name']
                if (result['member']['stats']['shows'] > 0):
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter(
                        'site_url', 'https://api.betaseries.com/members/infos')
                    output_parameter_handler.addParameter('param', 'shows')
                    gui.addDir(SITE_IDENTIFIER, 'getBseries', 'Series (' +
                               str(result['member']['stats']['shows']) +
                               ')', 'mark.png', output_parameter_handler)

                if (result['member']['stats']['movies'] > 0):
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter(
                        'site_url', 'https://api.betaseries.com/members/infos')
                    output_parameter_handler.addParameter('param', 'movies')
                    gui.addDir(SITE_IDENTIFIER, 'getBseries', 'Films (' +
                               str(result['member']['stats']['movies']) +
                               ')', 'mark.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', 'https://api.betaseries.com/movies/member')
        gui.addDir(
            SITE_IDENTIFIER,
            'getBseries',
            'Films (favories)',
            'mark.png',
            output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', 'https://api.betaseries.com/shows/member')
        gui.addDir(
            SITE_IDENTIFIER,
            'getBseries',
            'Series (favories)',
            'mark.png',
            output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', 'https://api.betaseries.com/timeline/member')
        gui.addDir(
            SITE_IDENTIFIER,
            'getBseries',
            'Testt (favories)',
            'mark.png',
            output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://')
        output_parameter_handler.addParameter('userID', result['member']['id'])
        gui.addDir(
            SITE_IDENTIFIER,
            'getBtimeline',
            'Timeline',
            'mark.png',
            output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', 'https://api.betaseries.com/members/destroy')
        gui.addDir(
            SITE_IDENTIFIER,
            'getBsout',
            'Deconnection',
            'mark.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def getBtimeline(self):

        import datetime
        import time
        # self.getToken()
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        userID = input_parameter_handler.getValue('userID')

        # timeline
        request_handler = RequestHandler(
            'https://api.betaseries.com/timeline/member')
        request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        request_handler.addHeaderEntry(
            'Authorization', cConfig().getSetting("bstoken"))
        request_handler.addParameters('id', userID)

        html_content = request_handler.request()
        result = json.loads(html_content)

        # xbmc.log(str(result))

        total = len(html_content)
        if (total > 0):
            for i in result['events']:
                sHtml = unicodedata.normalize(
                    'NFD', i['html']).encode(
                    'ascii', 'ignore').decode("unicode_escape")
                sHtml.encode("utf-8")  # on repasse en utf-8
                titre = re.sub('<a href(.+?)>|<\\/a>', '', sHtml)

                xbmc.log(str(i['date']))
                # 2016-11-14 09:50:35
                # date = datetime.datetime.strptime("2016-11-14", "%Y-%m-%d")
                date = datetime.datetime(
                    *(time.strptime(i['date'], "%Y-%m-%d %H:%M:%S")[0:6])).strftime('%d-%m-%Y %H:%M')

                title = ('%s - %s') % (date, titre)
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', 'http://')
                gui.addText(SITE_IDENTIFIER, title, output_parameter_handler)

        gui.setEndOfDirectory()

    def getBsout(self):

        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        gui = Gui()

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        request_handler.addHeaderEntry(
            'Authorization', cConfig().getSetting("bstoken"))
        # api buguer normalement ça affiche que les films et series
        request_handler.addParameters('token', cConfig().getSetting("bstoken"))

        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        html_content = request_handler.request()
        result = json.loads(html_content)
        total = len(html_content)
        if (total > 0):
            cConfig().setSetting('bstoken', '')
            gui.showNofication('Vous avez ?t? d?connect? avec succ?s')
            xbmc.executebuiltin("Container.Refresh")

        return

    def getBseries(self):

        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        sParam = input_parameter_handler.getValue('param')

        gui = Gui()

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        request_handler.addHeaderEntry(
            'Authorization', cConfig().getSetting("bstoken"))
        # api buguer normalement ça affiche que les films et series
        # request_handler.addParameters('only', 'true')

        html_content = request_handler.request()
        result = json.loads(html_content)

        xbmc.log(str(result))

        total = len(html_content)

        if (total > 0):
            for i in result['member'][sParam]:
                if sParam == 'shows':
                    s_id, sImdb_id, title, desc, sSeasons, sEpisodes, thumb, sRemaining, sLast = i['id'], i['imdb_id'], i['title'], i[
                        'description'], i['seasons'], i['episodes'], i['images']['show'], i['user']['remaining'], i['user']['last']

                    title = ('%s - Saisons (%s) / Episodes (%s/%s) / Dernier %s') % (
                        title.encode("utf-8"), sSeasons, sRemaining, sEpisodes, sLast)
                else:
                    s_id, sImdb_id, title, desc, year, thumb, sStatus = i['id'], i['imdb_id'], i[
                        'title'], i['synopsis'], i['production_year'], i['poster'], str(i['user']['status'])

                    sStatus = sStatus.replace(
                        '0',
                        'Non vue').replace(
                        '1',
                        'Vue').replace(
                        '2',
                        'Ne pas voir')

                    title = (
                        '%s - (%s) / %s') % (title.encode("utf-8"), int(year), sStatus)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', 'http://')

                gui_element = GuiElement()

                gui_element.setSiteName(SITE_IDENTIFIER)
                gui_element.setFunction('load')
                gui_element.setTitle(title)
                gui_element.setIcon("mark.png")
                gui_element.setMeta(0)
                gui_element.setThumbnail(thumb)
                gui_element.setTmdbId(sImdb_id)
                gui_element.setDescription(desc)
                # gui_element.setFanart(fanart)

                # gui.createContexMenuDelFav(gui_element, output_parameter_handler)

                # gui.addHost(gui_element, output_parameter_handler)
                gui.addFolder(gui_element, output_parameter_handler)
                # gui.addDir(SITE_IDENTIFIER, 'showMovies', title, 'next.png', output_parameter_handler)

            gui.setEndOfDirectory()
        return

    def getBseries2(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        # aParams = input_parameter_handler.getAllParameter()

        iPage = 1
        if (input_parameter_handler.exist('page')):
            iPage = input_parameter_handler.getValue('page')

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        request_handler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        request_handler.addHeaderEntry(
            'Authorization', cConfig().getSetting("bstoken"))
        # request_handler.addParameters('start', iPage)

        html_content = request_handler.request()
        result = json.loads(html_content)

        xbmc.log(str(result))

        total = len(html_content)

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
                output_parameter_handler.addParameter('site_url', siteurl)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumbnail', thumbnail)

                if (function == 'play'):
                    hoster = HosterGui().checkHoster(siteurl)
                    output_parameter_handler.addParameter(
                        'hoster_identifier', hoster.getPluginIdentifier())
                    output_parameter_handler.addParameter(
                        'file_name', hoster.getFileName())
                    output_parameter_handler.addParameter('media_url', siteurl)

                if (cat == cat):
                    gui_element = GuiElement()

                    gui_element.setSiteName(site)
                    gui_element.setFunction(function)
                    gui_element.setTitle(title)
                    gui_element.setIcon("mark.png")
                    gui_element.setMeta(0)
                    gui_element.setThumbnail(thumbnail)
                    gui_element.setFanart(fanart)

                    gui.createContexMenuDelFav(
                        gui_element, output_parameter_handler)

                    if (function == 'play'):
                        gui.addHost(gui_element, output_parameter_handler)
                    else:
                        gui.addFolder(gui_element, output_parameter_handler)

                    # gui.addFav(site, function, title, "mark.png", thumbnail, fanart, output_parameter_handler)

            gui.setEndOfDirectory()
        except BaseException:
            pass
        return

    def setFavorite(self):
        input_parameter_handler = InputParameterHandler()
        # xbmc.log(str(input_parameter_handler.getAllParameter()))

        if int(input_parameter_handler.getValue('cat')) < 1:
            cConfig().showInfo('Error', 'Mise en Favoris non possible pour ce lien')
            return

        meta = {}
        meta['siteurl'] = input_parameter_handler.getValue('site_url')
        meta['site'] = input_parameter_handler.getValue('s_id')
        meta['fav'] = input_parameter_handler.getValue('fav')
        meta['cat'] = input_parameter_handler.getValue('cat')

        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            Db().insert_favorite(meta)
        except BaseException:
            pass
