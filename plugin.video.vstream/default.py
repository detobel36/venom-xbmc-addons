# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import xbmc

# from resources.lib.statistic import cStatistic
from resources.lib.home import Home
from resources.lib.gui.gui import Gui
from resources.lib.handler.pluginHandler import PluginHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import Progress, VSlog, addon, SiteManager
from resources.lib.search import Search
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
            sys.stderr.write(
                "Error: " +
                "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:

    def __init__(self):
        self.parseUrl()

    def parseUrl(self):
        # Exclue les appels par des plugins qu'on ne sait pas gérer, par
        # exemple :  plugin://plugin.video.vstream/extrafanart
        oPluginHandler = PluginHandler()
        pluginPath = oPluginHandler.getPluginPath()
        if pluginPath == 'plugin://plugin.video.vstream/extrafanart/':
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
            plugins = __import__(
                'resources.lib.home',
                fromlist=['home']).Home()
            function = getattr(plugins, 'load')
            function()
            return

        if input_parameter_handler.exist('site'):
            sSiteName = input_parameter_handler.getValue('site')
            VSlog('load site ' + sSiteName + ' and call function ' + function)

            if isHosterGui(sSiteName, function):
                return

            if isGui(sSiteName, function):
                return

            if isFav(sSiteName, function):
                return

            if isViewing(sSiteName, function):
                return

            if isLibrary(sSiteName, function):
                return

            if isDl(sSiteName, function):
                return

            if isHome(sSiteName, function):
                return

            if isSearch(sSiteName, function):
                return

            if isTrakt(sSiteName, function):
                return

            if sSiteName == 'globalRun':
                __import__('resources.lib.runscript', fromlist=['runscript'])
                # function = getattr(plugins, function)
                # function()
                return

            if sSiteName == 'globalSources':
                gui = Gui()
                aPlugins = oPluginHandler.getAvailablePlugins(
                    force=(function == 'globalSources'))

                sitesManager = SiteManager()

                if len(aPlugins) == 0:
                    addons = addon()
                    addons.openSettings()
                    gui.updateDirectory()
                else:
                    for aPlugin in aPlugins:

                        sitename = aPlugin[0]
                        if not sitesManager.isActive(aPlugin[1]):
                            sitename = '[COLOR red][OFF] ' + \
                                sitename + '[/COLOR]'

                        output_parameter_handler = OutputParameterHandler()
                        output_parameter_handler.addParameter(
                            'siteUrl', 'http://venom')
                        icon = 'sites/%s.png' % (aPlugin[1])
                        gui.addDir(
                            aPlugin[1],
                            'load',
                            sitename,
                            icon,
                            output_parameter_handler)

                gui.setEndOfDirectory()
                return

            if sSiteName == 'globalParametre':
                addons = addon()
                addons.openSettings()
                return
            # if isAboutGui(sSiteName, function) == True:
                # return

            # charge sites
            try:
                plugins = __import__(
                    'resources.sites.%s' %
                    sSiteName, fromlist=[sSiteName])
                function = getattr(plugins, function)
                function()
            except Exception as e:
                Progress().VSclose()  # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                VSlog(
                    'could not load site: ' +
                    sSiteName +
                    ' error: ' +
                    str(e))
                import traceback
                traceback.print_exc()
                return


def setSetting(plugin_id, value):
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
def setSettings(input_parameter_handler):
    addons = addon()

    for i in range(1, 100):
        plugin_id = input_parameter_handler.getValue('id' + str(i))
        if plugin_id:
            value = input_parameter_handler.getValue('value' + str(i))
            value = value.replace('\n', '')
            oldSetting = addons.getSetting(plugin_id)
            # modifier si différent
            if oldSetting != value:
                addons.setSetting(plugin_id, value)

    return True


def isHosterGui(sSiteName, function):
    if sSiteName == 'HosterGui':
        plugins = __import__(
            'resources.lib.gui.hoster',
            fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isGui(sSiteName, function):
    if sSiteName == 'Gui':
        gui = Gui()
        exec("gui." + function + "()")
        return True
    return False


def isFav(sSiteName, function):
    if sSiteName == 'cFav':
        plugins = __import__(
            'resources.lib.bookmark',
            fromlist=['cFav']).cFav()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isViewing(sSiteName, function):
    if sSiteName == 'cViewing':
        plugins = __import__(
            'resources.lib.viewing',
            fromlist=['cViewing']).cViewing()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isLibrary(sSiteName, function):
    if sSiteName == 'Library':
        plugins = __import__(
            'resources.lib.library',
            fromlist=['Library']).Library()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isDl(sSiteName, function):
    if sSiteName == 'cDownload':
        plugins = __import__(
            'resources.lib.download',
            fromlist=['cDownload']).cDownload()
        function = getattr(plugins, function)
        function()
        return True
    return False


def isHome(sSiteName, function):
    if sSiteName == 'Home':
        oHome = Home()
        exec("oHome." + function + "()")
        return True
    return False


def isSearch(sSiteName, function):
    if sSiteName == 'Search' or sSiteName == 'globalSearch':
        oSearch = Search()
        if sSiteName == 'globalSearch':
            exec("oSearch.searchGlobal()")
        else:
            exec("oSearch." + function + "()")
        return True
    return False


def isTrakt(sSiteName, function):
    if sSiteName == 'cTrakt':
        plugins = __import__(
            'resources.lib.trakt',
            fromlist=['cTrakt']).cTrakt()
        function = getattr(plugins, function)
        function()
        return True
    return False


main()
