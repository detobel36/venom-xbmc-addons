# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# le 04/03/20
from resources.lib.comaddon import Progress  # ,VSlog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False


SITE_IDENTIFIER = 'skstream_co'
SITE_NAME = 'Skstream'
SITE_DESC = 'Films & Séries'

URL_MAIN = 'https://www.skstream.to/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = ('http://films', 'showMenuMovies')
MOVIE_GENRES = (URL_MAIN + 'film/', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'film/date-', 'showYears')
MOVIE_PAYS = (URL_MAIN + 'film/', 'showPays')

SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')
SERIE_SERIES = ('http://series', 'showMenuSeries')
SERIE_GENRES = (URL_MAIN + 'serie/', 'showGenres')
SERIE_ANNEES = (URL_MAIN + 'serie/date-', 'showYears')
SERIE_PAYS = (URL_MAIN + 'serie/', 'showPays')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'search?Search=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')


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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films (Menu)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries (Menu)',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

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
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_PAYS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_PAYS[1],
        'Films (Par Pays)',
        'lang.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_PAYS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_PAYS[1],
        'Séries (Par Pays)',
        'lang.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        # + '&_token=5Z4MWpyCQOERtMOYGRVUKwr8LzQvH1ktwVeAVqpi'
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    liste.append(['Action', url + 'genre-Action'])
    liste.append(['Animation', url + 'genre-Animation'])
    liste.append(['Arts Martiaux', url + 'genre-Art_Martiaux'])
    liste.append(['Aventure', url + 'genre-Aventure'])
    liste.append(['Biopic', url + 'genre-Biopic'])
    liste.append(['Comédie', url + 'genre-Comedie'])
    liste.append(['Comédie Dramatique', url + 'genre-Comedie_Dramatique'])
    liste.append(['Documentaire', url + 'genre-Documentaire'])
    liste.append(['Drame', url + 'genre-Drame'])
    liste.append(['Epouvante Horreur', url + 'genre-Epouvante-Horreur'])
    liste.append(['Espionnage', url + 'genre-Espionnage'])
    liste.append(['Famille', url + 'genre-famille'])
    liste.append(['Fantastique', url + 'genre-Fantastique'])
    liste.append(['Guerre', url + 'genre-guerre'])
    liste.append(['Policier', url + 'genre-Policier'])
    liste.append(['Romance', url + 'genre-Romance'])
    liste.append(['Science Fiction', url + 'genre-Science_Fiction'])
    liste.append(['Thriller', url + 'genre-Thriller'])
    liste.append(['Western', url + 'genre-Western'])

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


def showPays():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    if 'film' in url:  # films
        liste.append(['Américain', url + 'nat-u.s.a'])
        liste.append(['Allemand', url + 'nat-allemagne'])
        liste.append(['Belgique', url + 'nat-belgique'])
        liste.append(['Bulgarie', url + 'nat-bulgarie'])
        liste.append(['Britanique', url + 'nat-u.k'])
        liste.append(['Canada', url + 'nat-canada'])
        liste.append(['Chine', url + 'nat-chine'])
        liste.append(['Danemark', url + 'nat-danemark'])
        liste.append(['Français', url + 'nat-france'])
        liste.append(['Japon', url + 'nat-japan'])
        liste.append(['Norvégien', url + 'nat-norvaege'])
        liste.append(['Russie', url + 'nat-russie'])
    else:  # séries
        liste.append(['Américain', url + 'nat-U.S.A'])
        liste.append(['Australie', url + 'nat-Australie'])
        liste.append(['Britanique', url + 'nat-Grande-Bretagne'])
        liste.append(['Espagne', url + 'nat-Espagne'])
        liste.append(['Français', url + 'nat-France'])
        liste.append(['Canada', url + 'nat-Canada'])
        liste.append(['Russie', url + 'nat-Russie'])
        liste.append(['Korean', url + 'nat-KOREAN'])
        liste.append(['Allemagne', url + 'nat-Allemagne'])
        liste.append(['Japon', url + 'nat-Japon'])
        liste.append(['Turquie', url + 'nat-Turquie'])
        # liste.append( ['Brésil', url + 'nat-Br%C3%83%C2%A9sil'] )
        liste.append(['Belgique', url + 'nat-belgique'])
        liste.append(['Danemark', url + 'nat-danemark'])
        liste.append(['Norvégien', url + 'nat-norvaege'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'lang.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    for i in reversed(range(1980, 2020)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', ('%s%s') % (url, Year))
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        url = search.replace(' ', '+')
        pattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)"[^<>]+ alt="([^"]+)"'

    elif '/film' in url:
        pattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)" title="([^"]+)".+?class="qual".+?<span>([^<]+)<.+?class="lang_img_poster".+?alt="([^"]+)"'
    else:
        pattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)" title="([^"]+)"'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            url = entry[0]
            thumb = URL_MAIN[:-1] + entry[1]
            title = entry[2]
            qual = ''
            lang = ''
            if len(entry) > 3:
                qual = entry[3]
                lang = entry[4].upper()

            display_title = ('%s [%s] (%s)') % (title, qual, lang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url:
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
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Suivant >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'href="([^"]+)" rel="next" aria-label="Next »"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    try:
        pattern = '<div class="details text-muted">([^<]+)<'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].replace(
                'Ã©',
                'é').replace(
                'Â',
                'â').replace(
                'Ã',
                'à')
    except BaseException:
        pass

    pattern = 'w3l-movie-gride-agile">.+?<img src="([^"]+)".+?<h6><a href="([^"]+)">([^<]+)<'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:

            thumb = URL_MAIN[:-1] + entry[0]
            url = entry[1]
            title = movie_title + ' ' + entry[2]

            output_parameter_handler = OutputParameterHandler()
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

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'href="([^"]+)" class="epi_box".+?<span>([^<]+)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            title = entry[1].replace('Ep', 'episode') + movie_title

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    if url.endswith(' '):
        url = url[:-1]

    request = RequestHandler(url)
    html_content = request.request()

    parser = Parser()
    pattern = "href='([^']+)' (?:|target=\"_blank\" )class=\"a_server"

    results = parser.parse(html_content, pattern)

    if results[0]:
        for hoster_url in results[1]:
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
