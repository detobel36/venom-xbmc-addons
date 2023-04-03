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

SITE_IDENTIFIER = 'stream_complet'
SITE_NAME = 'Stream Complet'
SITE_DESC = 'Voir les meilleurs films en version française'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?keymovies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'series-streaming/?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SERIES_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        'Recherche Films ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        'Recherche Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIES_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIES_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_SERIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_MOVIES[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


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

    # ajout: documentaire, fantastique, western
    listegenre = [
        'action',
        'animation',
        'aventure',
        'comedie',
        'documentaire',
        'drame',
        'fantastique',
        'guerre',
        'historique',
        'horreur',
        'musical',
        'policier',
        'romance',
        'science-fiction',
        'thriller',
        'western']

    url1g = URL_MAIN + 'film/'

    output_parameter_handler = OutputParameterHandler()
    for igenre in listegenre:
        url = url1g + igenre + '/'
        title = igenre.capitalize()
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

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<div class="moviefilm">.+?href="([^"]+).+? src="([^"]+).+?alt="([^"]+)'
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

            url2 = entry[0]
            thumb = entry[1]
            title = entry[2]
            title = title.replace('streaming VF', '')

            if URL_SEARCH_MOVIES[0] in url:
                if '/serie' in url2:
                    continue

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if 'serie' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page, sPagination = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                sPagination,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'class="nextpostslink.+?href="([^"]+).+?class="last.+?href=.*?page.([0-9]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][1]
        next_page = results[1][0][0]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        sPagination = number_next + '/' + number_max
        return next_page, sPagination
    return False, False


def showSaison():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    parser = Parser()
    pattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = parser.parse(html_content, pattern)
    if aResultDesc[0] is True:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                       aResultDesc[1][0])

    pattern = '(\\d+)<\\/a><\\/h3>'
    results = parser.parse(html_content, pattern)
    sSaison = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:
            sNumSaison = entry[0]
            sSaison = 'Saison ' + entry[0]
            sUrlSaison = url + "?sNumSaison=" + sNumSaison

            title = movie_title + sSaison
            display_title = title + '' + sSaison
            output_parameter_handler.addParameter('site_url', sUrlSaison)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showSXE',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSXE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    url, sNumSaison = url.split('?sNumSaison=')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    start = 'id="saison-' + sNumSaison
    end = '<div id="alt">'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">épisode (\\d+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            Ep = entry[1]
            Saison = 'Saison ' + sNumSaison
            title = movie_title + Saison + ' Episode ' + Ep

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    parser = Parser()
    pattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = parser.parse(html_content, pattern)
    if aResultDesc[0] is True:
        desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ',
                                                       aResultDesc[1][0])

    pattern = 'class="player link" data-player="([^"]+).+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            lang = entry[1]
            sHostname = entry[2].capitalize()
            sDisplayName = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (title, lang, sHostname)
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('siteReferer', url)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', sHostname)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayName,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    pattern = '(?:class="players">|</a>)\\s*<a href="([^"]+).+?<li class="player".+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    # avec href="([^"]+)"; '"' à garder  pour éviter oublie avec test reg101
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            lang = entry[1]

            sHostname = entry[2].lower()
            sHostname = sHostname.capitalize()
            display_title = '%s (%s) [COLOR coral]%s[/COLOR]' % (title,
                                                                 lang, sHostname)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('siteReferer', url)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', sHostname)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersDL',
                display_title,
                thumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oHosterGui = HosterGui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    siteReferer = input_parameter_handler.getValue('siteReferer')

    if 'sstatic' in url:
        sUrl1 = url + '/ajax'
        request_handler = RequestHandler(sUrl1)
        request_handler.addHeaderEntry('Referer', url)
        request_handler.addHeaderEntry(
            'Accept', 'application/json, text/javascript, */*; q=0.01')
        request_handler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        html_content = request_handler.request()

        parser = Parser()
        pattern = 'url":"([^"]+)'  # tjrs doodstream
        results = parser.parse(html_content, pattern)

        if results[0]:
            hoster_url = results[1][0]
            hoster = oHosterGui.checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                oHosterGui.showHoster(
                    gui,
                    hoster,
                    hoster_url,
                    thumb,
                    input_parameter_handler=input_parameter_handler)
    else:
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('Referer', siteReferer)
        html_content = request_handler.request()

        parser = Parser()
        pattern = 'url=([^"]+)'
        results = parser.parse(html_content, pattern)

        if results[0]:
            for entry in results[1]:
                hoster_url = entry
                hoster = oHosterGui.checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    oHosterGui.showHoster(
                        gui,
                        hoster,
                        hoster_url,
                        thumb,
                        input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHostersDL(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    lang = input_parameter_handler.getValue('lang')

    sDisplayName = ('%s (%s)') % (movie_title, lang)

    if 'shortn.co' in url:
        bvalid, shost = Hoster_shortn(url)
        if bvalid:
            hoster_url = shost
            hoster = HosterGui().checkHoster(hoster_url)

            if hoster:
                hoster.setDisplayName(sDisplayName)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        hoster_url = url
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(sDisplayName)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def Hoster_shortn(url):
    shost = ''
    url = url.replace('%22', '')
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request()
    cookies = request_handler.GetCookies()
    pattern = "type.*?name=.*?value='([^']+)"
    results = re.findall(pattern, html_content)
    if results:
        token = results[0]
        data = '_token=' + token
        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Referer', url)
        request_handler.addHeaderEntry(
            'Accept',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            'Content-Type', "application/x-www-form-urlencoded")
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addParametersLine(data)
        html_content = request_handler.request()

        pattern = 'href="([^"]+).+?target="_blank'
        results = re.findall(pattern, html_content)
        if results:
            shost = results[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
