# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil, QuotePlus, Noredirection
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimité'
SITE_DESC = 'Films, Séries HD en streaming'

URL_MAIN = 'https://www.official-film-illimite.to/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/streaming-720p-streaming-1080p/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
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
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_HD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_HD[1],
        'Films (HD)',
        'hd.png',
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
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Ultra-HD', URL_MAIN + 'ultra-hd/'])
    liste.append(['720p/1080p', URL_MAIN +
                  'films/streaming-720p-streaming-1080p/'])
    liste.append(['Action/Aventure', URL_MAIN + 'films/action-aventure/'])
    liste.append(['Animation', URL_MAIN + 'films/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'films/arts-martiaux/'])
    liste.append(['Biographie', URL_MAIN + 'films/biographique/'])
    liste.append(['Comédie', URL_MAIN + 'films/comedie/'])
    liste.append(['Crime/Gangster', URL_MAIN + 'films/crimegangster/'])
    liste.append(['Documentaire', URL_MAIN + 'films/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'films/drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'films/epouvante-horreur/'])
    liste.append(['Etranger', URL_MAIN + 'films/etranger/'])
    liste.append(['Famille', URL_MAIN + 'films/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'films/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'films/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'films/histoire/'])
    liste.append(['Musique/Danse', URL_MAIN + 'films/musiquedanse/'])
    liste.append(['Mystère', URL_MAIN + 'films/mystere/'])
    liste.append(['Policier', URL_MAIN + 'films/policier/'])
    liste.append(['Romance', URL_MAIN + 'films/romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'films/science-fiction/'])
    liste.append(['Spectacle (FR)', URL_MAIN +
                 'spectacle/francais-spectacle/'])
    liste.append(['Spectacle (VOSTFR)', URL_MAIN +
                 'spectacle/vostfr-spectacle/'])
    liste.append(['Sport', URL_MAIN + 'films/sport/'])
    liste.append(['Suspense/Thriller', URL_MAIN + 'films/thrillersuspense/'])
    liste.append(['Téléfilm', URL_MAIN + 'films/telefilm/'])
    liste.append(['VOSTFR', URL_MAIN + 'films/vostfr/'])
    liste.append(['Western', URL_MAIN + 'films/western/'])

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


def showYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    start = '<div class="filter-content-slider">'
    end = '<div class="filter-slide filter-slide-down">'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = html_content.replace('en illimité', 'en illimite')

    parser = Parser()
    pattern = 'class="item">.+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?ttx">([^<]+).+?(?:|class="year">([^<]+).+?)class="calidad2'
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

            title = entry[2].replace(
                ' Streaming Ultra-HD',
                '').replace(
                ' Streaming Full-HD',
                '') .replace(
                ' en Streaming HD',
                '').replace(
                ' Streaming HD',
                '') .replace(
                    ' streaming',
                    '').replace(
                        'HD',
                '')

            url2 = entry[0]
            thumb = re.sub('/w\\d+', '/w342', entry[1])
            if thumb.startswith('//'):
                thumb = 'http:' + thumb
            desc = entry[3].split('en illimite')[1].replace('&#160;', '')
            year = entry[4]

            # Si recherche et trop de resultat, on filtre
            if search and total > 2:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            sPattern1 = '.+?saison [0-9]+'
            aResult1 = parser.parse(title, sPattern1)

            if aResult1[0]:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                str(number) +
                ' >>>[/COLOR]',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = "<a class=\'current.+?href=\'([^']+)\'"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Vire les bandes annonces
    html_content = html_content.replace('src="//www.youtube.com/', '')

    pattern = '<iframe.+?src="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            hoster_url = str(entry)
            if '//goo.gl' in hoster_url:
                try:
                    url8 = hoster_url.replace('https', 'http')

                    opener = Noredirection()
                    opener.addheaders.append(('User-Agent', UA))
                    opener.addheaders.append(('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    hoster_url = HttpReponse.headers['Location']
                    hoster_url = hoster_url.replace('https', 'http')
                except BaseException:
                    pass

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = html_content.replace(
        '<iframe width="420" height="315" src="https://www.youtube.com/', '')
    pattern = '<iframe.+?src="(http.+?)".+?>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        i = 1
        for entry in results[1]:

            url = entry
            title = '%s episode %s' % (
                movie_title.replace(' - Saison', ' Saison'), i)

            i = i + 1

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowSpecialHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowSpecialHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    data = re.sub('(.+?f=)', '', url)
    data = data.replace('&c=', '')
    pdata = 'data=' + QuotePlus(data)

    if 'fr-land.me' in url:
        request = RequestHandler('http://fr-land.me/Htplugins/Loader.php')
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        # request.addHeaderEntry('Host', 'official-film-illimite.to')
        request.addHeaderEntry('Referer', url)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(pdata)

        html_content = request.request()
        html_content = html_content.replace('\\', '')

        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        pattern = '\\[(.+?)\\]'

        parser = Parser()
        results = parser.parse(html_content, pattern)
        if results[0]:
            listurl = results[1][0].replace('"', '').split(',http')
            listqual = results[1][1].replace('"', '').split(',')

            tab = zip(listurl, listqual)

            for url, qual in tab:
                hoster_url = url
                if not hoster_url.startswith('http'):
                    hoster_url = 'http' + hoster_url

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    display_title = '[' + qual + '] ' + movie_title
                    hoster.setDisplayName(display_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    else:

        hoster = HosterGui().checkHoster(url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, url, thumb)

    gui.setEndOfDirectory()
