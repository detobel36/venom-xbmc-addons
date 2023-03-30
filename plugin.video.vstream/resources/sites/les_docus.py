# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager

SITE_IDENTIFIER = 'les_docus'
SITE_NAME = 'Les docus'
SITE_DESC = 'Documentaires reportages et vidéos en streaming en francais.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_DOCS = (True, 'load')
DOC_GENRES = (True, 'showGenres')
DOC_NEWS = (URL_MAIN, 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Nouveautés',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['[COLOR teal]ARTS[/COLOR]', 'arts/'])
    liste.append(['Architecture', 'arts/architecture/'])
    liste.append(['Cinéma', 'arts/cinema/'])
    liste.append(['Dessin', 'arts/dessin/'])
    liste.append(['Littérature', 'arts/litterature/'])
    liste.append(['Musique', 'arts/musique/'])
    liste.append(['Peinture', 'arts/peinture/'])
    liste.append(['Sculpture', 'arts/sculpture/'])

    liste.append(['[COLOR teal]HISTOIRE[/COLOR]', 'histoire/'])
    liste.append(['Préhistoire', 'histoire/prehistoire/'])
    liste.append(['Antiquité', 'histoire/antiquite/'])
    liste.append(['Moyen age', 'histoire/moyen-age/'])
    liste.append(['Temps modernes', 'histoire/temps-modernes/'])
    liste.append(['Temps révolutionnaires',
                  'histoire/temps-revolutionnaires/'])
    liste.append(['19 eme siecle', 'histoire/19eme-siecle/'])
    liste.append(['20 eme siecle', 'histoire/20eme-siecle/'])
    liste.append(['Epoque contemporaine', 'histoire/epoque-contemporaine/'])

    liste.append(['[COLOR teal]SOCIETE[/COLOR]', 'societe/'])
    liste.append(['Argent', 'societe/argent/'])
    liste.append(['Monde', 'societe/monde/'])
    liste.append(['Politique', 'societe/politique/'])
    liste.append(['Sexualité', 'societe/sexualite/'])
    liste.append(['Social', 'societe/social/'])

    liste.append(['[COLOR teal]SCIENCES[/COLOR]', 'sciences/'])
    liste.append(['Astronomie', 'sciences/astronomie/'])
    liste.append(['Ecologie', 'sciences/ecologie/'])
    liste.append(['Economie', 'sciences/economie/'])
    liste.append(['Génétique', 'sciences/genetique/'])
    liste.append(['Géographie', 'sciences/geographie/'])
    liste.append(['Géologie', 'sciences/geologie/'])
    liste.append(['Mathématiques', 'sciences/mathematique/'])
    liste.append(['Médecine', 'sciences/medecine/'])
    liste.append(['Physique', 'sciences/physique/'])
    liste.append(['Psychologie', 'sciences/psychologie/'])

    liste.append(['[COLOR teal]TECHNOLOGIE[/COLOR]', 'technologie/'])
    liste.append(['Aviation', 'technologie/aviation/'])
    liste.append(['Informatique', 'technologie/informatique/'])
    liste.append(['Marine', 'technologie/marine/'])
    liste.append(['Téléphonie', 'technologie/telephonie'])

    liste.append(['[COLOR teal]PARANORMAL[/COLOR]', 'paranormal/'])
    liste.append(['Fantames et esprits', 'paranormal/fantomes-et-esprits/'])
    liste.append(['OVNI et extraterrestres',
                  'paranormal/ovnis-et-extraterrestres/'])
    liste.append(['Cryptozoologie', 'paranormal/cryptozoologie/'])
    liste.append(['Mysteres et legendes', 'paranormal/mysteres-et-legendes/'])
    liste.append(['Divers', 'paranormal/divers/'])

    liste.append(['[COLOR teal]AUTRES[/COLOR]', 'autres/'])
    liste.append(['Animaux', 'autres/animaux/'])
    liste.append(['Gastronomie', 'autres/gastronomie/'])
    liste.append(['Jeux video', 'autres/jeux-video/'])
    liste.append(['Loisirs', 'autres/loisirs/'])
    liste.append(['Métiers', 'autres/metiers/'])
    liste.append(['Militaire', 'autres/militaire/'])
    liste.append(['Nature', 'autres/nature/'])
    liste.append(['Policier', 'autres/policier/'])
    liste.append(['Religion', 'autres/religion/'])
    liste.append(['Santé', 'autres/sante/'])
    liste.append(['Sport', 'autres/sport/'])
    liste.append(['Voyage', 'autres/voyage/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch.replace(" ", "+")
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'post-header"><a href="([^"]+)" title="([^"]+).+?src="(https[^"]+)".+?<p *style.+?>([^<]+)</p>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            title = aEntry[1]
            sThumb = aEntry[2]
            desc = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                sThumb,
                desc,
                output_parameter_handler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '>([^<]+)</a> *<a *class="next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent1 = re.sub('<iframe.+?src="(.+?amazon.+?)"', '', sHtmlContent)

    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if not (aResult[0] is True):
        sPattern = 'data-video_id="(.+?)"'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            sHosterUrl = 'https://www.youtube.com/embed/' + aResult[1][0]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)
        else:
            sPattern = '<iframe.+?data-src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)
    else:
        for aEntry in list(set(aResult[1])):
            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
