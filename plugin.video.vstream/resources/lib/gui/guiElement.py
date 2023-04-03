# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import xbmc

from resources.lib.comaddon import Addon, isMatrix, isNexus
from resources.lib.db import Db
from resources.lib.util import cUtil, QuoteSafe

# rouge E26543
# jaune F7D571
# bleu clair 87CEEC  ou skyblue / hoster
# vert 37BCB5
# bleu foncé 08435A / non utilisé


class GuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'

    def __init__(self):

        self.addons = Addon()

        # self.__sRootArt = cConfig().getRootArt()
        self.__sFunctionName = ''
        self.__sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/'
        self.__sType = 'video'
        self.__sMeta = 0
        self.__sTrailer = ''
        self.__sMetaAddon = self.addons.getSetting('meta-view')
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        # contient le titre qui sera coloré
        self.__sTitle = ''
        # contient le titre propre
        self.__sCleanTitle = ''
        # titre considéré Vu
        self.__sTitleWatched = ''
        self.__ResumeTime = 0   # Durée déjà lue de la vidéo
        self.__TotalTime = 0    # Durée totale de la vidéo

        # contient le titre modifié pour BDD
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sGenre = ''
        self.__sThumbnail = ''
        self.__sPoster = ''
        self.__Season = ''
        self.__Episode = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = 'special://home/addons/plugin.video.vstream/fanart.jpg'
        self.poster = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting(
            'poster_tmdb')
        self.fanart = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting(
            'backdrop_tmdb')
        # For meta search
        # TmdbId the movie database https://developers.themoviedb.org/
        self.__TmdbId = ''
        # ImdbId pas d'api http://www.imdb.com/
        self.__ImdbId = ''
        self.__Year = ''

        self.__sRes = ''  # resolution

        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''

        # categorie utilisé pour marque-page et recherche.
        # 1 - movies/saga , 2 - tvshow/episode/anime, 5 - misc/Next
        self.__sCat = ''

    # def __len__(self): return self.__sCount

    # def getCount(self):
    #     return GuiElement.COUNT

    def setType(self, _type):
        self.__sType = _type

    def getType(self):
        return self.__sType

    def setCat(self, cat):
        self.__sCat = cat

    def getCat(self):
        return self.__sCat

    def setMetaAddon(self, sMetaAddon):
        self.__sMetaAddon = sMetaAddon

    def getMetaAddon(self):
        return self.__sMetaAddon

    def setTrailer(self, sTrailer):
        self.__sTrailer = sTrailer

    def getTrailer(self):
        return self.__sTrailer

    def setTmdbId(self, data):
        self.__TmdbId = data if data != '0' else ''

    def getTmdbId(self):
        return self.__TmdbId

    def setImdbId(self, data):
        self.__ImdbId = data

    def getImdbId(self):
        return self.__ImdbId

    def setYear(self, data):
        self.__Year = data

    def getYear(self):
        return self.__Year

    def setRes(self, data):
        if data.upper() in ('1080P', 'FHD', 'FULLHD'):
            data = '1080p'
        elif data.upper() in ('720P', 'DVDRIP', 'DVDSCR', 'HD', 'HDLIGHT', 'HDRIP', 'BDRIP', 'BRRIP'):
            data = '720p'
        elif data.upper() in ('4K', 'UHD', '2160P'):
            data = '2160p'

        self.__sRes = data

    def getRes(self):
        return self.__sRes

    def setGenre(self, genre):
        self.__sGenre = genre

    def getGenre(self):
        return self.__sGenre

    def getSeason(self):
        return self.__Season

    def getEpisode(self):
        return self.__Episode

    def setTotalTime(self, data):
        self.__TotalTime = data

    def getTotalTime(self):
        return self.__TotalTime

    def setResumeTime(self, data):
        self.__ResumeTime = data

    def getResumeTime(self):
        return self.__ResumeTime

    def setMeta(self, sMeta):
        self.__sMeta = sMeta

    def getMeta(self):
        return self.__sMeta

    def setMediaUrl(self, media_url):
        self.__sMediaUrl = media_url

    def getMediaUrl(self):
        return self.__sMediaUrl

    def setSiteUrl(self, site_url):
        self.__sSiteUrl = site_url

    def getSiteUrl(self):
        return self.__sSiteUrl

    def setSiteName(self, site_name):
        self.__sSiteName = site_name

    def getSiteName(self):
        return self.__sSiteName

    def setFileName(self, file_name):
        self.__sFileName = cUtil().titleWatched(file_name)

    def getFileName(self):
        return self.__sFileName

    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def TraiteTitre(self, title):

        # convertion unicode ne fonctionne pas avec les accents
        try:
            # traitement du titre pour retirer le - quand c'est une Saison.
            # Tiret, tiret moyen et cadratin
            title = title.replace(
                'Season',
                'saison').replace(
                'season',
                'saison').replace(
                'SEASON',
                'saison') .replace(
                'Saison',
                'saison').replace(
                    'SAISON',
                'saison')
            title = title.replace(
                ' - saison',
                ' saison').replace(
                ' – saison',
                ' saison') .replace(
                ' — saison',
                ' saison')

            if not isMatrix():
                title = title.decode('utf-8')
        except BaseException:
            pass

        """ Début du nettoyage du titre """
        # vire doubles espaces et double points
        title = re.sub(' +', ' ', title)
        title = re.sub('\\.+', '.', title)

        # enleve les crochets et les parentheses si elles sont vides
        title = title.replace('()', '').replace('[]', '').replace('- -', '-')

        # vire espace et - a la fin
        title = re.sub('[- –_\\.]+$', '', title)
        # et au debut
        title = re.sub('^[- –_\\.]+', '', title)

        """ Fin du nettoyage du titre """

        # recherche l'année, uniquement si entre caractere special a cause de
        # 2001 odysse de l'espace ou k2000
        string = re.search('[^\\w ]([0-9]{4})[^\\w ]', title)
        if string:
            title = title.replace(string.group(0), '')
            self.__Year = str(string.group(1))
            self.addItemValues('year', self.__Year)

        # recherche une date
        string = re.search('([\\d]{2}[\\/|-]\\d{2}[\\/|-]\\d{4})', title)
        if string:
            title = title.replace(string.group(0), '')
            self.__Date = str(string.group(0))
            title = '%s (%s) ' % (title, self.__Date)

        # recherche les Tags restant : () ou [] sauf tag couleur
        sDecoColor = self.addons.getSetting('deco_color')
        title = re.sub(
            '([\\(|\\[](?!\\/*COLOR)[^\\)\\(\\]\\[]+?[\\]|\\)])',
            '[COLOR ' + sDecoColor + ']\\1[/COLOR]',
            title)

        # Recherche saisons et episodes
        sa = ep = ''
        m = re.search(
            '(|S|saison)(\\s?|\\.)(\\d+)(\\s?|\\.)(E|Ep|x|\\wpisode)(\\s?|\\.)(\\d+)',
            title,
            re.UNICODE)
        if m:
            title = title.replace(m.group(0), '')
            sa = m.group(3)
            ep = m.group(7)
        else:  # Juste l'épisode
            m = re.search(
                '(^|\\s|\\.)(E|Ep|\\wpisode)(\\s?|\\.)(\\d+)',
                title,
                re.UNICODE)
            if m:
                title = title.replace(m.group(0), '')
                ep = m.group(4)
            else:  # juste la saison
                m = re.search(
                    '( S|saison)(\\s?|\\.)(\\d+)',
                    title,
                    re.UNICODE)
                if m:
                    title = title.replace(m.group(0), '')
                    sa = m.group(3)

        # enleve les crochets et les parentheses si elles sont vides
        if sa or ep:
            title = title.replace(
                '()',
                '').replace(
                '[]',
                '').replace(
                '- -',
                '-')

        if sa:
            self.__Season = sa
            self.addItemValues('Season', self.__Season)
        if ep:
            self.__Episode = ep
            self.addItemValues('Episode', self.__Episode)

        # on repasse en utf-8
        if not isMatrix():
            try:
                title = title.encode('utf-8')
            except BaseException:
                pass

        # on reformate SXXEXX Titre [tag] (Annee)
        title2 = ''
        if self.__Season:
            title2 = title2 + 'S%02d' % int(self.__Season)
        if self.__Episode:
            title2 = title2 + 'E%02d' % int(self.__Episode)

        # Titre unique pour marquer VU (avec numéro de l'épisode pour les
        # séries)
        self.__sTitleWatched = cUtil().titleWatched(title).replace(' ', '')
        if title2:
            self.addItemValues('tvshowtitle', cUtil().getSerieTitre(title))
            self.__sTitleWatched += '_' + title2
        self.addItemValues('originaltitle', self.__sTitleWatched)

        if title2:
            title2 = '[COLOR %s]%s[/COLOR] ' % (sDecoColor, title2)

        title2 = title2 + title

        if self.__Year:
            title2 = '%s [COLOR %s](%s)[/COLOR]' % (title2,
                                                     sDecoColor, self.__Year)

        return title2

    def setTitle(self, title):
        # Nom en clair sans les langues, qualités, et autres décorations
        self.__sCleanTitle = re.sub('\\[.*\\]|\\(.*\\)', '', title)
        if not self.__sCleanTitle:
            self.__sCleanTitle = re.sub('\\[.+?\\]|\\(.+?\\)', '', title)
            if not self.__sCleanTitle:
                self.__sCleanTitle = title.replace(
                    '[', '').replace(
                    ']', '').replace(
                    '(', '').replace(
                    ')', '')

        if isMatrix():
            # Python 3 decode title
            try:
                title = str(title.encode('latin-1'), 'utf-8')
            except BaseException:
                pass
        else:
            try:
                title = str(title.strip().decode('utf-8'))
            except BaseException:
                pass

        if not title.startswith('[COLOR'):
            self.__sTitle = self.TraiteTitre(title)
        else:
            self.__sTitle = title

    def getTitle(self):
        return self.__sTitle

    def getCleanTitle(self):
        return self.__sCleanTitle

   # def setTitleWatched(self, title_watched):
       # self.__sTitleWatched = title_watched

    def getTitleWatched(self):
        return self.__sTitleWatched

    def setDescription(self, description):
        # Py3
        if isMatrix():
            try:
                if 'Ã' in description or '\\xc' in description:
                    self.__sDescription = str(
                        description.encode('latin-1'), 'utf-8')
                else:
                    self.__sDescription = description
            except BaseException:
                self.__sDescription = description
        else:
            self.__sDescription = description

    def getDescription(self):
        return self.__sDescription

    def setThumbnail(self, thumbnail):
        self.__sThumbnail = thumbnail

    def getThumbnail(self):
        return self.__sThumbnail

    def setPoster(self, sPoster):
        self.__sPoster = sPoster

    def getPoster(self):
        return self.__sPoster

    def setFanart(self, sFanart):
        if sFanart != '':
            self.__sFanart = sFanart

    def setMovieFanart(self):
        self.__sFanart = self.__sFanart

    def setTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirectTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirFanart(self, icon):
        self.__sFanart = self.__sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, icon):
        if not icon:
            self.__sIcon = ''
            return
        try:
            self.__sIcon = unicode(icon, 'utf-8')
        except BaseException:
            self.__sIcon = icon
        self.__sIcon = self.__sIcon.encode('utf-8')
        self.__sIcon = QuoteSafe(self.__sIcon)

    def getIcon(self):
        # if 'http' in self.__sIcon:
        #    return UnquotePlus(self.__sIcon)
        folder = 'special://home/addons/plugin.video.vstream/resources/art'
        path = '/'.join([folder, self.__sIcon])
        # return os.path.join(unicode(self.__sRootArt, 'utf-8'), self.__sIcon)
        return path

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue

    def getItemValue(self, sItemKey):
        if sItemKey not in self.__aItemValues:
            return
        return self.__aItemValues[sItemKey]

    def getWatched(self):

        # Fonctionne pour marquer lus un dossier
        if not self.getTitleWatched():
            return 0

        meta = {'title': self.getTitleWatched(),
                'site': self.getSiteUrl(),
                'cat': self.getCat()
                }

        with Db() as db:
            data = db.get_watched(meta)
        return data

    def getInfoLabel(self):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'),
                # 'label': xbmc.getInfoLabel('ListItem.title'),
                # 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'),
                'year': xbmc.getInfoLabel('ListItem.year'),
                'genre': xbmc.getInfoLabel('ListItem.genre'),
                'director': xbmc.getInfoLabel('ListItem.director'),
                'country': xbmc.getInfoLabel('ListItem.country'),
                'rating': xbmc.getInfoLabel('ListItem.rating'),
                'votes': xbmc.getInfoLabel('ListItem.votes'),
                'mpaa': xbmc.getInfoLabel('ListItem.mpaa'),
                'duration': xbmc.getInfoLabel('ListItem.duration'),
                'trailer': xbmc.getInfoLabel('ListItem.trailer'),
                'writer': xbmc.getInfoLabel('ListItem.writer'),
                'studio': xbmc.getInfoLabel('ListItem.studio'),
                'tagline': xbmc.getInfoLabel('ListItem.tagline'),
                'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'),
                'plot': xbmc.getInfoLabel('ListItem.plot'),
                'poster_path': xbmc.getInfoLabel('ListItem.Art(thumb)'),
                'backdrop_path': xbmc.getInfoLabel('ListItem.Art(fanart)'),
                'imdbnumber': xbmc.getInfoLabel('ListItem.IMDBNumber'),
                'season': xbmc.getInfoLabel('ListItem.season'),
                'episode': xbmc.getInfoLabel('ListItem.episode'),
                'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle')
                }

        if 'title' in meta and meta['title']:
            meta['title'] = self.getTitle()

        if 'backdrop_path' in meta and meta['backdrop_path']:
            url = meta.pop('backdrop_path')
            self.addItemProperties('fanart_image', url)
            self.__sFanart = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'poster_path' in meta and meta['poster_path']:
            url = meta.pop('poster_path')
            self.__sThumbnail = url
            self.__sPoster = url

        # Completer au besoin
        for key, value in meta.items():
            if value:
                self.addItemValues(key, value)

        return

    def getMetadonne(self):
        meta_type = self.getMeta()
        if meta_type == 0:  # non media -> on sort, et on enleve le fanart
            self.addItemProperties('fanart_image', '')
            return

        from resources.lib.tmdb import TMDb
        TMDb = TMDb()

        title = self.__sFileName

        # title = self.__sTitle.decode('latin-1').encode('utf-8')
        # title = re.sub(r'\[.*\]|\(.*\)', r'', str(self.__sFileName))
        # title = title.replace('VF', '').replace('VOSTFR', '').replace('FR', '')

        # On nettoie le titre pour la recherche
        title = title.replace('version longue', '')

        # Integrale de films, on nettoie le titre pour la recherche
        if meta_type == 3:
            title = title.replace('integrales', '')
            title = title.replace('integrale', '')
            title = title.replace('2 films', '')
            title = title.replace('6 films', '')
            title = title.replace('7 films', '')
            title = title.replace('trilogie', '')
            title = title.replace('trilogy', '')
            title = title.replace('quadrilogie', '')
            title = title.replace('pentalogie', '')
            title = title.replace('octalogie', '')
            title = title.replace('hexalogie', '')
            title = title.replace('tetralogie', '')
            title = title.strip()
            if title.endswith(' les'):
                title = title[:-4]
            elif title.endswith(' la'):
                title = title[:-3]
            elif title.endswith(' l'):
                title = title[:-2]
            title = title.strip()

        # tvshow
        if meta_type in (2, 4, 5, 6):
            tvshowtitle = self.getItemValue('tvshowtitle')
            if tvshowtitle:
                title = tvshowtitle

        _type = str(meta_type).replace(
            '1',
            'movie').replace(
            '2',
            'tvshow').replace(
            '3',
            'collection') .replace(
                '4',
                'anime').replace(
                    '5',
                    'season').replace(
                        '6',
                        'episode') .replace(
                            '7',
                            'person').replace(
                                '8',
            'network')

        meta = {}
        try:
            if _type:
                args = (_type, title)
                kwargs = {}
                if self.__ImdbId:
                    kwargs['imdb_id'] = self.__ImdbId
                if self.__TmdbId:
                    kwargs['tmdb_id'] = self.__TmdbId
                if self.__Year:
                    kwargs['year'] = self.__Year
                if self.__Season:
                    kwargs['season'] = self.__Season
                if self.__Episode:
                    kwargs['episode'] = self.__Episode

                meta = TMDb.get_meta(*args, **kwargs)
                if not meta:
                    return
            else:
                return
        except BaseException:
            return

        if 'media_type' in meta:
            meta.pop('media_type')

        if 'imdb_id' in meta:
            imdb_id = meta.pop('imdb_id')
            if imdb_id:
                self.__ImdbId = imdb_id

        if 'tmdb_id' in meta:
            tmdb_id = meta.pop('tmdb_id')
            if tmdb_id:
                self.__TmdbId = tmdb_id

        if 'tvdb_id' in meta:
            meta.pop('tvdb_id')

        if 'backdrop_path' in meta:
            url = meta.pop('backdrop_path')
            if url:
                self.addItemProperties('fanart_image', url)
                self.__sFanart = url
            else:
                self.addItemProperties('fanart_image', '')

        if 'poster_path' in meta:
            url = meta.pop('poster_path')
            if url:
                self.__sThumbnail = url
                self.__sPoster = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'guest_stars' in meta:
            meta.pop('guest_stars')

        if 'nbseasons' in meta:
            meta['season'] = meta.pop('nbseasons')

        # Retrait des tags intermédiaires
        if 'vote' in meta:
            meta.pop('vote')
        if 'runtime' in meta:
            meta.pop('runtime')
        if 'crew' in meta:
            meta.pop('crew')
        if 'overview' in meta:
            meta.pop('overview')
        if 'vote_average' in meta:
            meta.pop('vote_average')
        if 'vote_count' in meta:
            meta.pop('vote_count')
        if 'backdrop_url' in meta:
            meta.pop('backdrop_url')

        for key, value in meta.items():
            self.addItemValues(key, value)

        return

    def getItemValues(self):
        self.addItemValues('title', self.getTitle())

        # https://kodi.wiki/view/InfoLabels
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14

        # - Video Values:
        # - genre : string (Comedy)
        # - year : integer (2009)
        # - episode : integer (4)
        # - season : integer (1)
        # - top250 : integer (192)
        # - tracknumber : integer (3)
        # - rating : float (6.4) - range is 0..10
        # - watched : depreciated - use playcount instead
        # - playcount : integer (2) - number of times this item has been played
        # - overlay : integer (2) - range is 0..8. See GUIListItem.h for values
        # - cast : list (Michal C. Hall)
        # - castandrole : list (Michael C. Hall|Dexter)
        # - director : string (Dagur Kari)
        # - mpaa : string (PG-13)
        # - plot : string (Long Description)
        # - plotoutline : string (Short Description)
        # - title : string (Big Fan)
        # - originaltitle : string (Big Fan)
        # - sorttitle : string (Big Fan)
        # - duration : string (3:18)
        # - studio : string (Warner Bros.)
        # - tagline : string (An awesome movie) - short description of movie
        # - writer : string (Robert D. Siegel)
        # - tvshowtitle : string (Heroes)
        # - premiered : string (2005-03-04)
        # - status : string (Continuing) - status of a TVshow
        # - code : string (tt0110293) - IMDb code
        # - aired : string (2008-12-07)
        # - credits : string (Andy Kaufman) - writing credits
        # - lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
        # - album : string (The Joshua Tree)
        # - artist : list (['U2'])
        # - votes : string (12345 votes)
        # - trailer : string (/home/user/trailer.avi)
        # - dateadded : string (Y-m-d h:m:s = 2009-04-05 23:16:04)

        if self.getMetaAddon() == 'true':
            self.getMetadonne()

        # tmdbid
        if self.getTmdbId():
            self.addItemProperties('TmdbId', str(self.getTmdbId()))
            # only for library content : self.addItemValues('DBID',
            # str(self.getTmdbId()))

        # imdbid
        if self.getImdbId():
            self.addItemProperties('ImdbId', str(self.getImdbId()))
            # self.addItemValues('imdbnumber', str(self.getTmdbId()))

        # Utilisation des infos connues si non trouvées
        if not self.getItemValue('plot') and self.getDescription():
            self.addItemValues('plot', self.getDescription())
        if not self.getItemValue('year') and self.getYear():
            self.addItemValues('year', self.getYear())
        if not self.getItemValue('genre') and self.getGenre():
            self.addItemValues('genre', self.getGenre())
        # if not self.getItemValue('cover_url') and self.getThumbnail():
            # self.addItemValues('cover_url', self.getThumbnail())
        # if not self.getItemValue('backdrop_path') and self.getPoster():
            # self.addItemValues('backdrop_path', self.getPoster())
        if not self.getItemValue('trailer'):
            if self.getTrailer():
                self.addItemValues('trailer', self.getTrailer())
            else:
                # Faux trailer qui ne se lance pas mais evite une erreur
                self.addItemValues('trailer', 'plugin')
                # self.addItemValues('trailer', self.getDefaultTrailer())

        # Used only if there is data in db, overwrite getMetadonne()
        cat = str(self.getCat())
        try:
            if cat and int(cat) in (
                    1, 2, 3, 4, 5, 8, 9):  # Vérifier seulement si de type média
                if self.getWatched():
                    self.addItemValues('playcount', 1)
        except BaseException:
            cat = False

        self.addItemProperties('site_url', self.getSiteUrl())
        self.addItemProperties('clean_title', self.getFileName())
        self.addItemProperties('s_id', self.getSiteName())
        self.addItemProperties('fav', self.getFunction())
        self.addItemProperties('sMeta', str(self.getMeta()))
        if isNexus():
            self.addItemValues('resumetime', self.getResumeTime())
            self.addItemValues('totaltime', self.getTotalTime())
        else:
            self.addItemProperties('resumetime', self.getResumeTime())
            self.addItemProperties('totaltime', self.getTotalTime())

        if cat:
            self.addItemProperties('cat', cat)
            mediatypes = {
                '1': 'movie',
                '2': 'tvshow',
                '3': 'tvshow',
                '4': 'season',
                '5': 'video',
                '6': 'video',
                '7': 'season',
                '8': 'episode',
                '9': 'tvshow'}
            if cat in mediatypes.keys():
                mediatype = mediatypes.get(cat)
                # video, movie, tvshow, season, episode, musicvideo
                self.addItemValues('mediatype', mediatype)

        if self.getSeason():
            self.addItemValues('season', int(self.getSeason()))

        if self.getEpisode():
            self.addItemValues('episode', int(self.getEpisode()))

        return self.__aItemValues

    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements
