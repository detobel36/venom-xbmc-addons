# -*- coding: utf-8 -*-
# From Patoche2025

from resources.lib.config import cConfig
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import Gui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

import urllib
import re
import xbmcgui
import xbmc

from resources.lib.dl_deprotect import DecryptDlProtect


SITE_IDENTIFIER = 'exdown_com'
SITE_NAME = '[COLOR violet]Extreme Download[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = 'http://www.exdown.net/'

URL_SEARCH = (URL_MAIN + 'index.php?do=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_BDRIPSD = (
    URL_MAIN + 'films-sd/dvdrip',
    'showMovies')  # films BDRIP_DVDRIP
MOVIE_VOSTFRSD = (
    URL_MAIN +
    'films-sd/dvdrip-vostfr',
    'showMovies')  # films VOSTFR
MOVIE_DVDSCR = (URL_MAIN + 'films-sd/dvdscr-r5', 'showMovies')  # films DVDSCR
MOVIE_TSCAM = (URL_MAIN + 'films-sd/ts-cam', 'showMovies')  # films TS/CAM
MOVIE_FILMOGRAPHIE = (
    URL_MAIN + 'films-sd/filmographie',
    'showMovies')  # filmographie

MOVIE_BDRIPHD = (URL_MAIN + 'films-hd/bdrip-720p',
                 'showMovies')  # films BDRIP 720P
MOVIE_BLURAY720P = (
    URL_MAIN + 'films-hd/bluray-720p',
    'showMovies')  # films BluRay 720P
MOVIE_BLURAY1080P = (
    URL_MAIN + 'films-hd/bluray-1080p',
    'showMovies')  # films BluRay 1080P
MOVIE_BLURAYVOSTFR = (
    URL_MAIN + 'films-hd/bluray-vostfr',
    'showMovies')  # films BluRay VOSTFR
MOVIE_BLURAY3D = (
    URL_MAIN +
    'films-hd/bluray-vostfr',
    'showMovies')  # films BluRay 3D

MOVIE_CLASSIQUESD = (
    URL_MAIN +
    'films-hd/films-classique/classiques-sd',
    'showMovies')  # films Classique SD
MOVIE_CLASSIQUEHD = (
    URL_MAIN +
    'films-hd/films-classique/classiques-hd',
    'showMovies')  # films Classique HD

MOVIE_GENRES = (True, 'showGenre')
# MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies') # films VF
# MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies') # films VOSTFR
# MOVIE_ANIME = (URL_MAIN + 'dessins-animes.html', 'showMovies') # dessins
# animes

SERIE_SDVF = (URL_MAIN + 'series/vf', 'showMovies')  # serie SD VF
SERIE_SDVOSTFR = (URL_MAIN + 'series/vostfr', 'showMovies')  # serie SD VOSTFR
SERIE_PACKSD = (
    URL_MAIN + 'series-vostfr.html',
    'showMovies')  # serie PACK SERIES SD

SERIE_HDVF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies')  # serie HD VF
SERIE_HDVOSTFR = (
    URL_MAIN +
    'series-hd/hd-series-vostfr',
    'showMovies')  # serie HD VOSTFR
SERIE_PACKHD = (URL_MAIN + 'series-hd/pack-series-hd',
                'showMovies')  # serie PACK SERIES HD

# SERIE_GENRE = (True, 'showGenre')

ANIM_FILMS = (URL_MAIN + 'mangas/manga-films', 'showMovies')  # FILMS MANGAS
ANIM_VF = (URL_MAIN + 'mangas/series-vf', 'showMovies')  # ANIMES VF
ANIM_VOSTFR = (
    URL_MAIN +
    'mangas/series-vostfr',
    'showMovies')  # ANIMES VOSTFR


