# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import xbmc
import traceback

# from resources.lib.statistic import cStatistic
from resources.lib.home import cHome
from resources.lib.gui.gui import Gui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window, siteManager
from resources.lib.search import cSearch
# http://kodi.wiki/view/InfoLabels
# http://kodi.wiki/view/List_of_boolean_conditions


####################
#
#  Permet de debuguer avec Eclipse
#
# Tuto ici :
# https://github.com/Kodi-vStream/venom-xbmc-addons/wiki
#
####################

# Mettre True pour activer le debug
DEBUG = False

if DEBUG:

    import sys  # pydevd module need to be copied in Kodi\system\python\Lib\pysrc
    sys.path.append('H:\\Program Files\\Kodi\\system\\Python\\Lib\\pysrc')

    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        try:
            import pydevd  # with the addon script.module.pydevd, only use `import pydevd`
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class Main:

    def __init__(self):
        self.site_name = 'cHome'
        self.function_name = 'load'

        self.plugin_handler = cPluginHandler()
        self.parse_url()

    def parse_url(self):
        # Exclue les appels par des plugins qu'on ne sait pas gérer, par exemple :
        # plugin://plugin.video.vstream/extrafanart
        plugin_path = self.plugin_handler.getPluginPath()
        if plugin_path == 'plugin://plugin.video.vstream/extrafanart/':
            return

        input_parameter_handler = InputParameterHandler()

        # Get SiteName
        if input_parameter_handler.exist('site'):
            self.site_name = input_parameter_handler.getValue('site')
        else:
            self.site_name = 'cHome'
            self.function_name = 'load'

        # Get function name
        if input_parameter_handler.exist('function'):
            self.function_name = input_parameter_handler.getValue('function')
        else:
            VSlog('call load methode')
            self.function_name = "load"

        if self.function_name == 'setSetting':
            set_setting(input_parameter_handler)
            return
        elif self.function_name == 'setSettings':
            set_settings(input_parameter_handler)
            return
        elif self.function_name == 'DoNothing':
            return
        self.parse_url_for_site()

    def parse_url_for_site(self):
        VSlog('load site ' + self.site_name + ' and call function ' + self.function_name)
        list_action = {
            'cHosterGui': 'resources.lib.gui.hoster',
            'Gui': 'resources.lib.gui.gui',
            'Fav': 'resources.lib.bookmark',
            'cViewing': 'resources.lib.viewing',
            'cLibrary': 'resources.lib.library',
            'cDownload': 'resources.lib.download',
            'cHome': 'resources.lib.home',
            'cTrakt': 'resources.lib.trakt'
        }
        for action in list_action:
            if self.try_to_call_method(action, list_action[action]):
                return

            if self.site_name == 'globalSearch':
                search_global()
            elif self.site_name == 'globalRun':
                __import__('resources.lib.runscript', fromlist=['runscript'])
                # function = getattr(plugins, sFunction)
                # function()
                return
            elif self.site_name == 'globalSources':
                gui = Gui()
                list_plugins = self.plugin_handler.getAvailablePlugins(force=(self.function_name == 'globalSources'))

                sites_manager = siteManager()

                if len(list_plugins) == 0:
                    addons = addon()
                    addons.openSettings()
                    gui.updateDirectory()
                else:
                    for plugin in list_plugins:
                        site_name = plugin[0]
                        if not sites_manager.isActive(plugin[1]):
                            site_name = '[COLOR red][OFF] ' + site_name + '[/COLOR]'

                        output_parameter_handler = OutputParameterHandler()
                        output_parameter_handler.addParameter('siteUrl', 'http://venom')
                        icon = 'sites/%s.png' % (plugin[1])
                        gui.addDir(plugin[1], 'load', site_name, icon, output_parameter_handler)

                gui.setEndOfDirectory()
                return
            elif self.site_name == 'globalParametre':
                addons = addon()
                addons.openSettings()
                return
            else:
                try:
                    plugins = __import__('resources.sites.%s' % self.site_name, fromlist=[self.site_name])
                    function = getattr(plugins, self.function_name)
                    function()
                except Exception as e:
                    progress().VSclose()  # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                    VSlog('could not load site: ' + self.site_name + ' error: ' + str(e))
                    traceback.print_exc()
                return

    def try_to_call_method(self, action_site_name, path):
        if self.site_name == action_site_name:
            imported_plugin = __import__(path, fromlist=[self.site_name])
            plugin_object = getattr(imported_plugin, self.site_name)()
            function = getattr(plugin_object, self.function_name)
            function()
            return True
        return False


def set_setting(input_parameter_handler):
    if not (input_parameter_handler.exist('id') or input_parameter_handler.exist('value')):
        return

    plugin_id = input_parameter_handler.getValue('id')
    value = input_parameter_handler.getValue('value')
    addons = addon()
    setting = addons.getSetting(plugin_id)

    # modifier si différent
    if setting != value:
        addons.setSetting(plugin_id, value)
        return True

    return False


# Permet la modification des settings depuis un raccourci dans le skin (jusqu'à 100 paramètres).
# Supporte les retours à la ligne seulement derrière le paramètre, exemple :
# RunAddon(plugin.video.vstream,function=setSettings&id1=plugin_cinemay_com&value1=true
# &id2=plugin_cinemegatoil_org&value2=false
# &id3=hoster_uploaded_premium&value3=true
# &id4=hoster_uploaded_username&value4=MyName
# &id5=hoster_uploaded_password&value5=MyPass)
def set_settings(input_parameter_handler):
    addons = addon()

    for i in range(1, 100):
        plugin_id = input_parameter_handler.getValue('id' + str(i))
        if plugin_id:
            value = input_parameter_handler.getValue('value' + str(i))
            value = value.replace('\n', '')
            old_setting = addons.getSetting(plugin_id)
            # modifier si différent
            if old_setting != value:
                addons.setSetting(plugin_id, value)

    return True


def search_global():
    search = cSearch()
    exec("search.searchGlobal()")
    return True


def _plugin_search(plugin, search_text):

    # Appeler la source en mode Recherche globale
    window(10101).setProperty('search', 'true')

    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        url = plugin['search'][0] + str(search_text)
        function(url)

        VSlog('Load Search: ' + str(plugin['identifier']))
    except BaseException:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')


Main()
