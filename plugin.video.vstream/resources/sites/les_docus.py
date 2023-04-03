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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Nouveautés',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search.replace(" ", "+")
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'post-header"><a href="([^"]+)" title="([^"]+).+?src="(https[^"]+)".+?<p *style.+?>([^<]+)</p>'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            title = entry[1]
            thumb = entry[2]
            desc = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                thumb,
                desc,
                output_parameter_handler)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>([^<]+)</a> *<a *class="next page-numbers" href="([^"]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    sHtmlContent1 = re.sub('<iframe.+?src="(.+?amazon.+?)"', '', html_content)

    pattern = '<iframe.+?src="(.+?)"'
    results = parser.parse(sHtmlContent1, pattern)

    if not (results[0] is True):
        pattern = 'data-video_id="(.+?)"'
        results = parser.parse(sHtmlContent1, pattern)
        if results[0]:
            hoster_url = 'https://www.youtube.com/embed/' + results[1][0]
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)
        else:
            pattern = '<iframe.+?data-src="([^"]+)'
            results = parser.parse(html_content, pattern)
            if results[0]:
                hoster_url = results[1][0]
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)
    else:
        for entry in list(set(results[1])):
            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