BLURAY_NEWS = (URL_MAIN + 'films-hd/full-bluray',
               'showMovies')  # derniers Blu-Rays


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovies',
        'Recherche de films ou series',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BDRIPSD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIPSD[1],
        'films BDRIP_DVDRIP',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VOSTFRSD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VOSTFRSD[1],
        'films VOSTFR',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BDRIPHD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BDRIPHD[1],
        'films BDRIP 720P',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BLURAY720P[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAY720P[1],
        'films BluRay 720P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BLURAY1080P[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAY1080P[1],
        'films BluRay 1080P',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BLURAYVOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAYVOSTFR[1],
        'films BluRay VOSTFR',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_BLURAY3D[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_BLURAY3D[0],
        'films BluRay 3D',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', BLURAY_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'BLURAY_NEWS[1]',
        'derniers Blu-Rays',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_FILMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'ANIM_FILMS[1]',
        'Film MANGAS',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'ANIM_VF[1]',
        'ANIMES VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'ANIM_VOSTFR[1]',
        'ANIMES VOSTFR',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films Genre',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SDVF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VF[1],
        'serie SD VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SDVOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFR[1],
        'serie SD VOSTFR',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_PACKSD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_PACKSD[1],
        'serie PACK SERIES SD',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_HDVF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_HDVF[1],
        'serie HD VF',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_HDVOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'SERIE_HDVOSTFR[1]',
        'serie HD VOSTFR',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_PACKHD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'serie PACK SERIES HD',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchMovies():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_MOVIES[0] + search_text + \
            '&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSeries():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH_SERIES[0] + search_text + \
            '&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenre():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'tags/Action'])
    liste.append(['Animation', URL_MAIN + 'tags/Animation'])
    liste.append(['Arts Martiaux', URL_MAIN + 'tags/Arts+Martiaux'])
    liste.append(['Biopic', URL_MAIN + 'tags/Biopic'])
    liste.append(['Comedie', URL_MAIN + 'tags/Comédie'])
    liste.append(['Comedie Dramatique', URL_MAIN + 'tags/Comédie+dramatique'])
    liste.append(['Comedie Musicale', URL_MAIN + 'tags/Comédie+musicale'])
    liste.append(['Drame', URL_MAIN + 'tags/Drame'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'tags/Epouvante-horreur'])
    liste.append(['Espionnage', URL_MAIN + 'tags/Espionnage'])
    liste.append(['Famille', URL_MAIN + 'tags/Famille'])
    liste.append(['Fantastique', URL_MAIN + 'tags/Fantastique'])
    liste.append(['Guerre', URL_MAIN + 'tags/Guerre'])
    liste.append(['Historique', URL_MAIN + 'tags/Historique'])
    liste.append(['Musical', URL_MAIN + 'tags/Musical'])
    liste.append(['Policier', URL_MAIN + 'tags/Policier'])
    liste.append(['Romance', URL_MAIN + 'tags/Romance'])
    liste.append(['Science Fiction', URL_MAIN + 'tags/Science+fiction'])
    liste.append(['Thriller', URL_MAIN + 'tags/Thriller'])
    liste.append(['Western', URL_MAIN + 'tags/Western'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div style="height:[0-9]{3}px;"><a title="" href="([^"]+)[^>]+?><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<a title="" href[^>]+?>([^<]+?)<'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    # print results

    if results[0]:
        total = len(results[1])
        for entry in results[1]:

            title = str(entry[2])
            url2 = entry[0]
            sFanart = entry[1]
            thumbnail = entry[1]
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', str(url2))
            output_parameter_handler.addParameter('movie_title', str(title))
            output_parameter_handler.addParameter('thumbnail', thumbnail)

            display_title = cUtil().DecoTitle(title)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showLinks',
                display_title,
                'films.png',
                thumbnail,
                sFanart,
                output_parameter_handler)

        next_page = __checkForNextPage(
            html_content)  # cherche la page suivante
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                'next.png',
                output_parameter_handler)

    # tPassage en mode vignette sauf en cas de recherche globale
    if 'index.php?q=' not in url:
        xbmc.executebuiltin('Container.SetViewMode(500)')

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a style="margin-left:2%;" href="(.+?)">'
    results = parser.parse(html_content, pattern)

    if results[0]:
        # print results
        return results[1][0]

    return False


def showLinks():

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    # print url

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Bon ici, grosse bataille, c'est un film ou une serie ?
    # On peut utiliser l'url redirigÃ©e ou cette astuce en test

    if 'infos_film.png' in html_content:
        if 'Ã©pisode par Ã©pisode' in html_content:
            showSeriesLinks(html_content)
        else:
            showMoviesLinks(html_content)
    else:
        showSeriesLinks(html_content)

    return


