# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import requests

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, Addon

SITE_IDENTIFIER = 'alldebrid'
SITE_NAME = '[COLOR violet]Alldebrid[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

ITEM_PAR_PAGE = 20


def load():
    gui = Gui()
    addon = Addon()

    URL_HOST = addon.getSetting('urlmain_alldebrid')
    ALL_ALL = (URL_HOST + 'links/', 'showLiens')
    ALL_MAGNETS = (URL_HOST + 'magnets/', 'showMagnets')
    ALL_INFORMATION = ('https://alldebrid.fr', 'showInfo')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ALL_ALL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_ALL[1],
        'Liens',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ALL_MAGNETS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_MAGNETS[1],
        'Magnets',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ALL_INFORMATION[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_INFORMATION[1],
        'Information sur les hébergeurs ',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showLiens(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        '</h1><hr><pre><a href="../">../</a>', '')
    pattern = '<a href="(.+?)">([^<>]+)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        nbItem = 0
        index = 0
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = entry[1]
            url2 = url + entry[0]
            thumb = ''
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)
            progress_.VSclose(progress_)

            if not search:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

        gui.setEndOfDirectory()


def showMagnets(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        '</h1><hr><pre><a href="../">../</a>', '')
    # Pattern servant à retrouver les éléments dans la page
    pattern = '<a href="(.+?)">([^<]+)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        nbItem = 0
        index = 0

        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = entry[0]
            url2 = url + entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if not search:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

            if 'mp4' in url2 or 'avi' in url2 or 'mkv' in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'series.png',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showseriesHoster',
                    title,
                    'movies.png',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showseriesHoster(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    numItem = input_parameter_handler.getValue('numItem')
    numPage = input_parameter_handler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    try:  # Dans le cas ou le mot mp4/avi/mkv n'est pas présent quand c'est un seul fichier
        s = requests.Session()
        resp = s.head(url)
        result = resp.headers['location']
        hoster_url = result
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, movie_title,
                                   input_parameter_handler=input_parameter_handler)
            gui.setEndOfDirectory()
    except BaseException:
        pass

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        '</h1><hr><pre><a href="../">../</a>', '')

    pattern = '<a href="(.+?)">([^<>]+)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        nbItem = 0
        index = 0
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:

            index += 1
            if index <= numItem:
                continue
            numItem += 1
            nbItem += 1

            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            title = entry[1]
            url2 = url + entry[0]
            thumb = ''
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

            if not search:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('site_url', url)
                    output_parameter_handler.addParameter('numItem', numItem)
                    output_parameter_handler.addParameter('numPage', numPage)
                    gui.addNext(
                        SITE_IDENTIFIER,
                        'showLiens',
                        'Page ' + str(numPage),
                        output_parameter_handler)
                    break

            progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    hoster_url = url
    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, movie_title,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showInfo():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<li class="([^"]+)">.+?<i alt=".+?" title="([^"]+)".+?</li>'

    parser = Parser()
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

            sDisponible = entry[0].replace(
                'downloaders_available',
                'Disponible') .replace(
                'downloaders_unavailable',
                'Non Disponible')
            sHebergeur = entry[1]

            display_title = ('%s (%s)') % (sHebergeur, sDisponible)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('movie_title', display_title)

            gui.addText(SITE_IDENTIFIER, display_title)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()
