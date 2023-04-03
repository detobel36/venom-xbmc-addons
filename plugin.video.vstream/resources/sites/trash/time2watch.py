# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.multihost import cMultiup
from resources.lib.util import Noredirection, urlEncode
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.config import GestionCookie
from resources.lib.comaddon import Progress, dialog, xbmc, xbmcgui, VSlog, Addon
import xbmcvfs
import xbmcaddon
import re
import os
import base64
return False


ADDON = Addon()
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'time2watch'
SITE_NAME = '[COLOR violet]Time2Watch[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://time2watch.io/'

URL_SEARCH = (URL_MAIN + 'search/?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuFilms')
DERNIER_AJOUT = (URL_MAIN + 'last/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film/last/', 'showMovies')
MOVIE_POPULAR = (URL_MAIN + "film/popular/", 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'film/bluray/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')
MOVIE_VFR = (URL_MAIN + 'film/vfr/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'film/loved/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film/genre/', 'showGenre')
MOVIE_ANNEES = (URL_MAIN + 'film/date/', 'showYears')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'serie/last/', 'showMovies')
SERIE_POPULAR = (URL_MAIN + "serie/popular/", 'showMovies')
SERIE_HD1080 = (URL_MAIN + 'serie/bluray/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'serie/vostfr/', 'showMovies')
SERIE_VFR = (URL_MAIN + 'serie/vfr/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'serie/loved/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/genre/', 'showGenre')
SERIE_ANNEES = (URL_MAIN + 'serie/date/', 'showYears')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + 'anime/last/', 'showMovies')
ANIM_POPULAR = (URL_MAIN + "anime/popular/", 'showMovies')
ANIM_HD1080 = (URL_MAIN + 'anime/bluray/', 'showMovies')
ANIM_VOSTFR = (URL_MAIN + 'anime/vostfr/', 'showMovies')
ANIM_VFR = (URL_MAIN + 'anime/vfr/', 'showMovies')
ANIM_NOTES = (URL_MAIN + 'anime/loved/', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'anime/genre/', 'showGenre')
ANIM_ANNEES = (URL_MAIN + 'anime/date/', 'showYears')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS = (URL_MAIN + 'theatre/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showDetail',
        '[COLOR red]Explication pour le site[/COLOR]',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DERNIER_AJOUT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DERNIER_AJOUT[1],
        'Derniers Ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMangas',
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuAutre',
        'Autres',
        'tv.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HD1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD1080[1],
        'Bluray 1080P',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_POPULAR[1],
        'Films (Les plus populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFR[1],
        'Films (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VFR[1],
        'Films (VFR)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Series (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Series (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Series (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_HD1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HD1080[1],
        'Bluray 1080P',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_POPULAR[1],
        'Series (Les plus populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFR[1],
        'Series (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFR[1],
        'Series (VFR)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NOTES[1],
        'Series (Les mieux notées)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMangas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animes (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animes (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animes (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_HD1080[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_HD1080[1],
        'Bluray 1080P',
        'hd.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_POPULAR[1],
        'Animes (Les plus populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFR[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFR[1],
        'Animés (VFR)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NOTES[1],
        'Animés (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showDetail():
    dialog().VStextView(desc="""Explication du Captcha:
Pour passer le Captcha il suffit de choisir l'image qui corresponds la plus a celle de gauche.
Il se peut que la couleur ou l'orientation de l'image sous différente.
Mais le pictogramme lui sera le meme.
Attention vous avez 20 secondes pour valider votre réponse.
Si jamais vous vous trompez il suffit de recharger la page.

Utilité d'avoir un compte:
Le site est limité en nombre de passage pour les personnes qui n'ont pas de compte.
Avoir un compte permet aussi de ne pas avoir le Captcha qui apparait à chaque fois.
Vous pouvez activer la connexion au compte dans les paramètres de vStream.""", title="Fonctionnement du site")


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html = re.search(
        '<section id="section_genre">(.+?)</section>',
        html_content,
        re.DOTALL).group(1)
    pattern = '<a href="([^"]+)">([^"]+)</a>'

    parser = Parser()
    results = parser.parse(html, pattern)

    for genre in results[1]:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', URL_MAIN + genre[0])
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            genre[1],
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html = re.search(
        '<section id="section_genre">(.+?)</section>',
        html_content,
        re.DOTALL).group(1)
    pattern = '<a href="([^"]+)">([^"]+)</a>'

    parser = Parser()
    results = parser.parse(html, pattern)

    for Years in results[1]:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', URL_MAIN + Years[0])
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Years[1],
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    Cookie = GestionCookie().Readcookie('time2watch')

    request_handler = RequestHandler(url)
    if Cookie:
        request_handler.addHeaderEntry('Cookie', Cookie)
    html_content = request_handler.request()

    # Connection pour passer la limite
    if 'Déconnexion' not in html_content and ADDON.getSetting(
            'hoster_time2watch_premium') == "true":
        VSlog("Connection")

        data = {
            'username': ADDON.getSetting('hoster_time2watch_username'),
            'pwd': ADDON.getSetting('hoster_time2watch_password')}

        data = urlEncode(data)

        opener = Noredirection()

        opener.addheaders = [('User-Agent', UA)]
        opener.addheaders.append(
            ('Content-Type', 'application/x-www-form-urlencoded'))
        opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
        opener.addheaders.append(('Content-Length', str(len(data))))

        response = opener.open("https://time2watch.io/login/", data)
        head = response.info()

        # get cookie
        Cookie = ''
        if 'Set-Cookie' in head:
            parser = Parser()
            pattern = '(?:^|,) *([^;,]+?)=([^;,\\/]+?);'
            results = parser.parse(str(head['Set-Cookie']), pattern)
            # print(results)
            if results[0]:
                for cook in results[1]:
                    if 'deleted' in cook[1]:
                        continue
                    Cookie = Cookie + cook[0] + '=' + cook[1] + ';'

        GestionCookie().SaveCookie('time2watch', Cookie)

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Cookie', Cookie)
        html_content = request_handler.request()

    pattern = '<div class="col-lg-4.+?<a href="([^"]+)">.+?affiche_liste" src="([^"]+)".+?alt="([^"]+)".+?<i class="fa fa-tv"></i>([^<]+)<.+?div class="synopsis_hover".+?>([^<]+)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = URL_MAIN + entry[0]
            thumb = URL_MAIN + entry[1]
            title = entry[2]
            qual = entry[3].replace(' ', '')
            desc = entry[4]

            title = title.replace('En streaming', '')

            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sCookie', Cookie)

            if '/serie/' in url2 or '/anime/' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisonEpisodes',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMoviesLink',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                number +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a class="light_pagination" href="([^"]+)" aria-label="Next">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return URL_MAIN + results[1][0]

    return False