def showMoviesLinks(html_content):
    xbmc.log('mode film')

    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # print url

    parser = Parser()

    # Recuperation infos
    sNote = ''
    sCom = ''
    sBA = ''

    pattern = 'itemprop="ratingValue">([0-9,]+)<\\/span>.+?synopsis\\.png" *\\/*></div><br /><div align="center">(.+?)<'
    results = parser.parse(html_content, pattern)

    if (results[0]):
        sNote = results[1][0][0]
        sCom = results[1][0][1]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        gui.addText(SITE_IDENTIFIER, 'Note : ' + str(sNote))

    pattern = '(http:\\/\\/www\\.exdown\\.net\\/engine\\/ba\\.php\\?id=[0-9]+)'
    results = parser.parse(html_content, pattern)
    if (results[0]):
        sBA = results[1][0]
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('url', sBA)
        output_parameter_handler.addParameter('movie_title', 'Bande annonce')
        output_parameter_handler.addParameter('thumbnail', str(thumbnail))
        gui.addMovie(
            SITE_IDENTIFIER,
            'ShowBA',
            'Bande annonce',
            '',
            thumbnail,
            '',
            output_parameter_handler)

    # Affichage du menu
    gui.addText(
        SITE_IDENTIFIER,
        '[COLOR olive]QualitÃ©s disponibles pour ce film :[/COLOR]')

    # on recherche d'abord la qualitÃ© courante
    pattern = '<b>(?:<strong>)*QualitÃ© (.+?)<'
    results = parser.parse(html_content, pattern)
    # print results

    qual = ''
    if (results[0]):
        qual = results[1][0]

    title = movie_title + ' - [COLOR skyblue]' + qual + '[/COLOR]'

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', str(movie_title))
    output_parameter_handler.addParameter('thumbnail', str(thumbnail))
    gui.addMovie(
        SITE_IDENTIFIER,
        'showHosters',
        title,
        '',
        thumbnail,
        sCom,
        output_parameter_handler)

    # on regarde si dispo dans d'autres qualitÃ©s
    pattern = '<a title="TÃ©lÃ©chargez.+?en (.+?)" href="(.+?)"><button class="button_subcat"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = movie_title + \
                ' - [COLOR skyblue]' + entry[0] + '[/COLOR]'
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[1])
            output_parameter_handler.addParameter(
                'movie_title', str(movie_title))
            output_parameter_handler.addParameter(
                'thumbnail', str(thumbnail))
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumbnail,
                sCom,
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showSeriesLinks(html_content):
    xbmc.log('mode serie')

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # print url

    parser = Parser()

    # Mise Ã jour du titre
    pattern = '<h1 style="font-family:\'Ubuntu Condensed\',\'Segoe UI\',Verdana,Helvetica,sans-serif;">(?:<span itemprop="name">)*([^<]+?)<'
    results = parser.parse(html_content, pattern)
    if (results[0]):
        movie_title = results[1][0]

    # Utile ou pas ?
    movie_title = movie_title.replace(
        '[Complete]', '').replace(
        '[ComplÃ¨te]', '')

    gui.addText(
        SITE_IDENTIFIER,
        '[COLOR olive]QualitÃ©s disponibles pour cette saison :[/COLOR]')

    # on recherche d'abord la qualitÃ© courante
    pattern = '<span style="color:#[0-9a-z]{6}"><b>(?:<strong>)* *\\[[^\\]]+?\\] ([^<]+?)<'
    results = parser.parse(html_content, pattern)
    # print results

    qual = ''
    if (results[1]):
        qual = results[1][0]

    display_title = cUtil().DecoTitle(movie_title) + \
        ' - [COLOR skyblue]' + qual + '[/COLOR]'

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    output_parameter_handler.addParameter('movie_title', str(movie_title))
    output_parameter_handler.addParameter('thumbnail', str(thumbnail))
    gui.addMovie(
        SITE_IDENTIFIER,
        'showSeriesHosters',
        display_title,
        '',
        thumbnail,
        '',
        output_parameter_handler)

    # on regarde si dispo dans d'autres qualitÃ©s
    sPattern1 = '<a title="TÃ©lÃ©chargez.+?en ([^"]+?)" href="([^"]+?)"><button class="button_subcat"'
    aResult1 = parser.parse(html_content, sPattern1)
    # print aResult1

    if (aResult1[0]):
        total = len(aResult1[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in aResult1[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            display_title = cUtil().DecoTitle(movie_title) + \
                ' - [COLOR skyblue]' + entry[0] + '[/COLOR]'
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[1])
            output_parameter_handler.addParameter(
                'movie_title', str(movie_title))
            output_parameter_handler.addParameter(
                'thumbnail', str(thumbnail))
            gui.addMovie(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                display_title,
                '',
                thumbnail,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    # on regarde si dispo d'autres saisons

    sPattern2 = '<a title="TÃ©lÃ©chargez[^"]+?" href="([^"]+?)"><button class="button_subcat" style="font-size: 12px;height: 26px;width:190px;color:666666;letter-spacing:0.05em">([^<]+?)</button>'
    aResult2 = parser.parse(html_content, sPattern2)
    # print aResult2

    if (aResult2[0]):
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR olive]Saisons aussi disponibles pour cette sÃ©rie :[/COLOR]')

        for entry in aResult2[1]:

            title = '[COLOR skyblue]' + entry[1] + '[/COLOR]'
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', entry[0])
            output_parameter_handler.addParameter(
                'movie_title', str(movie_title))
            output_parameter_handler.addParameter(
                'thumbnail', str(thumbnail))
            gui.addTV(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'series.png',
                thumbnail,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():  # recherche et affiche les hotes
    # print "ZT:showHosters"

    gui = Gui()
    input_parameter_handler = InputParameterHandler()  # apelle l'entree de paramettre
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    xbmc.log(url)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Fonction pour recuperer uniquement les liens
    html_content = Cutlink(html_content)

    # Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in html_content or 'PREMIUM' in html_content:
        html_content = CutNonPremiumlinks(html_content)

    parser = Parser()

    pattern = '<span style="color:#.{6}">([^>]+?)<\\/span>(?:.(?!color))+?<a href="([^<>"]+?)" target="_blank">TÃ©lÃ©charger<\\/a>|>\\[(Liens Premium) \\]<|<span style="color:#FF0000">([^<]+)<'
    results = parser.parse(html_content, pattern)

    # print results

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if entry[2]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', str(url))
                output_parameter_handler.addParameter(
                    'movie_title', str(movie_title))
                output_parameter_handler.addParameter(
                    'thumbnail', str(thumbnail))
                if 'TÃ©lÃ©charger' in entry[2]:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR olive]' + str(entry[2]) + '[/COLOR]')
                else:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR red]' + str(entry[2]) + '[/COLOR]')

            elif entry[3]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', str(url))
                output_parameter_handler.addParameter(
                    'movie_title', str(movie_title))
                output_parameter_handler.addParameter(
                    'thumbnail', str(thumbnail))
                gui.addText(SITE_IDENTIFIER,
                            '[COLOR olive]' + str(entry[3]) + '[/COLOR]')

            else:
                title = '[COLOR skyblue]' + \
                    entry[0] + '[/COLOR] ' + movie_title
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', entry[1])
                output_parameter_handler.addParameter(
                    'movie_title', str(movie_title))
                output_parameter_handler.addParameter(
                    'thumbnail', str(thumbnail))
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    title,
                    '',
                    thumbnail,
                    '',
                    output_parameter_handler)

            cConfig().finishDialog(dialog)

        gui.setEndOfDirectory()


