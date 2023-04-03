# -*- coding: utf-8 -*-
# Venom.

# desactiver le 18/09
import xbmc
import re
from resources.lib.config import cConfig
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'filmstreamingv2'
SITE_NAME = '[COLOR violet]Films Streaming V2[/COLOR]'
SITE_DESC = 'Film streaming (Version 2) - Premier site de streaming film VF en HD'

URL_MAIN = 'http://www.filmstreamingv2.com/'

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_SAGAS = (URL_MAIN + 'les-sagas-de-films.html', 'showMoviesHtml')
MOVIE_MARVEL = (
    URL_MAIN +
    'telecharger-les-films-de-lunivers-marvel.html',
    'showMoviesHtml')
MOVIE_JAMESB = (
    URL_MAIN +
    'integrale-james-bond-films-collection-complete.html',
    'showMoviesHtml')
MOVIE_TOP = (URL_MAIN + 'top-250-imdb.html', 'showMoviesHtml')
MOVIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (
    URL_MAIN +
    'les-films-disney-en-streaming.html',
    'showMoviesHtml')

URL_SEARCH = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_SAGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_SAGAS[1],
        'Films (Sagas)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MARVEL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MARVEL[1],
        'Films (Marvel)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_JAMESB[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_JAMESB[1],
        'Films (Saga James Bond)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Top 250 IMDB)',
        'star.png',
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
    output_parameter_handler.addParameter('site_url', ANIM_ENFANTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ENFANTS[1],
        'Les Walt Disney',
        'enfants.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'xfsearch/action'])
    liste.append(['Animation', URL_MAIN + 'xfsearch/animation'])
    liste.append(['Aventure', URL_MAIN + 'xfsearch/aventure'])
    liste.append(['Biopic', URL_MAIN + 'xfsearch/biopic'])
    liste.append(['Comédie', URL_MAIN + 'xfsearch/Comedie'])
    liste.append(['Documentaire', URL_MAIN + 'xfsearch/documentaire'])
    liste.append(['Drame', URL_MAIN + 'xfsearch/drame'])
    liste.append(['Famille', URL_MAIN + 'xfsearch/famille'])
    liste.append(['Fantastique', URL_MAIN + 'xfsearch/fantastique'])
    liste.append(['Historique', URL_MAIN + 'xfsearch/historique'])
    liste.append(['Horreur', URL_MAIN + 'xfsearch/horreur'])
    liste.append(['Musical', URL_MAIN + 'xfsearch/musical'])
    liste.append(['Policier', URL_MAIN + 'xfsearch/policier'])
    liste.append(['Romance', URL_MAIN + 'xfsearch/romance'])
    liste.append(['Science fiction', URL_MAIN + 'xfsearch/fiction'])
    liste.append(['Thriller', URL_MAIN + 'xfsearch/thriller'])
    liste.append(['Western', URL_MAIN + 'xfsearch/western'])

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
        if URL_SEARCH[0] in search:
            url = search
        else:
            url = URL_SEARCH[0] + search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="hover-special"></div><img src="([^"]+)" alt="([^"]+)"><div class="hd720p">([^<]+)</div>.+?<div class="pipay1"><a href="([^"]+)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            qual = ' (' + entry[2] + ')'
            title = str(entry[1]).replace('streaming', '')
            url = entry[3]
            thumb = entry[0]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            display_title = title + qual

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<span class="pnext"><a href="([^"]+)">Suivant'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        url = results[1][0]
        # correction d'1 bug de leur site
        url = url.replace('xfsearch//page/2/', 'xfsearch/page/2/page/2/')
        return url

    return False


def showMoviesHtml():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<li class="tops-item"><a href="([^<]+)">.+?<img src="([^<]+)" alt="(.+?)"/>'

    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            title = str(entry[2]).replace('streaming', '')
            url2 = entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/les-sagas-' in url:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showSagas',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showSagas():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<span style="color:.+?">([^<]+)</span>.+?<a href="([^<]+)">.+?<img src="(.+?)".+?>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            title = entry[0]
            url = entry[1]
            thumb = entry[2]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    # recherche des liens de streaming
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<iframe.+?src="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]' +
            'Liens Streaming :' +
            '[/COLOR]')
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            # print entry
            if dialog.iscanceled():
                break

            hoster_url = str(entry)
            hoster_url = hoster_url.replace('//ok.ru', 'https://ok.ru')
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, '')

    # recherche des liens de telechargement
    url = url + '#example'
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<div id="download-quality-([^"]+)">.+?<span class="download-filesize">([^<]+)</span>|<a class="download-torrent leta-[^"]+" target="_blank" href="([^"]+)" rel="external noopener noreferrer">([^>]+)</a>'

    results = parser.parse(html_content, pattern)
    print results
    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]' +
            'Liens Download :' +
            '[/COLOR]')
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            # print entry
            if dialog.iscanceled():
                break

            if entry[0]:  # affichage format et taille du fichier
                gui.addText(SITE_IDENTIFIER, '[COLOR olive]' + str(
                    entry[0]) + ' (' + str(entry[1]) + ')' + '[/COLOR]')

            else:
                display_title = entry[3]

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', entry[2])
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def Display_protected_link():
    # xbmc.log('Display_protected_link')
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()

    # Est ce un lien ushort-links?
    if 'ushort-links' in url:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        if html_content:
            pattern = '<a id="download" href="(.+?)"'
            results = parser.parse(html_content, pattern)
            hoster_url = results[1][0]
            # print hoster_url

            title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                display_title = cUtil().DecoTitle(title)
                hoster.setDisplayName(display_title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        else:
            oDialog = cConfig().createDialogOK('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    gui.setEndOfDirectory()