def showMoviesLink():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    Cookie = input_parameter_handler.getValue('sCookie')

    request_handler = RequestHandler(url)
    if Cookie:
        request_handler.addHeaderEntry('Cookie', Cookie)
    html_content = request_handler.request()

    pattern = '<i class="fa fa-download fa-fw"></i>.+?<b>(.+?)</b></a>'
    var = re.search(
        'var hash = (.+?);',
        html_content).group(1).replace(
        '"',
        "").strip('][').split(',')
    url = re.search(
        "document\\.getElementById\\(\'openlink_\'\\+n\\).href = '(.+?)';",
        html_content).group(1)

    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry, VAR in zip(results[1], var):
            url2 = URL_MAIN + url.replace("'+nhash+'", VAR)
            title = ('%s [%s]') % (movie_title, entry)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('sCookie', Cookie)

            gui.addLink(
                SITE_IDENTIFIER,
                'decryptTime',
                title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSaisonEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    Cookie = input_parameter_handler.getValue('sCookie')

    request_handler = RequestHandler(url)
    if Cookie:
        request_handler.addHeaderEntry('Cookie', Cookie)
    html_content = request_handler.request()

    url = re.search(
        "document\\.getElementById\\(\'openlink_\'\\+n\\).href = '(.+?)';",
        html_content).group(1)
    parser = Parser()
    pattern = '<span style="margin-left: 20px;">(.+?)</span>|<span style="margin-left: 35px;">(.+?)<.+?<span class="fa arrow">|setfatherasseen.+?<i class="fa fa-download fa-fw">.+?<b>(.+?)</b>.+?var hash_.+?= "(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                ses = entry[0]

            elif entry[1]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    ses +
                    ' ' +
                    entry[1] +
                    '[/COLOR]')

            else:
                url2 = URL_MAIN + url.replace("'+nhash+'", entry[3])
                display_title = ('%s [%s]') % (movie_title, entry[2])

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('sCookie', Cookie)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'decryptTime',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def getLinkHtml(html_content):
    if "Limite atteinte" not in html_content:
        parser = Parser()
        pattern = 'style="color: #adadad;"(.+?)no_our_shit_us'
        results = parser.parse(html_content, pattern)
        return results[1][0]
    return False


