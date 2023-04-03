# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import requests

from resources.hosters.youtube import cHoster
from resources.lib.gui.guiElement import GuiElement
from resources.lib.player import Player
from resources.lib.config import GestionCookie

UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

try:
    import json
except BaseException:
    import simplejson as json

SITE_IDENTIFIER = 'cBA'
SITE_NAME = 'BA'


class ShowBA:
    def __init__(self):
        self.trailerUrl = ''  # fournie par les metadata
        self.search = ''
        self.year = ''
        self.meta_type = 'movie'
        self.key = 'AIzaSyC5grY-gOPMpUM_tn0sfTKV3pKUtf9---M'

    def SetSearch(self, search):
        self.search = search

    def SetYear(self, year):
        if year:
            self.year = year

    def SetTrailerUrl(self, trailer_url):
        if trailer_url:
            try:
                trailer_id = trailer_url.split('=')[1]
                self.trailerUrl = 'http://www.youtube.com/watch?v=' + trailer_id
            except BaseException:
                pass

    def SetMetaType(self, meta_type):
        self.meta_type = str(meta_type).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'movie') .replace(
                '4', 'tvshow').replace('5', 'tvshow').replace('6', 'tvshow')

    def SearchBA(self, window=False):
        search_title = self.search + ' - Bande Annonce VF'
        if self.year:
            search_title += ' (%s)' % self.year

        # Le lien sur la BA est déjà connu
        url_trailer = self.trailerUrl

        # Sinon recherche de la BA officielle dans TMDB
        if not url_trailer:
            from resources.lib.tmdb import TMDb
            meta = TMDb().get_meta(self.meta_type, self.search, year=self.year)
            if 'trailer' in meta and meta['trailer']:
                self.SetTrailerUrl(meta['trailer'])
                url_trailer = self.trailerUrl

        # Sinon recherche dans youtube
        if not url_trailer:
            headers = {'User-Agent': UA}
            url = 'https://www.youtube.com/results'
            html_content = requests.get(url,
                                        params={'search_query': search_title},
                                        cookies={'CONSENT': GestionCookie().Readcookie("youtube")},
                                        headers=headers).text

            try:
                result = re.search('"contents":\\[{"videoRenderer":{"videoId":"([^"]+)', str(html_content)).group(1)
            except BaseException:
                result = re.search('"contents":\\[{"videoRenderer":{"videoId":"([^"]+)',
                                   html_content.encode('utf-8')).group(1)

            if result:
                # Premiere video trouvée
                url_trailer = 'https://www.youtube.com/watch?v=' + result

        # BA trouvée
        if url_trailer:
            hote = cHoster()
            hote.setUrl(url_trailer)
            # hote.setResolution('720p') Pas utilisé
            api_call = hote.getMediaLink()[1]

            if not api_call:
                return

            gui_element = GuiElement()
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setTitle(search_title)
            gui_element.setMediaUrl(api_call)
            gui_element.setThumbnail(gui_element.getIcon())

            player = Player()
            player.clearPlayList()
            player.addItemToPlaylist(gui_element)
            player.startPlayer(window)
