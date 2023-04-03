# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import RequestHandler

from resources.lib.comaddon import Addon, dialog, VSlog
from resources.lib.config import GestionCookie
from resources.lib.parser import Parser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cPremiumHandler:
    ADDON = Addon()
    DIALOG = dialog()

    def __init__(self, hoster_identifier):
        self.__sHosterIdentifier = hoster_identifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False
        self.__LoginTry = False
        self.__ssl = False

        # hack pour garder la compatiblité avec ceux qui ont déjà reglé les
        # settings
        if self.__sHosterIdentifier == '1fichier':
            self.__sHosterIdentifier = 'onefichier'

        self.__Ispremium = False
        bIsPremium = self.ADDON.getSetting(
            'hoster_' + str(self.__sHosterIdentifier) + '_premium')
        if bIsPremium == 'true':
            VSlog("Utilise compte premium pour hoster " +
                  str(self.__sHosterIdentifier))
            self.__Ispremium = True
        else:
            VSlog("Utilise compte gratuit pour hoster " +
                  str(self.__sHosterIdentifier))

    def isPremiumModeAvailable(self):
        return self.__Ispremium

    def getUsername(self):
        username = self.ADDON.getSetting(
            'hoster_' + str(self.__sHosterIdentifier) + '_username')
        return username

    def getPassword(self):
        password = self.ADDON.getSetting(
            'hoster_' + str(self.__sHosterIdentifier) + '_password')
        return password

    def AddCookies(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

    def Checklogged(self, code):
        if 'uptobox' in self.__sHosterIdentifier:
            if '//uptobox.com/logout?' in code or 'Success' in code:
                return True

        if 'onefichier' in self.__sHosterIdentifier:
            # test ok mais pas convaincu....
            if 'premium' in code or 'jqueryFileTree' in code or '1fichier.com/logout' in code:
                return True

        return False

    def CheckCookie(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if cookies != '':
            return True
        return False

    def Authentificate(self):

        # un seul essais par session, pas besoin de bombarder le serveur
        if self.__LoginTry:
            return False
        self.__LoginTry = True

        if not self.__Ispremium:
            return False

        post_data = {}

        if 'uptobox' in self.__sHosterIdentifier:
            url = 'https://uptobox.com/login'
            post_data['login'] = self.getUsername()
            post_data['password'] = self.getPassword()

        elif 'onefichier' in self.__sHosterIdentifier:
            url = 'https://1fichier.com/login.pl'
            post_data['mail'] = self.getUsername()
            post_data['pass'] = self.getPassword()
            post_data['lt'] = 'on'
            post_data['purge'] = 'on'
            post_data['valider'] = 'Send'

        elif 'uploaded' in self.__sHosterIdentifier:
            url = 'http://uploaded.net/io/login'
            post_data['id'] = self.getUsername()
            post_data['pw'] = self.getPassword()

        # si aucun de trouve on retourne
        else:
            return False

        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)

        if 'uptobox' in self.__sHosterIdentifier:
            request_handler.disableRedirect()

            request_handler.addHeaderEntry('User-Agent', UA)
            request_handler.addHeaderEntry(
                'Content-Type', "application/x-www-form-urlencoded")
            request_handler.addHeaderEntry(
                'Content-Length', str(len(post_data)))

        for data in post_data:
            request_handler.addParameters(data, post_data[data])

        html_content = request_handler.request()
        head = request_handler.getResponseHeader()

        if 'uptobox' in self.__sHosterIdentifier:
            if 'Set-Cookie' in head and 'xfss' in head['Set-Cookie']:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo(
                    'Authentification rate',
                    self.__sDisplayName)
                return False
        elif 'onefichier' in self.__sHosterIdentifier:
            if 'You are logged in. This page will redirect you.' in html_content:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo(
                    'Authentification rate',
                    self.__sDisplayName)
                return False
        elif 'uploaded' in self.__sHosterIdentifier:
            if html_content == '':
                self.isLogin = True
            else:
                self.DIALOG.VSinfo(
                    'Authentification rate',
                    self.__sDisplayName)
                return False
        else:
            return False

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            parser = Parser()
            pattern = '(?:^|,) *([^;,]+?)=([^;,\\/]+?);'
            results = parser.parse(str(head['Set-Cookie']), pattern)
            # print(results)
            if results[0]:
                for cook in results[1]:
                    if 'deleted' in cook[1]:
                        continue
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'

        # save cookie
        GestionCookie().SaveCookie(self.__sHosterIdentifier, cookies)

        self.DIALOG.VSinfo('Authentification reussie', self.__sDisplayName)
        VSlog('Auhentification reussie')

        return True

    def GetHtmlwithcookies(self, url, data, cookies):
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        if not (data is None):
            request_handler.addParametersLine(data)
            request_handler.addHeaderEntry('Referer', url)

        request_handler.addHeaderEntry('Cookie', cookies)

        html_content = request_handler.request()
        return html_content

    def GetHtml(self, url, data=None):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        # aucun ne marche sans cookies
        if (cookies == '') and not self.__LoginTry and self.__Ispremium:
            self.Authentificate()
            if not self.isLogin:
                return ''
            cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        html_content = self.GetHtmlwithcookies(url, data, cookies)

        # Les cookies ne sont plus valables, mais on teste QUE si la personne
        # n'a pas essaye de s'authentifier
        if not self.Checklogged(
                html_content) and not self.__LoginTry and self.__Ispremium:
            VSlog('Cookies non valables')
            self.Authentificate()
            if self.isLogin:
                cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
                html_content = self.GetHtmlwithcookies(url, data, cookies)
            else:
                return ''

        return html_content

    def setToken(self, sToken):
        self.ADDON.setSetting('hoster_' +
                              str(self.__sHosterIdentifier) +
                              '_token', sToken)

    def getToken(self):

        # pas de premium, pas de token
        if not self.__Ispremium:
            return None

        # le token est connu, on le retourne
        sToken = self.ADDON.getSetting(
            'hoster_' + str(self.__sHosterIdentifier) + '_token')
        if sToken:
            return sToken

        # token alldebrid était connu avec un aute setting
        if 'alldebrid' in self.__sHosterIdentifier:
            # ancien nom, à supprimer après quelques temps
            sToken = self.ADDON.getSetting('token_alldebrid')
            if sToken:
                self.ADDON.setSetting(
                    'hoster_' + str(self.__sHosterIdentifier) + '_token', sToken)
            return sToken

        # Si pas de token pour uptobox, on le récupère depuis le compte
        if 'uptobox' in self.__sHosterIdentifier:

            if not self.isLogin:
                self.Authentificate()

            # on retrouve le token et on le sauvegarde
            if self.isLogin:
                html_content = self.GetHtml('https://uptobox.com/my_account')
                pattern = 'data-clipboard-text="(.+?)" data-tippy-content="Token'
                results = Parser().parse(html_content, pattern, 1)
                if results[0]:
                    sToken = results[1][0]
                    self.ADDON.setSetting(
                        'hoster_' + str(self.__sHosterIdentifier) + '_token', sToken)
                    return sToken

        return None
