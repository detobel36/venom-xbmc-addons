# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
# import unicodedata

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

SITE_IDENTIFIER = 'cinemay_com'
SITE_NAME = 'Cinemay'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film-vf-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN + '?keyword=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
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

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films & Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', output_parameter_handler)

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

    liste = [
        [
            'Action', 'action'], [
            'Animation', 'animation'], [
                'Aventure', 'aventure'], [
                    'Comédie', 'comédie'], [
                        'Crime', 'crime'], [
                            'Documentaire', 'documentaire'], [
                                'Drame', 'drame'], [
                                    'Familial', 'familial'], [
                                        'Fantastique', 'fantastique'], [
                                            'Guerre', 'guerre'], [
                                                'Histoire', 'histoire'], [
                                                    'Horreur', 'horreur'], [
                                                        'Enfants', 'kids'], [
                                                            'Musique', 'musique'], [
                                                                'Mystère', 'mystère'], [
                                                                    'Téléfilm', 'telefilm'], [
                                                                        'Romance', 'romance'], [
                                                                            'Science-Fiction', 'science_fiction'], [
                                                                                'Soap', 'soap'], [
                                                                                    'Thriller', 'thriller'], [
                                                                                        'Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genre/' + url + '/')
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

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        util = cUtil()
        url = search.replace(' ', '+')
        search = util.CleanName(search.replace(URL_SEARCH[0], ''))

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a href="([^"]+)" data-url=".+?" class=".+?" title="([^"]+)"><img.+?src="([^"]*)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(results[1])
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            # Nettoyage du titre
            title = entry[1].replace(
                ' en streaming', '').replace(
                '- Saison ', ' S')
            if title.startswith('Film'):
                title = title.replace('Film ', '')

            # filtre search
            if search and total > 5:
                if not util.CheckOccurence(search, title):
                    continue

            url = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN[:-1] + entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url:
                movie_title = re.sub('  S\\d+', '', title)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showSeries',
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

    if not search:
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


def __checkForNextPage(html_content):
    parser = Parser()
    # jusqu'au 5 dernières pages on utilise cette regex
    pattern = 'href="([^"]+)">>><.+?">(\\d+)</a></div>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = URL_MAIN[:-1] + results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    # à partir des 5 dernières pages on change de regex
    pattern = '>([^<]+)</a> <a class="inactive" style="margin-bottom:5px;" href="([^"]+)">>>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSeriesNews():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="titleE".+?<a href="([^"]+)">([^<]+)</a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = re.sub('(\\d+)&#215;(\\d+)', 'S\\g<1>E\\g<2>', entry[1])
            title = title.replace(':', '')
            cCleantitle = re.sub('- Saison \\d+', '', title)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', cCleantitle)
            gui.addTV(SITE_IDENTIFIER, 'showSeries', title,
                      '', '', '', output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<li class="alpha-title"><h3>([^<]+)</h3>|</li><li class="item-title">.+?href="([^"]+)">([^<]+)</a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            else:
                url = entry[1]
                title = entry[2]

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                gui.addTV(SITE_IDENTIFIER, 'showSeries', title,
                          '', '', '', output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # on remplace pour afficher la langue
    html_content = html_content.replace('width: 50%;float: left;', 'VF')
    html_content = html_content.replace('width: 50%;float: right;', 'VOSTFR')

    parser = Parser()

    desc = ''
    try:
        pattern = '<p>Résumé.+?omplet : (.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].split('Résumé')[0]
    except BaseException:
        pass

    pattern = 'class="episodios" style="([^"]+)">|class="numerando" style="margin: 0">([^<]+)<.+?data-target="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        lang = ''
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:  # Affichage de la langue
                lang = entry[0]
            else:
                # on vire le double affichage de la saison
                title = movie_title + ' ' + \
                    entry[1].replace(' x ', '').replace(' ', '')
                display_title = title + ' ' + '(' + lang + ')'
                sData = entry[2]

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('sData', sData)
                output_parameter_handler.addParameter('lang', lang)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sRefUrl = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(sRefUrl)
    html_content = request_handler.request()
    parser = Parser()

    desc = ''
    try:
        pattern = '<p>([^<>"]+)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'var movie.+?id.+?"(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        movie_url = URL_MAIN + 'playery/?id=' + results[1][0]

        request_handler = RequestHandler(movie_url)
        request_handler.addHeaderEntry("User-Agent", UA)
        request_handler.addHeaderEntry("Referer", sRefUrl)
        html_content = request_handler.request()
        head = request_handler.getResponseHeader()
        cookies = getCookie(head)

    pattern = 'hidden" name="videov" id="videov" value="([^"]+).+?</b>([^<]+)<span class="dt_flag">.+?/flags/(.+?)\\.'
    results = parser.parse(html_content, pattern)
    if results[0]:
        oHosterGui = HosterGui()
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = URL_MAIN[:-1] + entry[0]
            host = entry[1].replace(' ', '').replace('.ok.ru', 'ok.ru')
            host = re.sub('\\.\\w+', '', host)
            host = host.capitalize()
            if not oHosterGui.checkHoster(host):
                continue

            lang = entry[2].upper()
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('sRefUrl', sRefUrl)
            output_parameter_handler.addParameter('cookies', cookies)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'id="videov" value="([^"]+)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sData = input_parameter_handler.getValue('sData')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    # Decoupage pour cibler l'épisode
    pattern = sData + '">(.+?)</ul>'
    html_content = parser.parse(html_content, pattern)

    pattern = 'id="videov" value="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def getCookie(head):
    # get cookie
    cookies = ''
    if 'Set-Cookie' in head:
        parser = Parser()
        pattern = '(?:^|,) *([^;,]+?)=([^;,\\/]+?);'
        results = parser.parse(str(head['Set-Cookie']), pattern)
        if results[0]:
            for cook in results[1]:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'
            return cookies


# author @NizarAlaoui
def decode_js(k, i, s, e):
    varinc = 0
    incerement2 = 0
    finalincr = 0
    firsttab = []
    secondtab = []
    while True:
        if varinc < 5:
            secondtab.append(k[varinc])
        elif varinc < len(k):
            firsttab.append(k[varinc])
        varinc = varinc + 1
        if incerement2 < 5:
            secondtab.append(i[incerement2])
        elif incerement2 < len(i):
            firsttab.append(i[incerement2])
        incerement2 = incerement2 + 1
        if finalincr < 5:
            secondtab.append(s[finalincr])
        elif finalincr < len(s):
            firsttab.append(s[finalincr])
        finalincr = finalincr + 1
        if (len(k) + len(i) + len(s) + len(e)
                ) == (len(firsttab) + len(secondtab) + len(e)):
            break

    firststr = ''.join(firsttab)
    secondstr = ''.join(secondtab)
    incerement2 = 0
    finaltab = []
    for varinc in range(0, len(firsttab), 2):
        localvar = -1
        if ord(secondstr[incerement2]) % 2:
            localvar = 1
        finaltab.append(
            chr(int(firststr[varinc: varinc + 2], base=36) - localvar))
        incerement2 = incerement2 + 1
        if incerement2 >= len(secondtab):
            incerement2 = 0

    return ''.join(finaltab)
