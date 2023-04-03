# -*- coding: utf-8 -*-
import json
import xbmc
import xbmcaddon
import xbmcvfs
import sys
import re
from base64 import b64encode
from resources.lib.comaddon import dialog, Addon, addonManager, VSlog, isMatrix
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.util import UnquotePlus

# Utilisation de l'extension UpNext
# Documentation : https://github.com/im85288/service.upnext/wiki/Integration


class UpNext:
    # Prépare le lien du prochain épisode d'une série
    def nextEpisode(self, guiElement):

        # tester s'il s'agit d'une série
        if not guiElement.getItemValue('mediatype') == "episode":
            return

        # Demander d'installer l'extension
        if not self.use_up_next():
            return

        # La source
        input_parameter_handler = InputParameterHandler()
        site_name = input_parameter_handler.getValue('sourceName')
        if not site_name:
            return

        # La saison
        sSaison = input_parameter_handler.getValue('season')

        # l'ID tmdb
        tmdb_id = input_parameter_handler.getValue('tmdb_id')

        # Calcule l'épisode suivant à partir de l'épisode courant
        sEpisode = input_parameter_handler.getValue('sEpisode')
        if not sEpisode:
            sEpisode = str(guiElement.getEpisode())
            if not sEpisode:
                return  # impossible de déterminer l'épisode courant

        # tvShowTitle n'est pas toujours disponible.
        tvShowTitle = guiElement.getItemValue('tvshowtitle')
        if not tvShowTitle:
            tvShowTitle = re.search(
                '\\[\\/COLOR\\](.+?)\\[COLOR',
                guiElement.getItemValue('title')).group(1)

        movie_title = tvShowTitle

        numEpisode = int(sEpisode)
        nextEpisode = numEpisode + 1
        sNextEpisode = '%02d' % nextEpisode

        saison_url = input_parameter_handler.getValue('saison_url')
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', saison_url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('tvshowtitle', movie_title)
        output_parameter_handler.addParameter('tmdb_id', tmdb_id)
        sParams = output_parameter_handler.getParameterAsUri()

        hoster_identifier = input_parameter_handler.getValue(
            'hoster_identifier')
        nextSaisonFunc = input_parameter_handler.getValue('nextSaisonFunc')
        lang = input_parameter_handler.getValue('lang')

        try:
            # sauvegarde des parametres d'appel
            oldParams = sys.argv[2]

            hoster_identifier, media_url, nextTitle, desc, thumb = self.getMediaUrl(
                site_name, nextSaisonFunc, sParams, sSaison, nextEpisode, lang, hoster_identifier)

            # restauration des anciens params
            sys.argv[2] = oldParams

            # pas d'épisode suivant
            if not media_url:
                return

            file_name = tvShowTitle.replace(
                ' & ', ' and ')   # interdit dans un titre
            file_name += ' - '
            if sSaison:
                file_name += 'S%s' % sSaison
            file_name += 'E%s' % sNextEpisode
            nextTitle = UnquotePlus(nextTitle)

            if lang:
                nextTitle += ' (%s)' % lang

            episodeTitle = nextTitle

            saison_url = input_parameter_handler.getValue('saison_url')
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('hoster_identifier', hoster_identifier)
            output_parameter_handler.addParameter('sourceName', site_name)
            output_parameter_handler.addParameter('file_name', file_name)
            output_parameter_handler.addParameter('title', file_name)
            output_parameter_handler.addParameter('cat', 8)  # Catégorie épisode
            output_parameter_handler.addParameter('sMeta', 6)  # Meta épisode
            output_parameter_handler.addParameter('fav', 'play')
            output_parameter_handler.addParameter('media_url', str(media_url))
            output_parameter_handler.addParameter('saison_url', saison_url)
            output_parameter_handler.addParameter('nextSaisonFunc', nextSaisonFunc)
            output_parameter_handler.addParameter('season', sSaison)
            output_parameter_handler.addParameter('sEpisode', sNextEpisode)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('tvshowtitle', tvShowTitle)
            output_parameter_handler.addParameter('tmdb_id', tmdb_id)

            sParams = output_parameter_handler.getParameterAsUri()
            url = 'plugin://plugin.video.vstream/?site=HosterGui&function=play&%s' % sParams

            # thumbnail = guiElement.getThumbnail()
            thumbnail = thumb

            nextInfo = dict(
                current_episode=dict(
                    episodeid=numEpisode,
                    tvshowid=0,
                    showtitle=tvShowTitle,
                    season=sSaison if sSaison else '',
                    episode='%02d' % numEpisode,
                    title='',
                    plot='',
                    art={
                        'thumb': thumbnail,
                        'tvshow.clearart': '',
                        'tvshow.clearlogo': '',
                        'tvshow.fanart': '',
                        'tvshow.landscape': '',
                        'tvshow.poster': '',
                    },
                ),
                next_episode=dict(
                    episodeid=nextEpisode,
                    tvshowid=0,
                    showtitle=tvShowTitle,
                    season=sSaison if sSaison else '',  # déjà dans le titre
                    episode=sNextEpisode,  # déjà dans le titre
                    title=nextTitle,  # titre de l'épisode
                    plot=desc,
                    art={
                        'thumb': thumbnail,
                        'tvshow.clearart': '',
                        'tvshow.clearlogo': '',
                        'tvshow.fanart': thumbnail,  # guiElement.getFanart(),
                        'tvshow.landscape': thumbnail,  # guiElement.getPoster(),
                        'tvshow.poster': thumbnail,  # guiElement.getPoster(),
                    },
                ),
                play_url=url  # provide either `play_info` or `play_url`
            )

            self.notifyUpnext(nextInfo)
        except Exception as e:
            VSlog('UpNext : %s' % e)

    def getMediaUrl(
            self,
            site_name,
            function,
            sParams,
            sSaison,
            iEpisode,
            lang,
            hoster_identifier,
            title='',
            desc='',
            thumb=''):

        try:
            sys.argv[2] = '?%s' % sParams
            plugins = __import__(
                'resources.sites.%s' %
                site_name, fromlist=[site_name])
            function = getattr(plugins, function)
            function()
        except Exception as e:
            VSlog('could not load site: ' + site_name + ' error: ' + str(e))
            return None, None, None, None, None

        media_url = ''
        for url, listItem, isFolder in Gui().getEpisodeListing():
            sParams = url.split('?', 1)[1]
            aParams = dict(param.split('=') for param in sParams.split('&'))
            function = aParams['function']
            if function == 'DoNothing':
                continue

            if lang and 'lang' in aParams and UnquotePlus(
                    aParams['lang']) != lang:
                continue           # La langue est connue, mais ce n'est pas la bonne

            if sSaison and 'season' in aParams and aParams['season'] and int(
                    aParams['season']) != int(sSaison):
                continue           # La saison est connue, mais ce n'est pas la bonne

            if 'sEpisode' in aParams and aParams['sEpisode'] and int(
                    aParams['sEpisode']) != iEpisode:
                continue           # L'épisode est connu, mais ce n'est pas le bon

            media_url = aParams['media_url'] if 'media_url' in aParams else None
            infoTag = listItem.getVideoInfoTag()
            tagLine = infoTag.getTagLine()
            if tagLine:
                title = tagLine
            else:
                title = listItem.getLabel()

            if not desc:
                desc = infoTag.getPlot()

            if not title:
                title = UnquotePlus(
                    aParams['title']) if 'title' in aParams else None
            if 'host' in aParams and aParams['host']:
                hoster = HosterGui().checkHoster(aParams['host'])
                if not hoster:
                    continue
                hostName = hoster.getPluginIdentifier()
                if hostName != hoster_identifier:
                    continue

            hostName = hoster_identifier
            if 'hoster_identifier' in aParams:
                hostName = aParams['hoster_identifier']
                if hostName != hoster_identifier:
                    continue

            thumb = listItem.getArt('thumb')
            if 'thumb' in aParams and aParams['thumb']:
                thumb = UnquotePlus(aParams['thumb'])
            if not desc and 'desc' in aParams and aParams['desc']:
                desc = UnquotePlus(aParams['desc'])

            if media_url:
                return hostName, media_url, title, desc, thumb

            # if function != 'play':
            return self.getMediaUrl(
                site_name,
                function,
                sParams,
                sSaison,
                iEpisode,
                lang,
                hoster_identifier,
                title,
                desc,
                thumb)

        if media_url:    # si on n'a pas trouvé le bon host on en retourne un autre, il pourrait fonctionner
            return hostName, media_url, title, desc, thumb

        return None, None, None, None, None

    # Envoi des infos à l'addon UpNext
    def notifyUpnext(self, data):

        try:
            next_data = json.dumps(data)
            # if not isinstance(next_data, bytes):
            next_data = next_data.encode('utf-8')
            data = b64encode(next_data)
            if isMatrix():
                data = data.decode('ascii')

            jsonrpc_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "JSONRPC.NotifyAll",
                "params": {
                    "sender": "%s.SIGNAL" % 'plugin.video.vStream',
                    "message": 'upnext_data',
                    "data": [data],
                }
            }

            request = json.dumps(jsonrpc_request)
            response = xbmc.executeJSONRPC(request)
            response = json.loads(response)
            return response['result'] == 'OK'

        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    # Charge l'addon UpNext, ou l'installe à la demande
    def use_up_next(self):

        addons = Addon()
        if addons.getSetting('upnext') == 'false':
            return False

        upnext_id = 'service.upnext'
        try:
            # tente de charger UpNext pour tester sa présence
            xbmcaddon.Addon(upnext_id)
            return True
        except RuntimeError:    # Addon non installé ou désactivé
            if not dialog().VSyesno(addons.VSlang(30505)):  # Voulez-vous l'activer ?
                addons.setSetting('upnext', 'false')
                return False

            addon_xml = xbmc.translatePath(
                'special://home/addons/%s/addon.xml' %
                upnext_id)
            if xbmcvfs.exists(
                    addon_xml):  # si addon.xml existe, add-on présent mais désactivé

                # Impossible d'activer UpNext ou si on confirme de ne pas
                # vouloir l'utiliser
                if not addonManager().enableAddon(upnext_id):
                    addons.setSetting('upnext', 'false')
                    return False

                return True  # addon activé
            else:                          # UpNext non installé, on l'installe et on l'utilise
                addonManager().installAddon(upnext_id)
                # ce n'est pas pris en compte à l'installation de l'addon, donc
                # return False, il faudra attendre le prochain épisode
                return False
