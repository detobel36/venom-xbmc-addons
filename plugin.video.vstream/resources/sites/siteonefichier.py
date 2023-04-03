# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc
import xbmcgui

from resources.lib.comaddon import Progress, Addon, SiteManager
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'siteonefichier'
SITE_NAME = '[COLOR %s]%s[/COLOR]' % ('dodgerblue', 'Compte1fichier')

SITE_DESC = 'Fichiers sur compte 1Fichier'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_FILE = URL_MAIN + 'console/files.pl'
URL_REMOTE = URL_MAIN + 'console/remote.pl'
URL_VERIF = URL_MAIN + 'check_links.pl?links[]='


def load():
    addons = Addon()

    if (addons.getSetting('hoster_onefichier_username') == '') and (
            addons.getSetting('hoster_onefichier_password') == ''):
        gui = Gui()
        gui.addText(
            SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' %
            ('red', 'Nécessite un Compte 1Fichier Premium ou Gratuit'))

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://venom/')
        gui.addDir(
            SITE_IDENTIFIER,
            'opensetting',
            addons.VSlang(30023),
            'none.png',
            output_parameter_handler)
        gui.setEndOfDirectory()
    else:
        if GestionCookie().Readcookie('onefichier') != '':
            showFile(URL_FILE)

        else:
            premium_handler = cPremiumHandler('onefichier')
            Connection = premium_handler.Authentificate()
            if Connection is False:
                gui = Gui()
                gui.addText(
                    SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' %
                    ('red', 'Connexion refusée'))
                gui.setEndOfDirectory()

            else:
                showFile(URL_FILE)


def opensetting():
    Addon().openSettings()


def showFile(sFileTree=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    # url = input_parameter_handler.getValue('site_url')
    if input_parameter_handler.exist('site_url'):
        url = input_parameter_handler.getValue('site_url')

    if sFileTree:
        url = sFileTree

    premium_handler = cPremiumHandler('onefichier')

    html_content = premium_handler.GetHtml(url)

    parser = Parser()
    pattern = '((?:|directory")) *rel="([^"]+)"><div class="dF"><a href="#" onclick="return false">(.+?)</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                output_parameter_handler.addParameter(
                    'site_url', '%s%s%s%s' %
                    (URL_FILE, '?dir_id=', entry[1], '&oby=0&search='))
                output_parameter_handler.addParameter('sCode', '')
                output_parameter_handler.addParameter('title', entry[2])
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showFile',
                    entry[2],
                    'genres.png',
                    output_parameter_handler)

            else:
                output_parameter_handler.addParameter(
                    'site_url', '%s%s' %
                    (URL_MAIN, 'console/link.pl'))
                output_parameter_handler.addParameter('sCode', entry[1])
                output_parameter_handler.addParameter('title', entry[2])
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showHosters',
                    entry[2],
                    'genres.png',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    sCode = input_parameter_handler.getValue('sCode')

    premium_handler = cPremiumHandler('onefichier')
    html_content = premium_handler.GetHtml(url, 'selected%5B%5D=' + sCode)

    pattern = '<a href="([^"]+)">(.+?)</a></td>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        hoster_url = results[1][0][0]
        title = results[1][0][1]

        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(title)
            hoster.setFileName(title)
            HosterGui().showHoster(gui, hoster, hoster_url, '',
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def upToMyAccount():
    input_parameter_handler = InputParameterHandler()
    media_url = input_parameter_handler.getValue('media_url')

    premium_handler = cPremiumHandler('onefichier')
    # vérification du lien
    html_content = premium_handler.GetHtml('%s' % (URL_VERIF + media_url))
    if html_content:
        sCheck = html_content.find('NOT FOUND')
        if sCheck != -1:
            # pénible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification(
                'Info upload',
                'Fichier introuvable',
                xbmcgui.NOTIFICATION_INFO,
                2000,
                False)

        else:
            # si liens ok >> requête
            html_content = premium_handler.GetHtml(
                URL_REMOTE, '%s%s%s' %
                ('links=', media_url, '&did=0'))
            if html_content:
                sCheck = html_content.find('1 liens')
                if sCheck != -1:
                    # pénible ce dialog auth
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmcgui.Dialog().notification(
                        'Info upload',
                        'Ajouter à votre compte',
                        xbmcgui.NOTIFICATION_INFO,
                        2000,
                        False)
