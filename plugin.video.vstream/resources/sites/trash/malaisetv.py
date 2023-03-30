# -*- coding: utf-8 -*-
# Venom.kodigoal
# from resources.lib.gui.hoster import HosterGui
# ne fonctionne plus : une reprise depuis twitter vraiment utile ?
import xbmcgui
from resources.lib.player import cPlayer
from resources.lib.gui.guiElement import GuiElement
import xbmc
from resources.lib import util
from resources.lib.parser import cParser
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
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Vidéos (Derniers ajouts)', 'news.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()

    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" class="tweet.+?" title=".+?\\-([^"]+)".+?background-image:url((.+?))">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        dialog = util.createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            util.updateDialog(dialog, total)

            sUrl = 'https://twitter.com' + str(aEntry[0])

            sThumbnail = str(aEntry[2]).replace("'", '').replace('(', '').replace(')', '')

            sTitle = (' %s ') % (str(aEntry[1]))

            # recup id last tweet pour NextPage
            sNext = str(aEntry[0]).replace('/malaisetele/status/', '')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, 'films.png', sThumbnail, '', output_parameter_handler)

        util.finishDialog(dialog)

        sNextPage = __checkForNextPage(sNext)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(url):

    sUrl = 'https://twitter.com/malaisetele/media?include_available_features=1&include_entities=1&lang=fr&max_position=' + \
        url + '&reset_error_state=false'
    return sUrl


def showLinks():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumbnail = input_parameter_handler.getValue('sThumbnail')

    # recup lien mp4 video twitter via twdown.net
    sUrl2 = 'http://twdown.net/download.php'

    oRequestHandler = RequestHandler(sUrl2)
    oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('URL', sUrl)
    oRequestHandler.addParameters('submit', 'Download')
    oRequestHandler.addParameters('submit', '')
    sHtmlContent = oRequestHandler.request()

    # recup du lien mp4
    sPattern = '<td>[0-9]+P</td>.+?<a download href="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        sUrl = str(aResult[1][0])

        # on lance video directement
        oGuiElement = GuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return

    else:
        return

    oGui.setEndOfDirectory()
