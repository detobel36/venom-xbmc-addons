# -*- coding: utf-8 -*-
# Venom.kodigoal
# from resources.lib.gui.hoster import HosterGui
# ne fonctionne plus : une reprise depuis twitter vraiment utile ?
import xbmcgui
from resources.lib.player import Player
from resources.lib.gui.guiElement import GuiElement
import xbmc
from resources.lib import util
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
return False
# player

SITE_IDENTIFIER = 'malaisetv'
SITE_NAME = 'Malaise TV'
SITE_DESC = 'Les séquences les plus embarrassantes de la télévision française'

URL_MAIN = 'https://twitter.com/malaisetele/media?lang=fr'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos (Derniers ajouts)',
        'news.png',
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

    pattern = '<a href="([^"]+)" class="tweet.+?" title=".+?\\-([^"]+)".+?background-image:url((.+?))">'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        dialog = util.createDialog(SITE_NAME)

        for entry in results[1]:
            util.updateDialog(dialog, total)

            url = 'https://twitter.com' + str(entry[0])

            thumbnail = str(
                entry[2]).replace(
                "'",
                '').replace(
                '(',
                '').replace(
                ')',
                '')

            title = (' %s ') % (str(entry[1]))

            # recup id last tweet pour NextPage
            sNext = str(entry[0]).replace('/malaisetele/status/', '')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumbnail)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'films.png',
                thumbnail,
                '',
                output_parameter_handler)

        util.finishDialog(dialog)

        next_page = __checkForNextPage(sNext)
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


def __checkForNextPage(url):

    url = 'https://twitter.com/malaisetele/media?include_available_features=1&include_entities=1&lang=fr&max_position=' + \
        url + '&reset_error_state=false'
    return url


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # recup lien mp4 video twitter via twdown.net
    url2 = 'http://twdown.net/download.php'

    request_handler = RequestHandler(url2)
    request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    request_handler.addParameters('URL', url)
    request_handler.addParameters('submit', 'Download')
    request_handler.addParameters('submit', '')
    html_content = request_handler.request()

    # recup du lien mp4
    pattern = '<td>[0-9]+P</td>.+?<a download href="([^"]+)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        url = str(results[1][0])

        # on lance video directement
        gui_element = GuiElement()
        gui_element.setSiteName(SITE_IDENTIFIER)
        gui_element.setTitle(movie_title)
        gui_element.setMediaUrl(url)
        gui_element.setThumbnail(thumbnail)

        player = Player()
        player.clearPlayList()
        player.addItemToPlaylist(gui_element)
        player.startPlayer()
        return

    else:
        return

    gui.setEndOfDirectory()
