# -*- coding: utf-8 -*-
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Addon, xbmcgui, dialog, VSPath
import xbmcvfs
import datetime
import time

SITE_IDENTIFIER = 'Enregistrement'
SITE_NAME = 'enregistrement'


class Enregistremement:

    def programmation_enregistrement(self, url):
        gui = Gui()
        ADDON = Addon()
        if '.m3u8' in url:
            header = '-fflags +genpts+igndts -y -i "' + url + '"'
        else:
            header = '-re -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 4294 ' \
                     '-timeout 2000000000 -f mpegts -re -flags +global_header -fflags +genpts+igndts -y -i "' + url + \
                '" -headers "User-Agent: Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)' \
                '+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36" -sn -c:v libx264 -c:a ' \
                'copy -map 0 -segment_format mpegts -segment_time -1'

        pathEnregistrement = ADDON.getSetting(
            'path_enregistrement_programmation')
        currentPath = ADDON.getSetting(
            'path_enregistrement').replace('\\', '/')
        ffmpeg = ADDON.getSetting('path_ffmpeg').replace('\\', '/')

        heureFichier = gui.showKeyBoard(
            heading="Début d'enregistrement au format Jour-Heure-Minute, vide pour maintenant")
        heureFin = gui.showKeyBoard(
            heading="Heure de fin d'enregistrement au format Heure-Minute")
        if not heureFin:   # pas de fin, on annule
            return
        titre = gui.showKeyBoard(
            heading="Titre de l'enregistrement").replace(
            "'", "\\'")
        if not titre:
            return

        # début non précisé -> enregistrement maintenant
        if not heureFichier:
            d = datetime.now()
            heureFichier = d.strftime('%d-%H-%M')

        heureDebut = GetTimeObject(heureFichier, '%d-%H-%M')
        heureFin = GetTimeObject(heureFin, '%H-%M')
        duree = heureFin - heureDebut

        marge = ADDON.getSetting('marge_auto')
        timedelta = datetime.timedelta(minutes=int(marge))
        duree += timedelta

        realPath = VSPath(
            pathEnregistrement +
            '/' +
            str(heureFichier) +
            '.py').replace(
            '\\',
            '\\\\')

        f = xbmcvfs.File(realPath, 'w')
        read = f.write('''#-*- coding: utf-8 -*-
import os,subprocess
command = '"''' + ffmpeg + '''" ''' + header + ''' -t ''' + str(duree) + ''' "''' + currentPath + '/' + titre + '''.mkv"'
proc = subprocess.Popen(command, stdout=subprocess.PIPE)
p_status = proc.wait()
f = open("''' + currentPath + '''/test.txt",'w')
f.write('Fini avec code erreur ' + str(p_status))
f.close()''')
        f.close()
        oDialog = dialog().VSinfo(
            'Redémarrer Kodi pour prendre en compte la planification', 'Vstream', 10)
        gui.setEndOfDirectory()


def GetTimeObject(duree, formats):
    try:
        res = datetime.datetime.strptime(duree, formats).time()
    except TypeError:
        res = datetime.datetime(*time.strptime(duree, formats)[0:6]).time()
    tmp_datetime = datetime.datetime.combine(datetime.date.today(), res)
    return tmp_datetime