def showSeriesHosters():  # recherche et affiche les hotes
    # print "ZT:showSeriesHosters"
    gui = Gui()
    input_parameter_handler = InputParameterHandler()  # apelle l'entree de paramettre
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Fonction pour recuperer uniquement les liens
    html_content = Cutlink(html_content)

    # Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in html_content or 'PREMIUM' in html_content:
        html_content = CutPremiumlinks(html_content)

    parser = Parser()

    pattern = '<a href="([^"]+?)" target="_blank">([^<]+)<\\/a>|<span style="color:#.{6}">([^<]+)<\\/span>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            # print entry
            if dialog.iscanceled():
                break

            if entry[2]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', str(url))
                output_parameter_handler.addParameter(
                    'movie_title', str(movie_title))
                output_parameter_handler.addParameter(
                    'thumbnail', str(thumbnail))
                if 'TÃ©lÃ©charger' in entry[2]:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR olive]' + str(entry[2]) + '[/COLOR]')
                else:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR red]' + str(entry[2]) + '[/COLOR]')
            else:
                sName = entry[1]
                sName = sName.replace('TÃ©lÃ©charger', '')
                sName = sName.replace('pisodes', 'pisode')

                title = movie_title + ' ' + sName
                display_title = cUtil().DecoTitle(title)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', entry[0])
                output_parameter_handler.addParameter(
                    'movie_title', str(movie_title))
                output_parameter_handler.addParameter(
                    'thumbnail', str(thumbnail))
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    display_title,
                    '',
                    thumbnail,
                    '',
                    output_parameter_handler)

            cConfig().finishDialog(dialog)

        gui.setEndOfDirectory()


