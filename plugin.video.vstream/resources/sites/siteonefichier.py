# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc
import xbmcgui

from resources.lib.comaddon import Progress, addon, SiteManager
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
    addons = addon()

    if (addons.getSetting('hoster_onefichier_username') == '') and (
            addons.getSetting('hoster_onefichier_password') == ''):
        gui = Gui()
        gui.addText(
            SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' %
            ('red', 'Nécessite un Compte 1Fichier Premium ou Gratuit'))

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://venom/')
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
            oPremiumHandler = cPremiumHandler('onefichier')
            Connection = oPremiumHandler.Authentificate()
            if Connection is False:
                gui = Gui()
                gui.addText(
                    SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' %
                    ('red', 'Connexion refusée'))
                gui.setEndOfDirectory()

            else:
                showFile(URL_FILE)


def opensetting():
    addon().openSettings()


def showFile(sFileTree=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    # sUrl = input_parameter_handler.getValue('siteUrl')
    if input_parameter_handler.exist('siteUrl'):
        sUrl = input_parameter_handler.getValue('siteUrl')

    if sFileTree:
        sUrl = sFileTree

    oPremiumHandler = cPremiumHandler('onefichier')

    sHtmlContent = oPremiumHandler.GetHtml(sUrl)

    oParser = Parser()
    sPattern = '((?:|directory")) *rel="([^"]+)"><div class="dF"><a href="#" onclick="return false">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                output_parameter_handler.addParameter(
                    'siteUrl', '%s%s%s%s' %
                    (URL_FILE, '?dir_id=', aEntry[1], '&oby=0&search='))
                output_parameter_handler.addParameter('sCode', '')
                output_parameter_handler.addParameter('title', aEntry[2])
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showFile',
                    aEntry[2],
                    'genres.png',
                    output_parameter_handler)

            else:
                output_parameter_handler.addParameter(
                    'siteUrl', '%s%s' %
                    (URL_MAIN, 'console/link.pl'))
                output_parameter_handler.addParameter('sCode', aEntry[1])
                output_parameter_handler.addParameter('title', aEntry[2])
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showHosters',
                    aEntry[2],
                    'genres.png',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sCode = input_parameter_handler.getValue('sCode')

    oPremiumHandler = cPremiumHandler('onefichier')
    sHtmlContent = oPremiumHandler.GetHtml(sUrl, 'selected%5B%5D=' + sCode)

    sPattern = '<a href="([^"]+)">(.+?)</a></td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0][0]
        title = aResult[1][0][1]

        oHoster = HosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(title)
            oHoster.setFileName(title)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, '',
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def upToMyAccount():
    input_parameter_handler = InputParameterHandler()
    sMediaUrl = input_parameter_handler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('onefichier')
    # vérification du lien
    sHtmlContent = oPremiumHandler.GetHtml('%s' % (URL_VERIF + sMediaUrl))
    if sHtmlContent:
        sCheck = sHtmlContent.find('NOT FOUND')
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
            sHtmlContent = oPremiumHandler.GetHtml(
                URL_REMOTE, '%s%s%s' %
                ('links=', sMediaUrl, '&did=0'))
            if sHtmlContent:
                sCheck = sHtmlContent.find('1 liens')
                if sCheck != -1:
                    # pénible ce dialog auth
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmcgui.Dialog().notification(
                        'Info upload',
                        'Ajouter à votre compte',
                        xbmcgui.NOTIFICATION_INFO,
                        2000,
                        False)
