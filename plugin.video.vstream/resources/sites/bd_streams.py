# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser


SITE_IDENTIFIER = 'bd_streams'
SITE_NAME = 'BD Streams'
SITE_DESC = 'Match de foot en direct'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_LIVE = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')


def load():
    gui = Gui()
    url = URL_MAIN

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "<li class='archivedate'><a href='(.+?)'>"
    results = parser.parse(html_content, pattern)

    if results[0]:
        url = results[1][0]
        pattern = "<h3 class='post-title entry-title'><a href='(.+?)'>(.+?)</a>"
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        results = parser.parse(html_content, pattern)

        if not results[0]:
            gui.addText(SITE_IDENTIFIER)
        else:
            output_parameter_handler = OutputParameterHandler()
            for entry in results[1]:
                url = entry[0]
                title = entry[1]
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('desc', title)
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showLink',
                    title,
                    'genres.png',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'load',
        'Football',
        'genres.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    pattern = 'player = new Clappr\\.Player.+?source: "([^"]+)'
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    results = parser.parse(html_content, pattern)

    if results[0]:
        hoster_url = results[1][0].strip()
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, '')

    gui.setEndOfDirectory()
