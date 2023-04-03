# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import copy
import json
import threading
import xbmc
import xbmcplugin
import sys

from resources.lib.comaddon import listitem, Addon, dialog, window, isNexus, Progress, VSlog
from resources.lib.gui.contextElement import ContextElement
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.pluginHandler import PluginHandler
from resources.lib.parser import Parser
from resources.lib.util import QuotePlus


class Gui:

    SITE_NAME = 'Gui'
    CONTENT = ''
    listing = []
    thread_listing = []
    episodeListing = []  # Pour gérer l'enchainement des episodes
    ADDON = Addon()
    displaySeason = Addon().getSetting('display_season_title')
    # Gérer les résultats de la recherche
    searchResults = {}
    searchResultsSemaphore = threading.Semaphore()

    def emptySearchResult(self, siteName):
        Gui.searchResultsSemaphore.acquire()
        Gui.searchResults[siteName] = []  # vider le tableau de résultats
        Gui.searchResultsSemaphore.release()

    def getEpisodeListing(self):
        return self.episodeListing

    def addNewDir(
            self,
            Type,
            s_id,
            function,
            label,
            icon,
            thumbnail='',
            desc='',
            output_parameter_handler='',
            sMeta=0,
            cat=None):
        gui_element = GuiElement()
        # dir ou link => CONTENT par défaut = files
        if Type != 'dir' and Type != 'link':
            Gui.CONTENT = Type
        gui_element.setSiteName(s_id)
        gui_element.setFunction(function)
        gui_element.setTitle(label)
        gui_element.setIcon(icon)

        if thumbnail == '':
            gui_element.setThumbnail(gui_element.getIcon())
        else:
            gui_element.setThumbnail(thumbnail)
            gui_element.setPoster(thumbnail)

        gui_element.setDescription(desc)

        if cat is not None:
            gui_element.setCat(cat)

        # Pour addLink on recupere le cat et sMeta precedent.
        if Type == 'link':
            input_parameter_handler = InputParameterHandler()
            cat = input_parameter_handler.getValue('cat')
            if cat:
                gui_element.setCat(cat)

            sMeta = input_parameter_handler.getValue('sMeta')
            if sMeta:
                gui_element.setMeta(sMeta)
        else:
            output_parameter_handler.addParameter('sMeta', sMeta)
            gui_element.setMeta(sMeta)

        # Si pas d'id TMDB pour un episode, on recupère le précédent qui vient
        # de la série
        if cat and not output_parameter_handler.getValue('tmdb_id'):
            input_parameter_handler = InputParameterHandler()
            sPreviousMeta = int(input_parameter_handler.getValue('sMeta'))
            if 0 < sPreviousMeta < 7:
                sTmdbID = input_parameter_handler.getValue('tmdb_id')
                if sTmdbID:
                    output_parameter_handler.addParameter('tmdb_id', sTmdbID)

        output_parameter_handler.addParameter('fav', function)

        resumeTime = output_parameter_handler.getValue('ResumeTime')
        if resumeTime:
            gui_element.setResumeTime(resumeTime)
            gui_element.setTotalTime(
                output_parameter_handler.getValue('TotalTime'))

        # Lecture en cours
        isViewing = output_parameter_handler.getValue('isViewing')
        if isViewing:
            gui_element.addItemProperties('isViewing', True)

        title = output_parameter_handler.getValue('movie_title')
        if title:
            gui_element.setFileName(title)
        else:
            gui_element.setFileName(label)

        try:
            return self.addFolder(gui_element, output_parameter_handler)
        except Exception as error:
            VSlog("addNewDir error: " + str(error))

    #    Categorie       Meta          cat     CONTENT
    #    Film            1             1        movies
    #    Serie           2             2        tvshows
    #    Anime           4             3        tvshows
    #    Saison          5             4        episodes
    #    Divers          0             5        videos
    #    IPTV (Officiel) 0             6        files
    #    Saga            3             7        movies
    #    Episodes        6             8        episodes
    #    Drama           2             9        tvshows
    #    Person          7             /        artists
    #    Network         8             /        files

    def addMovie(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        movie_url = output_parameter_handler.getValue('site_url')
        output_parameter_handler.addParameter('movie_url', QuotePlus(movie_url))
        output_parameter_handler.addParameter('movieFunc', function)
        return self.addNewDir('movies', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 1, 1)

    def addTV(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saison_url = output_parameter_handler.getValue('site_url')
        if saison_url:
            output_parameter_handler.addParameter('saison_url', QuotePlus(saison_url))
            output_parameter_handler.addParameter('nextSaisonFunc', function)

        return self.addNewDir(
            'tvshows',
            s_id,
            function,
            label,
            icon,
            thumbnail,
            desc,
            output_parameter_handler,
            2,
            2)

    def addAnime(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saison_url = output_parameter_handler.getValue('site_url')
        if saison_url:
            output_parameter_handler.addParameter(
                'saison_url', QuotePlus(saison_url))
            output_parameter_handler.addParameter('nextSaisonFunc', function)

        return self.addNewDir('tvshows', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 4, 3)

    def addDrama(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saison_url = output_parameter_handler.getValue('site_url')
        if saison_url:
            output_parameter_handler.addParameter(
                'saison_url', QuotePlus(saison_url))
            output_parameter_handler.addParameter('nextSaisonFunc', function)

        return self.addNewDir('tvshows', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 2, 9)

    def addMisc(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        if thumbnail or desc:
            type = 'videos'
        else:
            type = 'files'
        movie_url = output_parameter_handler.getValue('site_url')
        output_parameter_handler.addParameter('movie_url', QuotePlus(movie_url))
        output_parameter_handler.addParameter('movieFunc', function)
        return self.addNewDir(type, s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 0, 5)

    def addMoviePack(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        return self.addNewDir('sets', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 3, 7)

    def addDir(self, s_id, function, label, icon, output_parameter_handler='', desc=""):
        return self.addNewDir('dir', s_id, function, label, icon, '', desc, output_parameter_handler, 0, None)

    def addLink(self, s_id, function, label, thumbnail, desc, output_parameter_handler='',
                input_parameter_handler=False):
        # Pour gérer l'enchainement des épisodes
        if not input_parameter_handler:
            input_parameter_handler = InputParameterHandler()
        output_parameter_handler.addParameter(
            'saison_url', input_parameter_handler.getValue('saison_url'))
        output_parameter_handler.addParameter(
            'nextSaisonFunc', input_parameter_handler.getValue('nextSaisonFunc'))
        output_parameter_handler.addParameter(
            'movie_url', input_parameter_handler.getValue('movie_url'))
        output_parameter_handler.addParameter(
            'movieFunc', input_parameter_handler.getValue('movieFunc'))

        if not output_parameter_handler.getValue('lang'):
            output_parameter_handler.addParameter(
                'lang', input_parameter_handler.getValue('lang'))

        icon = thumbnail
        return self.addNewDir('link', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 0, None)

    def addSeason(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saison_url = output_parameter_handler.getValue('site_url')
        output_parameter_handler.addParameter(
            'saison_url', QuotePlus(saison_url))
        output_parameter_handler.addParameter('nextSaisonFunc', function)

        return self.addNewDir('seasons', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 5, 4)

    def addEpisode(self, s_id, function, label, icon, thumbnail, desc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes, l'URL de la saison
        input_parameter_handler = InputParameterHandler()
        saison_url = input_parameter_handler.getValue('saison_url')
        if saison_url:   # Retenu depuis "addSeason"
            output_parameter_handler.addParameter('saison_url', saison_url)
            output_parameter_handler.addParameter(
                'nextSaisonFunc', input_parameter_handler.getValue('nextSaisonFunc'))
        else:           # calculé depuis l'url qui nous a emmené ici sans passé par addSeason
            output_parameter_handler.addParameter(
                'saison_url', input_parameter_handler.getValue('site_url'))
            output_parameter_handler.addParameter(
                'nextSaisonFunc', input_parameter_handler.getValue('function'))

        if not output_parameter_handler.getValue('lang'):
            output_parameter_handler.addParameter(
                'lang', input_parameter_handler.getValue('lang'))

        return self.addNewDir('episodes', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 6, 8)

    # Affichage d'une personne (acteur, réalisateur, ..)
    def addPerson(self, s_id, function, label, icon, thumbnail, output_parameter_handler=''):
        thumbnail = ''
        desc = ''
        return self.addNewDir('artists', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 7,
                              None)

    # Affichage d'un réseau de distribution du média
    def addNetwork(self, s_id, function, label, icon, output_parameter_handler=''):
        thumbnail = ''
        desc = ''
        return self.addNewDir('', s_id, function, label, icon, thumbnail, desc, output_parameter_handler, 8, None)

    def addNext(self, s_id, function, label, output_parameter_handler):
        gui_element = GuiElement()
        gui_element.setSiteName(s_id)
        gui_element.setFunction(function)
        gui_element.setTitle('[COLOR teal]' + label + ' >>>[/COLOR]')
        gui_element.setIcon('next.png')
        gui_element.setThumbnail(gui_element.getIcon())
        gui_element.setMeta(0)
        gui_element.setCat(5)

        self.createContexMenuPageSelect(gui_element, output_parameter_handler)
        self.createContexMenuViewBack(gui_element, output_parameter_handler)
        return self.addFolder(gui_element, output_parameter_handler)

    # utiliser gui.addText(SITE_IDENTIFIER)
    def addNone(self, s_id):
        return self.addText(s_id)

    def addText(self, s_id, label='', icon='none.png'):
        # Pas de texte lors des recherches globales
        if window(10101).getProperty('search') == 'true':
            return

        gui_element = GuiElement()
        gui_element.setSiteName(s_id)
        gui_element.setFunction('DoNothing')
        if not label:
            label = self.ADDON.VSlang(30204)
        gui_element.setTitle(label)
        gui_element.setIcon(icon)
        gui_element.setThumbnail(gui_element.getIcon())
        gui_element.setMeta(0)

        output_parameter_handler = OutputParameterHandler()
        return self.addFolder(gui_element, output_parameter_handler)

    # afficher les liens non playable
    def addFolder(self, gui_element, output_parameter_handler='', _isFolder=True):
        if _isFolder is False:
            Gui.CONTENT = 'files'

        # recherche append les reponses
        if window(10101).getProperty('search') == 'true':
            self.addSearchResult(gui_element, output_parameter_handler)
            return

        # Des infos a rajouter ?
        params = {'site_url': gui_element.setSiteUrl,
                  'tmdb_id': gui_element.setTmdbId,
                  'year': gui_element.setYear,
                  'resolution': gui_element.setRes}

        try:  # Py2
            for sParam, callback in params.iteritems():
                value = output_parameter_handler.getValue(sParam)
                if value:
                    callback(value)

        except AttributeError:  # py3
            for sParam, callback in params.items():
                value = output_parameter_handler.getValue(sParam)
                if value:
                    callback(value)

        list_item = self.createListItem(gui_element)

    # affiche tag HD
        # https://alwinesch.github.io/group__python__xbmcgui__listitem.html#ga99c7bf16729b18b6378ea7069ee5b138
        resolution = gui_element.getRes()
        if resolution:
            if '2160' in resolution:
                list_item.addStreamInfo(
                    'video', {'width': 3840, 'height': 2160})
            elif '1080' in resolution:
                list_item.addStreamInfo(
                    'video', {'width': 1920, 'height': 1080})
            elif '720' in resolution:
                list_item.addStreamInfo(
                    'video', {'width': 1280, 'height': 720})
            elif '480' in resolution:
                list_item.addStreamInfo('video', {'width': 720, 'height': 576})

        cat = gui_element.getCat()
        if cat:
            Gui.cat = cat
            output_parameter_handler.addParameter('cat', cat)

        sItemUrl = self.__createItemUrl(gui_element, output_parameter_handler)

        output_parameter_handler.addParameter(
            'title_watched', gui_element.getTitleWatched())

        list_item = self.__createContextMenu(gui_element, list_item)

        if _isFolder is True:
            # list_item.setProperty('IsPlayable', 'true')
            if cat:    # 1 = movies, moviePack; 2 = series, animes, episodes; 5 = MISC
                if gui_element.getMeta():
                    self.createContexMenuinfo(
                        gui_element, output_parameter_handler)
                    self.createContexMenuba(
                        gui_element, output_parameter_handler)
                if not list_item.getProperty('isBookmark'):
                    self.createContexMenuBookmark(
                        gui_element, output_parameter_handler)

                if cat in (1, 2, 3, 4, 8, 9):
                    if self.ADDON.getSetting('bstoken') != '':
                        self.createContexMenuTrakt(
                            gui_element, output_parameter_handler)
                    if self.ADDON.getSetting('tmdb_account') != '':
                        self.createContexMenuTMDB(
                            gui_element, output_parameter_handler)
                if cat in (1, 2, 3, 4, 9):
                    self.createContexMenuSimil(
                        gui_element, output_parameter_handler)
                if cat != 6:
                    self.createContexMenuWatch(
                        gui_element, output_parameter_handler)
        else:
            list_item.setProperty('IsPlayable', 'true')
            self.createContexMenuWatch(gui_element, output_parameter_handler)

        list_item = self.__createContextMenu(gui_element, list_item)
        self.listing.append((sItemUrl, list_item, _isFolder))

        # Vider les paramètres pour être recyclé
        output_parameter_handler.clearParameter()
        return list_item

    def createListItem(self, gui_element):

        # Récupération des metadonnées par thread
        if gui_element.getMeta() and gui_element.getMetaAddon() == 'true':
            return self.createListItemThread(gui_element)

        # pas de meta, appel direct
        return self._createListItem(gui_element)

    # Utilisation d'un Thread pour un chargement des metas en parallèle
    def createListItemThread(self, gui_element):
        itemTitle = gui_element.getTitle()
        list_item = listitem(itemTitle)
        t = threading.Thread(
            target=self._createListItem,
            name=itemTitle,
            args=(
                gui_element,
                list_item))
        self.thread_listing.append(t)
        t.start()
        return list_item

    def _createListItem(self, gui_element, list_item=None):

        # Enleve les elements vides
        data = {
            key: val for key,
            val in gui_element.getItemValues().items() if val != ""}

        itemTitle = gui_element.getTitle()

        # Formatage nom episode
        cat = gui_element.getCat()
        if cat and int(cat) == 8:  # Nom de l'épisode
            try:
                if 'tagline' in data and data['tagline']:
                    episodeTitle = data['tagline']
                else:
                    episodeTitle = 'Episode ' + str(data['episode'])
                host = ''
                if 'tvshowtitle' in data:
                    host = itemTitle.split(data['tvshowtitle'])[1]
                if self.displaySeason == "true":
                    itemTitle = str(data['season']) + "x" + \
                        str(data['episode']) + ". " + episodeTitle
                else:
                    itemTitle = episodeTitle
                if len(host) > 3:
                    itemTitle += " " + host
                data['title'] = itemTitle
            except BaseException:
                data['title'] = itemTitle
                pass
        else:
            # Permets d'afficher toutes les informations pour les films.
            data['title'] = itemTitle

        if ":" in str(data.get('duration')):
            # Convertion en seconde, utile pour le lien final.
            data['duration'] = (sum(
                x * int(t) for x, t in zip([1, 60, 3600], reversed(data.get('duration', '').split(":")))))

        if not list_item:
            list_item = listitem(itemTitle)

        if data.get('cast'):
            credits = json.loads(data['cast'])
            data['cast'] = []
            for i in credits:
                if isNexus():
                    data['cast'].append(
                        xbmc.Actor(
                            i['name'],
                            i['character'],
                            i['order'],
                            i.get(
                                'thumbnail',
                                "")))
                else:
                    data['cast'].append(
                        (i['name'], i['character'], i['order'], i.get(
                            'thumbnail', "")))

        if not isNexus():
            # voir : https://kodi.wiki/view/InfoLabels
            list_item.setInfo(gui_element.getType(), data)

        else:
            videoInfoTag = list_item.getVideoInfoTag()

            # https://alwinesch.github.io/class_x_b_m_c_addon_1_1xbmc_1_1_info_tag_video.html
            # gestion des valeurs par defaut si non renseignées
            videoInfoTag.setMediaType(data.get('mediatype', ''))
            videoInfoTag.setTitle(data.get('title', ""))
            videoInfoTag.setTvShowTitle(data.get('tvshowtitle', ''))
            videoInfoTag.setOriginalTitle(data.get('originaltitle', ""))
            videoInfoTag.setPlot(data.get('plot', ""))
            videoInfoTag.setPlotOutline(data.get('tagline', ""))
            videoInfoTag.setYear(int(data.get('year', 0)))
            videoInfoTag.setRating(float(data.get('rating', 0.0)))
            videoInfoTag.setMpaa(data.get('mpaa', ""))
            videoInfoTag.setDuration(int(data.get('duration', 0)))
            videoInfoTag.setPlaycount(int(data.get('playcount', 0)))
            videoInfoTag.setCountries(data.get('country', [""]))
            videoInfoTag.setTrailer(data.get('trailer', ""))
            videoInfoTag.setTagLine(data.get('tagline', ""))
            videoInfoTag.setStudios(list(data.get('studio', '').split("/")))
            videoInfoTag.setWriters(list(data.get('writer', '').split("/")))
            videoInfoTag.setDirectors(
                list(data.get('director', '').split("/")))
            videoInfoTag.setGenres(''.join(data.get('genre', [""])).split('/'))
            videoInfoTag.setSeason(int(data.get('season', 0)))
            videoInfoTag.setEpisode(int(data.get('episode', 0)))
            videoInfoTag.setResumePoint(
                float(
                    data.get(
                        'resumetime', 0.0)), float(
                    data.get(
                        'totaltime', 0.0)))

            videoInfoTag.setCast(data.get('cast', []))

        list_item.setArt({'poster': gui_element.getPoster(),
                          'thumb': gui_element.getThumbnail(),
                          'icon': gui_element.getIcon(),
                          'fanart': gui_element.getFanart()})

        aProperties = gui_element.getItemProperties()
        for sPropertyKey, sPropertyValue in aProperties.items():
            list_item.setProperty(sPropertyKey, str(sPropertyValue))

        return list_item

    # Marquer vu/Non vu
    def createContexMenuWatch(self, gui_element, output_parameter_handler=''):
        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'Gui',
            gui_element.getSiteName(),
            'setWatched',
            self.ADDON.VSlang(30206))

    def createContexMenuPageSelect(
            self,
            gui_element,
            output_parameter_handler):
        oContext = ContextElement()
        oContext.setFile('Gui')
        oContext.setSiteName('Gui')
        oContext.setFunction('selectPage')
        oContext.setTitle(self.ADDON.VSlang(30017))
        output_parameter_handler.addParameter(
            'OldFunction', gui_element.getFunction())
        output_parameter_handler.addParameter('s_id', gui_element.getSiteName())
        oContext.setOutputParameterHandler(output_parameter_handler)
        gui_element.addContextItem(oContext)

    def createContexMenuViewBack(self, gui_element, output_parameter_handler):
        oContext = ContextElement()
        oContext.setFile('Gui')
        oContext.setSiteName('Gui')
        oContext.setFunction('viewBack')
        oContext.setTitle(self.ADDON.VSlang(30018))
        output_parameter_handler.addParameter('s_id', gui_element.getSiteName())
        oContext.setOutputParameterHandler(output_parameter_handler)
        gui_element.addContextItem(oContext)

    # marque page
    def createContexMenuBookmark(
            self,
            gui_element,
            output_parameter_handler=''):
        output_parameter_handler.addParameter(
            'clean_title', gui_element.getCleanTitle())
        output_parameter_handler.addParameter('s_id', gui_element.getSiteName())
        output_parameter_handler.addParameter(
            'fav', gui_element.getFunction())
        output_parameter_handler.addParameter('cat', gui_element.getCat())

        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'cFav',
            'cFav',
            'setBookmark',
            self.ADDON.VSlang(30210))

    def createContexMenuTrakt(self, gui_element, output_parameter_handler=''):
        output_parameter_handler.addParameter(
            'sImdbId', gui_element.getImdbId())
        output_parameter_handler.addParameter(
            'tmdb_id', gui_element.getTmdbId())
        output_parameter_handler.addParameter(
            'file_name', gui_element.getFileName())

        _type = Gui.CONTENT.replace('tvshows', 'shows')
        output_parameter_handler.addParameter('_type', _type)
        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'cTrakt',
            'cTrakt',
            'getAction',
            self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, gui_element, output_parameter_handler=''):
        output_parameter_handler.addParameter(
            'sImdbId', gui_element.getImdbId())
        output_parameter_handler.addParameter(
            'tmdb_id', gui_element.getTmdbId())
        output_parameter_handler.addParameter(
            'file_name', gui_element.getFileName())

        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'themoviedb_org',
            'themoviedb_org',
            'getAction',
            'TMDB')

    def createContexMenuDownload(
            self,
            gui_element,
            output_parameter_handler='',
            status='0'):
        if status == '0':
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'StartDownloadOneFile',
                self.ADDON.VSlang(30215))

        if status == '0' or status == '2':
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'delDownload',
                self.ADDON.VSlang(30216))
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'DelFile',
                self.ADDON.VSlang(30217))

        if status == '1':
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'StopDownloadList',
                self.ADDON.VSlang(30218))

        if status == '2':
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'ReadDownload',
                self.ADDON.VSlang(30219))
            self.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'ResetDownload',
                self.ADDON.VSlang(30220))

    # Information
    def createContexMenuinfo(self, gui_element, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'title', gui_element.getCleanTitle())
        output_parameter_handler.addParameter(
            'file_name', gui_element.getFileName())
        output_parameter_handler.addParameter('s_id', gui_element.getSiteName())
        output_parameter_handler.addParameter('sMeta', gui_element.getMeta())
        output_parameter_handler.addParameter('year', gui_element.getYear())
        output_parameter_handler.addParameter(
            'fav', gui_element.getFunction())
        output_parameter_handler.addParameter('cat', gui_element.getCat())

        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'Gui',
            gui_element.getSiteName(),
            'viewInfo',
            self.ADDON.VSlang(30208))

    # Bande annonce
    def createContexMenuba(self, gui_element, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('title', gui_element.getTitle())
        output_parameter_handler.addParameter(
            'file_name', gui_element.getFileName())
        output_parameter_handler.addParameter('year', gui_element.getYear())
        output_parameter_handler.addParameter(
            'trailerUrl', gui_element.getTrailer())
        output_parameter_handler.addParameter('sMeta', gui_element.getMeta())

        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'Gui',
            gui_element.getSiteName(),
            'viewBA',
            self.ADDON.VSlang(30212))

    # Recherche similaire
    def createContexMenuSimil(self, gui_element, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'file_name', gui_element.getFileName())
        output_parameter_handler.addParameter('title', gui_element.getTitle())
        output_parameter_handler.addParameter('cat', gui_element.getCat())

        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'Gui',
            gui_element.getSiteName(),
            'viewSimil',
            self.ADDON.VSlang(30213))

    def createSimpleMenu(
            self,
            gui_element,
            output_parameter_handler,
            file,
            sName,
            function,
            title):
        oContext = ContextElement()
        oContext.setFile(file)
        oContext.setSiteName(sName)
        oContext.setFunction(function)
        oContext.setTitle(title)

        oContext.setOutputParameterHandler(output_parameter_handler)
        gui_element.addContextItem(oContext)

    def createContexMenuDelFav(self, gui_element, output_parameter_handler=''):
        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'cFav',
            'cFav',
            'delBookmarksMenu',
            self.ADDON.VSlang(30209))

    def createContexMenuSettings(
            self,
            gui_element,
            output_parameter_handler=''):
        self.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'globalParametre',
            'globalParametre',
            'opensetting',
            self.ADDON.VSlang(30023))

    def __createContextMenu(self, gui_element, list_item):
        plugin_path = PluginHandler().getPluginPath()
        aContextMenus = []

        # Menus classiques reglés a la base
        nb_context_menu = len(gui_element.getContextItems())
        if nb_context_menu > 0:
            for oContextItem in gui_element.getContextItems():
                output_parameter_handler = oContextItem.getOutputParameterHandler()
                sParams = output_parameter_handler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (
                    plugin_path, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                sDecoColor = self.ADDON.getSetting('deco_color')
                titleMenu = '[COLOR %s]%s[/COLOR]' % (
                    sDecoColor, oContextItem.getTitle())
                aContextMenus += [(titleMenu, 'RunPlugin(%s)' % sTest)]

            list_item.addContextMenuItems(aContextMenus)
        list_item.setProperty('nbcontextmenu', str(nb_context_menu))

        return list_item

    def __createItemUrl(self, gui_element, output_parameter_handler=''):
        if output_parameter_handler == '':
            output_parameter_handler = OutputParameterHandler()

        # On descend l'id TMDB dans les saisons et les épisodes
        output_parameter_handler.addParameter(
            'tmdb_id', gui_element.getTmdbId())

        # Pour gérer l'enchainement des épisodes
        output_parameter_handler.addParameter(
            'season', gui_element.getSeason())
        output_parameter_handler.addParameter(
            'sEpisode', gui_element.getEpisode())

        sParams = output_parameter_handler.getParameterAsUri()

        plugin_path = PluginHandler().getPluginPath()

        if len(gui_element.getFunction()) == 0:
            sItemUrl = '%s?site=%s&title=%s&%s' % (plugin_path, gui_element.getSiteName(
            ), QuotePlus(gui_element.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (plugin_path, gui_element.getSiteName(
            ), gui_element.getFunction(), QuotePlus(gui_element.getCleanTitle()), sParams)

        return sItemUrl

    def setEndOfDirectory(self, forceViewMode=False):
        # On n'affiche pas si on fait une recherche
        if window(10101).getProperty('playVideo') == 'true':
            return

        iHandler = PluginHandler().getPluginHandle()

        if not self.listing:
            self.addText('Gui')

        # attendre l'arret des thread utilisés pour récupérer les métadonnées
        total = len(self.thread_listing)
        if total > 0:
            progress_ = Progress().VScreate(Addon().VSlang(30141))
            for thread in self.thread_listing:
                progress_.VSupdate(progress_, total)
                thread.join(100)
            progress_.VSclose(progress_)

        del self.thread_listing[:]

        xbmcplugin.addDirectoryItems(iHandler, self.listing, len(self.listing))
        xbmcplugin.setPluginCategory(iHandler, '')
        xbmcplugin.setContent(iHandler, Gui.CONTENT)
        if Gui.CONTENT == 'episodes':
            xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_EPISODE)
        else:
            xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(iHandler, succeeded=True, cacheToDisc=True)
        # reglage vue
        # 50 = liste / 51 grande liste / 500 icone / 501 gallerie / 508 fanart
        # /
        if forceViewMode:
            xbmc.executebuiltin(
                'Container.SetViewMode(' + str(forceViewMode) + ')')
        else:
            if self.ADDON.getSetting('active-view') == 'true':
                if Gui.CONTENT == 'movies' or Gui.CONTENT == 'artists':
                    # xbmc.executebuiltin('Container.SetViewMode(507)')
                    xbmc.executebuiltin(
                        'Container.SetViewMode(%s)' %
                        self.ADDON.getSetting('movies-view'))
                elif Gui.CONTENT in ['tvshows', 'seasons', 'episodes']:
                    xbmc.executebuiltin(
                        'Container.SetViewMode(%s)' %
                        self.ADDON.getSetting(
                            Gui.CONTENT + '-view'))
                elif Gui.CONTENT == 'files':
                    xbmc.executebuiltin(
                        'Container.SetViewMode(%s)' %
                        self.ADDON.getSetting('default-view'))

        del self.episodeListing[:]  # Pour l'enchainement des episodes
        self.episodeListing.extend(self.listing)

        del self.listing[:]

    def updateDirectory(self):  # refresh the content
        xbmc.executebuiltin('Container.Refresh')
        xbmc.sleep(600)    # Nécessaire pour laisser le temps du refresh

    def viewBA(self):
        input_parameter_handler = InputParameterHandler()
        file_name = input_parameter_handler.getValue('file_name')
        year = input_parameter_handler.getValue('year')
        trailerUrl = input_parameter_handler.getValue('trailerUrl')
        sMeta = input_parameter_handler.getValue('sMeta')

        from resources.lib.ba import ShowBA
        cBA = ShowBA()
        cBA.SetSearch(file_name)
        cBA.SetYear(year)
        cBA.SetTrailerUrl(trailerUrl)
        cBA.SetMetaType(sMeta)
        cBA.SearchBA()

    def viewBack(self):
        plugin_path = PluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        # sParams = input_parameter_handler.getAllParameter()
        s_id = input_parameter_handler.getValue('s_id')
        sTest = '%s?site=%s' % (plugin_path, s_id)

        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def viewInfo(self):
        if Addon().getSetting('information-view') == "false":
            from resources.lib.config import WindowsBoxes

            input_parameter_handler = InputParameterHandler()
            clean_title = input_parameter_handler.getValue('title') if input_parameter_handler.exist(
                'title') else xbmc.getInfoLabel('ListItem.Title')
            sMeta = input_parameter_handler.getValue('sMeta') if input_parameter_handler.exist(
                'sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            year = input_parameter_handler.getValue('year') if input_parameter_handler.exist(
                'year') else xbmc.getInfoLabel('ListItem.Year')
            url = input_parameter_handler.getValue('site_url') if input_parameter_handler.exist(
                'site_url') else xbmc.getInfoLabel('ListItem.Property(site_url)')
            sSite = input_parameter_handler.getValue('s_id') if input_parameter_handler.exist(
                's_id') else xbmc.getInfoLabel('ListItem.Property(s_id)')
            fav = input_parameter_handler.getValue('fav') if input_parameter_handler.exist(
                'fav') else xbmc.getInfoLabel('ListItem.Property(fav)')
            cat = input_parameter_handler.getValue('cat') if input_parameter_handler.exist(
                'cat') else xbmc.getInfoLabel('ListItem.Property(cat)')

            WindowsBoxes(clean_title, url, sMeta, year, sSite, fav, cat)
        else:
            # On appel la fonction integrée a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')

    def viewSimil(self):
        plugin_path = PluginHandler().getPluginPath()

        input_parameter_handler = InputParameterHandler()
        clean_title = input_parameter_handler.getValue('title') if input_parameter_handler.exist(
            'title') else xbmc.getInfoLabel('ListItem.Title')
        cat = input_parameter_handler.getValue('cat') if input_parameter_handler.exist(
            'cat') else xbmc.getInfoLabel('ListItem.Property(cat)')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('searchtext', clean_title)
        output_parameter_handler.addParameter('cat', cat)

        sParams = output_parameter_handler.getParameterAsUri()
        sTest = '?site=%s&function=%s&%s' % (
            'globalSearch', 'globalSearch', sParams)
        sys.argv[2] = sTest
        sTest = plugin_path + sTest

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour
        # lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % 10025)

        xbmc.executebuiltin('Container.Update(%s)' % sTest)
        return True

    def selectPage(self):
        plugin_path = PluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        # sParams = input_parameter_handler.getAllParameter()
        s_id = input_parameter_handler.getValue('s_id')
        function = input_parameter_handler.getValue('OldFunction')
        site_url = input_parameter_handler.getValue('site_url')

        if site_url.endswith(
                '/'):  # for the url http.://www.1test.com/annee-2020/page-2/
            urlSource = site_url.rsplit('/', 2)[0]
            endOfUrl = site_url.rsplit('/', 2)[1] + '/'
        else:  # for the url http.://www.1test.com/annee-2020/page-2 or /page-2.html
            urlSource = site_url.rsplit('/', 1)[0]
            endOfUrl = site_url.rsplit('/', 1)[1]

        parser = Parser()
        oldNum = parser.getNumberFromString(endOfUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                site_url = urlSource + '/' + endOfUrl.replace(oldNum, newNum, 1)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', site_url)
                sParams = output_parameter_handler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (
                    plugin_path, s_id, function, sParams)
                xbmc.executebuiltin('Container.Update(%s)' % sTest)
            except BaseException:
                return False

        return False

    def selectPage2(self):
        plugin_path = PluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        s_id = input_parameter_handler.getValue('s_id')
        function = input_parameter_handler.getValue('OldFunction')
        site_url = input_parameter_handler.getValue('site_url')

        selpage = self.showNumBoard()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', site_url)
        output_parameter_handler.addParameter('Selpage', selpage)

        sParams = output_parameter_handler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (
            plugin_path, s_id, function, sParams)
        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def setWatched(self):
        if True:
            # Use vStream database
            input_parameter_handler = InputParameterHandler()
            sSite = input_parameter_handler.getValue('site_url')
            title = input_parameter_handler.getValue('title_watched')
            cat = input_parameter_handler.getValue('cat')
            if not title:
                return

            meta = {}
            meta['title'] = title
            meta['titleWatched'] = title
            meta['site'] = sSite
            meta['cat'] = cat

            from resources.lib.db import Db
            with Db() as db:
                row = db.get_watched(meta)
                if row:
                    db.del_watched(meta)
                    db.del_resume(meta)
                else:
                    db.insert_watched(meta)
                    db.del_viewing(meta)

        else:
            # Use kodi buildin feature
            xbmc.executebuiltin('Action(ToggleWatched)')

        self.updateDirectory()

    def showKeyBoard(self, sDefaultText='', heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(heading)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_text = keyboard.getText()
            if (len(search_text)) > 0:
                return search_text

        return False

    def showNumBoard(self, title="", sDefaultNum=''):
        dialogs = dialog()
        if not title:
            title = self.ADDON.VSlang(30019)
        numboard = dialogs.numeric(0, title, sDefaultNum)
        # numboard.doModal()
        if numboard is not None:
            return numboard

        return False

    def openSettings(self):
        return False

    def showNofication(self, title, seconds=0):
        return False

    def showError(self, title, description, seconds=0):
        return False

    def showInfo(self, title, description, seconds=0):
        return False

    def getSearchResult(self):
        Gui.searchResultsSemaphore.acquire()
        result = copy.deepcopy(Gui.searchResults)
        Gui.searchResultsSemaphore.release()
        return result

    def addSearchResult(self, gui_element, output_parameter_handler):
        Gui.searchResultsSemaphore.acquire()
        searchSiteId = output_parameter_handler.getValue('searchSiteId')
        if not searchSiteId:
            searchSiteId = gui_element.getSiteName()

        if searchSiteId not in Gui.searchResults:
            Gui.searchResults[searchSiteId] = []

        Gui.searchResults[searchSiteId].append(
            {'guiElement': gui_element, 'params': copy.deepcopy(output_parameter_handler)})
        Gui.searchResultsSemaphore.release()

    def resetSearchResult(self):
        Gui.searchResultsSemaphore.acquire()
        Gui.searchResults = {}
        Gui.searchResultsSemaphore.release()
