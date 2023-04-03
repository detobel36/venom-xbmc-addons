# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False
# clone de voirfilm_org

SITE_IDENTIFIER = 'voirstream_ws'
SITE_NAME = 'VoirStream'
SITE_DESC = 'Films, Séries et mangas en streaming'

URL_MAIN = 'http://www.voirstream.ws/'

URL_SEARCH = (URL_MAIN + 'recherche?story=', 'showMovie')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?story=', 'showMovie')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?story=', 'showMovie')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = (URL_MAIN + 'alphabet', 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (URL_MAIN + 'series/alphabet', 'showAlpha')

ANIM_ANIMS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/dernier/', 'showMovies')
ANIM_LIST = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')


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
    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par ordre alphabétique)',
        'az.png',
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
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
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
    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VIEWS[1],
        'Animés (Les plus vus)',
        'views.png',
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


def AlphaSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    progress_ = Progress().VScreate(SITE_NAME)

    for i in range(0, 27):
        progress_.VSupdate(progress_, 36)

        if (i > 0):
            title = chr(64 + i)
        else:
            title = '09'

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url + title.upper())
        output_parameter_handler.addParameter('movie_title', title)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'serie' in url:
        URL = '%s/series/' % URL_MAIN
    else:
        URL = URL_MAIN

    liste = []
    liste.append(['Aventure', URL + 'aventure_1'])
    liste.append(['Action', URL + 'action_1'])
    liste.append(['Animation', URL + 'animation_1'])
    liste.append(['Arts Martiaux', URL + 'arts-martiaux_1'])
    liste.append(['Biopic', URL + 'biopic_1'])
    # liste.append( ['Classique', URL + 'classique.htm'] )
    liste.append(['Comédie', URL + 'comedie_1'])
    liste.append(['Comédie Dramatique', URL + 'comedie-dramatique_1'])
    # liste.append( ['Comédie Musicale', URL + 'comedie-musicale.htm'] )
    # liste.append( ['Dessin animé', URL + 'dessin-anime.htm'] )
    # liste.append( ['Divers', URL + 'divers.htm'] )
    liste.append(['Documentaire', URL + 'documentaire_1'])
    liste.append(['Drame', URL + 'drame_1'])
    liste.append(['Epouvante Horreur', URL + 'epouvante-horreur_1'])
    liste.append(['Erotique', URL + 'erotique_1'])
    liste.append(['Espionnage', URL + 'espionnage_1'])
    # liste.append( ['Expérimental', URL + 'experimental.htm'] )
    # liste.append( ['Famille', URL + 'famille.htm'] )
    liste.append(['Fantastique', URL + 'fantastique_1'])
    liste.append(['Guerre', URL + 'guerre_1'])
    liste.append(['Historique', URL + 'historique_1'])
    # liste.append( ['Judicaire', URL + 'judiciaire.htm'] )
    liste.append(['Musical', URL + 'musical_1'])
    liste.append(['Policier', URL + 'policier_1'])
    # liste.append( ['Péplum', URL + 'peplum.htm'] )
    liste.append(['Romance', URL + 'romance_1'])
    liste.append(['Science Fiction', URL + 'science-fiction_1'])
    # liste.append( ['Sport event', URL + 'sport-event.htm'] )
    liste.append(['Thriller', URL + 'thriller_1'])
    liste.append(['Western', URL + 'western_1'])
    liste.append(['Non classé', URL + 'non-classe_1'])

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