def decryptTime():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    Cookie = input_parameter_handler.getValue('sCookie')

    request_handler = RequestHandler(url)
    if Cookie:
        request_handler.addHeaderEntry('Cookie', Cookie)
    html_content = request_handler.request()

    if "Test de s" in html_content:
        pattern = '<img style="margin: auto; display: block; width: 120px; height: 120px;" src="([^"]+)"/>.+?name="challenge" value="([^"]+)"'
        result = parser.parse(html_content, pattern)
        challenge = result[1][0][0]
        challengeTok = result[1][0][1]

        pattern = '<img onclick="choose\\(\'([^\']+)\'\\).+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)

        Filename = []
        i = 0

        request_handler = RequestHandler(challenge)
        if Cookie:
            request_handler.addHeaderEntry('Cookie', Cookie)
        html_content = request_handler.request()

        downloaded_image = xbmcvfs.File(
            "special://home/userdata/addon_data/plugin.video.vstream/challenge.png", 'wb')
        downloaded_image.write(bytearray(html_content))
        downloaded_image.close()

        for imgURL in results[1]:
            request_handler = RequestHandler(imgURL[1])
            if Cookie:
                request_handler.addHeaderEntry('Cookie', Cookie)
            imgdata = request_handler.request()

            downloaded_image = xbmcvfs.File(
                "special://home/userdata/addon_data/plugin.video.vstream/test" +
                str(i) +
                ".png",
                'wb')
            downloaded_image.write(bytearray(imgdata))
            downloaded_image.close()
            Filename.append(
                "special://home/userdata/addon_data/plugin.video.vstream/test" +
                str(i) +
                ".png")
            i = i + 1

        oSolver = cInputWindow(
            captcha=Filename,
            challenge="special://home/userdata/addon_data/plugin.video.vstream/challenge.png")
        retArg = oSolver.get()

        data = "g-recaptcha-response=" + \
            results[1][int(retArg)][0] + "&challenge=" + challengeTok

        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            'Content-Type', "application/x-www-form-urlencoded")
        request_handler.addHeaderEntry('Content-Length', len(str(data)))
        if Cookie:
            request_handler.addHeaderEntry('Cookie', Cookie)
        request_handler.addParametersLine(data)
        html_content = getLinkHtml(request_handler.request())
        if not html_content:
            dialog().VSok(
                desc="Limite journalière atteinte, pour continuez à utiliser le site aujourd'hui, il faut utilisez un compte (c'est gratuit)",
                title="Limites atteintes")

    else:
        html_content = getLinkHtml(html_content)

    pattern = '<img src=.+?<a href="([^"]+)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            if 'multiup' in entry:
                results = cMultiup().GetUrls(entry)

                if (results):
                    for entry in results:
                        hoster_url = entry

                        hoster = HosterGui().checkHoster(hoster_url)
                        if (hoster):
                            hoster.setDisplayName(movie_title)
                            hoster.setFileName(movie_title)
                            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

            else:
                hoster = HosterGui().checkHoster(entry)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, entry, thumb)

    gui.setEndOfDirectory()


