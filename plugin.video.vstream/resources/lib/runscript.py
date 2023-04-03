# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# vstream = xbmcaddon.Addon('plugin.video.vstream')
# sLibrary = VSPath(vstream.getAddonInfo("path")).decode("utf-8")
# sys.path.append (sLibrary)
import json
import xbmcvfs
import xbmc
import xbmcgui
import sys

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.comaddon import Addon, dialog, VSlog, window, VSPath, SiteManager
# from resources.lib.util import urlEncode

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine')
except BaseException:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine')


SITE_IDENTIFIER = 'runscript'
SITE_NAME = 'runscript'


class cClear:

    DIALOG = dialog()
    ADDON = Addon()

    def __init__(self):
        self.main(sys.argv[1])

    def main(self, env):
        if env == 'urlresolver':
            Addon('script.module.urlresolver').openSettings()
            return

        elif env == 'metahandler':
            Addon('script.module.metahandler').openSettings()
            return

        elif env == 'changelog_old':
            url = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/' + \
                  'changelog.txt'
            try:
                request = urllib2.Request(url)
                reponse = urllib2.urlopen(request)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    content = reponse.read().decode('utf-8')
                else:
                    content = reponse.read()

                self.TextBoxes('vStream Changelog', content)
            except BaseException:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), url))
            return

        elif env == 'changelog':

            class XMLDialog(xbmcgui.WindowXMLDialog):

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel('ChangeLog')
                    self.button.setLabel('OK')

                    url = 'https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/commits'
                    request = urllib2.Request(url)
                    reponse = urllib2.urlopen(request)

                    # En python 3 on doit décoder la reponse
                    if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                        content = reponse.read().decode('utf-8')
                    else:
                        content = reponse.read()

                    result = json.loads(content)
                    listitems = []

                    for item in result:
                        # autor
                        icon = item['author']['avatar_url']
                        login = item['author']['login']
                        # message
                        try:
                            desc = item['commit']['message'].encode("utf-8")
                        except BaseException:
                            desc = 'None'

                        listitem = xbmcgui.ListItem(label=login, label2=desc)
                        listitem.setArt({'icon': icon, 'thumb': icon})
                        listitems.append(listitem)

                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    self.close()
                    return

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif env == 'soutient':
            url = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/' + \
                  'soutient.txt'
            try:
                request = urllib2.Request(url)
                reponse = urllib2.urlopen(request)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    content = reponse.read().decode('utf-8')
                else:
                    content = reponse.read()

                self.TextBoxes('vStream Soutient', content)
            except BaseException:
                self.DIALOG.VSerror(
                    "%s, %s" %
                    (self.ADDON.VSlang(30205), url))
            return

        elif env == 'addon':  # Vider le cache des métadonnées
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                cached_cache = "special://home/userdata/addon_data/plugin.video.vstream/video_cache.db"
                # important seul xbmcvfs peux lire le special
                try:
                    cached_cache = VSPath(cached_cache).decode("utf-8")
                except AttributeError:
                    cached_cache = VSPath(cached_cache)

                try:
                    db = sqlite.connect(cached_cache)
                    dbcur = db.cursor()
                    dbcur.execute('DELETE FROM movie')
                    dbcur.execute('DELETE FROM tvshow')
                    dbcur.execute('DELETE FROM season')
                    dbcur.execute('DELETE FROM episode')
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30090))
                except BaseException:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
            return

        elif env == 'clean':
            liste = [
                'Historiques des recherches',
                'Marque-Pages',
                'En cours de lecture',
                'Niveau de lecture',
                'Marqués vues',
                'Téléchargements']
            ret = self.DIALOG.VSselect(liste, self.ADDON.VSlang(30110))
            cached_db = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            # important seul xbmcvfs peux lire le special
            try:
                cached_db = VSPath(cached_db).decode("utf-8")
            except AttributeError:
                cached_db = VSPath(cached_db)

            sql_drop = ""

            if ret > -1:

                if ret == 0:
                    sql_drop = 'DELETE FROM history'
                elif ret == 1:
                    sql_drop = 'DELETE FROM favorite'
                elif ret == 2:
                    sql_drop = 'DELETE FROM viewing'
                elif ret == 3:
                    sql_drop = 'DELETE FROM resume'
                elif ret == 4:
                    sql_drop = 'DELETE FROM watched'
                elif ret == 5:
                    sql_drop = 'DELETE FROM download'

                try:
                    db = sqlite.connect(cached_db)
                    dbcur = db.cursor()
                    dbcur.execute(sql_drop)
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSok(self.ADDON.VSlang(30090))
                except Exception as err:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
                    VSlog("Exception runscript sql_drop: {0}".format(err))
            return

        elif env == 'xbmc':
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30092))
                except BaseException:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30093))
            return

        elif env == 'fi':
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/archive_cache/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30095))
                except BaseException:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30096))
            return

        # activer toutes les sources
        elif env == 'enableSources':
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                sites_manager = SiteManager()
                sites_manager.enableAll()
                sites_manager.save()
                self.DIALOG.VSinfo(self.ADDON.VSlang(30014))

            return

        # désactiver toutes les sources
        elif env == 'disableSources':
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                sites_manager = SiteManager()
                sites_manager.disableAll()
                sites_manager.save()
                self.DIALOG.VSinfo(self.ADDON.VSlang(30014))

            return

        # aciver/désactiver les sources
        elif env == 'search':
            from resources.lib.handler.pluginHandler import PluginHandler
            valid = '[COLOR green][x][/COLOR]'

            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = Addon()
                sites_manager = SiteManager()

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(self.ADDON.VSlang(30094))
                    self.button.setLabel('OK')
                    listitems = []
                    plugin_handler = PluginHandler()
                    list_plugins = plugin_handler.getAllPlugins()

                    # self.data = json.load(open(self.path))

                    for plugin in list_plugins:
                        # teste si deja dans le dsip
                        sPluginName = plugin[1]
                        isActive = self.sites_manager.isActive(sPluginName)
                        icon = "special://home/addons/plugin.video.vstream/resources/art/sites/%s.png" % sPluginName
                        stitle = self.sites_manager.getProperty(
                            sPluginName, self.sites_manager.LABEL)

                        if isActive:
                            stitle = '%s %s' % (stitle, valid)
                        listitem = xbmcgui.ListItem(
                            label=stitle, label2=plugin[2])
                        listitem.setArt({'icon': icon, 'thumb': icon})
                        listitem.setProperty('Addon.Summary', plugin[2])
                        listitem.setProperty('sitename', plugin[1])
                        if isActive:
                            listitem.select(True)

                        listitems.append(listitem)
                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    if controlId == 5:       # OK
                        self.sites_manager.save()
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 7:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 6:
                        item = self.container.getSelectedItem()
                        if item.isSelected():
                            label = item.getLabel().replace(valid, '')
                            item.setLabel(label)
                            item.select(False)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sites_manager.setActive(
                                sPluginSettingsName, False)
                        else:
                            label = '%s %s' % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sites_manager.setActive(
                                sPluginSettingsName, True)
                        return

                def onFocus(self, controlId):
                    self.controlId = controlId

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif env == 'thumb':

            if self.DIALOG.VSyesno(self.ADDON.VSlang(30098)):

                text = False
                path = "special://userdata/Thumbnails/"
                path_db = "special://userdata/Database"
                try:
                    xbmcvfs.rmdir(path, True)
                    text = 'Clear Thumbnail Folder, Successful[CR]'
                except BaseException:
                    text = 'Clear Thumbnail Folder, Error[CR]'

                folder, items = xbmcvfs.listdir(path_db)
                items.sort()
                for sItemName in items:
                    if "extures" in sItemName:
                        cached_cache = "/".join([path_db, sItemName])
                        try:
                            xbmcvfs.delete(cached_cache)
                            text += 'Clear Thumbnail DB, Successful[CR]'
                        except BaseException:
                            text += 'Clear Thumbnail DB, Error[CR]'

                if text:
                    text = "%s (Important relancer Kodi)" % text
                    self.DIALOG.VSok(text)
            return

        elif env == 'sauv':
            select = self.DIALOG.VSselect(['Import', 'Export'])
            db = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            if select >= 0:
                try:
                    if select == 0:
                        # sélection d'un fichier
                        new = self.DIALOG.VSbrowse(1, 'vStream', "files")
                        if new:
                            xbmcvfs.delete(db)
                            xbmcvfs.copy(new, db)
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                    elif select == 1:
                        # sélection d'un répertoire
                        new = self.DIALOG.VSbrowse(3, 'vStream', "files")
                        if new:
                            xbmcvfs.copy(db, new + 'vstream.db')
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                except BaseException:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30100))
                return
        else:
            return

        return

    # def ClearDir(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     for the_file in os.listdir(dir):
    #         file_path = os.path.join(dir, the_file).encode('utf-8')
    #         if clearNested and os.path.isdir(file_path):
    #             self.ClearDir(file_path, clearNested)
    #             try:
    #                 os.rmdir(file_path)
    #             except Exception as e:
    #                 print(str(e))
    #         else:
    #             try:
    #                 os.unlink(file_path)
    #             except Exception as e:
    #                 print str(e)

    # def ClearDir2(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     try:
    #         os.unlink(dir)
    #     except Exception as e:
    #         print(str(e))

    def TextBoxes(self, heading, anounce):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % 10147)
        # get window
        win = window(10147)
        # win.show()
        # give window time to initialize
        xbmc.sleep(100)
        # set heading
        win.getControl(1).setLabel(heading)
        win.getControl(5).setText(anounce)
        return


cClear()
