# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import copy
import json
import threading
import xbmc
import xbmcplugin
import sys

from resources.lib.comaddon import listitem, addon, dialog, window, isNexus, progress, VSlog
from resources.lib.gui.contextElement import cContextElement
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.parser import cParser
from resources.lib.util import QuotePlus


class Gui:

    SITE_NAME = 'Gui'
    CONTENT = ''
    listing = []
    thread_listing = []
    episodeListing = []  # Pour gérer l'enchainement des episodes
    ADDON = addon()
    displaySeason = addon().getSetting('display_season_title')

    # Gérer les résultats de la recherche
    search_results = {}
    search_results_semaphore = threading.Semaphore()

    def get_episode_listing(self):
        return self.episodeListing

    def addNewDir(
            self,
            Type,
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail='',
            sDesc='',
            output_parameter_handler='',
            sMeta=0,
            sCat=None):
        oGuiElement = GuiElement()
        # dir ou link => CONTENT par défaut = files
        if Type != 'dir' and Type != 'link':
            Gui.CONTENT = Type
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)

        if sThumbnail == '':
            oGuiElement.setThumbnail(oGuiElement.getIcon())
        else:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        oGuiElement.setDescription(sDesc)

        if sCat is not None:
            oGuiElement.setCat(sCat)

        # Pour addLink on recupere le sCat et sMeta precedent.
        if Type == 'link':
            input_parameter_handler = InputParameterHandler()
            sCat = input_parameter_handler.getValue('sCat')
            if sCat:
                oGuiElement.setCat(sCat)

            sMeta = input_parameter_handler.getValue('sMeta')
            if sMeta:
                oGuiElement.setMeta(sMeta)
        else:
            output_parameter_handler.addParameter('sMeta', sMeta)
            oGuiElement.setMeta(sMeta)

        # Si pas d'id TMDB pour un episode, on recupère le précédent qui vient de la série
        if sCat and not output_parameter_handler.getValue('sTmdbId'):
            input_parameter_handler = InputParameterHandler()
            sPreviousMeta = int(input_parameter_handler.getValue('sMeta'))
            if 0 < sPreviousMeta < 7:
                sTmdbID = input_parameter_handler.getValue('sTmdbId')
                if sTmdbID:
                    output_parameter_handler.addParameter('sTmdbId', sTmdbID)

        output_parameter_handler.addParameter('sFav', sFunction)

        resumeTime = output_parameter_handler.getValue('ResumeTime')
        if resumeTime:
            oGuiElement.setResumeTime(resumeTime)
            oGuiElement.setTotalTime(output_parameter_handler.getValue('TotalTime'))

        # Lecture en cours
        isViewing = output_parameter_handler.getValue('isViewing')
        if isViewing:
            oGuiElement.addItemProperties('isViewing', True)

        sTitle = output_parameter_handler.getValue('sMovieTitle')
        if sTitle:
            oGuiElement.setFileName(sTitle)
        else:
            oGuiElement.setFileName(sLabel)

        try:
            return self.addFolder(oGuiElement, output_parameter_handler)
        except Exception as error:
            VSlog("addNewDir error: " + str(error))

    #    Categorie       Meta          sCat     CONTENT
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

    def addMovie(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        movieUrl = output_parameter_handler.getValue('siteUrl')
        output_parameter_handler.addParameter('movieUrl', QuotePlus(movieUrl))
        output_parameter_handler.addParameter('movieFunc', sFunction)
        return self.addNewDir('movies', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler, 1, 1)

    def addTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = output_parameter_handler.getValue('siteUrl')
        if saisonUrl:
            output_parameter_handler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            output_parameter_handler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir(
            'tvshows',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            2,
            2)

    def addAnime(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = output_parameter_handler.getValue('siteUrl')
        if saisonUrl:
            output_parameter_handler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            output_parameter_handler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir(
            'tvshows',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            4,
            3)

    def addDrama(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = output_parameter_handler.getValue('siteUrl')
        if saisonUrl:
            output_parameter_handler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            output_parameter_handler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir(
            'tvshows',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            2,
            9)

    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        if sThumbnail or sDesc:
            type = 'videos'
        else:
            type = 'files'
        movieUrl = output_parameter_handler.getValue('siteUrl')
        output_parameter_handler.addParameter('movieUrl', QuotePlus(movieUrl))
        output_parameter_handler.addParameter('movieFunc', sFunction)
        return self.addNewDir(type, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler, 0, 5)

    def addMoviePack(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        return self.addNewDir('sets', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler, 3, 7)

    def addDir(self, sId, sFunction, sLabel, sIcon, output_parameter_handler='', sDesc=""):
        return self.addNewDir('dir', sId, sFunction, sLabel, sIcon, '', sDesc, output_parameter_handler, 0, None)

    def addLink(self, sId, sFunction, sLabel, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        input_parameter_handler = InputParameterHandler()
        output_parameter_handler.addParameter('saisonUrl', input_parameter_handler.getValue('saisonUrl'))
        output_parameter_handler.addParameter('nextSaisonFunc', input_parameter_handler.getValue('nextSaisonFunc'))
        output_parameter_handler.addParameter('movieUrl', input_parameter_handler.getValue('movieUrl'))
        output_parameter_handler.addParameter('movieFunc', input_parameter_handler.getValue('movieFunc'))

        if not output_parameter_handler.getValue('sLang'):
            output_parameter_handler.addParameter('sLang', input_parameter_handler.getValue('sLang'))

        sIcon = sThumbnail
        return self.addNewDir(
            'link',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            0,
            None)

    def addSeason(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = output_parameter_handler.getValue('siteUrl')
        output_parameter_handler.addParameter('saisonUrl', QuotePlus(saisonUrl))
        output_parameter_handler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir(
            'seasons',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            5,
            4)

    def addEpisode(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler=''):
        # Pour gérer l'enchainement des épisodes, l'URL de la saison
        input_parameter_handler = InputParameterHandler()
        saisonUrl = input_parameter_handler.getValue('saisonUrl')
        if saisonUrl:   # Retenu depuis "addSeason"
            output_parameter_handler.addParameter('saisonUrl', saisonUrl)
            output_parameter_handler.addParameter('nextSaisonFunc', input_parameter_handler.getValue('nextSaisonFunc'))
        else:           # calculé depuis l'url qui nous a emmené ici sans passé par addSeason
            output_parameter_handler.addParameter('saisonUrl', input_parameter_handler.getValue('siteUrl'))
            output_parameter_handler.addParameter('nextSaisonFunc', input_parameter_handler.getValue('function'))

        if not output_parameter_handler.getValue('sLang'):
            output_parameter_handler.addParameter('sLang', input_parameter_handler.getValue('sLang'))

        return self.addNewDir(
            'episodes',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            6,
            8)

    # Affichage d'une personne (acteur, réalisateur, ..)
    def addPerson(self, sId, sFunction, sLabel, sIcon, sThumbnail, output_parameter_handler=''):
        sThumbnail = ''
        sDesc = ''
        return self.addNewDir(
            'artists',
            sId,
            sFunction,
            sLabel,
            sIcon,
            sThumbnail,
            sDesc,
            output_parameter_handler,
            7,
            None)

    # Affichage d'un réseau de distribution du média
    def addNetwork(self, sId, sFunction, sLabel, sIcon, output_parameter_handler=''):
        sThumbnail = ''
        sDesc = ''
        return self.addNewDir('', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, output_parameter_handler, 8, None)

    def addNext(self, sId, sFunction, sLabel, output_parameter_handler):
        oGuiElement = GuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle('[COLOR teal]' + sLabel + ' >>>[/COLOR]')
        oGuiElement.setIcon('next.png')
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        oGuiElement.setCat(5)

        self.createContexMenuPageSelect(oGuiElement, output_parameter_handler)
        self.createContexMenuViewBack(oGuiElement, output_parameter_handler)
        return self.addFolder(oGuiElement, output_parameter_handler)

    # utiliser oGui.addText(SITE_IDENTIFIER)
    def addNone(self, sId):
        return self.addText(sId)

    def addText(self, sId, sLabel='', sIcon='none.png'):
        # Pas de texte lors des recherches globales
        if window(10101).getProperty('search') == 'true':
            return

        oGuiElement = GuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction('DoNothing')
        if not sLabel:
            sLabel = self.ADDON.VSlang(30204)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)

        output_parameter_handler = OutputParameterHandler()
        return self.addFolder(oGuiElement, output_parameter_handler)

    # afficher les liens non playable
    def addFolder(self, oGuiElement, output_parameter_handler='', _isFolder=True):
        if _isFolder is False:
            Gui.CONTENT = 'files'

        # recherche append les reponses
        if window(10101).getProperty('search') == 'true':
            self.addSearchResult(oGuiElement, output_parameter_handler)
            return

        # Des infos a rajouter ?
        params = {'siteUrl': oGuiElement.setSiteUrl,
                  'sTmdbId': oGuiElement.setTmdbId,
                  'sYear': oGuiElement.setYear,
                  'sRes': oGuiElement.setRes}

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

        oListItem = self.createListItem(oGuiElement)

    # affiche tag HD
        # https://alwinesch.github.io/group__python__xbmcgui__listitem.html#ga99c7bf16729b18b6378ea7069ee5b138
        sRes = oGuiElement.getRes()
        if sRes:
            if '2160' in sRes:
                oListItem.addStreamInfo('video', {'width': 3840, 'height': 2160})
            elif '1080' in sRes:
                oListItem.addStreamInfo('video', {'width': 1920, 'height': 1080})
            elif '720' in sRes:
                oListItem.addStreamInfo('video', {'width': 1280, 'height': 720})
            elif '480' in sRes:
                oListItem.addStreamInfo('video', {'width': 720, 'height': 576})

        sCat = oGuiElement.getCat()
        if sCat:
            Gui.sCat = sCat
            output_parameter_handler.addParameter('sCat', sCat)

        sItemUrl = self.__createItemUrl(oGuiElement, output_parameter_handler)

        output_parameter_handler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        if _isFolder is True:
            # oListItem.setProperty('IsPlayable', 'true')
            if sCat:    # 1 = movies, moviePack; 2 = series, animes, episodes; 5 = MISC
                if oGuiElement.getMeta():
                    self.createContexMenuinfo(oGuiElement, output_parameter_handler)
                    self.createContexMenuba(oGuiElement, output_parameter_handler)
                if not oListItem.getProperty('isBookmark'):
                    self.createContexMenuBookmark(oGuiElement, output_parameter_handler)

                if sCat in (1, 2, 3, 4, 8, 9):
                    if self.ADDON.getSetting('bstoken') != '':
                        self.createContexMenuTrakt(oGuiElement, output_parameter_handler)
                    if self.ADDON.getSetting('tmdb_account') != '':
                        self.createContexMenuTMDB(oGuiElement, output_parameter_handler)
                if sCat in (1, 2, 3, 4, 9):
                    self.createContexMenuSimil(oGuiElement, output_parameter_handler)
                if sCat != 6:
                    self.createContexMenuWatch(oGuiElement, output_parameter_handler)
        else:
            oListItem.setProperty('IsPlayable', 'true')
            self.createContexMenuWatch(oGuiElement, output_parameter_handler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)
        self.listing.append((sItemUrl, oListItem, _isFolder))

        # Vider les paramètres pour être recyclé
        output_parameter_handler.clearParameter()
        return oListItem

    def createListItem(self, oGuiElement):

        # Récupération des metadonnées par thread
        if oGuiElement.getMeta() and oGuiElement.getMetaAddon() == 'true':
            return self.createListItemThread(oGuiElement)

        # pas de meta, appel direct
        return self._createListItem(oGuiElement)

    # Utilisation d'un Thread pour un chargement des metas en parallèle
    def createListItemThread(self, oGuiElement):
        itemTitle = oGuiElement.getTitle()
        oListItem = listitem(itemTitle)
        t = threading.Thread(target=self._createListItem, name=itemTitle, args=(oGuiElement, oListItem))
        self.thread_listing.append(t)
        t.start()
        return oListItem

    def _createListItem(self, oGuiElement, oListItem=None):

        # Enleve les elements vides
        data = {key: val for key, val in oGuiElement.getItemValues().items() if val != ""}

        itemTitle = oGuiElement.getTitle()

        # Formatage nom episode
        sCat = oGuiElement.getCat()
        if sCat and int(sCat) == 8:  # Nom de l'épisode
            try:
                if 'tagline' in data and data['tagline']:
                    episodeTitle = data['tagline']
                else:
                    episodeTitle = 'Episode ' + str(data['episode'])
                host = ''
                if 'tvshowtitle' in data:
                    host = itemTitle.split(data['tvshowtitle'])[1]
                if self.displaySeason == "true":
                    itemTitle = str(data['season']) + "x" + str(data['episode']) + ". " + episodeTitle
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
            data['duration'] = (sum(x * int(t)
                                for x, t in zip([1, 60, 3600], reversed(data.get('duration', '').split(":")))))

        if not oListItem:
            oListItem = listitem(itemTitle)

        if data.get('cast'):
            credits = json.loads(data['cast'])
            data['cast'] = []
            for i in credits:
                if isNexus():
                    data['cast'].append(xbmc.Actor(i['name'], i['character'], i['order'], i.get('thumbnail', "")))
                else:
                    data['cast'].append((i['name'], i['character'], i['order'], i.get('thumbnail', "")))

        if not isNexus():
            # voir : https://kodi.wiki/view/InfoLabels
            oListItem.setInfo(oGuiElement.getType(), data)

        else:
            videoInfoTag = oListItem.getVideoInfoTag()

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
            videoInfoTag.setDirectors(list(data.get('director', '').split("/")))
            videoInfoTag.setGenres(''.join(data.get('genre', [""])).split('/'))
            videoInfoTag.setSeason(int(data.get('season', 0)))
            videoInfoTag.setEpisode(int(data.get('episode', 0)))
            videoInfoTag.setResumePoint(float(data.get('resumetime', 0.0)), float(data.get('totaltime', 0.0)))

            videoInfoTag.setCast(data.get('cast', []))

        oListItem.setArt({'poster': oGuiElement.getPoster(),
                          'thumb': oGuiElement.getThumbnail(),
                          'icon': oGuiElement.getIcon(),
                          'fanart': oGuiElement.getFanart()})

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey, sPropertyValue in aProperties.items():
            oListItem.setProperty(sPropertyKey, str(sPropertyValue))

        return oListItem

    # Marquer vu/Non vu
    def createContexMenuWatch(self, oGuiElement, output_parameter_handler=''):
        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Gui',
            oGuiElement.getSiteName(),
            'setWatched',
            self.ADDON.VSlang(30206))

    def createContexMenuPageSelect(self, oGuiElement, output_parameter_handler):
        oContext = cContextElement()
        oContext.setFile('Gui')
        oContext.setSiteName('Gui')
        oContext.setFunction('selectPage')
        oContext.setTitle(self.ADDON.VSlang(30017))
        output_parameter_handler.addParameter('OldFunction', oGuiElement.getFunction())
        output_parameter_handler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(output_parameter_handler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuViewBack(self, oGuiElement, output_parameter_handler):
        oContext = cContextElement()
        oContext.setFile('Gui')
        oContext.setSiteName('Gui')
        oContext.setFunction('viewBack')
        oContext.setTitle(self.ADDON.VSlang(30018))
        output_parameter_handler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(output_parameter_handler)
        oGuiElement.addContextItem(oContext)

    # marque page
    def createContexMenuBookmark(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler.addParameter('sCleanTitle', oGuiElement.getCleanTitle())
        output_parameter_handler.addParameter('sId', oGuiElement.getSiteName())
        output_parameter_handler.addParameter('sFav', oGuiElement.getFunction())
        output_parameter_handler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Fav',
            'Fav',
            'setBookmark',
            self.ADDON.VSlang(30210))

    def createContexMenuTrakt(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler.addParameter('sImdbId', oGuiElement.getImdbId())
        output_parameter_handler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        output_parameter_handler.addParameter('sFileName', oGuiElement.getFileName())

        sType = Gui.CONTENT.replace('tvshows', 'shows')
        output_parameter_handler.addParameter('sType', sType)
        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'cTrakt',
            'cTrakt',
            'getAction',
            self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler.addParameter('sImdbId', oGuiElement.getImdbId())
        output_parameter_handler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        output_parameter_handler.addParameter('sFileName', oGuiElement.getFileName())

        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'themoviedb_org',
            'themoviedb_org',
            'getAction',
            'TMDB')

    def createContexMenuDownload(self, oGuiElement, output_parameter_handler='', status='0'):
        if status == '0':
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'StartDownloadOneFile',
                self.ADDON.VSlang(30215))

        if status == '0' or status == '2':
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'delDownload',
                self.ADDON.VSlang(30216))
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'DelFile',
                self.ADDON.VSlang(30217))

        if status == '1':
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'StopDownloadList',
                self.ADDON.VSlang(30218))

        if status == '2':
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'ReadDownload',
                self.ADDON.VSlang(30219))
            self.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                'cDownload',
                'cDownload',
                'ResetDownload',
                self.ADDON.VSlang(30220))

    # Information
    def createContexMenuinfo(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sTitle', oGuiElement.getCleanTitle())
        output_parameter_handler.addParameter('sFileName', oGuiElement.getFileName())
        output_parameter_handler.addParameter('sId', oGuiElement.getSiteName())
        output_parameter_handler.addParameter('sMeta', oGuiElement.getMeta())
        output_parameter_handler.addParameter('sYear', oGuiElement.getYear())
        output_parameter_handler.addParameter('sFav', oGuiElement.getFunction())
        output_parameter_handler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Gui',
            oGuiElement.getSiteName(),
            'viewInfo',
            self.ADDON.VSlang(30208))

    # Bande annonce
    def createContexMenuba(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sTitle', oGuiElement.getTitle())
        output_parameter_handler.addParameter('sFileName', oGuiElement.getFileName())
        output_parameter_handler.addParameter('sYear', oGuiElement.getYear())
        output_parameter_handler.addParameter('sTrailerUrl', oGuiElement.getTrailer())
        output_parameter_handler.addParameter('sMeta', oGuiElement.getMeta())

        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Gui',
            oGuiElement.getSiteName(),
            'viewBA',
            self.ADDON.VSlang(30212))

    # Recherche similaire
    def createContexMenuSimil(self, oGuiElement, output_parameter_handler=''):
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sFileName', oGuiElement.getFileName())
        output_parameter_handler.addParameter('sTitle', oGuiElement.getTitle())
        output_parameter_handler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Gui',
            oGuiElement.getSiteName(),
            'viewSimil',
            self.ADDON.VSlang(30213))

    def createSimpleMenu(self, oGuiElement, output_parameter_handler, sFile, sName, sFunction, sTitle):
        oContext = cContextElement()
        oContext.setFile(sFile)
        oContext.setSiteName(sName)
        oContext.setFunction(sFunction)
        oContext.setTitle(sTitle)

        oContext.setOutputParameterHandler(output_parameter_handler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuDelFav(self, oGuiElement, output_parameter_handler=''):
        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'Fav',
            'Fav',
            'delBookmarksMenu',
            self.ADDON.VSlang(30209))

    def createContexMenuSettings(self, oGuiElement, output_parameter_handler=''):
        self.createSimpleMenu(
            oGuiElement,
            output_parameter_handler,
            'globalParametre',
            'globalParametre',
            'opensetting',
            self.ADDON.VSlang(30023))

    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        # Menus classiques reglés a la base
        nbContextMenu = len(oGuiElement.getContextItems())
        if nbContextMenu > 0:
            for oContextItem in oGuiElement.getContextItems():
                output_parameter_handler = oContextItem.getOutputParameterHandler()
                sParams = output_parameter_handler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (
                    sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                sDecoColor = self.ADDON.getSetting('deco_color')
                titleMenu = '[COLOR %s]%s[/COLOR]' % (sDecoColor, oContextItem.getTitle())
                aContextMenus += [(titleMenu, 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus)
        oListItem.setProperty('nbcontextmenu', str(nbContextMenu))

        return oListItem

    def __createItemUrl(self, oGuiElement, output_parameter_handler=''):
        if output_parameter_handler == '':
            output_parameter_handler = OutputParameterHandler()

        # On descend l'id TMDB dans les saisons et les épisodes
        output_parameter_handler.addParameter('sTmdbId', oGuiElement.getTmdbId())

        # Pour gérer l'enchainement des épisodes
        output_parameter_handler.addParameter('sSeason', oGuiElement.getSeason())
        output_parameter_handler.addParameter('sEpisode', oGuiElement.getEpisode())

        sParams = output_parameter_handler.getParameterAsUri()

        sPluginPath = cPluginHandler().getPluginPath()

        if len(oGuiElement.getFunction()) == 0:
            sItemUrl = '%s?site=%s&title=%s&%s' % (
                sPluginPath, oGuiElement.getSiteName(), QuotePlus(oGuiElement.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(
            ), oGuiElement.getFunction(), QuotePlus(oGuiElement.getCleanTitle()), sParams)

        return sItemUrl

    def setEndOfDirectory(self, forceViewMode=False):
        iHandler = cPluginHandler().getPluginHandle()

        if not self.listing:
            self.addText('Gui')

        # attendre l'arret des thread utilisés pour récupérer les métadonnées
        total = len(self.thread_listing)
        if total > 0:
            progress_ = progress().VScreate(addon().VSlang(30141))
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
        # 50 = liste / 51 grande liste / 500 icone / 501 gallerie / 508 fanart /
        if forceViewMode:
            xbmc.executebuiltin('Container.SetViewMode(' + str(forceViewMode) + ')')
        else:
            if self.ADDON.getSetting('active-view') == 'true':
                if Gui.CONTENT == 'movies' or Gui.CONTENT == 'artists':
                    # xbmc.executebuiltin('Container.SetViewMode(507)')
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('movies-view'))
                elif Gui.CONTENT in ['tvshows', 'seasons', 'episodes']:
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting(Gui.CONTENT + '-view'))
                elif Gui.CONTENT == 'files':
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('default-view'))

        del self.episodeListing[:]  # Pour l'enchainement des episodes
        self.episodeListing.extend(self.listing)

        del self.listing[:]

    def updateDirectory(self):  # refresh the content
        xbmc.executebuiltin('Container.Refresh')
        xbmc.sleep(600)    # Nécessaire pour laisser le temps du refresh

    def viewBA(self):
        input_parameter_handler = InputParameterHandler()
        sFileName = input_parameter_handler.getValue('sFileName')
        sYear = input_parameter_handler.getValue('sYear')
        sTrailerUrl = input_parameter_handler.getValue('sTrailerUrl')
        sMeta = input_parameter_handler.getValue('sMeta')

        from resources.lib.ba import cShowBA
        cBA = cShowBA()
        cBA.set_search(sFileName)
        cBA.set_year(sYear)
        cBA.set_trailer_url(sTrailerUrl)
        cBA.set_meta_type(sMeta)
        cBA.search_ba()

    def viewBack(self):
        sPluginPath = cPluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        # sParams = input_parameter_handler.getAllParameter()
        sId = input_parameter_handler.getValue('sId')
        sTest = '%s?site=%s' % (sPluginPath, sId)

        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def viewInfo(self):
        if addon().getSetting('information-view') == "false":
            from resources.lib.config import WindowsBoxes

            input_parameter_handler = InputParameterHandler()
            sCleanTitle = input_parameter_handler.getValue('sTitle') if input_parameter_handler.exist(
                'sTitle') else xbmc.getInfoLabel('ListItem.Title')
            sMeta = input_parameter_handler.getValue('sMeta') if input_parameter_handler.exist(
                'sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            sYear = input_parameter_handler.getValue('sYear') if input_parameter_handler.exist(
                'sYear') else xbmc.getInfoLabel('ListItem.Year')
            sUrl = input_parameter_handler.getValue('siteUrl') if input_parameter_handler.exist(
                'siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
            sSite = input_parameter_handler.getValue('sId') if input_parameter_handler.exist(
                'sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
            sFav = input_parameter_handler.getValue('sFav') if input_parameter_handler.exist(
                'sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')
            sCat = input_parameter_handler.getValue('sCat') if input_parameter_handler.exist(
                'sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

            WindowsBoxes(sCleanTitle, sUrl, sMeta, sYear, sSite, sFav, sCat)
        else:
            # On appel la fonction integrée a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')

    def viewSimil(self):
        sPluginPath = cPluginHandler().getPluginPath()

        input_parameter_handler = InputParameterHandler()
        sCleanTitle = input_parameter_handler.getValue('sTitle') if input_parameter_handler.exist(
            'sTitle') else xbmc.getInfoLabel('ListItem.Title')
        sCat = input_parameter_handler.getValue('sCat') if input_parameter_handler.exist(
            'sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('searchtext', sCleanTitle)
        output_parameter_handler.addParameter('sCat', sCat)

        sParams = output_parameter_handler.getParameterAsUri()
        sTest = '?site=%s&function=%s&%s' % ('globalSearch', 'globalSearch', sParams)
        sys.argv[2] = sTest
        sTest = sPluginPath + sTest

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % 10025)

        xbmc.executebuiltin('Container.Update(%s)' % sTest)
        return True

    def selectPage(self):
        sPluginPath = cPluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        # sParams = input_parameter_handler.getAllParameter()
        sId = input_parameter_handler.getValue('sId')
        sFunction = input_parameter_handler.getValue('OldFunction')
        siteUrl = input_parameter_handler.getValue('siteUrl')

        if siteUrl.endswith('/'):  # for the url http.://www.1test.com/annee-2020/page-2/
            urlSource = siteUrl.rsplit('/', 2)[0]
            endOfUrl = siteUrl.rsplit('/', 2)[1] + '/'
        else:  # for the url http.://www.1test.com/annee-2020/page-2 or /page-2.html
            urlSource = siteUrl.rsplit('/', 1)[0]
            endOfUrl = siteUrl.rsplit('/', 1)[1]

        oParser = cParser()
        oldNum = oParser.getNumberFromString(endOfUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = urlSource + '/' + endOfUrl.replace(oldNum, newNum, 1)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', siteUrl)
                sParams = output_parameter_handler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
                xbmc.executebuiltin('Container.Update(%s)' % sTest)
            except BaseException:
                return False

        return False

    def selectPage2(self):
        sPluginPath = cPluginHandler().getPluginPath()
        input_parameter_handler = InputParameterHandler()
        sId = input_parameter_handler.getValue('sId')
        sFunction = input_parameter_handler.getValue('OldFunction')
        siteUrl = input_parameter_handler.getValue('siteUrl')

        selpage = self.showNumBoard()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', siteUrl)
        output_parameter_handler.addParameter('Selpage', selpage)

        sParams = output_parameter_handler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def setWatched(self):
        if True:
            # Use vStream database
            input_parameter_handler = InputParameterHandler()
            sSite = input_parameter_handler.getValue('siteUrl')
            sTitle = input_parameter_handler.getValue('sTitleWatched')
            sCat = input_parameter_handler.getValue('sCat')
            if not sTitle:
                return

            meta = {}
            meta['title'] = sTitle
            meta['titleWatched'] = sTitle
            meta['site'] = sSite
            meta['cat'] = sCat

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
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def showNumBoard(self, sTitle="", sDefaultNum=''):
        dialogs = dialog()
        if not sTitle:
            sTitle = self.ADDON.VSlang(30019)
        numboard = dialogs.numeric(0, sTitle, sDefaultNum)
        # numboard.doModal()
        if numboard is not None:
            return numboard

        return False

    def openSettings(self):
        return False

    def showNofication(self, sTitle, iSeconds=0):
        return False

    def showError(self, sTitle, sDescription, iSeconds=0):
        return False

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        return False

    def getSearchResult(self):
        Gui.search_results_semaphore.acquire()
        result = copy.deepcopy(Gui.search_results)
        Gui.search_results_semaphore.release()
        return result

    def addSearchResult(self, oGuiElement, output_parameter_handler):
        Gui.search_results_semaphore.acquire()
        searchSiteId = output_parameter_handler.getValue('searchSiteId')
        if not searchSiteId:
            searchSiteId = oGuiElement.getSiteName()

        if searchSiteId not in Gui.search_results:
            Gui.search_results[searchSiteId] = []

        Gui.search_results[searchSiteId].append({'guiElement': oGuiElement,
                                                 'params': copy.deepcopy(output_parameter_handler)})
        Gui.search_results_semaphore.release()

    def resetSearchResult(self):
        Gui.search_results_semaphore.acquire()
        Gui.search_results = {}
        Gui.search_results_semaphore.release()
