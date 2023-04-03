# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser

SITE_IDENTIFIER = 'reportagestv_com'
SITE_NAME = 'Reportages TV'
SITE_DESC = 'Reportages TV - Replay des reportages télé français en streaming.'

URL_MAIN = 'http://www.reportagestv.com/'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Derniers ajouts',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
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
    if (search_text):
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['TF1', URL_MAIN + 'category/tf1/'])
    liste.append(['TF1 - Appels d\'Urgence',
                  URL_MAIN + 'category/tf1/appels-durgence/'])
    liste.append(['TF1 - Sept à Huit', URL_MAIN + 'category/tf1/sept-a-huit/'])
    liste.append(['France 2', URL_MAIN + 'category/france-2/'])
    liste.append(['France 2 - Apocalypse la 1ère guerre mondiale',
                  URL_MAIN + 'category/france-2/apocalypse-la-1-ere-guerre-mondiale/'])
    liste.append(['France 2 - Envoyé Spécial', URL_MAIN +
                 'category/france-2/envoye-special/'])
    liste.append(['Canal+', URL_MAIN + 'category/canal-plus/'])
    liste.append(['Canal+ - Nouvelle Vie', URL_MAIN +
                 'category/canal-plus/nouvelle-vie/'])
    liste.append(['Canal+ - Spécial Investigation', URL_MAIN +
                 'category/canal-plus/special-investigation/'])
    liste.append(['D8 - Au coeur de l\'Enquête',
                  URL_MAIN + 'category/d8/au-coeur-de-lenquete/'])
    liste.append(['D8 - En quête d\'Actualité',
                  URL_MAIN + 'category/d8/en-quete-dactualite/'])
    liste.append(['D8', URL_MAIN + 'category/d8/'])
    liste.append(['TMC', URL_MAIN + 'category/tmc/'])
    liste.append(['TMC - 90 Enquêtes', URL_MAIN + 'category/tmc/90-enquetes/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'doc.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        '&#039;',
        '\'').replace(
        '&#8217;',
        '\'').replace(
            '&laquo;',
            '<<').replace(
                '&raquo;',
                '>>').replace(
                    '&nbsp;',
        '')

    pattern = 'class="mh-loop-thumb".+?src="([^"]+)" class="attachment.+?href="([^"]+)" rel="bookmark">([^<]+)</a>.+?<div class="mh-excerpt"><p>(.+?)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            thumb = entry[0]
            url = entry[1]
            title = entry[2]
            # .replace('&laquo;', '<<').replace('&raquo;', '>>')
            desc = entry[3]

            output_parameter_handler = OutputParameterHandler()
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

        next_page = __checkForNextPage(html_content)
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


def __checkForNextPage(html_content):
    pattern = '<a class="next page-numbers" href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def __checkForRealUrl(html_content):
    pattern = '<a href="([^"]+)" target="_blank".+?class="btns btn-lancement">Lancer La Video</a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    sRealUrl = __checkForRealUrl(html_content)

    if (sRealUrl):
        request_handler = RequestHandler(sRealUrl)
        html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            hoster_url = str(entry)
            if hoster_url.startswith('//'):
                hoster_url = 'https:' + hoster_url

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
