# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

SITE_IDENTIFIER = '_33seriestreaming'
SITE_NAME = '33 Séries'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = "https://33seriestreaming.rip/"
# Clone -> https://33streaming.co/

# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = (URL_MAIN, 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'series-streaming', 'showMovies')
SERIE_GENRES = (URL_MAIN, 'showSeriesGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = (
    URL_MAIN +
    'index.php?do=search&subaction=search&story=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&titleonly=3&catlist[]=1&story=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'index.php?do=search&subaction=search&titleonly=3&catlist[]=2&story=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films & Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher Films',
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

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()

    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Rechercher Séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url += search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showAlpha():
    import string

    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    listalpha = [str(i) for i in range(1, 10)]
    listalpha.extend(list(string.ascii_lowercase))
    for alpha in listalpha:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'catalog/' + alpha + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            str(alpha).upper() +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [
        'Action',
        'Aventure',
        'Animation',
        'Comédie',
        'Crime',
        'Documentaire',
        'Drame',
        'Familial',
        'Fantastique',
        'Histoire',
        'Horreur',
        'Musique',
        'Thriller',
        'Téléfilm',
        'Western']

    output_parameter_handler = OutputParameterHandler()
    for igenre in liste:
        title = igenre.capitalize()
        url = URL_MAIN + 'film-streaming/genre/' + igenre + '.html'
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesGenres():
    gui = Gui()

    liste = [
        'Action & Adventure',
        'Animation',
        'Comédie',
        'Crime',
        'Documentaire',
        'Drame',
        'Familial',
        'Kids',
        'Musique',
        'Mystère',
        'Reality',
        'Romance',
        'Science-Fiction & Fantastique',
        'Soap',
        'Thriller',
        'Western']

    output_parameter_handler = OutputParameterHandler()
    for igenre in liste:
        title = igenre.capitalize()
        url = URL_MAIN + 'series-streaming/genre/' + igenre + '.html'
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    import datetime
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'film-streaming/annee/' + year + '.html')
        output_parameter_handler.addParameter('year', year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    import datetime
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1930, int(datetime.datetime.now().year) + 1)):
        year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series-streaming/annee/' + year + '.html')
        output_parameter_handler.addParameter('year', year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    year = input_parameter_handler.getValue('year')

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+').replace('%20 ', '+')
    pattern = 'class=".+?grid-item.+?href="([^"]+).+?-src="([^"]+).+?alt="([^"]+)'
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

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
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            title = entry[2]

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue  # Filtre de recherche

            display_title = title
            desc = ''
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if '/series' in url2 or '/series' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
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

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page is not False:
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
    pattern = 'id="pagination".+?\\d+</span>.<a href="([^"]+)">(\\d+)(</a> *</div|<.+?(\\d+)</a> *</div)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page_data = results[1][0]
        next_page = next_page_data[0]
        number_next = next_page_data[1]
        number_max = next_page_data[3]
        if not number_max:
            number_max = number_next
        paging = number_next + '/' + number_max
        return next_page, paging
    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'grid-item" href="([^"]+).+?-src="([^"]*).+?(saison \\d+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:
            url2 = entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + entry[1]
            saison = entry[2]

            title = movie_title + ' ' + saison

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('year', year)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    start = 'class="pmovie__subtitle"'
    end = 'pmovie__bottom-btns'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+).+?(épisode \\d+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:
            url2 = entry[0]
            sEp = entry[1]

            title = movie_title + ' ' + sEp

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')
    is_serie = '-episode.html' in url

    parser = Parser()
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Accept', '*/*')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    html_content = request_handler.request()

    if is_serie:  # episode d'une série
        pattern = 'class="ser_pl" data-name="([^"]+)" data-hash="([^"]+)" data-episode="(\\d+)".+?">([^<]+).+?img src="([^\\.]+)'
    else:        # Film
        pattern = 'class="nopl" data-id="(\\d+)" data-name="([^"]+)" data-hash="([^"]+).+?">([^<]+).+?img src="([^\\.]+)'

    results = parser.parse(html_content, pattern)

    if results[0]:
        url2 = URL_MAIN + 'engine/ajax/controller.php'
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if is_serie:  # episode d'une série
                data_name = entry[0]
                dataHash = entry[1]
                dataEp = entry[2]
                pdata = 'mod=xfield_ajaxs&name=' + data_name + \
                    '&hash=' + dataHash + '&episode=' + dataEp
                # pdata = {'mod': 'xfield_ajax', 'hash': dataHash, 'episode': dataEp, 'name' :  data_name}
                pdata = str(pdata)
            else:
                data_id = entry[0]
                data_name = entry[1]
                dataHash = entry[2]
                # pdata = 'mod=xfield_ajax&hash=' + dataHash + '&id=' + data_id + '&name=' + data_name
                pdata = {
                    'mod': 'xfield_ajax',
                    'hash': dataHash,
                    'id': data_id,
                    'name': data_name}
                pdata = str(pdata)

            host = entry[3].strip()
            if not HosterGui().checkHoster(host):
                continue

            lang = entry[4]
            if lang:
                lang = lang.split('/')[-1:][0]

            display_title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang.upper(), host.capitalize())

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'hostersLink',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def hostersLink(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    # Fonctionnement différent entre film et serie
    if 'episode' in pdata:
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(pdata)
    else:
        # import string
        # boundary = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        # request.addHeaderEntry('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundary%s' % boundary)
        import ast
        pdata = ast.literal_eval(pdata)
        request.addMultipartFiled(pdata)

    html_content = request.request()

    pattern = '(http[^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            hoster_url = entry
            if 'userload' in hoster_url:
                hoster_url = hoster_url + "|Referer=" + URL_MAIN

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
