# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import SiteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# On garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

# Source compatible avec les clones : toblek, bofiaz, nimvon
# mais pas compatible avec les clones, qui ont une redirection directe :
# sajbo, trozam, radego
URL_HOST = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_HOST = dans sites.json
URL_MAIN = 'URL_MAIN'

# pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'c/poblom/29/0', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

DOC_NEWS = (URL_MAIN + 'c/poblom/26/0', 'showMovies')
SHOW_SHOWS = (URL_MAIN + 'c/poblom/3/0', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_MISC = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


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

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films (A l\'affiche)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SHOW_SHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SHOW_SHOWS[1],
        'Spectacles',
        'doc.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showMovies(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['A l\'affiche', 29])
    liste.append(['Action', 1])
    liste.append(['Animation', 2])
    liste.append(['Aventure', 4])
    # liste.append(['Biographie', 5])  # aucun
    liste.append(['Comédie', 6])
    liste.append(['Documentaires', 26])
    liste.append(['Drame', 7])
    liste.append(['Epouvante Horreur', 9])
    liste.append(['Fantastique', 8])
    liste.append(['Policier', 10])
    liste.append(['Science Fiction', 11])
    liste.append(['Spectacle', 3])
    liste.append(['Thriller', 12])

    output_parameter_handler = OutputParameterHandler()
    for title, iGenre in liste:
        url = URL_MAIN + 'c/poblom/%d/0' % iGenre
        output_parameter_handler.addParameter('site_url', url)
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

    # L'url change tres souvent donc faut la retrouver
    request_handler = RequestHandler(URL_HOST)
    data = request_handler.request()
    # Compatible avec plusieurs clones
    results = parser.parse(data, '<a.+?href="(/*[0-9a-zA-Z]+)"')
    if not results[0]:
        return   # Si ca ne marche pas, pas la peine de continuer

    # memorisation pour la suite
    sMainUrl = URL_HOST + results[1][0] + '/'
    # correction de l'url

    # En cas de recherche direct OU lors de la navigation dans les differentes
    # pages de résultats d'une recherche
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_MISC[0], '')
        search_text = util.CleanName(search_text)

        search = search[:20]  # limite de caractere sinon bug de la recherche
        request_handler = RequestHandler(sMainUrl + 'home/poblom/')
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addParameters('searchword', search.replace(' ', '+'))
        sABPattern = '<div class="column24"'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        if url == URL_MAIN:  # page d'accueil
            sABPattern = '<div class="column1"'
        else:
            sABPattern = '<div class="column20"'
        url = url.replace(URL_MAIN, sMainUrl)
        request_handler = RequestHandler(url)

    html_content = request_handler.request()
    html_content = parser.abParse(
        html_content, sABPattern, '<div class="column2"')
    pattern = '<span style="list-style-type:none;".+? href="\\/[0-9a-zA-Z]+\\/([^"]+)">(.+?)\\((.+?)\\).+?>(<i>(.+?)</i>|)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            title = entry[1].strip()
            year = entry[2]
            qual = entry[4]
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            display_title = ("%s (%s) [%s]") % (title, year, qual)
            output_parameter_handler.addParameter('site_url', sMainUrl + url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('sMainUrl', sMainUrl)
            output_parameter_handler.addParameter('year', year)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                'films.png',
                '',
                '',
                output_parameter_handler)

    if not search:
        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter(
                'site_url', URL_HOST[:-1] + next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Suivant',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = 'a><a style="position: relative;top: 3px;margin-right: 6px;" href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    # sMainUrl = input_parameter_handler.getValue('sMainUrl')
    # year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = html_content.replace('<br/>', '')  # traitement de desc

    # Recuperation info film, com et image
    thumb = ''
    desc = ''
    pattern = '<img src="([^"]+).+?<p.+?>([^<]+)</p>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        thumb = results[1][0][0]
        desc = results[1][0][1]

    pattern = '<iframe.+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        sLink = results[1][0]
        if sLink.startswith('/'):
            sLink = URL_HOST[:-1] + sLink

        request_handler = RequestHandler(sLink)
        data = request_handler.request()

        pattern = 'file: "(.+?)"'
        results = parser.parse(data, pattern)

        if results[0]:
            for entry in results[1]:

                sLink2 = entry
                hoster = HosterGui().checkHoster(sLink2)

                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, sLink2, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
