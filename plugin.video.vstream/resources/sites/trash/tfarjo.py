# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.comaddon import Progress, Addon
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False
sColor = Addon().getSetting("deco_color")

SITE_IDENTIFIER = 'tfarjo'
SITE_NAME = 'Tfarjo'
SITE_DESC = 'Films & Séries en streaming VO | VF | VOSTFR'

# URL_MAIN = 'https://www5.tfarjo.ws/'
# URL_MAIN = 'https://www.filmz.cc/'
URL_MAIN = 'https://www.tfarjo.cc/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series', 'showSeries')
# SERIE_VFS = (URL_MAIN + 'series/vf', 'showSeries')
# SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr', 'showSeries')  # pas fiable
# et pareil que dernier ajouts

URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'


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
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', output_parameter_handler)

    # output_parameter_handler = OutputParameterHandler()
    # output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        text = search_text
        showMovies(text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'films/genre/action'])
    liste.append(['Animation', URL_MAIN + 'films/genre/animation'])
    liste.append(['Arts Martiaux', URL_MAIN + 'films/genre/arts-Martiaux'])
    liste.append(['Aventure', URL_MAIN + 'films/genre/aventure'])
    liste.append(['Biopic', URL_MAIN + 'films/genre/biopic'])
    liste.append(['Comédie', URL_MAIN + 'films/genre/comédie'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                 'films/genre/comédie-dramatique'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 'films/genre/comédie-musicale'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/crime'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/dance'])
    liste.append(['Documentaire', URL_MAIN + 'films/genre/documentaire'])
    liste.append(['Drame', URL_MAIN + 'films/genre/drame'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 'films/genre/epouvante-horreur'])
    liste.append(['Erotique', URL_MAIN + 'films/genre/erotique'])
    liste.append(['Espionnage', URL_MAIN + 'films/genre/espionnage'])
    liste.append(['Famille', URL_MAIN + 'films/genre/famille'])
    liste.append(['Fantastique', URL_MAIN + 'films/genre/fantastique'])
    liste.append(['Guerre', URL_MAIN + 'films/genre/guerre'])
    liste.append(['Historique', URL_MAIN + 'films/genre/historique'])
    liste.append(['Musical', URL_MAIN + 'films/genre/musical'])
    liste.append(['Spectacle', URL_MAIN + 'films/genre/mystere'])
    liste.append(['Policier', URL_MAIN + 'films/genre/policier'])
    liste.append(['Romance', URL_MAIN + 'films/genre/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'films/genre/science-fiction'])
    liste.append(['Divers', URL_MAIN + 'films/genre/sport'])
    liste.append(['Thriller', URL_MAIN + 'films/genre/thriller'])
    liste.append(['Western', URL_MAIN + 'films/genre/western'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def getcode(html_content):
    sPattern1 = '<input type="hidden" name="csrf_test_name" id="csrf_test_name" value="([^"]+)">'
    sCode = re.search(sPattern1, html_content)
    if sCode:
        return sCode.group(1)
    else:
        return ''


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        request = RequestHandler(URL_MAIN)
        html_content = request.request()
        cook = request.GetCookies()

        sCode = getcode(html_content)

        text = search
        request = RequestHandler(URL_MAIN + 'search')
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry('Cookie', cook)
        request.addParametersLine(
            'search=' + text + '&csrf_test_name=' + sCode)

        html_content = request.request()
        html_content = re.sub(
            '<h2></h2>',
            '<span class="Langue..."></span><span class="qalite">Qualité...</span>',
            html_content)  # recherche pas de qualité,langue

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        # parfois pas de qualité,langue,liens >> BA
        html_content = re.sub(
            '<span class="bientot"></span>',
            '<span class="nothing"></span><span class="qalite">nothing</span>',
            html_content)

    pattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">.+?<span class="([^"]+)"></span><span class="qalite">([^<]+)</span>'

    results = parser.parse(html_content, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # pas de qualité,langue,liens >> BA
            if entry[3] == 'nothing' and entry[4] == 'nothing':
                continue

            url = entry[0]
            thumb = entry[1]
            title = entry[2]
            lang = entry[3]
            qual = entry[4]

            display_title = ('%s [%s] (%s)') % (title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            if 'serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<span class="active">\\d+</span>.+?<a href="([^"]+)" data-ci'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSeries():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            thumb = entry[1]
            title = entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # html_content = parser.abParse(html_content, 'begin seasons', 'end seasons')
    # pas encore d'épisode >> timer avant sortie
    html_content = re.sub('<kbd><span', '<kbd>nothing</span>', html_content)

    pattern = '<h3 class="panel-title"><a href=".+?">(saison *\\d+)<\\/a>|<div class="panel-body">.+?href="([^"]+)">.+?<\\/span>([^"]+)</a>'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')

            else:
                url = entry[1]

                display_title = "%s %s" % (
                    movie_title, entry[2].replace(',', ''))

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request = RequestHandler(url)
    html_content = request.request()
    cook = request.GetCookies()
    sCode = getcode(html_content)

    sPattern2 = "<button *class=\"players(?:(vf|vo|vostfr))\" *onclick=\"getIframe\\('([^']+)'\\).+?<\\/span> *([^<]+)<"
    results = parser.parse(html_content, sPattern2)

    if results[0]:
        for entry in results[1]:

            lang = entry[0].upper()
            host = entry[2].capitalize()
            sCode2 = entry[1]

            display_title = (
                '%s (%s) [COLOR %s]%s[/COLOR]') % (movie_title, lang, sColor, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sCode', sCode)
            output_parameter_handler.addParameter('sCode2', sCode2)
            output_parameter_handler.addParameter('sCook', cook)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
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
    sCode = input_parameter_handler.getValue('sCode')
    sCode2 = input_parameter_handler.getValue('sCode2')
    sCook = input_parameter_handler.getValue('sCook')

    parser = Parser()

    # VSlog(URL_MAIN + 'getlinke')
    # VSlog(sCook)

    if '/serie' in url:
        request = RequestHandler(URL_MAIN + 'getlinke')
        request.addParametersLine(
            'csrf_test_name=' + sCode + '&episode=' + sCode2)
    else:
        request = RequestHandler(URL_MAIN + 'getlink')
        request.addParametersLine(
            'csrf_test_name=' + sCode + '&movie=' + sCode2)

    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addHeaderEntry('Referer', url)
    request.addHeaderEntry('Cookie', sCook)

    html_content = request.request()
    html_content = html_content.replace('\\', '')

    pattern = '<iframe.+?src="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0]:

        hoster_url = results[1][0]

        hoster = HosterGui().checkHoster(hoster_url)

        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
