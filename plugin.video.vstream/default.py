# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import xbmc

# from resources.lib.statistic import cStatistic
from resources.lib.home import Home
from resources.lib.gui.gui import Gui
from resources.lib.handler.pluginHandler import PluginHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import Progress, VSlog, Addon, SiteManager
from resources.lib.search import Search
import traceback
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
            pydevd.settrace(
                'localhost',
                stdoutToServer=True,
                stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:

    def __init__(self):
        self.parseUrl()

    def parseUrl(self):
        # Exclue les appels par des plugins qu'on ne sait pas gérer, par
        # exemple :  plugin://plugin.video.vstream/extrafanart
        plugin_handler = PluginHandler()
        if plugin_handler.getPluginPath() == 'plugin://plugin.video.vstream/extrafanart/':
            return

        input_parameter_handler = InputParameterHandler()

        if input_parameter_handler.exist('function'):
            function = input_parameter_handler.getValue('function')
        else:
            VSlog('call load methode')
            function = "load"

        if function == 'setSetting':
            if input_parameter_handler.exist('id'):
                plugin_id = input_parameter_handler.getValue('id')
            else:
                return

            if input_parameter_handler.exist('value'):
                value = input_parameter_handler.getValue('value')
            else:
                return

            setSetting(plugin_id, value)
            return

        if function == 'setSettings':
            setSettings(input_parameter_handler)
            return

        if function == 'DoNothing':
            return

        if not input_parameter_handler.exist('site'):
            # charge home
            plugins = __import__('resources.lib.home', fromlist=['home']).Home()
            function = getattr(plugins, 'load')
            function()
            return

        if input_parameter_handler.exist('site'):
            site_name = input_parameter_handler.getValue('site')
            VSlog('load site ' + site_name + ' and call function ' + function)

            if isHosterGui(site_name, function):
                return

            if isGui(site_name, function):
                return

            if isFav(site_name, function):
                return

            if isViewing(site_name, function):
                return

            if isLibrary(site_name, function):
                return

            if isDl(site_name, function):
                return

            if isHome(site_name, function):
                return

            if isSearch(site_name, function):
                return

            if isTrakt(site_name, function):
                return

            if site_name == 'globalRun':
                __import__('resources.lib.runscript', fromlist=['runscript'])
                # function = getattr(plugins, function)
                # function()
                return

            if site_name == 'globalSources':
                gui = Gui()
                list_plugins = plugin_handler.getAvailablePlugins(force=(function == 'globalSources'))

                sites_manager = SiteManager()

                if len(list_plugins) == 0:
                    addons = Addon()
                    addons.openSettings()
                    gui.updateDirectory()
                else:
                    for plugin in list_plugins:

                        sitename = plugin[0]
                        if not sites_manager.isActive(plugin[1]):
                            sitename = '[COLOR red][OFF] ' + sitename + '[/COLOR]'

                        output_parameter_handler = OutputParameterHandler()
                        output_parameter_handler.addParameter('site_url', 'http://venom')
                        icon = 'sites/%s.png' % (plugin[1])
                        gui.addDir(plugin[1], 'load', sitename, icon, output_parameter_handler)

                gui.setEndOfDirectory()
                return

            if site_name == 'globalParametre':
                Addon().openSettings()
                return
            # if isAboutGui(site_name, function) == True:
                # return

            # charge sites
            try:
                plugins = __import__('resources.sites.%s' % site_name, fromlist=[site_name])
                function = getattr(plugins, function)
                function()
            except Exception as e:
                Progress().VSclose()  # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                VSlog('could not load site: ' + site_name +' error: ' + str(e))
                traceback.print_exc()
                return


def setSetting(plugin_id, value):
    addons = Addon()
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
def setSettings(input_parameter_handler):
    addons = Addon()

    for i in range(1, 100):
        plugin_id = input_parameter_handler.getValue('id' + str(i))
        if plugin_id:
            value = input_parameter_handler.getValue('value' + str(i)).replace('\n', '')
            # modifier si différent
            if addons.getSetting(plugin_id) != value:
                addons.setSetting(plugin_id, value)

    return True


def isHosterGui(site_name, function):
    if site_name == 'HosterGui':
        plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isGui(site_name, function):
    if site_name == 'Gui':
        gui = Gui()
        exec("gui." + function + "()")
        return True
    return False


def isFav(site_name, function):
    if site_name == 'cFav':
        plugins = __import__('resources.lib.bookmark', fromlist=['cFav']).cFav()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isViewing(site_name, function):
    if site_name == 'cViewing':
        plugins = __import__('resources.lib.viewing', fromlist=['cViewing']).cViewing()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isLibrary(site_name, function):
    if site_name == 'Library':
        plugins = __import__('resources.lib.library', fromlist=['Library']).Library()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isDl(site_name, function):
    if site_name == 'cDownload':
        plugins = __import__('resources.lib.download', fromlist=['cDownload']).cDownload()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isHome(site_name, function):
    if site_name == 'Home':
        home = Home()
        exec("home." + function + "()")
        return True
    return False


def isSearch(site_name, function):
    if site_name == 'Search' or site_name == 'globalSearch':
        search = Search()
        if site_name == 'globalSearch':
            exec("search.searchGlobal()")
        else:
            exec("search." + function + "()")
        return True
    return False


def isTrakt(site_name, function):
    if site_name == 'cTrakt':
        plugins = __import__(
            'resources.lib.trakt',
            fromlist=['cTrakt']).cTrakt()
        function = getattr(plugins, function)
        function()
        return True
    return False


main()
