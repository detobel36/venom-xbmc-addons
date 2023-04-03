# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import datetime
import re
import time
import unicodedata
import xbmc

from resources.lib.comaddon import Addon, dialog, Progress, VSlog
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.util import Quote

SITE_IDENTIFIER = 'cTrakt'
SITE_NAME = 'Trakt'

URL_API = 'https://api.trakt.tv/'

API_KEY = '7139b7dace25c7bdf0bd79acf46fb02bd63310548b1f671d88832f75a4ac3dd6'
API_SECRET = 'bb02b2b0267b045590bc25c21dac21b1c47446a62b792091b3275e9c4a943e74'
API_VERS = '2'

MAXRESULT = Addon().getSetting('trakt_number_element')


class cTrakt:
    CONTENT = '0'
    ADDON = Addon()
    DIALOG = dialog()

    def __init__(self):
        self.__sTitle = ''
        self.__sAction = ''
        self.__sType = ''

    def getToken(self):
        request_handler = RequestHandler(URL_API + 'oauth/device/code')
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addJSONEntry('client_id', API_KEY)
        html_content = request_handler.request(json_decode=True)

        total = len(html_content)

        if total > 0:
            text = (self.ADDON.VSlang(30304)) % (html_content['verification_url'], html_content['user_code'])

            dialog_result = self.DIALOG.VSyesno(text)
            if dialog_result == 0:
                return False

            if dialog_result == 1:
                try:
                    request_handler = RequestHandler(URL_API + 'oauth/device/token')
                    request_handler.setRequestType(1)
                    request_handler.addHeaderEntry('Content-Type', 'application/json')
                    request_handler.addJSONEntry('client_id', API_KEY)
                    request_handler.addJSONEntry('client_secret', API_SECRET)
                    request_handler.addJSONEntry('code', html_content['device_code'])
                    html_content = request_handler.request(json_decode=True)

                    if html_content['access_token']:
                        self.ADDON.setSetting('bstoken', str(html_content['access_token']))
                        self.DIALOG.VSinfo(self.ADDON.VSlang(30000))
                        return
                except BaseException:
                    pass

            return
        return

    def search(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'https://')
        output_parameter_handler.addParameter('type', 'movie')
        gui.addDir('themoviedb_org', 'showSearchMovie', self.ADDON.VSlang(30423), 'films.png', output_parameter_handler)

        output_parameter_handler.addParameter('type', 'show')
        gui.addDir('themoviedb_org', 'showSearchSerie', self.ADDON.VSlang(30424), 'series.png',
                   output_parameter_handler)

        gui.setEndOfDirectory()

    def getLoad(self):
        # pour regen le token()
        # self.getToken()
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        if self.ADDON.getSetting('bstoken') == '':
            VSlog('bstoken invalid')
            output_parameter_handler.addParameter('site_url', 'https://')
            output_parameter_handler.addParameter('type', 'movie')
            gui.addDir(SITE_IDENTIFIER, 'getToken', self.ADDON.VSlang(30305), 'trakt.png', output_parameter_handler)
        else:
            # nom de l'user
            try:
                request_handler = RequestHandler(URL_API + 'users/me')
                request_handler.addHeaderEntry('Content-Type', 'application/json')
                request_handler.addHeaderEntry('trakt-api-key', API_KEY)
                request_handler.addHeaderEntry('trakt-api-version', API_VERS)
                request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                html_content = request_handler.request(json_decode=True)
            except BaseException:
                return self.getToken()

            if len(html_content) > 0:
                username = html_content['username']
                output_parameter_handler.addParameter('site_url', 'https://')
                gui.addText(SITE_IDENTIFIER, (self.ADDON.VSlang(30306)) % username)

            output_parameter_handler.addParameter('site_url', 'https://')
            output_parameter_handler.addParameter('type', 'movie')
            gui.addDir(SITE_IDENTIFIER, 'search', self.ADDON.VSlang(30330), 'search.png', output_parameter_handler)

            output_parameter_handler.addParameter('type', 'movie')
            gui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30120), 'films.png', output_parameter_handler)

            output_parameter_handler.addParameter('type', 'show')
            gui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30121), 'series.png', output_parameter_handler)

            if self.ADDON.getSetting('trakt_show_lists') == 'true':
                output_parameter_handler.addParameter('type', 'custom-lists')
                gui.addDir(SITE_IDENTIFIER, 'menuList', "Listes", 'trakt.png', output_parameter_handler)

            output_parameter_handler.addParameter('site_url',
                                                  URL_API + 'users/me/history?page=1&limit=' + str(MAXRESULT))
            gui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30308), 'trakt.png', output_parameter_handler)

            output_parameter_handler.addParameter('site_url', URL_API + 'oauth/revoke')
            gui.addDir(SITE_IDENTIFIER, 'getCalendrier', self.ADDON.VSlang(30331), 'trakt.png',
                       output_parameter_handler)

            output_parameter_handler.addParameter('site_url', URL_API + 'oauth/revoke')
            gui.addDir(SITE_IDENTIFIER, 'getBsout', self.ADDON.VSlang(30309), 'trakt.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def menuList(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'https://')
        output_parameter_handler.addParameter('type', 'lists-tendances')
        gui.addDir(SITE_IDENTIFIER, 'getLists', "Listes tendances", 'trakt.png', output_parameter_handler)

        output_parameter_handler.addParameter('type', 'lists-pop')
        gui.addDir(SITE_IDENTIFIER, 'getLists', "Listes populaires", 'trakt.png', output_parameter_handler)

        output_parameter_handler.addParameter('type', 'custom-lists')
        gui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30360), 'trakt.png', output_parameter_handler)

        output_parameter_handler.addParameter('type', 'liked-lists')
        gui.addDir(SITE_IDENTIFIER, 'getLists', 'Mes listes aimées', 'trakt.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def getCalendrier(self):
        gui = Gui()

        today_date = str(datetime.datetime.now().date())

        # DANGER ca rame, freeze
        liste = [['Mes sorties sur les 7 jours à venir', URL_API + 'calendars/my/shows/' + today_date + '/7'],
                 ['Mes sorties sur les 30 jours à venir', URL_API + 'calendars/my/shows/' + today_date + '/30'],
                 ['Nouveautées sur 7 jours', URL_API + 'calendars/all/shows/new/' + today_date + '/7']]

        for title, url in liste:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(SITE_IDENTIFIER, 'getTrakt', title, 'genres.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def getLists(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        _type = input_parameter_handler.getValue('type')

        # stats user
        request_handler = RequestHandler(URL_API + 'users/me/stats')
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        html_content = request_handler.request(json_decode=True)

        liste = []
        if _type == 'movie':
            liste.append(['%s (%s)' % (self.ADDON.VSlang(30310), html_content['movies']['collected']),
                          URL_API + 'users/me/collection/movies'])

            if self.ADDON.getSetting('trakt_movies_show_watchlist') == 'true':
                liste.append([self.ADDON.VSlang(30311),
                              URL_API + 'users/me/watchlist/movies?page=1&limit=' + str(MAXRESULT)])

            if self.ADDON.getSetting('trakt_movies_show_watched') == 'true':
                liste.append(['%s (%s)' % (self.ADDON.VSlang(30312), html_content['movies']['watched']),
                              URL_API + 'users/me/watched/movies'])

            if self.ADDON.getSetting('trakt_movies_show_recommended') == 'true':
                liste.append([self.ADDON.VSlang(30313), URL_API + 'recommendations/movies'])

            if self.ADDON.getSetting('trakt_movies_show_boxoffice') == 'true':
                liste.append([self.ADDON.VSlang(30314), URL_API + 'movies/boxoffice'])

            if self.ADDON.getSetting('trakt_movies_show_popular') == 'true':
                liste.append([self.ADDON.VSlang(30315), URL_API + 'movies/popular'])

            if self.ADDON.getSetting('trakt_movies_show_most_weekly') == 'true':
                liste.append([self.ADDON.VSlang(30316), URL_API + 'movies/played/weekly'])

            if self.ADDON.getSetting('trakt_movies_show_most_monthly') == 'true':
                liste.append([self.ADDON.VSlang(30317), URL_API + 'movies/played/monthly'])

        elif _type == 'show':
            liste.append(['%s (%s)' % (self.ADDON.VSlang(30310), html_content['shows']['collected']),
                          URL_API + 'users/me/collection/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist') == 'true':
                liste.append([self.ADDON.VSlang(30311), URL_API + 'users/me/watchlist/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist_seasons') == 'true':
                liste.append([self.ADDON.VSlang(30318), URL_API + 'users/me/watchlist/seasons'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist_episodes') == 'true':
                liste.append([self.ADDON.VSlang(30319), URL_API + 'users/me/watchlist/episodes'])

            if self.ADDON.getSetting('trakt_tvshows_show_watched') == 'true':
                liste.append(['%s (%s)' % (self.ADDON.VSlang(30312), html_content['shows']['watched']),
                              URL_API + 'users/me/watched/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_recommended') == 'true':
                liste.append([self.ADDON.VSlang(30313), URL_API + 'recommendations/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_popular') == 'true':
                liste.append([self.ADDON.VSlang(30315), URL_API + 'shows/popular'])

            if self.ADDON.getSetting('trakt_tvshows_show_most_weekly') == 'true':
                liste.append([self.ADDON.VSlang(30316), URL_API + 'shows/played/weekly'])

            if self.ADDON.getSetting('trakt_tvshows_show_most_monthly') == 'true':
                liste.append([self.ADDON.VSlang(30317), URL_API + 'shows/played/monthly'])

        elif _type == 'custom-lists':
            request_handler = RequestHandler(URL_API + 'users/me/lists')
            request_handler.addHeaderEntry('Content-Type', 'application/json')
            request_handler.addHeaderEntry('trakt-api-key', API_KEY)
            request_handler.addHeaderEntry('trakt-api-version', API_VERS)
            request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
            html_content = request_handler.request(json_decode=True)

            for List in html_content:
                url = URL_API + 'users/me/lists/' + List['ids']['slug'] + '/items'
                liste.append([self.decode((List['name'] + ' (' + str(List['item_count']) + ')')), url])

        elif _type == 'liked-lists' or _type == 'lists-tendances' or _type == 'lists-pop':
            if _type == 'liked-lists':
                url = URL_API + '/users/likes/lists'
            elif _type == "lists-tendances":
                url = URL_API + '/lists/trending'
            elif _type == 'lists-pop':
                url = URL_API + 'lists/popular'

            request_handler = RequestHandler(url)
            request_handler.addHeaderEntry('Content-Type', 'application/json')
            request_handler.addHeaderEntry('trakt-api-key', API_KEY)
            request_handler.addHeaderEntry('trakt-api-version', API_VERS)
            request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
            html_content = request_handler.request(json_decode=True)

            for List in html_content:
                if _type == 'liked-lists':
                    url = URL_API + 'users/' + List['list']['user']['ids']['slug'] + '/lists/' + \
                          List['list']['ids']['slug'] + '/items'
                else:
                    url = URL_API + '/lists/' + List['list']['ids']['slug'] + '/items'

                liste.append([self.decode(
                    (List['list']['name'] + ' (' + str(List['list']['item_count']) + ')')), url])

        for title, url in liste:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(SITE_IDENTIFIER, 'getTrakt', title, 'genres.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def getBsout(self):
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        request_handler.addJSONEntry('client_id', API_KEY)
        request_handler.addJSONEntry('client_secret', API_SECRET)
        request_handler.addJSONEntry('token', self.ADDON.getSetting('bstoken'))
        html_content = request_handler.request()

        if len(html_content) > 0:
            self.ADDON.setSetting('bstoken', '')
            self.DIALOG.VSinfo(self.ADDON.VSlang(30320))
            xbmc.executebuiltin('Container.Refresh')

    def decode(self, elem, with_unicode=False):
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            return elem
        else:
            if with_unicode:
                try:
                    elem = unicodedata.normalize('NFD', unicode(elem)).encode('ascii', 'ignore')\
                        .decode('unicode_escape')
                except UnicodeDecodeError:
                    elem = elem.decode('utf-8')
                except BaseException:
                    pass

            return elem.encode('utf-8')

    def getTrakt(self, url2=None):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        if url2:
            url = url2
            current_limit = False
        else:
            current_limit = input_parameter_handler.getValue('limite')
            url = input_parameter_handler.getValue('site_url')

        url = url + "?page=1&limit=" + MAXRESULT

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        html_content = request_handler.request(json_decode=True)
        headers = request_handler.getResponseHeader()

        # Fonctionnement specifique au calendrier.
        if 'X-Pagination-Page-Count' not in headers:
            if not current_limit:
                current_limit = 0
            else:
                # Supprimer les elements deja afficher.
                html_content = html_content[int(current_limit):]

            if len(html_content) > 20:
                total = int(MAXRESULT)
            else:
                total = len(html_content)
        else:
            total = len(html_content)

        if 'X-Pagination-Page' in headers:
            page = headers['X-Pagination-Page']
        if 'X-Pagination-Page-Count' in headers:
            max_page = headers['X-Pagination-Page-Count']

        key = 0
        function = 'getLoad'
        s_id = SITE_IDENTIFIER
        searchtext = ''
        old_date = None

        if total > 0:
            progress_ = Progress().VScreate(SITE_NAME)

            for i in html_content:
                # Limite les elements du calendrier
                if 'X-Pagination-Page-Count' not in headers:
                    if progress_.getProgress() >= int(MAXRESULT):
                        break

                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                if 'collection' in url:

                    try:
                        s_date = i['last_collected_at']
                    except BaseException:
                        s_date = ""

                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        cTrakt.CONTENT = '2'
                        function = 'getBseasons'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']

                        cTrakt.CONTENT = '1'
                        function = 'showSearch'
                        s_id = 'globalSearch'

                    title = self.decode(title)
                    searchtext = '%s' % title

                    if year:
                        file = '%s - (%s)' % (title, int(year))
                        title = '%s - (%s)' % (title, int(year))
                    else:
                        file = '%s' % title
                        title = '%s' % title

                elif 'history' in url:
                    # commun
                    function = 'showSearch'
                    s_id = 'globalSearch'
                    if 'episode' in i:
                        type_of_resource = 'Episode'
                        eps = i['episode']
                        title = self.getLocalizedTitle(i, 'episodes')
                        trakt = eps['ids']['trakt']
                        imdb = eps['ids']['imdb']
                        tmdb = eps['ids']['tmdb']
                        season = eps['season']
                        number = eps['number']
                        extra = '(S%02dE%02d)' % (season, number)
                        cTrakt.CONTENT = '2'
                    else:
                        type_of_resource = 'Film'
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        extra = '(%s)' % year
                        cTrakt.CONTENT = '1'

                    title = self.decode(title, with_unicode=True)
                    searchtext = '%s' % title
                    file = '%s - (%s)' % (title, extra)
                    title = '[COLOR gold]%s %s [/COLOR]- %s %s' % (type_of_resource, 'vu', title, extra)

                elif 'watchlist' in url:
                    # commun
                    function = 'showSearch'
                    s_id = 'globalSearch'

                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        extra = '(%s)' % year
                        cTrakt.CONTENT = '2'
                    elif 'episode' in i:
                        eps = i['episode']
                        title = self.getLocalizedTitle(i, 'episodes')
                        trakt = eps['ids']['trakt']
                        imdb = eps['ids']['imdb']
                        tmdb = eps['ids']['tmdb']
                        season = eps['season']
                        number = eps['number']
                        extra = '(S%02dE%02d)' % (season, number)
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        extra = '(%s)' % year
                        cTrakt.CONTENT = '1'

                    title = self.decode(title, with_unicode=True)
                    searchtext = '%s' % title
                    file = '%s %s' % (title, extra)
                    title = '%s %s' % (title, extra)

                elif 'watched' in url:
                    # commun
                    plays = i['plays']
                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        cTrakt.CONTENT = '2'
                        function = 'getBseasons'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        cTrakt.CONTENT = '1'
                        function = 'showSearch'
                        s_id = 'globalSearch'

                    if title:
                        title = self.decode(title, with_unicode=True)
                        searchtext = '%s' % title
                        file = '%s - %s' % (title, year)
                        title = '%s Lectures - %s (%s)' % (plays, title, year)

                elif 'played' in url:
                    # commun
                    # sWatcher_count = i['watcher_count']
                    # sPlay_count = i['play_count']
                    # sCollected_count = i['collected_count']
                    function = 'showSearch'
                    s_id = 'globalSearch'
                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        cTrakt.CONTENT = '1'

                    title = self.decode(title)
                    searchtext = '%s' % title
                    file = '%s - (%s)' % (title, int(year))
                    title = '%s - (%s)' % (title, int(year))

                elif 'calendars' in url:
                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        first_aired = i['first_aired']

                        saison = i['episode']['season']
                        episode = i['episode']['number']
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        first_aired = i['first_aired']
                        cTrakt.CONTENT = '1'

                    if title:
                        s_date = datetime.datetime(*(time.strptime(first_aired, '%Y-%m-%dT%H:%M:%S.%fZ')[0:6])).\
                            strftime('%d-%m-%Y')
                        if old_date != s_date:
                            old_date = s_date
                            gui.addText(SITE_IDENTIFIER, '[COLOR olive]Episode prévu pour le :' + old_date + '[/COLOR]')

                        title = self.decode(title)
                        searchtext = '%s' % title
                        file = title
                        if year:
                            file += ' - (%s)' % year
                        title = '%s S%02dE%02d' % (self.decode(title, with_unicode=True), saison, episode)

                    function = 'showSearch'
                    s_id = 'globalSearch'

                elif 'search' in url:
                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        cTrakt.CONTENT = '2'
                        function = 'getBseasons'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        cTrakt.CONTENT = '1'
                        function = 'showSearch'
                        s_id = 'globalSearch'

                    title = self.decode(title, with_unicode=True)
                    searchtext = '%s' % title
                    file = '%s - (%s)' % (title, year)
                    title = '%s (%s)' % (title, year)

                elif 'recommendations' in url or 'popular' in url:
                    if 'shows' in url:
                        title = self.getLocalizedTitle(i, 'shows')
                        cTrakt.CONTENT = '2'
                    else:
                        title = self.getLocalizedTitle(i, 'movies')
                        cTrakt.CONTENT = '1'
                    trakt = i['ids']['trakt']
                    imdb = i['ids']['imdb']
                    tmdb = i['ids']['tmdb']
                    year = i['year']
                    title = self.decode(title)
                    searchtext = '%s' % title
                    if year:
                        file = '%s - (%s)' % (title, int(year))
                        title = '%s - (%s)' % (title, int(year))
                    else:
                        file = '%s' % title
                        title = '%s' % title

                    function = 'showSearch'
                    s_id = 'globalSearch'

                elif 'boxoffice' in url:
                    movie = i['movie']
                    title = self.getLocalizedTitle(movie, 'movies')
                    trakt = movie['ids']['trakt']
                    imdb = movie['ids']['imdb']
                    tmdb = movie['ids']['tmdb']
                    year = movie['year']
                    cTrakt.CONTENT = '1'

                    title = self.decode(title)
                    searchtext = '%s' % title
                    file = '%s - (%s)' % (title, int(year))
                    title = '%s - (%s)' % (title, int(year))
                    function = 'showSearch'
                    s_id = 'globalSearch'

                elif 'lists' in url:

                    function = 'showSearch'
                    s_id = 'globalSearch'

                    if 'show' in i:
                        show = i['show']
                        title = self.getLocalizedTitle(show, 'shows')
                        trakt = show['ids']['trakt']
                        imdb = show['ids']['imdb']
                        tmdb = show['ids']['tmdb']
                        year = show['year']
                        extra = '(%s)' % year
                        cTrakt.CONTENT = '2'
                    elif 'episode' in i:
                        eps = i['episode']
                        title = self.getLocalizedTitle(i, 'episodes')
                        trakt = eps['ids']['trakt']
                        imdb = eps['ids']['imdb']
                        tmdb = eps['ids']['tmdb']
                        year = eps['year']
                        season = eps['season']
                        number = eps['number']
                        extra = '(S%02dE%02d)' % (season, number)
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        title = self.getLocalizedTitle(movie, 'movies')
                        trakt = movie['ids']['trakt']
                        imdb = movie['ids']['imdb']
                        tmdb = movie['ids']['tmdb']
                        year = movie['year']
                        extra = '(%s)' % year
                        cTrakt.CONTENT = '1'

                    title = self.decode(title, with_unicode=True)
                    searchtext = '%s' % title
                    file = '%s %s' % (title, extra)
                    title = '%s %s' % (title, extra)

                else:
                    return

                if title:
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url + str(trakt))
                    output_parameter_handler.addParameter('file', file)
                    output_parameter_handler.addParameter('key', key)
                    output_parameter_handler.addParameter('searchtext', searchtext)
                    self.getFolder(gui, s_id, title, file, function, imdb, tmdb, output_parameter_handler)
                    key += 1

            progress_.VSclose(progress_)

            try:
                if page != max_page:
                    next_page = url.replace('page=' + str(page), 'page=' + str(int(page) + 1))
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', next_page)
                    gui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page ' + str(int(page) + 1) + '/' + max_page,
                                output_parameter_handler)
            except BaseException:
                pass

            if 'X-Pagination-Page-Count' not in headers and len(html_content) > int(MAXRESULT):
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('limite', int(current_limit) + int(MAXRESULT))
                gui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page suivante', output_parameter_handler)

        gui.setEndOfDirectory()

    def getBseasons(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        file = input_parameter_handler.getValue('file')
        key = input_parameter_handler.getValue('key')
        searchtext = input_parameter_handler.getValue('searchtext')

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        html_content = request_handler.request(json_decode=True)

        num = 0
        if len(html_content) > 0:
            for i in html_content[int(key)]['seasons']:

                if 'collection' in url or 'watched' in url:
                    number = i['number']
                    cTrakt.CONTENT = '2'
                else:
                    return

                title2 = '%s - (S%02d)' % (self.decode(file), int(number))
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url + str(number))
                output_parameter_handler.addParameter('Key', key)
                output_parameter_handler.addParameter('num', num)
                output_parameter_handler.addParameter('file', file)
                output_parameter_handler.addParameter('title', title2)
                output_parameter_handler.addParameter('searchtext', searchtext)
                self.getFolder(gui, SITE_IDENTIFIER, title2, file, 'getBepisodes', '', '', output_parameter_handler)
                num += 1

        gui.setEndOfDirectory()

    def getLocalizedTitle(self, item, what):
        try:
            if 'episode' not in what:
                request_handler = RequestHandler(URL_API + '%s/%s/translations/fr' % (what, item['ids']['slug']))
                request_handler.addHeaderEntry('Content-Type', 'application/json')
                request_handler.addHeaderEntry('trakt-api-key', API_KEY)
                request_handler.addHeaderEntry('trakt-api-version', API_VERS)
                request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                html_content = request_handler.request(json_decode=True)
            else:
                show_title = self.getLocalizedTitle(item['show'], 'shows')
                t_values = (item['show']['ids']['slug'], item['episode']['season'], item['episode']['number'])

                request_handler = RequestHandler(URL_API + 'shows/%s/seasons/%s/episodes/%s/translations/fr' % t_values)
                request_handler.addHeaderEntry('Content-Type', 'application/json')
                request_handler.addHeaderEntry('trakt-api-key', API_KEY)
                request_handler.addHeaderEntry('trakt-api-version', API_VERS)
                request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                html_content = request_handler.request(json_decode=True)

            title = next((title for title in html_content if title['language'].lower() == 'fr'), item)['title']

            if title is None:
                return item['title']
            else:
                return title if 'episode' not in what else show_title + ' - ' + title

        except BaseException:
            try:
                return item['title']
            except BaseException:
                return item['show']['title']

    def getBepisodes(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        title = input_parameter_handler.getValue('title')
        file = input_parameter_handler.getValue('file')
        key = input_parameter_handler.getValue('key')
        num = input_parameter_handler.getValue('num')
        searchtext = input_parameter_handler.getValue('searchtext')

        cTrakt.CONTENT = '2'

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        html_content = request_handler.request(json_decode=True)

        total = len(html_content)

        number = 0
        if total > 0:
            for i in html_content[int(key)]['seasons'][int(num)]['episodes']:

                if 'collection' in url:
                    number = i['number']
                    title2 = '%s (E%02d)' % (self.decode(title), int(number))

                elif 'watched' in url:
                    number, plays = i['number'], i['plays']
                    title2 = '%s Lectures - %s(E%02d)' % (plays, self.decode(title), int(number))

                else:
                    return

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url + str(number))
                output_parameter_handler.addParameter('file', file)
                output_parameter_handler.addParameter('searchtext', searchtext)
                self.getFolder(gui, 'globalSearch', title2, file, 'showSearch', '', '', output_parameter_handler)

        gui.setEndOfDirectory()
        return

    def getFolder(self, gui, s_id, title, file, function, imdb, tmdb, output_parameter_handler):
        gui_element = GuiElement()
        gui_element.setSiteName(s_id)
        gui_element.setFunction(function)
        gui_element.setTitle(title)
        gui_element.setFileName(file)
        gui_element.setIcon('trakt.png')
        gui_element.setImdbId(imdb)
        gui_element.setTmdbId(tmdb)

        if self.ADDON.getSetting('meta-view') == 'false':
            gui_element.setMetaAddon('true')

        if cTrakt.CONTENT == '2':
            gui_element.setMeta(2)
            gui_element.setCat(2)
            Gui.CONTENT = 'tvshows'
        else:
            gui_element.setMeta(1)
            gui_element.setCat(1)
            Gui.CONTENT = 'movies'

        gui.addFolder(gui_element, output_parameter_handler)

    def getContext(self):
        disp = []
        lang = []
        disp.append(URL_API + 'sync/collection')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30310))

        disp.append(URL_API + 'sync/collection/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]')

        disp.append(URL_API + 'sync/watchlist')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30311))

        disp.append(URL_API + 'sync/watchlist/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]')

        disp.append(URL_API + 'sync/history')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30312))

        disp.append(URL_API + 'sync/history/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]')

        ret = self.DIALOG.VSselect(lang, 'Trakt')

        if ret > -1:
            self.__sAction = disp[ret]
        return self.__sAction

    def getType(self):
        disp = ['movies', 'shows']
        dialog2 = self.DIALOG.Dialog()
        dialog_select = 'Films', 'Series'

        ret = dialog2.select('Trakt', dialog_select)

        if ret > -1:
            self.__sType = disp[ret]
        return self.__sType

    def getAction(self, action_to_execute='', episode=''):
        if self.ADDON.getSetting('bstoken') == '':
            self.DIALOG.VSinfo('Vous devez être connecté')
            return

        input_parameter_handler = InputParameterHandler()

        if not action_to_execute == "SetWatched":
            action = input_parameter_handler.getValue('action')
            if not action:
                action = self.getContext()
            if not action:
                return

        _type = input_parameter_handler.getValue('cat')
        if not _type:
            _type = self.getType()
        # entrer imdb ? venant d'ou?
        imdb = input_parameter_handler.getValue('sImdbId')
        tmdb = input_parameter_handler.getValue('tmdb_id')
        season = False
        episode = False

        # Film, serie, anime, saison, episode
        if _type not in ('1', '2', '3', '4', '8'):
            return

        _type = _type.replace('1', 'movies').replace('2', 'shows').replace('3', 'shows').replace('4', 'shows'). \
            replace('8', 'shows')

        # Mettre en vu automatiquement.
        if action_to_execute == "SetWatched":
            file_name = input_parameter_handler.getValue('file_name')

            if _type == "shows":
                if self.ADDON.getSetting('trakt_tvshows_activate_scrobbling') == 'false':
                    return

                title = input_parameter_handler.getValue('tvshowtitle')
                season = input_parameter_handler.getValue('season')
                if not season:
                    season = re.search('(?i)( s(?:aison +)*([0-9]+(?:\\-[0-9\\?]+)*))', title).group(2)
                if not episode:
                    episode = input_parameter_handler.getValue('sEpisode')
                if not episode:
                    episode = re.search('(?i)(?:^|[^a-z])((?:E|(?:\\wpisode\\s?))([0-9]+(?:[\\-\\.][0-9\\?]+)*))',
                        file_name).group(2)
            else:
                if self.ADDON.getSetting('trakt_movies_activate_scrobbling') == 'false':
                    return
                title = file_name

            action = URL_API + 'sync/history'

            if not title:
                title = input_parameter_handler.getValue('movie_title')
        else:
            title = input_parameter_handler.getValue('movie_title')

        if not imdb:
            if not tmdb:
                tmdb = int(self.getTmdbID(title, _type))

            if not tmdb:
                return
            post = {_type: [{'ids': {'tmdb': tmdb}}]}
            if season:
                post = {_type: [{'ids': {'tmdb': tmdb}, 'seasons': [{'number': int(season)}]}]}
            if episode:
                post = {_type: [{'ids': {'tmdb': tmdb}, 'seasons': [
                    {'number': int(season), 'episodes': [{'number': int(episode)}]}
                ]}]}
        else:
            post = {_type: [{'ids': {'imdb': imdb}}]}

        request_handler = RequestHandler(action)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Content-Type', 'application/json')
        request_handler.addHeaderEntry('trakt-api-key', API_KEY)
        request_handler.addHeaderEntry('trakt-api-version', API_VERS)
        request_handler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        for a in post:
            request_handler.addJSONEntry(a, post[a])
        html_content = request_handler.request(json_decode=True)

        try:
            html_added = html_content['added']
            if html_added['movies'] == 1 or html_added['episodes'] > 0 or html_added['shows'] > 0:
                text = 'Ajouté avec succès'
        except BaseException:
            pass

        try:
            html_updated = html_content['updated']
            if html_updated['movies'] == 1 or html_updated['episodes'] > 0 or html_updated['shows'] > 0:
                text = 'Mise à jour avec succès'
        except BaseException:
            pass

        try:
            html_deleted = html_content['deleted']
            if html_deleted['movies'] == 1 or html_deleted['episodes'] > 0:
                text = 'Supprimé avec succès'
        except BaseException:
            pass

        try:
            html_existing = html_content['existing']
            if html_existing['movies'] > 0 or html_existing['episodes'] > 0 or html_existing['seasons'] > 0 or \
                    html_existing['shows'] > 0:
                text = 'Entrée déjà présente'
        except BaseException:
            pass

        try:
            self.DIALOG.VSinfo(text, 'trakt')
        except UnboundLocalError:
            self.DIALOG.VSinfo("Erreur")

        if input_parameter_handler.exist('sReload'):
            xbmc.executebuiltin('Container.Refresh')
        return

    def createContexTrakt(self, gui, gui_element, output_parameter_handler=''):

        liste = [
            ['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]',
              URL_API + 'sync/collection'],
             ['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]',
              URL_API + 'sync/collection/remove'],
             ['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]',
              URL_API + 'sync/watchlist'],
             ['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]',
              URL_API + 'sync/watchlist/remove'],
             ['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]',
              URL_API + 'sync/history'],
             ['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]',
              URL_API + 'sync/history/remove']
        ]

        for title, url in liste:
            output_parameter_handler = OutputParameterHandler()
            if cTrakt.CONTENT == '2':
                output_parameter_handler.addParameter('_type', 'shows')
            else:
                output_parameter_handler.addParameter('_type', 'movies')
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('action', url)
            output_parameter_handler.addParameter('sReload', True)
            # output_parameter_handler.addParameter('imdb', gui_element.getImdbId())
            output_parameter_handler.addParameter('tmdb_id', gui_element.getTmdbId())
            gui.createSimpleMenu(gui_element, output_parameter_handler, 'cTrakt', 'cTrakt', 'getAction', title)
        return

    def showHosters(self):
        input_parameter_handler = InputParameterHandler()
        movie_title = input_parameter_handler.getValue('file')
        movie_title = self.decode(movie_title, with_unicode=True).lower()  # on repasse en utf-8
        movie_title = Quote(movie_title)
        # vire les tags entre parentheses
        movie_title = re.sub('\\(.+?\\)', ' ', movie_title)

        # modif venom si le titre comporte un - il doit le chercher
        # vire les caracteres a la con qui peuvent trainer
        movie_title = re.sub(r'[^a-z -]', ' ', movie_title)

        movie_title = re.sub('( |^)(le|la|les|du|au|a|l)( |$)', ' ', movie_title)  # vire les articles

        # vire les espaces multiples et on laisse les espaces sans modifs car
        # certains codent avec %20 d'autres avec +
        movie_title = re.sub(' +', ' ', movie_title)

        self.vStreamSearch(movie_title)

    def vStreamSearch(self, movie_title):
        gui = Gui()

        handler = cRechercheHandler()
        handler.setText(movie_title)
        list_plugins = handler.getAvailablePlugins()

        gui.setEndOfDirectory()

    def getTmdbInfo(self, tmdb, gui_element):

        return

        if not tmdb:
            VSlog('Problème tmdb')
            return

        request_handler = RequestHandler(
            'https://api.themoviedb.org/3/movie/' + str(tmdb))
        request_handler.addParameters(
            'api_key', '92ab39516970ab9d86396866456ec9b6')
        request_handler.addParameters('language', 'fr')

        html_content = request_handler.request(json_decode=True)

        # format
        meta = {
            'imdb_id': html_content['id'],
            'title': html_content['title'],
            'tagline': html_content['tagline'],
            'rating': html_content['vote_average'],
            'votes': html_content['vote_count'],
            'duration': html_content['runtime'],
            'plot': html_content['overview']
        }
        if html_content['poster_path']:
            gui_element.setThumbnail('https://image.tmdb.org/t/p/w396' + html_content['poster_path'])
        if html_content['backdrop_path']:
            gui_element.setFanart('https://image.tmdb.org/t/p/w1280' + html_content['backdrop_path'])

        for key, value in meta.items():
            gui_element.addItemValues(key, value)

        return

    def getTmdbID(self, title, _type):

        input_parameter_handler = InputParameterHandler()

        from resources.lib.tmdb import TMDb
        grab = TMDb()

        if _type == 'shows':
            _type = 'tv'
        elif _type == 'movies':
            _type = 'movie'

        meta = 0
        year = ''
        # on cherche l'annee
        r = re.search('(\\([0-9]{4}\\))', title)
        if r:
            year = str(r.group(0))
            title = title.replace(year, '')

        meta = grab.get_idbyname(title, year, _type)

        return int(meta)