class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        i = 0
        u = 0
        pos = []

        bg_image = 'special://home/addons/plugin.video.vstream/resources/art/background.png'
        check_image = 'special://home/addons/plugin.video.vstream/resources/art/trans_checked.png'

        self.ctrlBackground = xbmcgui.ControlImage(0, 0, 1280, 720, bg_image)
        self.cancelled = False
        self.addControl(self.ctrlBackground)

        self.img = [0] * 10

        self.strActionInfo = xbmcgui.ControlLabel(
            250,
            20,
            724,
            400,
            'Veuillez sélectionnez l\'image qui ressemble le plus \n a l\'image qui se trouve le plus a gauche.',
            'font40',
            '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.img[0] = xbmcgui.ControlImage(450, 110, 260, 166, self.cptloc[0])
        self.addControl(self.img[0])

        self.img[1] = xbmcgui.ControlImage(
            450 + 260, 110, 260, 166, self.cptloc[1])
        self.addControl(self.img[1])

        self.img[2] = xbmcgui.ControlImage(
            450 + 520, 110, 260, 166, self.cptloc[2])
        self.addControl(self.img[2])

        self.img[3] = xbmcgui.ControlImage(
            450, 110 + 166, 260, 166, self.cptloc[3])
        self.addControl(self.img[3])

        self.img[4] = xbmcgui.ControlImage(
            450 + 260, 110 + 166, 260, 166, self.cptloc[4])
        self.addControl(self.img[4])

        self.img[5] = xbmcgui.ControlImage(
            450 + 520, 110 + 166, 260, 166, self.cptloc[5])
        self.addControl(self.img[5])

        self.img[6] = xbmcgui.ControlImage(
            450, 110 + 332, 260, 166, self.cptloc[6])
        self.addControl(self.img[6])

        self.img[7] = xbmcgui.ControlImage(
            450 + 260, 110 + 332, 260, 166, self.cptloc[7])
        self.addControl(self.img[7])

        self.img[8] = xbmcgui.ControlImage(
            450 + 520, 110 + 332, 260, 166, self.cptloc[8])
        self.addControl(self.img[8])

        self.img[9] = xbmcgui.ControlImage(
            100, 80, 260, 166, kwargs.get('challenge'))
        self.addControl(self.img[9])

        self.chk = [0] * 9
        self.chkbutton = [0] * 9
        self.chkstate = [False] * 9

        if 1 == 2:
            self.chk[0] = xbmcgui.ControlCheckMark(
                450,
                110,
                260,
                166,
                '1',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[1] = xbmcgui.ControlCheckMark(
                450 + 260,
                110,
                260,
                166,
                '2',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[2] = xbmcgui.ControlCheckMark(
                450 + 520,
                110,
                260,
                166,
                '3',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)

            self.chk[3] = xbmcgui.ControlCheckMark(
                450,
                110 + 166,
                260,
                166,
                '4',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[4] = xbmcgui.ControlCheckMark(
                450 + 260,
                110 + 166,
                260,
                166,
                '5',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[5] = xbmcgui.ControlCheckMark(
                450 + 520,
                110 + 166,
                260,
                166,
                '6',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)

            self.chk[6] = xbmcgui.ControlCheckMark(
                450,
                110 + 332,
                260,
                166,
                '7',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[7] = xbmcgui.ControlCheckMark(
                450 + 260,
                110 + 332,
                260,
                166,
                '8',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)
            self.chk[8] = xbmcgui.ControlCheckMark(
                450 + 520,
                110 + 332,
                260,
                166,
                '9',
                font='font14',
                focusTexture=check_image,
                checkWidth=260,
                checkHeight=166)

        else:
            self.chk[0] = xbmcgui.ControlImage(450, 110, 260, 166, check_image)
            self.chk[1] = xbmcgui.ControlImage(
                450 + 260, 110, 260, 166, check_image)
            self.chk[2] = xbmcgui.ControlImage(
                450 + 520, 110, 260, 166, check_image)

            self.chk[3] = xbmcgui.ControlImage(
                450, 110 + 166, 260, 166, check_image)
            self.chk[4] = xbmcgui.ControlImage(
                450 + 260, 110 + 166, 260, 166, check_image)
            self.chk[5] = xbmcgui.ControlImage(
                450 + 520, 110 + 166, 260, 166, check_image)

            self.chk[6] = xbmcgui.ControlImage(
                450, 110 + 332, 260, 166, check_image)
            self.chk[7] = xbmcgui.ControlImage(
                450 + 260, 110 + 332, 260, 166, check_image)
            self.chk[8] = xbmcgui.ControlImage(
                450 + 520, 110 + 332, 260, 166, check_image)

            self.chkbutton[0] = xbmcgui.ControlButton(
                450, 110, 260, 166, '1', font='font1')
            self.chkbutton[1] = xbmcgui.ControlButton(
                450 + 260, 110, 260, 166, '2', font='font1')
            self.chkbutton[2] = xbmcgui.ControlButton(
                450 + 520, 110, 260, 166, '3', font='font1')

            self.chkbutton[3] = xbmcgui.ControlButton(
                450, 110 + 166, 260, 166, '4', font='font1')
            self.chkbutton[4] = xbmcgui.ControlButton(
                450 + 260, 110 + 166, 260, 166, '5', font='font1')
            self.chkbutton[5] = xbmcgui.ControlButton(
                450 + 520, 110 + 166, 260, 166, '6', font='font1')

            self.chkbutton[6] = xbmcgui.ControlButton(
                450, 110 + 332, 260, 166, '7', font='font1')
            self.chkbutton[7] = xbmcgui.ControlButton(
                450 + 260, 110 + 332, 260, 166, '8', font='font1')
            self.chkbutton[8] = xbmcgui.ControlButton(
                450 + 520, 110 + 332, 260, 166, '9', font='font1')

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(
            250 + 260 - 70, 620, 140, 50, 'Cancel', alignment=2)
        self.okbutton = xbmcgui.ControlButton(
            250 + 520 - 50, 620, 100, 50, 'OK', alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[6].controlDown(self.cancelbutton)
        self.chkbutton[6].controlUp(self.chkbutton[3])
        self.chkbutton[7].controlDown(self.cancelbutton)
        self.chkbutton[7].controlUp(self.chkbutton[4])
        self.chkbutton[8].controlDown(self.okbutton)
        self.chkbutton[8].controlUp(self.chkbutton[5])

        self.chkbutton[6].controlLeft(self.chkbutton[8])
        self.chkbutton[6].controlRight(self.chkbutton[7])
        self.chkbutton[7].controlLeft(self.chkbutton[6])
        self.chkbutton[7].controlRight(self.chkbutton[8])
        self.chkbutton[8].controlLeft(self.chkbutton[7])
        self.chkbutton[8].controlRight(self.chkbutton[6])

        self.chkbutton[3].controlDown(self.chkbutton[6])
        self.chkbutton[3].controlUp(self.chkbutton[0])
        self.chkbutton[4].controlDown(self.chkbutton[7])
        self.chkbutton[4].controlUp(self.chkbutton[1])
        self.chkbutton[5].controlDown(self.chkbutton[8])
        self.chkbutton[5].controlUp(self.chkbutton[2])

        self.chkbutton[3].controlLeft(self.chkbutton[5])
        self.chkbutton[3].controlRight(self.chkbutton[4])
        self.chkbutton[4].controlLeft(self.chkbutton[3])
        self.chkbutton[4].controlRight(self.chkbutton[5])
        self.chkbutton[5].controlLeft(self.chkbutton[4])
        self.chkbutton[5].controlRight(self.chkbutton[3])

        self.chkbutton[0].controlDown(self.chkbutton[3])
        self.chkbutton[0].controlUp(self.cancelbutton)
        self.chkbutton[1].controlDown(self.chkbutton[4])
        self.chkbutton[1].controlUp(self.cancelbutton)
        self.chkbutton[2].controlDown(self.chkbutton[5])
        self.chkbutton[2].controlUp(self.okbutton)

        self.chkbutton[0].controlLeft(self.chkbutton[2])
        self.chkbutton[0].controlRight(self.chkbutton[1])
        self.chkbutton[1].controlLeft(self.chkbutton[0])
        self.chkbutton[1].controlRight(self.chkbutton[2])
        self.chkbutton[2].controlLeft(self.chkbutton[1])
        self.chkbutton[2].controlRight(self.chkbutton[0])

        self.cancelled = False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton)
        self.okbutton.controlRight(self.cancelbutton)
        self.cancelbutton.controlLeft(self.okbutton)
        self.cancelbutton.controlRight(self.okbutton)
        self.okbutton.controlDown(self.chkbutton[2])
        self.okbutton.controlUp(self.chkbutton[8])
        self.cancelbutton.controlDown(self.chkbutton[0])
        self.cancelbutton.controlUp(self.chkbutton[6])

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval = ""
            for objn in range(9):
                if self.chkstate[objn]:
                    retval += ("" if retval == "" else ",") + str(objn)
            return retval

        else:
            return ""

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        if str(control.getLabel()) == "OK":
            if self.anythingChecked():
                self.close()
        elif str(control.getLabel()) == "Cancel":
            self.cancelled = True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index = control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index) -
                                  1] = not self.chkstate[int(index) - 1]
                    self.chk[int(index) -
                             1].setVisible(self.chkstate[int(index) - 1])

        except BaseException:
            pass

    def onAction(self, action):
        if action == 10:
            self.cancelled = True
            self.close()