def Display_protected_link():

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    parser = Parser()

    # xbmc.log(url)

    # Est ce un lien dl-protect ?
    if 'dl-protect' in url:
        html_content = DecryptDlProtect(url)

        if html_content:
            sPattern_dlprotect = '><a href="(.+?)" target="_blank">'
            aResult_dlprotect = parser.parse(html_content, sPattern_dlprotect)

        else:
            oDialog = cConfig().createDialogOK(
                'Desole, probleme de captcha.\n Veuillez en rentrer un directement sur le site, le temps de reparer')
            aResult_dlprotect = (False, False)

    # Si lien normal
    else:
        if not url.startswith('http'):
            url = 'http://' + url
        aResult_dlprotect = (True, [url])

    # print aResult_dlprotect

    if (aResult_dlprotect[0]):

        episode = 1

        for entry in aResult_dlprotect[1]:
            hoster_url = entry
            # print hoster_url

            title = movie_title
            if len(aResult_dlprotect[1]) > 1:
                title = movie_title + ' episode ' + str(episode)

            episode += 1

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                display_title = cUtil().DecoTitle(title)
                hoster.setDisplayName(display_title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()


def Cutlink(html_content):
    parser = Parser()
    pattern = '<img src="https*:\\/\\/www\\.exdown\\.net\\/prez\\/style\\/v1\\/liens\\.png"(.+?)<div class="divinnews"'
    results = parser.parse(html_content, pattern)
    # print results
    if (results[0]):
        return results[1][0]
    # ok c'est une page battarde, dernier essais
    else:
        pattern = '<div  class="maincont">(.+?)<div class="divinnews"'
        results = parser.parse(html_content, pattern)
        # print results
        if (results[0]):
            return results[1][0]

    return ''


def CutNonPremiumlinks(html_content):
    parser = Parser()
    pattern = '(?i)Liens* Premium(.+?)PubliÃ© le '
    results = parser.parse(html_content, pattern)
    # print results
    if (results[0]):
        return results[1][0]

    # Si ca marche pas on renvois le code complet
    return html_content


def CutPremiumlinks(html_content):
    parser = Parser()

    pattern = '(?i)^(.+?)premium'
    results = parser.parse(html_content, pattern)
    res = ''
    if (results[0]):
        res = results[1][0]

    # si l'ordre a Ã©tÃ© chnage ou si il ya un probleme
    if 'dl-protect.com' not in res:
        pattern = '(?i) par .{1,2}pisode(.+?)$'
        results = parser.parse(html_content, pattern)
        if (results[0]):
            html_content = results[1][0]
    else:
        html_content = res

    # Si ca marche pas on renvois le code complet
    return html_content


def ShowBA():
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'src="(http[^"]+)"'
    results = parser.parse(html_content, pattern)

    if (results[0]):
        request_handler = RequestHandler(results[1][0])
        html_content = request_handler.request()

        pattern = 'player_gen_cmedia=(.*?)&cfilm'
        results = parser.parse(html_content, pattern)

        if (results[0]):
            url2 = 'http://www.allocine.fr/ws/AcVisiondataV4.ashx?media=%s' % (
                results[1][0])
            request_handler = RequestHandler(url2)
            html_content = request_handler.request()

            pattern = 'md_path="([^"]+)"'
            results = parser.parse(html_content, pattern)

            if (results[0]):
                video = results[1][0]
                # print video

                import xbmcplugin
                import sys

                __handle__ = int(sys.argv[1])
                # from resources.lib.handler.pluginHandler import PluginHandler
                # __handle__ = PluginHandler().getPluginHandle()

                liz = xbmcgui.ListItem(
                    'Voir la bande annonce',
                    iconImage="DefaultVideo.png")
                liz.setInfo(type="Video", infoLabels={"Title": 'nom'})
                liz.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(
                    handle=__handle__, url=video, listitem=liz)
                xbmcplugin.endOfDirectory(__handle__)

    return
