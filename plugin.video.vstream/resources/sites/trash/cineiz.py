# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, VSlog
import re
return false

SITE_IDENTIFIER = 'cineiz'
SITE_NAME = 'Cineiz'
SITE_DESC = 'Films, Séries et mangas en streaming'

URL_MAIN = 'https://ww3.cineiz.io/'

URL_SEARCH = ('', 'showMovieSearch')
URL_SEARCH_MOVIES = ('', 'showMovieSearch')
URL_SEARCH_SERIES = ('', 'showMovieSearch')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_GENRES = ('http://film', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = ('http://film', 'showList')

SERIE_NEWS = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_GENRES = ('http://serie', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (True, 'showList')

ANIM_NEWS = (URL_MAIN + 'animes/dernier/', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.htm', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')
ANIM_GENRES = (True, 'showGenres')
ANIM_ANNEES = (True, 'showAnimesYears')
ANIM_ENFANTS = (URL_MAIN + 'animes', 'showMovies')
ANIM_LIST = (True, 'showAnimesList')


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
    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Liste)',
        'az.png',
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
        'Séries (Par Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'az.png',
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
    output_parameter_handler.addParameter('site_url', ANIM_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VIEWS[1],
        'Animés (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Liste)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovieSearch(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'film' in url:
        code = 'films-genre-'
    elif 'serie' in url:
        code = 'series-tv/genre-'
    else:
        code = 'animes-du-genre-'

    liste = []
    liste.append(['Action', URL_MAIN + code + 'action.htm'])
    liste.append(['Animation', URL_MAIN + code + 'animation.htm'])
    liste.append(['Arts Martiaux', URL_MAIN + code + 'arts-martiaux.htm'])
    liste.append(['Aventure', URL_MAIN + code + 'aventure.htm'])
    liste.append(['Biopic', URL_MAIN + code + 'biopic.htm'])
    liste.append(['Classique', URL_MAIN + code + 'classique.htm'])
    liste.append(['Comédie', URL_MAIN + code + 'comedie.htm'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                 code + 'comedie-dramatique.htm'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 code + 'comedie-musicale.htm'])
    liste.append(['Dessin animé', URL_MAIN + code + 'dessin-anime.htm'])
    liste.append(['Divers', URL_MAIN + code + 'divers.htm'])
    liste.append(['Documentaire', URL_MAIN + code + 'documentaire.htm'])
    liste.append(['Drame', URL_MAIN + code + 'drame.htm'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 code + 'epouvante-horreur.htm'])
    liste.append(['Erotique', URL_MAIN + code + 'erotique.htm'])
    liste.append(['Espionnage', URL_MAIN + code + 'espionnage.htm'])
    liste.append(['Expérimental', URL_MAIN + code + 'experimental.htm'])
    liste.append(['Famille', URL_MAIN + code + 'famille.htm'])
    liste.append(['Fantastique', URL_MAIN + code + 'fantastique.htm'])
    liste.append(['Guerre', URL_MAIN + code + 'guerre.htm'])
    liste.append(['Historique', URL_MAIN + code + 'historique.htm'])
    liste.append(['Judicaire', URL_MAIN + code + 'judiciaire.htm'])
    liste.append(['Musical', URL_MAIN + code + 'musical.htm'])
    liste.append(['Policier', URL_MAIN + code + 'policier.htm'])
    liste.append(['Péplum', URL_MAIN + code + 'peplum.htm'])
    liste.append(['Romance', URL_MAIN + code + 'romance.htm'])
    liste.append(['Science Fiction', URL_MAIN + code + 'science-fiction.htm'])
    liste.append(['Sport event', URL_MAIN + code + 'sport-event.htm'])
    liste.append(['Thriller', URL_MAIN + code + 'thriller.htm'])
    liste.append(['Western', URL_MAIN + code + 'western.htm'])
    liste.append(['Non classé', URL_MAIN + code + 'non-classe.htm'])

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


def showList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'film' in url:
        code = 'films-commence-par-'
    else:
        code = 'series-tv/commence-par-'

    liste = []
    liste.append(['0', URL_MAIN + code + '0.htm'])
    liste.append(['1', URL_MAIN + code + '1.htm'])
    liste.append(['2', URL_MAIN + code + '2.htm'])
    liste.append(['3', URL_MAIN + code + '3.htm'])
    liste.append(['4', URL_MAIN + code + '4.htm'])
    liste.append(['5', URL_MAIN + code + '5.htm'])
    liste.append(['6', URL_MAIN + code + '6.htm'])
    liste.append(['7', URL_MAIN + code + '7.htm'])
    liste.append(['8', URL_MAIN + code + '8.htm'])
    liste.append(['9', URL_MAIN + code + '9.htm'])
    liste.append(['A', URL_MAIN + code + 'A.htm'])
    liste.append(['B', URL_MAIN + code + 'b.htm'])
    liste.append(['C', URL_MAIN + code + 'C.htm'])
    liste.append(['D', URL_MAIN + code + 'D.htm'])
    liste.append(['E', URL_MAIN + code + 'E.htm'])
    liste.append(['F', URL_MAIN + code + 'F.htm'])
    liste.append(['G', URL_MAIN + code + 'G.htm'])
    liste.append(['H', URL_MAIN + code + 'H.htm'])
    liste.append(['I', URL_MAIN + code + 'I.htm'])
    liste.append(['J', URL_MAIN + code + 'J.htm'])
    liste.append(['K', URL_MAIN + code + 'K.htm'])
    liste.append(['L', URL_MAIN + code + 'L.htm'])
    liste.append(['M', URL_MAIN + code + 'M.htm'])
    liste.append(['N', URL_MAIN + code + 'N.htm'])
    liste.append(['O', URL_MAIN + code + 'O.htm'])
    liste.append(['P', URL_MAIN + code + 'P.htm'])
    liste.append(['Q', URL_MAIN + code + 'Q.htm'])
    liste.append(['R', URL_MAIN + code + 'R.htm'])
    liste.append(['S', URL_MAIN + code + 'S.htm'])
    liste.append(['T', URL_MAIN + code + 'T.htm'])
    liste.append(['U', URL_MAIN + code + 'U.htm'])
    liste.append(['V', URL_MAIN + code + 'V.htm'])
    liste.append(['W', URL_MAIN + code + 'W.htm'])
    liste.append(['X', URL_MAIN + code + 'X.htm'])
    liste.append(['Y', URL_MAIN + code + 'Y.htm'])
    liste.append(['Z', URL_MAIN + code + 'Z.htm'])

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


def showAnimesList():
    gui = Gui()

    liste = []
    liste.append(['09', URL_MAIN + 'animes/alphabet/09'])
    liste.append(['A', URL_MAIN + 'animes/alphabet/A'])
    liste.append(['B', URL_MAIN + 'animes/alphabet/B'])
    liste.append(['C', URL_MAIN + 'animes/alphabet/C'])
    liste.append(['D', URL_MAIN + 'animes/alphabet/D'])
    liste.append(['E', URL_MAIN + 'animes/alphabet/E'])
    liste.append(['F', URL_MAIN + 'animes/alphabet/F'])
    liste.append(['G', URL_MAIN + 'animes/alphabet/G'])
    liste.append(['H', URL_MAIN + 'animes/alphabet/H'])
    liste.append(['I', URL_MAIN + 'animes/alphabet/I'])
    liste.append(['J', URL_MAIN + 'animes/alphabet/J'])
    liste.append(['K', URL_MAIN + 'animes/alphabet/K'])
    liste.append(['L', URL_MAIN + 'animes/alphabet/L'])
    liste.append(['M', URL_MAIN + 'animes/alphabet/M'])
    liste.append(['N', URL_MAIN + 'animes/alphabet/N'])
    liste.append(['O', URL_MAIN + 'animes/alphabet/O'])
    liste.append(['P', URL_MAIN + 'animes/alphabet/P'])
    liste.append(['Q', URL_MAIN + 'animes/alphabet/Q'])
    liste.append(['R', URL_MAIN + 'animes/alphabet/R'])
    liste.append(['S', URL_MAIN + 'animes/alphabet/S'])
    liste.append(['T', URL_MAIN + 'animes/alphabet/T'])
    liste.append(['U', URL_MAIN + 'animes/alphabet/U'])
    liste.append(['V', URL_MAIN + 'animes/alphabet/V'])
    liste.append(['W', URL_MAIN + 'animes/alphabet/W'])
    liste.append(['X', URL_MAIN + 'animes/alphabet/X'])
    liste.append(['Y', URL_MAIN + 'animes/alphabet/Y'])
    liste.append(['Z', URL_MAIN + 'animes/alphabet/Z'])

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


def showMovieYears():
    gui = Gui()

    for i in reversed(xrange(1921, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films-annee-' + Year + '.htm')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    for i in reversed(xrange(1961, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series-tv/annee-' + Year + '.htm')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieSearch(search=''):
    gui = Gui()

    if not search:
        return
    else:
        url = URL_MAIN + 'recherche'

    request_handler = RequestHandler(url)
    # request_handler.addHeaderEntry('Referer', 'https://www.cineiz.io/recherche')
    request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    request_handler.addParameters('action', 'recherche')
    request_handler.addParameters('story', search)

    html_content = request_handler.request()

    pattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="linkfilm">(.+?)</span>'

    parser = Parser()
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

            url2 = str(entry[0])
            thumb = URL_MAIN + str(entry[1])
            title = str(entry[2])
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/series-tv/' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif '/anime/' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
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

    pattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="xquality">(.+?)</span>.+?<span class="xlangue">(.+?)</span>.+?<span class="linkfilm">(.+?)</span>'

    parser = Parser()
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

            url2 = str(entry[0])
            thumb = str(entry[1])
            if 'films' in url:
                qual = str(entry[2])
                lang = str(entry[3])
            else:
                qual = ''
                lang = ''
            title = str(entry[4])
            desc = ''

            display_title = ('%s (%s) (%s)') % (title, qual, lang.upper())

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif '/anime' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    desc,
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
    pattern = '<a href=\'([^<]+)\' rel=\'nofollow\'>suiv »'
    results = parser.parse(html_content, pattern)

    if results[0]:
        if results[1][0].startswith('/'):
            return URL_MAIN[:-1] + results[1][0]
        else:
            return results[1][0]

    return False


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="unepetitesaisons"><a href="(.+?)" title=.+?<div class="etlelien">(.+?)</div>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url2 = str(entry[0])
            # title = str(entry[1]) + movie_title
            title = ('%s %s') % (entry[1], movie_title)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', thumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a class="n_episode2".+?href="([^"]+)"><span class="head">(.+?)</span><span class="body">(.+?)</span>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = str(entry[1]) + str(entry[2]) + ' ' + movie_title
            url2 = str(entry[0])
            if url2.startswith('/'):
                url2 = URL_MAIN[:-1] + url2

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

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    import threading
    threads = []

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    parser = Parser()
    request_handler = RequestHandler(url)
    # faut post
    request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    request_handler.addParameters('levideo', '123456')
    html_content = request_handler.request().replace(
        '<span class="telecharger_sur_uptobox"></span>', '')

    desc = ''
    try:
        pattern = '<p>Synopsis.+?</strong> :(.+?)<\\/p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = '<div class="num_link">Lien:.+?<span class="(.+?)".+?span style="width:55px;" class="(.+?)">.+?<input name="levideo" value="(.+?)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            host = str(entry[0]).capitalize()
            if 'Nowvideo' in host:
                continue
            lang = str(entry[1])
            sPost = str(entry[2])
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('sPost', sPost)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            # gui.addMovie(SITE_IDENTIFIER, 'showHosters', title, '', thumb, desc, output_parameter_handler)
            # dispo a la version 0.6.2
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace(
        'https://streamcomplet.cineiz.io', URL_MAIN)
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    sPost = input_parameter_handler.getValue('sPost')

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addParameters('levideo', sPost)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '</script></div></div><iframe src="(.+?)"'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            url = URL_MAIN + entry
            request_handler = RequestHandler(url)
            html_content = request_handler.request()
            hoster_url = request_handler.getRealUrl()

            if 'facebook.com' in hoster_url:
                continue

            if 'vimple.org' in hoster_url:
                request_handler = RequestHandler(hoster_url)
                request_handler.addHeaderEntry('Referer', url)
                sHtmlContent2 = request_handler.request()
                try:
                    hoster_url = re.search(
                        'url=([^"]+)"', sHtmlContent2, re.DOTALL).group(1)
                except BaseException:
                    hoster_url = str(request_handler.getRealUrl())

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
