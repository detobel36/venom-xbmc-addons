# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.pluginHandler import PluginHandler
from resources.lib.gui.gui import Gui
from resources.lib.upnext import UpNext
from resources.lib.comaddon import Addon, dialog, xbmc, isKrypton, VSlog, addonManager, isMatrix
from resources.lib.db import Db
from resources.lib.util import cUtil, Unquote
import xbmcplugin

try:  # Python 2
    from urlparse import urlparse
except ImportError:  # Python 3
    from urllib.parse import urlparse

from os.path import splitext

# pour les sous titres
# https://github.com/amet/service.subtitles.demo/blob/master/service.subtitles.demo/service.py
# player API
# http://mirrors.xbmc.org/docs/python-docs/stable/xbmc.html#Player


class Player(xbmc.Player):

    ADDON = Addon()

    def __init__(self, input_parameter_handler=False, *args):

        sPlayerType = self.__getPlayerType()
        xbmc.Player.__init__(self, sPlayerType)

        self.Subtitles_file = []
        self.SubtitleActive = False

        if not input_parameter_handler:
            input_parameter_handler = InputParameterHandler()
        self.hoster_identifier = input_parameter_handler.getValue(
            'hoster_identifier')
        self.title = input_parameter_handler.getValue('file_name')
        if self.title:
            self.title = Unquote(self.title)
        self.cat = input_parameter_handler.getValue('cat')
        self.sSaison = input_parameter_handler.getValue('season')
        self.sEpisode = input_parameter_handler.getValue('sEpisode')

        self.sSite = input_parameter_handler.getValue('site_url')
        self.sSource = input_parameter_handler.getValue('sourceName')
        self.fav = input_parameter_handler.getValue('sourceFav')
        self.saison_url = input_parameter_handler.getValue('saison_url')
        self.nextSaisonFunc = input_parameter_handler.getValue(
            'nextSaisonFunc')
        self.movie_url = input_parameter_handler.getValue('movie_url')
        self.movieFunc = input_parameter_handler.getValue('movieFunc')
        self.tmdb_id = input_parameter_handler.getValue('tmdb_id')

        self.playBackEventReceived = False
        self.playBackStoppedEventReceived = False
        self.forcestop = False
        self.multi = False  # Plusieurs vidéos se sont enchainées

        VSlog('player initialized')

    def clearPlayList(self):
        oPlaylist = self.__getPlayList()
        oPlaylist.clear()

    def __getPlayList(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

    def addItemToPlaylist(self, gui_element):
        gui = Gui()
        list_item = gui.createListItem(gui_element)
        self.__addItemToPlaylist(gui_element, list_item)

    def __addItemToPlaylist(self, gui_element, list_item):
        oPlaylist = self.__getPlayList()
        oPlaylist.add(gui_element.getMediaUrl(), list_item)

    def AddSubtitles(self, files):
        if isinstance(files, list) or isinstance(files, tuple):
            self.Subtitles_file = files
        else:
            self.Subtitles_file.append(files)

    def run(self, gui_element, url):
        # Lancement d'une vidéo sans avoir arreté la précedente
        self.tvShowTitle = gui_element.getItemValue('tvshowtitle')
        if self.isPlaying():
            sEpisode = str(gui_element.getEpisode())
            if sEpisode:
                # la vidéo précédente doit être marquée comme VUE
                numEpisode = int(sEpisode)
                prevEpisode = numEpisode - 1
                sPrevEpisode = '%02d' % prevEpisode
                self._setWatched(sPrevEpisode)
            else:
                self._setWatched()
        self.totalTime = 0
        self.currentTime = 0

        sPluginHandle = PluginHandler().getPluginHandle()

        gui = Gui()
        item = gui._createListItem(gui_element)
        item.setPath(gui_element.getMediaUrl())

        # Sous titres
        if self.Subtitles_file:
            try:
                item.setSubtitles(self.Subtitles_file)
                VSlog('Load SubTitle :' + str(self.Subtitles_file))
                self.SubtitleActive = True
            except BaseException:
                VSlog("Can't load subtitle:" + str(self.Subtitles_file))

        player_conf = self.ADDON.getSetting('playerPlay')
        # Si lien dash, methode prioritaire
        if splitext(urlparse(url).path)[-1] in [".mpd", ".m3u8"]:
            if isKrypton():
                addonManager().enableAddon('inputstream.adaptive')
                item.setProperty('inputstream', 'inputstream.adaptive')
                if '.m3u8' in url:
                    item.setProperty(
                        'inputstream.adaptive.manifest_type', 'hls')
                else:
                    item.setProperty(
                        'inputstream.adaptive.manifest_type', 'mpd')
                xbmcplugin.setResolvedUrl(sPluginHandle, True, listitem=item)
                VSlog('Player use inputstream addon')
            else:
                dialog().VSerror('Nécessite kodi 17 minimum')
                return

        # 1 er mode de lecture
        elif player_conf == '0':
            self.play(url, item)
            VSlog('Player use Play() method')

        # 2 eme mode non utilise
        elif player_conf == 'neverused':
            xbmc.executebuiltin('PlayMedia(' + url + ')')
            VSlog('Player use PlayMedia() method')

        # 3 eme mode (defaut)
        else:
            xbmcplugin.setResolvedUrl(sPluginHandle, True, item)
            VSlog('Player use setResolvedUrl() method')

        # Attend que le lecteur demarre, avec un max de 20s
        for _ in range(20):
            if self.playBackEventReceived:
                break
            xbmc.sleep(1000)

        # active/desactive les sous titres suivant l'option choisie dans la
        # config
        if self.getAvailableSubtitleStreams():
            if self.ADDON.getSetting('srt-view') == 'true':
                self.showSubtitles(True)
            else:
                self.showSubtitles(False)
                dialog().VSinfo('Des sous-titres sont disponibles', 'Sous-titres', 4)

        waitingNext = 0

        while self.isPlaying() and not self.forcestop:
            try:
                self.currentTime = self.getTime()

                waitingNext += 1
                if waitingNext == 8:  # attendre un peu avant de chercher le prochain épisode d'une série
                    self.totalTime = self.getTotalTime()
                    self.infotag = self.getVideoInfoTag()
                    UpNext().nextEpisode(gui_element)

            except Exception as err:
                VSlog("Exception run: {0}".format(err))

            xbmc.sleep(1000)

        if not self.playBackStoppedEventReceived:
            self.onPlayBackStopped()

        # Uniquement avec la lecture avec play()
        if player_conf == '0':
            r = xbmcplugin.addDirectoryItem(
                handle=sPluginHandle, url=url, listitem=item, isFolder=False)
            return r

        VSlog('Closing player')
        return True

    # fonction light servant par exemple pour visualiser les DL ou les chaines
    # de TV
    def startPlayer(self, window=False):
        oPlayList = self.__getPlayList()
        self.play(oPlayList, windowed=window)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    # Attention pas de stop, si on lance une seconde video sans fermer la
    # premiere
    def onPlayBackStopped(self):
        VSlog('player stopped')

        # reçu deux fois, on n'en prend pas compte
        if self.playBackStoppedEventReceived:
            return
        self.playBackStoppedEventReceived = True

        self._setWatched(self.sEpisode)

    # MARQUER VU
    # utilise les informations de la vidéo qui vient d'etre lue
    # qui n'est pas celle qui a été lancée si plusieurs vidéos se sont enchainées
    # sEpisode = l'épisode précédent en cas d'enchainement d'épisode

    def _setWatched(self, sEpisode=''):

        try:
            with Db() as db:
                if self.isPlaying():
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()
                    self.infotag = self.getVideoInfoTag()

                if self.totalTime > 0:
                    pourcent = float('%.2f' %
                                     (self.currentTime / self.totalTime))

                    saisonViewing = False

                    # calcul le temp de lecture
                    # Dans le cas ou ont a vu intégralement le contenu, percent = 0.0
                    # Mais on a tout de meme terminé donc le temps actuel est
                    # egal au temps total.
                    if (pourcent > 0.90) or (pourcent ==
                                             0.0 and self.currentTime == self.totalTime):

                        # Marquer VU dans la BDD Vstream
                        title_watched = self.infotag.getOriginalTitle()
                        if title_watched:
                            meta = {}
                            meta['title'] = title_watched
                            meta['cat'] = self.cat
                            db.insert_watched(meta)

                            # RAZ du point de reprise
                            db.del_resume(meta)

                            # Sortie des LECTURE EN COURS pour les films, pour
                            # les séries la suppression est manuelle
                            if self.cat == '1':
                                meta['titleWatched'] = title_watched
                                meta['cat'] = self.cat
                                db.del_viewing(meta)
                            elif self.cat == '8':      # A la fin de la lecture d'un episode, on met la saison en "Lecture en cours"
                                saisonViewing = True

                        # Marquer VU dans les comptes perso
                        self.__setWatchlist(sEpisode)

                    # Sauvegarde du point de lecture pour une reprise
                    elif self.currentTime > 180.0:
                        title_watched = self.infotag.getOriginalTitle()
                        if title_watched:
                            meta = {}
                            meta['title'] = title_watched
                            meta['site'] = self.sSite
                            meta['point'] = self.currentTime
                            meta['total'] = self.totalTime
                            matchedrow = db.insert_resume(meta)

                            # Lecture en cours
                            meta['cat'] = self.cat
                            meta['site'] = self.sSource
                            meta['tmdb_id'] = self.tmdb_id

                            # Lecture d'un épisode, on sauvegarde la saison
                            if self.cat == '8':
                                saisonViewing = True
                            else:   # Lecture d'un film

                                # les 'divers' de moins de 45 minutes peuvent être de type 'adultes'
                                # pas de sauvegarde en attendant mieux
                                if self.cat == '5' and self.totalTime < 2700:
                                    pass
                                else:
                                    meta['title'] = self.title
                                    meta['titleWatched'] = title_watched
                                    if self.movie_url and self.movieFunc:
                                        meta['siteurl'] = self.movie_url
                                        meta['fav'] = self.movieFunc
                                    else:
                                        meta['siteurl'] = self.sSite
                                        meta['fav'] = self.fav

                                    db.insert_viewing(meta)

                    # Lecture d'un épisode, on met la saison "En cours de
                    # lecture"
                    if saisonViewing:
                        meta['cat'] = '4'  # saison
                        meta['tmdb_id'] = self.tmdb_id
                        tvShowTitle = cUtil().titleWatched(self.tvShowTitle).replace(' ', '')
                        if self.sSaison:
                            meta['season'] = self.sSaison
                            meta['title'] = self.tvShowTitle + \
                                " S" + self.sSaison
                            meta['titleWatched'] = tvShowTitle + \
                                "_S" + self.sSaison
                        else:
                            meta['title'] = self.tvShowTitle
                            meta['titleWatched'] = tvShowTitle
                        meta['site'] = self.sSource
                        meta['siteurl'] = self.saison_url
                        meta['fav'] = self.nextSaisonFunc
                        db.insert_viewing(meta)

        except Exception as err:
            VSlog("ERROR Player_setWatched : {0}".format(err))

    # def onPlayBackStarted(self):
    def onAVStarted(self):
        VSlog('player started')

        # Si on recoit une nouvelle fois l'event, c'est que ca buggue, on stope
        # tout
        if self.playBackEventReceived:
            self.forcestop = True
            return

        self.playBackEventReceived = True

        with Db() as db:
            # Reprendre la lecture
            if self.isPlayingVideo() and self.getTime(
            ) < 180:  # si supérieur à 3 minutes, la gestion de la reprise est assuré par KODI
                self.infotag = self.getVideoInfoTag()
                title_watched = self.infotag.getOriginalTitle()
                if title_watched:
                    meta = {}
                    meta['title'] = title_watched
                    resumePoint, total = db.get_resume(meta)
                    if resumePoint:
                        h = resumePoint // 3600
                        ms = resumePoint - h * 3600
                        m = ms // 60
                        s = ms - m * 60
                        ret = dialog().VSselect(['Reprendre depuis %02d:%02d:%02d' % (
                            h, m, s), 'Lire depuis le début'], 'Reprendre la lecture')
                        if ret == 0:
                            self.seekTime(resumePoint)
                        elif ret == 1:
                            self.seekTime(0.0)
                            # RAZ du point de reprise
                            db.del_resume(meta)

    def __setWatchlist(self, sEpisode=''):
        # Suivi de lecture dans Trakt si compte
        if self.ADDON.getSetting('bstoken') == '':
            return
        plugins = __import__(
            'resources.lib.trakt',
            fromlist=['trakt']).cTrakt()
        function = getattr(plugins, 'getAction')
        function(Action="SetWatched", sEpisode=sEpisode)

    def __getPlayerType(self):
        sPlayerType = self.ADDON.getSetting('playerType')

        try:
            if sPlayerType == '0':
                VSlog('playertype from config: auto')
                return xbmc.PLAYER_CORE_AUTO

            if sPlayerType == '1':
                VSlog('playertype from config: mplayer')
                return xbmc.PLAYER_CORE_MPLAYER

            if sPlayerType == '2':
                VSlog('playertype from config: dvdplayer')
                return xbmc.PLAYER_CORE_DVDPLAYER
        except BaseException:
            return False