def showMovieYears():
    gui = Gui()

    for i in reversed(xrange(1913, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    for i in reversed(xrange(1936, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'series' in url:
        code = 'series/alphabet/'
    else:
        code = 'alphabet/'

    liste = []
    liste.append(['0', URL_MAIN + code + '0'])
    liste.append(['1', URL_MAIN + code + '1'])
    liste.append(['2', URL_MAIN + code + '2'])
    liste.append(['3', URL_MAIN + code + '3'])
    liste.append(['4', URL_MAIN + code + '4'])
    liste.append(['5', URL_MAIN + code + '5'])
    liste.append(['6', URL_MAIN + code + '6'])
    liste.append(['7', URL_MAIN + code + '7'])
    liste.append(['8', URL_MAIN + code + '8'])
    liste.append(['9', URL_MAIN + code + '9'])
    liste.append(['A', URL_MAIN + code + 'A'])
    liste.append(['B', URL_MAIN + code + 'B'])
    liste.append(['C', URL_MAIN + code + 'C'])
    liste.append(['D', URL_MAIN + code + 'D'])
    liste.append(['E', URL_MAIN + code + 'E'])
    liste.append(['F', URL_MAIN + code + 'F'])
    liste.append(['G', URL_MAIN + code + 'G'])
    liste.append(['H', URL_MAIN + code + 'H'])
    liste.append(['I', URL_MAIN + code + 'I'])
    liste.append(['J', URL_MAIN + code + 'J'])
    liste.append(['K', URL_MAIN + code + 'K'])
    liste.append(['L', URL_MAIN + code + 'L'])
    liste.append(['M', URL_MAIN + code + 'M'])
    liste.append(['N', URL_MAIN + code + 'N'])
    liste.append(['O', URL_MAIN + code + 'O'])
    liste.append(['P', URL_MAIN + code + 'P'])
    liste.append(['Q', URL_MAIN + code + 'Q'])
    liste.append(['R', URL_MAIN + code + 'R'])
    liste.append(['S', URL_MAIN + code + 'S'])
    liste.append(['T', URL_MAIN + code + 'T'])
    liste.append(['U', URL_MAIN + code + 'U'])
    liste.append(['V', URL_MAIN + code + 'V'])
    liste.append(['W', URL_MAIN + code + 'W'])
    liste.append(['X', URL_MAIN + code + 'X'])
    liste.append(['Y', URL_MAIN + code + 'Y'])
    liste.append(['Z', URL_MAIN + code + 'Z'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="unfilm".+?<a href="(.+?)".+?<img src="(.+?)".+?class="titreunfilm".+?>(.+?)<(?:.+?<span class="qualite (.+?)"|)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # pas les memes url
            url = entry[0].replace(URL_MAIN, '')
            url = URL_MAIN + url
            thumb = entry[1].replace(URL_MAIN, '')
            thumb = URL_MAIN + thumb
            title = entry[2]

            if entry[3]:
                display_title = ('%s (%s)') % (title, entry[3])
            else:
                display_title = title

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('movie_title', title)

            if '/serie/' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '/anime' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
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
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = "<a href=\'([^<]+)\' rel=\'nofollow\'>suiv"
    results = parser.parse(html_content, pattern)

    if results[0]:
        url = results[1][0].replace(URL_MAIN, '')
        url = URL_MAIN + url
        return url
    else:
        return False


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="unepetitesaisons"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:

            url2 = entry[0].replace(URL_MAIN, '')
            url2 = URL_MAIN + url2
            # title = entry[1] + movie_title
            title = entry[1]
            thumb = entry[2].replace(URL_MAIN, '')
            thumb = URL_MAIN + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', thumb, '', output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a class="n_episode2" title="(.+?),.+?href="(.+?)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:

            title = entry[0]
            url2 = entry[1].replace(URL_MAIN, '')
            url2 = URL_MAIN + url2

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="seme.+?data-src="(.+?)".+?style="width:55px;" class="(.+?)".+?<img border="0".+?>(.+?)</span>'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            url = entry[0]
            lang = entry[1].replace('L', '')
            host = entry[2].capitalize()

            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang.upper(), host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
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
    # request_handler.addHeaderEntry('Host', 'www.voirstream.ws')
    request_handler.addHeaderEntry('Referer', URL_MAIN)

    html_content = request_handler.request()
    parser = Parser()

    pattern = 'url=(.+?)"'

    results = parser.parse(html_content, pattern)

    if results[0]:

        hoster_url = str(results[1][0])

        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
