# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.multihost import cMultiup
from resources.lib.util import cUtil
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'asia_insane'
SITE_NAME = 'Asia Insane'
SITE_DESC = 'Regarder Films et Séries Asiatique en Streaming gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

DRAMA_DRAMAS = (True, 'load')
DRAMA_MOVIES = (URL_MAIN + 'films-asiatiques-affichage-grid/', 'showMovies')
DRAMA_GENRES = (True, 'showGenres')
DRAMA_ANNEES = (True, 'showYears')
DRAMA_LIST = (True, 'showAlpha')
DRAMA_SERIES = (URL_MAIN + 'liste-des-dramas-vostfr-ddl/', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'wp-admin/admin-ajax.php', 'showMovies')
URL_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_MOVIES[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Dramas (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_ANNEES[1],
        'Dramas (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_LIST[1],
        'Films (Ordre alphabétique)',
        'listes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_SERIES[1],
        'Séries (Dramas)',
        'dramas.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Arts Martiaux', 'arts-martiaux'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Drame', 'drame'], ['Ecole', 'ecole'], ['Expérimental', 'experimental'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Gastronomie', 'gastronomie'],
             ['Guerre', 'guerre'], ['Histoire vraie', 'histoire-vraie'], ['Historique', 'historique'],
             ['Horreur', 'horreur'], ['Maladie', 'maladie'], ['Médecine', 'medecine'], ['Mélodrame', 'melodrame'],
             ['Musical', 'musical'], ['Mystère', 'mystere'], ['Policier', 'policier'], ['Psycologique', 'psycologique'],
             ['Romance', 'romance'], ['Science Fiction', 'science-fiction'], ['Sport', 'sport'],
             ['Suspense', 'suspense'], ['Travail', 'travail'], ['Tranche de vie', 'tranche-de-vie'],
             ['Thriller', 'thriller']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'amy_genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    from itertools import chain
    generator = chain([1966, 1972, 1987, 1988, 1990,
                      1991, 1992], range(1994, 2023))

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(list(generator)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'date/' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    parser = Parser()

    url = URL_MAIN + 'films-asiatiques-vostfr-affichage-alphanumerique/'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+)d{2}.+?.+?field-desc"><p>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            url = entry[1]
            title = entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/dramas/' in url:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showSerieEpisodes',
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

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        if URL_SEARCH[0] in search:
            search = search.replace(URL_SEARCH[0], '')

        util = cUtil()
        search_text = util.CleanName(search)

        pattern = '<a class=\'asp_res_image_url\' href=\'([^>]+)\'.+?url\\("([^"]+)"\\).+?\'>([^.]+)d{2}.+?<span.+?class="asp_res_text">([^<]+)'

        request_handler = RequestHandler(URL_SEARCH[0])
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            'Accept',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request_handler.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        request_handler.addHeaderEntry(
            'Referer', URL_MAIN + "recherche-avancee-asia-insane/")
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')

        request_handler.addParameters('action', "ajaxsearchpro_search")
        request_handler.addParameters('asid', "1")
        request_handler.addParameters('aspp', search)
        request_handler.addParameters('asp_inst_id', "1_1")
        request_handler.addParameters(
            'options',
            "current_page_id=413&qtranslate_lang=0&asp_gen%5B%5D=title&customset%5B%5D=amy_movie&customset%5B%5D=amy_tvshow&termset%5Bamy_director%5D%5B%5D=-1&termset%5Bamy_actor%5D%5B%5D=-1")
        html_content = request_handler.request()

    elif '/amy_genre/' in url or '/date/' in url:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = 'item-poster">.+?src="(http[^"]+).+?href="([^"]+)">([^<]+)d{2}.+?desc"><p>([^<]+)'

    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+)d{2}.+?field-desc"><p>([^<]+).+?(?:|/version/([^/]+).+?)(?:|/date/([^/]+).+?)Genre:'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if search:
                url2 = entry[0]
                thumb = entry[1]
                title = entry[2]
                desc = entry[3]

                display_title = '%s' % title

            elif '/amy_genre/' in url or '/date/' in url:
                thumb = entry[0]
                url2 = entry[1]
                title = entry[2]
                desc = entry[3]

                display_title = '%s' % title

            else:
                thumb = entry[0]
                url2 = entry[1]
                title = entry[2]
                desc = entry[3]
                qual = entry[4].upper()
                year = entry[5]

                display_title = ('%s [%s] (%s)') % (title, qual, year)

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)

            if '/dramas/' in url2:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showSerieEpisodes',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

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
    pattern = '>([^<]+)</a><a class="next page-numbers" href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)/', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSerieEpisodes():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<div class="entry-content e-content" itemprop="description articleBody">'
    end = '<div class="entry-comment">'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)</a>'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            title = movie_title + " E" + entry[1]
            url2 = entry[0]
            if not url2.startswith('http'):
                url2 = URL_MAIN + url2

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('HostUrl', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    url2 = input_parameter_handler.getValue('HostUrl')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    if '/dramas/' in url:
        if 'multiup' in url2:
            results = cMultiup().GetUrls(url2)

            if results:
                for entry in results:
                    hoster_url = entry

                    hoster = HosterGui().checkHoster(hoster_url)
                    if hoster:
                        hoster.setDisplayName(movie_title)
                        hoster.setFileName(movie_title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                               input_parameter_handler=input_parameter_handler)

        else:
            hoster_url = url2

            hoster = HosterGui().checkHoster(url2)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        start = '<pre>'
        end = '</pre>'
        html_content = parser.abParse(html_content, start, end)
        pattern = '>.+?href="([^"]+)">'
        results = parser.parse(html_content, pattern)

        if results[0]:
            for entry in results[1]:

                title = movie_title
                hoster_url = entry

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
