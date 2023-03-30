# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'filmspourenfants'
SITE_NAME = 'Films pour Enfants'
SITE_DESC = 'Des films poétiques pour sensibiliser les enfants aux pratiques artistiques. Des films éducatifs pour accompagner les programmes scolaires'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ENFANTS = (True, 'load')

AGE_3ANS = (URL_MAIN + 'films-enfants-3-ans.html', 'showMovies')
AGE_5ANS = (URL_MAIN + 'films-enfants-5-ans.html', 'showMovies')
AGE_7ANS = (URL_MAIN + 'films-enfants-7-ans.html', 'showMovies')
AGE_9ANS = (URL_MAIN + 'films-enfants-9-ans.html', 'showMovies')
AGE_11ANSETPLUS = (URL_MAIN + 'films-enfants-11-ans.html', 'showMovies')
ALL_ALL = (URL_MAIN + 'tous-les-films-pour-enfants.html', 'showMovies')
# BY_THEMES = (URL_MAIN + 'films-programmes-thematiques.html', 'showThemes')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', AGE_3ANS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_3ANS[1],
        'A partir de 3 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', AGE_5ANS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_5ANS[1],
        'A partir de  5 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', AGE_7ANS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_7ANS[1],
        'A partir de 7 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', AGE_9ANS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_9ANS[1],
        'A partir de 9 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', AGE_11ANSETPLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        AGE_11ANSETPLUS[1],
        'A partir de 11 ans',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ALL_ALL[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ALL_ALL[1],
        'Tous les ages',
        'enfants.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('siteUrl', BY_THEMES[0])
    # gui.addDir(SITE_IDENTIFIER, BY_THEMES[1], 'Films pour Enfants (Thèmes)', 'genres.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showThemes():
    gui = Gui()
    oParser = Parser()
    oRequestHandler = RequestHandler('siteUrl')
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(
        sHtmlContent,
        '<lien1>Portail pour les familles</lien1><br>',
        '<lien1><i class=icon-circle>')

    sPattern = '<a href=([^>]+)><lien3><i class=icon-circle></i>([^<]+)</lien3></a><br>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    oParser = Parser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class=portfolio-image>.+?src="*([^ ]+\\.jpg).+?synopsis>([^<]+)<.+?href="(https[^"]+)".+?<h4>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = URL_MAIN + aEntry[0]
            desc = aEntry[1]
            sUrl = aEntry[2]
            title = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'enfants.png',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    sHosterUrl = sUrl
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
