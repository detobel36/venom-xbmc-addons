# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'youtitou_com'
SITE_NAME = 'YouTitou'
SITE_DESC = 'Dessins animés pour les tous petits'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ENFANTS = ('http://', 'load')

AGE_2A4ANS = (
    URL_MAIN +
    'pages/dessins-animes-2-a-4-ans/jolies-histoires-pour-enfants-de-2-a-4-ans.html',
    'showMovies')
VIDEO_EDU2_4 = (
    URL_MAIN +
    'pages/dessins-animes-2-a-4-ans/videos-educatives-pour-enfant-de-2-a-4-ans.html',
    'showEpisode')

# AGE_4A6ANS = (URL_MAIN + 'pages/dessins-animes-4-a-6-ans/dessins-animes-pour-enfants-de-4-a-6-ans.html', 'showMovies')
# VIDEO_EDU4_6 = (URL_MAIN + 'pages/dessins-animes-4-a-6-ans/videos-educatives-pour-enfants-de-4-a-6-ans.html', 'showEdu')
#
# AGE_6A8ANS = (URL_MAIN + 'pages/dessins-animes-6-a-8-ans/dessins-animes-pour-enfants-de-6-a-8-ans.html', 'showMovies')
# VIDEO_EDU6_8 = (URL_MAIN + 'pages/dessins-animes-6-a-8-ans/videos-educatives-pour-enfants-de-6-a-8-ans.html', 'showEdu')

COMPIL = (URL_MAIN + 'videos/compilations-longues/', 'showEpisode')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', AGE_2A4ANS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_2A4ANS[1],
        'Dessins animés 2 à 8 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', VIDEO_EDU2_4[0])
    gui.addDir(
        SITE_IDENTIFIER,
        VIDEO_EDU2_4[1],
        'Vidéos éducative 2 à 8 ans',
        'enfants.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', AGE_4A6ANS[0])
    # gui.addDir(SITE_IDENTIFIER, AGE_4A6ANS[1], 'Dessins animés 4 à 6 ans', 'enfants.png', output_parameter_handler)
    #
    # output_parameter_handler.addParameter('site_url', VIDEO_EDU4_6[0])
    # gui.addDir(SITE_IDENTIFIER, VIDEO_EDU4_6[1], 'Vidéos éducative 4 à 6 ans', 'enfants.png', output_parameter_handler)
    #
    # output_parameter_handler.addParameter('site_url', AGE_6A8ANS[0])
    # gui.addDir(SITE_IDENTIFIER, AGE_6A8ANS[1], 'Dessins animés 6 à 8 ans', 'enfants.png', output_parameter_handler)
    #
    # output_parameter_handler.addParameter('site_url', VIDEO_EDU6_8[0])
    # gui.addDir(SITE_IDENTIFIER, VIDEO_EDU6_8[1], 'Vidéos éducative 6 à 8 ans', 'enfants.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', COMPIL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        COMPIL[1],
        'Compilation dessins animés',
        'enfants.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    sHtml = request_handler.request()
    pattern = 'style="background-image: url\\((.+?)\\);".+?href="([^"]+)"'
    results = parser.parse(sHtml, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            thumb = entry[0]
            url = entry[1]
            title = (url.split('/')[-1]).replace('-', ' ')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showEpisode',
                title,
                'enfants.png',
                thumb,
                title,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    oHosterGui = HosterGui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    sHtml = request_handler.request()
    pattern = '<h5 class=.+?>([^<]+)<.+?data-settings=".+?url":"(.+?)(&|")'
    results = parser.parse(sHtml, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            title = entry[0]
            url = entry[1]
            videoId = url.split('=')[-1]
            thumb = 'https://i.ytimg.com/vi/%s/mqdefault.jpg' % videoId

            hoster = oHosterGui.checkHoster(url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                oHosterGui.showHoster(
                    gui,
                    hoster,
                    url,
                    thumb,
                    input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
