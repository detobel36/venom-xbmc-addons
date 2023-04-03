# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.contextElement import ContextElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import dialog, Addon, VSlog, window


class HosterGui:
    SITE_NAME = 'HosterGui'
    ADDON = Addon()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(
            self,
            gui,
            hoster,
            media_url,
            thumbnail,
            bGetRedirectUrl=False,
            input_parameter_handler=False):
        output_parameter_handler = OutputParameterHandler()
        if not input_parameter_handler:
            input_parameter_handler = InputParameterHandler()

        # Gestion NextUp
        site_url = input_parameter_handler.getValue('site_url')
        site = input_parameter_handler.getValue('site')
        saison_url = input_parameter_handler.getValue('saison_url')
        nextSaisonFunc = input_parameter_handler.getValue('nextSaisonFunc')
        movie_url = input_parameter_handler.getValue('movie_url')
        movieFunc = input_parameter_handler.getValue('movieFunc')
        lang = input_parameter_handler.getValue('lang')
        resolution = input_parameter_handler.getValue('resolution')
        tmdb_id = input_parameter_handler.getValue('tmdb_id')
        fav = input_parameter_handler.getValue('fav')
        if not fav:
            fav = input_parameter_handler.getValue('function')
        searchSiteId = input_parameter_handler.getValue('searchSiteId')
        if searchSiteId:
            output_parameter_handler.addParameter('searchSiteId', searchSiteId)
        output_parameter_handler.addParameter(
            'searchSiteName', input_parameter_handler.getValue('searchSiteName'))
        output_parameter_handler.addParameter(
            'qual', input_parameter_handler.getValue('qual'))

        gui_element = GuiElement()
        gui_element.setSiteName(self.SITE_NAME)
        gui_element.setFunction('play')
        gui_element.setTitle(hoster.getDisplayName())

        # Catégorie de lecture
        if input_parameter_handler.exist('cat'):
            cat = input_parameter_handler.getValue('cat')
            if cat == '4':  # Si on vient de passer par un menu "Saison" ...
                cat = '8'   # ...  On est maintenant au niveau "Episode"
        else:
            cat = '5'     # Divers
        gui_element.setCat(cat)
        output_parameter_handler.addParameter('cat', cat)

        if input_parameter_handler.exist('sMeta'):
            sMeta = input_parameter_handler.getValue('sMeta')
            gui_element.setMeta(int(sMeta))

        gui_element.setFileName(hoster.getFileName())
        gui_element.getInfoLabel()
        gui_element.setIcon('host.png')
        if thumbnail:
            gui_element.setThumbnail(thumbnail)
            gui_element.setPoster(thumbnail)

        title = gui_element.getCleanTitle()

        output_parameter_handler.addParameter('media_url', media_url)
        output_parameter_handler.addParameter(
            'hoster_identifier', hoster.getPluginIdentifier())
        output_parameter_handler.addParameter(
            'bGetRedirectUrl', bGetRedirectUrl)
        output_parameter_handler.addParameter(
            'file_name', hoster.getFileName())
        output_parameter_handler.addParameter(
            'title_watched', gui_element.getTitleWatched())
        output_parameter_handler.addParameter('title', title)
        output_parameter_handler.addParameter('lang', lang)
        output_parameter_handler.addParameter('resolution', resolution)
        output_parameter_handler.addParameter('s_id', 'HosterGui')
        output_parameter_handler.addParameter('site_url', site_url)
        output_parameter_handler.addParameter('tmdb_id', tmdb_id)

        # gestion NextUp
        output_parameter_handler.addParameter(
            'sourceName', site)    # source d'origine
        output_parameter_handler.addParameter(
            'sourceFav', fav)    # source d'origine
        output_parameter_handler.addParameter('nextSaisonFunc', nextSaisonFunc)
        output_parameter_handler.addParameter('saison_url', saison_url)

        # gestion Lecture en cours
        output_parameter_handler.addParameter('movie_url', movie_url)
        output_parameter_handler.addParameter('movieFunc', movieFunc)

        # Download menu
        if hoster.isDownloadable():
            oContext = ContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(output_parameter_handler)
            gui_element.addContextItem(oContext)

            # Beta context download and view menu
            oContext = ContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(output_parameter_handler)
            gui_element.addContextItem(oContext)

        # Liste de lecture
        oContext = ContextElement()
        oContext.setFile('HosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(output_parameter_handler)
        gui_element.addContextItem(oContext)

        # Dossier Media
        gui.createSimpleMenu(
            gui_element,
            output_parameter_handler,
            'Library',
            'Library',
            'setLibrary',
            self.ADDON.VSlang(30324))

        # Upload menu uptobox
        if InputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting(
                'hoster_uptobox_premium') == 'true':
            host = hoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    gui.createSimpleMenu(
                        gui_element,
                        output_parameter_handler,
                        'siteuptobox',
                        'siteuptobox',
                        'upToMyAccount',
                        self.ADDON.VSlang(30325))
                    break

        # onefichier
        if InputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting(
                'hoster_onefichier_premium') == 'true':
            host = hoster.getPluginIdentifier()
            accept = '1fichier'  # les autres ne fonctionnent pas
            if host == accept:
                gui.createSimpleMenu(
                    gui_element,
                    output_parameter_handler,
                    'siteonefichier',
                    'siteonefichier',
                    'upToMyAccount',
                    '1fichier')

        gui.addFolder(gui_element, output_parameter_handler, False)

    def checkHoster(self, hoster_url, debrid=True):
        # securite
        if not hoster_url:
            return False

        # Petit nettoyage
        hoster_url = hoster_url.split('|')[0]
        hoster_url = hoster_url.split('?')[0]
        hoster_url = hoster_url.lower()

        # lien direct ?
        if any(
            hoster_url.endswith(x) for x in [
                '.mp4',
                '.avi',
                '.flv',
                '.m3u8',
                '.webm',
                '.mkv',
                '.mpd']):
            return self.getHoster('lien_direct')

        # Recuperation du host
        try:
            sHostName = hoster_url.split('/')[2]
        except BaseException:
            sHostName = hoster_url

        if debrid:
            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                return self.getHoster('alldebrid')

            # L'user a activé realbrid ?
            if self.ADDON.getSetting('hoster_realdebrid_premium') == 'true':
                return self.getHoster('realdebrid')

            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in hoster_url:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("lien_direct")

        supported_player = [
            'streamz',
            'streamax',
            'gounlimited',
            'xdrive',
            'facebook',
            'mixdrop',
            'mixloads',
            'vidoza',
            'rutube',
            'megawatch',
            'vidzi',
            'filetrip',
            'uptostream',
            'speedvid',
            'netu',
            'letsupload',
            'onevideo',
            'playreplay',
            'vimeo',
            'prostream',
            'vidfast',
            'uqload',
            'letwatch',
            'mail.ru',
            'filepup',
            'vimple',
            'wstream',
            'watchvideo',
            'vidwatch',
            'up2stream',
            'tune',
            'playtube',
            'vidup',
            'vidbull',
            'vidlox',
            'megaup',
            '33player'
            'easyload',
            'ninjastream',
            'cloudhost',
            'videobin',
            'stagevu',
            'gorillavid',
            'daclips',
            'hdvid',
            'vshare',
            'streamlare',
            'vidload',
            'giga',
            'vidbom',
            'upvid',
            'cloudvid',
            'megadrive',
            'downace',
            'clickopen',
            'supervideo',
            'jawcloud',
            'kvid',
            'soundcloud',
            'mixcloud',
            'ddlfr',
            'vupload',
            'dwfull',
            'vidzstore',
            'pdj',
            'rapidstream',
            'archive',
            'jetload',
            'dustreaming',
            'viki',
            'flix555',
            'onlystream',
            'upstream',
            'pstream',
            'vudeo',
            'dood',
            'vidia',
            'streamtape',
            'vidbem',
            'uptobox',
            'uplea',
            'sibnet',
            'vidplayer',
            'userload',
            'aparat',
            'evoload',
            'vidshar',
            'abcvideo',
            'plynow',
            'myvi',
            '33player',
            'videovard',
            'viewsb',
            'yourvid',
            'vf-manga',
            'oneupload']

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))

        # Gestion classique
        if ('vidbm' in sHostName) or ('vedbom' in sHostName):
            return self.getHoster('vidbm')

        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')

        if ('vk.com' in sHostName) or (
                'vkontakte' in sHostName) or ('vkcom' in sHostName):
            return self.getHoster('vk')

        if 'playvidto' in sHostName:
            return self.getHoster('vidto')

        if 'hd-stream' in sHostName:
            return self.getHoster('hd_stream')

        if 'vcstream' in sHostName:
            return self.getHoster('vidcloud')

        if 'livestream' in sHostName:
            return self.getHoster('lien_direct')

        # vidtodo et clone
        val = next(
            (x for x in [
                'vidtodo',
                'vixtodo',
                'viddoto',
                'vidstodo'] if x in sHostName),
            None)
        if val:
            return self.getHoster('vidtodo')

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in hoster_url:
                    return self.getHoster('lien_direct')
            except BaseException:
                pass
            else:
                return self.getHoster('dailymotion')
        if ('flashx' in sHostName) or ('filez' in sHostName):
            return self.getHoster('flashx')

        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp' in hoster_url) or ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('googlevideo' in sHostName) or ('picasaweb' in sHostName) or (
                'googleusercontent' in sHostName):
            return self.getHoster('googlevideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if 'iframe-secured' in sHostName:
            return self.getHoster('iframe_secured')

        if 'iframe-secure' in sHostName:
            return self.getHoster('iframe_secure')

        if ('thevideo' in sHostName) or (
                'video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('drive.google.com' in sHostName) or (
                'docs.google.com' in sHostName):
            return self.getHoster('googledrive')

        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        if 'voe' in sHostName:
            return self.getHoster('voe')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or (
                'streamcrypt' in sHostName) or ('opsktp' in hoster_url):
            return self.getHoster('allow_redirects')

        # frenchvid et clone
        val = next(
            (x for x in [
                'french-vid',
                'yggseries',
                'fembed',
                'fem.tohds',
                'feurl',
                'fsimg',
                'core1player',
                'vfsplayer',
                'gotochus',
                'sendvid',
                "femax"] if x in sHostName),
            None)
        if val:
            return self.getHoster("frenchvid")

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if '1fichier' in sHostName:
            return self.getHoster('1fichier')

        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if '/file/forbidden' in hoster_url:
                return False
            return self.getHoster('uploaded')

        if 'myfiles.alldebrid.com' in sHostName:
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        mod = __import__(
            'resources.hosters.' +
            sHosterFileName,
            fromlist=['cHoster'])
        klass = getattr(mod, 'cHoster')
        return klass()

    def play(self, input_parameter_handler=False, auto_play=False):
        gui = Gui()
        oDialog = dialog()

        if not input_parameter_handler:
            input_parameter_handler = InputParameterHandler()

        hoster_identifier = input_parameter_handler.getValue(
            'hoster_identifier')
        media_url = input_parameter_handler.getValue('media_url')
        bGetRedirectUrl = input_parameter_handler.getValue('bGetRedirectUrl')
        file_name = input_parameter_handler.getValue('file_name')
        title = input_parameter_handler.getValue('title')
        site_url = input_parameter_handler.getValue('site_url')
        cat = input_parameter_handler.getValue('cat')
        sMeta = input_parameter_handler.getValue('sMeta')

        if not title:
            title = file_name

        if bGetRedirectUrl == 'True':
            media_url = self.__getRedirectUrl(media_url)

        try:
            mediaDisplay = media_url.split('/')
            VSlog('Hoster %s - play : %s/ ... /%s' %
                  (hoster_identifier, '/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except BaseException:
            VSlog('Hoster %s - play : ' % (hoster_identifier, media_url))

        hoster = self.getHoster(hoster_identifier)
        hoster.setFileName(file_name)

        sHosterName = hoster.getDisplayName()
        if not auto_play:
            oDialog.VSinfo(sHosterName, 'Resolve')

        try:
            hoster.setUrl(media_url)
            aLink = hoster.getMediaLink(auto_play)

            if aLink and (
                    aLink[0] or aLink[1]):  # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0]:  # Voir exemple avec allDebrid qui : return False, URL
                    hoster = self.checkHoster(aLink[1], debrid=False)
                    if hoster:
                        hoster.setFileName(file_name)
                        sHosterName = hoster.getDisplayName()
                        if not auto_play:
                            oDialog.VSinfo(sHosterName, 'Resolve')
                        hoster.setUrl(aLink[1])
                        aLink = hoster.getMediaLink(auto_play)

                if aLink[0]:
                    gui_element = GuiElement()
                    gui_element.setSiteName(self.SITE_NAME)
                    gui_element.setSiteUrl(site_url)
                    gui_element.setMediaUrl(aLink[1])
                    gui_element.setFileName(file_name)
                    gui_element.setTitle(title)
                    gui_element.setCat(cat)
                    gui_element.setMeta(int(sMeta))
                    gui_element.getInfoLabel()

                    from resources.lib.player import Player
                    player = Player(input_parameter_handler)

                    # sous titres ?
                    if len(aLink) > 2:
                        player.AddSubtitles(aLink[2])

                    return player.run(gui_element, aLink[1])

            if not auto_play:
                oDialog.VSerror(self.ADDON.VSlang(30020))
            return False

        except Exception as e:
            oDialog.VSerror(self.ADDON.VSlang(30020))
            import traceback
            traceback.print_exc()
            return False

        if not auto_play:
            gui.setEndOfDirectory()
        return False

    def addToPlaylist(self):
        gui = Gui()
        input_parameter_handler = InputParameterHandler()
        hoster_identifier = input_parameter_handler.getValue(
            'hoster_identifier')
        media_url = input_parameter_handler.getValue('media_url')
        bGetRedirectUrl = input_parameter_handler.getValue('bGetRedirectUrl')
        file_name = input_parameter_handler.getValue('file_name')

        if bGetRedirectUrl == 'True':
            media_url = self.__getRedirectUrl(media_url)

        VSlog('Hoster - playlist ' + media_url)
        hoster = self.getHoster(hoster_identifier)
        hoster.setFileName(file_name)

        hoster.setUrl(media_url)
        aLink = hoster.getMediaLink()

        if aLink[0]:
            gui_element = GuiElement()
            gui_element.setSiteName(self.SITE_NAME)
            gui_element.setMediaUrl(aLink[1])
            gui_element.setTitle(hoster.getFileName())

            from resources.lib.player import Player
            player = Player()
            player.addItemToPlaylist(gui_element)
            dialog().VSinfo(str(hoster.getFileName()), 'Liste de lecture')
            return

        gui.setEndOfDirectory()

    def __getRedirectUrl(self, url):
        from resources.lib.handler.requestHandler import RequestHandler
        request = RequestHandler(url)
        request.request()
        return request.getRealUrl()
