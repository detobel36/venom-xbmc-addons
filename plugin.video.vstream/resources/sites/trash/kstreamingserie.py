# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'kstreamingserie'
SITE_NAME = 'K Streaming Série'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

SERIE_SERIE = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
# SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showList')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Afro', 'afro'], ['Animation', 'animation'], ['Arts Martiaux', 'art-martiaux'],
             ['Aventure', 'aventure'], ['Biographique', 'biographique'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Divers', 'divers'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Epouvante-horreur', 'epouvante-horreur'], ['Erotique', 'erotique'], ['Espionnage', 'espionnage'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Film-musical', 'film-musical'],
             ['Guerre', 'guerre'], ['Historique', 'historique'], ['Horreur', 'horreur'], ['Judiciaire', 'judiciaire'],
             ['Musical', 'musique'], ['Mystère', 'mystere'], ['Non classé', 'non-classe'], ['Policier', 'policier'],
             ['Romance', 'romance'], ['Science fiction', 'science-fiction'], ['Slasher', 'slasher'],
             ['Sport', 'sport-event'], ['Terreur', 'thriller/terreur'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    # html_content = parser.abParse(html_content, '<h1>Listes des séries:</h1>', 'Copyright')

    pattern = 'class="cat-item cat-item-.+?"><a href="([^"]+)">([^<]+)<'
    results = parser.parse(html_content, pattern)

    if results[0]:

        # series = []

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            # series.append((title, url))

        # Trie des séries par ordre alphabétique
        # series = sorted(series, key=lambda serie: serie[0])

        # for title, url:
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    if 'Récemment ajoutées' in html_content:
        start = 'Récemment ajoutées'
        end = 'Séries streaming les plus populaires'
        html_content = parser.abParse(html_content, start, end)

    pattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+).+?(?:|story\'>([^<]+).+?)movie-cast'
    if search:
        pattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+)'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            title = re.sub('\\(\\d{4}\\)', '', entry[1])
            url = entry[2]

            if search:     # Filtre de recherche
                if not util.CheckOccurence(search_text, title):
                    continue

            desc = ''  # absente pour la recherche
            if len(entry) > 3:
                desc = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addTV(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '>([^<]+)</a></div><div class="naviright"><a href="([^"]+?)" >Suivant'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'movie-poster.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):
            url = entry[0]
            thumb = entry[1]
            title = entry[2].replace(' Streaming', '')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    try:
        pattern = 'line-clamp line-hide">(.+?)</div>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].replace('<br />', '').replace('</div>', '')
    except BaseException:
        pass

    # recuperation du hoster de base
    pattern = '<div class="keremiya_part"> <span>([^<]+)<'
    results = parser.parse(html_content, pattern)

    ListeUrl = []
    if results[0]:
        ListeUrl = [(url, results[1][0])]

    # Recuperation des suivants
    pattern = '<a href="([^"]+)" class="post-page-numbers"><span>([^<]+)<'
    results = parser.parse(html_content, pattern)
    ListeUrl = ListeUrl + results[1]

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in ListeUrl:
            url = entry[0]
            title = movie_title + ' Episode' + entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    # si un seul episode
    else:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter(
            'movie_title', movie_title + ' episode 1')
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            movie_title +
            ' episode 1',
            '',
            thumb,
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<h3>.+?(VF|VOSTFR)\\s*<\\/h3>\\s*<p><\\/p>|<iframe.+?src="([^"]+)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            # langue
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            # hote
            else:
                hoster_url = entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
