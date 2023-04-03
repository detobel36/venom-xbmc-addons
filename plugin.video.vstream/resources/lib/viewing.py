# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.comaddon import dialog, Addon, xbmc, isMatrix
from resources.lib.db import Db
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cViewing'
SITE_NAME = 'Viewing'


class cViewing:
    DIALOG = dialog()
    ADDON = Addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delViewing(self):
        input_parameter_handler = InputParameterHandler()
        title_watched = input_parameter_handler.getValue('title_watched')
        cat = input_parameter_handler.getValue('cat')

        if not title_watched:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False

        meta = {'titleWatched': title_watched}
        if cat:
            meta['cat'] = cat

        with Db() as db:
            if db.del_viewing(meta):
                self.DIALOG.VSinfo(Addon().VSlang(30072))
                Gui().updateDirectory()
            return True

    # Suppression d'un bookmark depuis un Widget
    def delViewingMenu(self):
        title = xbmc.getInfoLabel('ListItem.OriginalTitle')
        if not title:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False
        cat = xbmc.getInfoLabel('ListItem.Property(cat)')
        meta = {}
        meta['titleWatched'] = title
        meta['cat'] = cat
        with Db() as db:
            if db.del_viewing(meta):
                self.DIALOG.VSinfo(Addon().VSlang(30072))
                Gui().updateDirectory()

            return True

    def showMenu(self):
        gui = Gui()
        addons = Addon()

        output_parameter_handler = OutputParameterHandler()
        gui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30126), 'genres.png', output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '1')  # films
        gui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30120), 'films.png', output_parameter_handler)

        output_parameter_handler.addParameter('cat', '4')  # saisons
        gui.addDir(SITE_IDENTIFIER, 'getViewing', '%s/%s' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122)),
                   'series.png', output_parameter_handler)

        output_parameter_handler.addParameter('cat', '5')  # Divers
        gui.addDir(SITE_IDENTIFIER, 'getViewing', self.ADDON.VSlang(30410), 'buzz.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def getViewing(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        cat_filter = input_parameter_handler.getValue('cat')

        with Db() as DB:
            row = DB.get_viewing()
            if not row:
                gui.setEndOfDirectory()
                return

            for data in row:

                try:
                    title = data['title'].encode('utf-8')
                except BaseException:
                    title = data['title']

                try:
                    try:
                        siteurl = data['siteurl'].encode('utf-8')
                    except BaseException:
                        siteurl = data['siteurl']

                    if isMatrix():
                        siteurl = UnquotePlus(siteurl.decode('utf-8'))
                        title = str(title, 'utf-8')
                    else:
                        siteurl = UnquotePlus(siteurl)

                    title_watched = data['title_id']
                    site = data['site']
                    function = data['fav']
                    cat = data['cat']
                    season = data['season']
                    tmdb_id = data['tmdb_id'] if data['tmdb_id'] != '0' else None

                    if cat_filter is not False and cat != cat_filter:
                        continue

                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', siteurl)
                    output_parameter_handler.addParameter('movie_title', title)
                    output_parameter_handler.addParameter('tmdb_id', tmdb_id)
                    output_parameter_handler.addParameter('title_watched', title_watched)
                    output_parameter_handler.addParameter('season', season)
                    output_parameter_handler.addParameter('cat', cat)
                    output_parameter_handler.addParameter('isViewing', True)

                    # pourcentage de lecture
                    meta = {'title': title_watched}
                    resume_time, total_time = DB.get_resume(meta)
                    output_parameter_handler.addParameter('ResumeTime', resume_time)
                    output_parameter_handler.addParameter('TotalTime', total_time)

                    if cat == '1':
                        list_item = gui.addMovie(site, function, title, 'films.png', '', title,
                                                 output_parameter_handler)
                    elif cat == '4':
                        list_item = gui.addSeason(site, function, title, 'series.png', '', title,
                                                  output_parameter_handler)
                    elif cat == '5':
                        list_item = gui.addMisc(site, function, title, 'buzz.png', '', title,
                                                output_parameter_handler)
                    else:
                        list_item = gui.addTV(site, function, title, 'series.png', '', title, output_parameter_handler)

                    output_parameter_handler.addParameter('title_watched', title_watched)
                    output_parameter_handler.addParameter('cat', cat)
                    list_item.addMenu(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30412), output_parameter_handler)

                except Exception as e:
                    pass

        # Vider toute la catégorie n'est pas accessible lors de l'utilisation
        # en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('cat', cat_filter)
            gui.addDir(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30211), 'trash.png', output_parameter_handler)

        gui.setEndOfDirectory()
