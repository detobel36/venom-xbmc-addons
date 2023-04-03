# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# tester le 30/10 ne fonctionne pas / SSL error
import urllib2
import urllib
import re
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'filmsvostfr_biz'
SITE_NAME = 'Filmsvostfr'
SITE_DESC = 'Films/Séries/Animés'

URL_MAIN = 'https://ww1.filmsvostfr.io/'

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMoviesYears')

SERIE_NEWS = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_GENRES = ('http://seriegenre', 'showGenres')
SERIE_ANNEES = (True, 'showSeriesYears')

ANIM_NEWS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_GENRES = ('http://animgenre', 'showGenres')
ANIM_ANNEES = (True, 'showAnimsYears')

URL_SEARCH = (URL_MAIN + 'recherche.htm?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche.htm?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche.htm?q=', 'showMovies')


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
    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
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


def showMovieGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + '1_1_action.html'])
    liste.append(['Animation', URL_MAIN + '2_1_animation.html'])
    liste.append(['Arts Martiaux', URL_MAIN + '24_1_arts-martiaux.html'])
    liste.append(['Aventure', URL_MAIN + '3_1_aventure.html'])
    liste.append(['Biopic', URL_MAIN + '13_1_biopic.html'])
    liste.append(['Bollywood', URL_MAIN + '26_1_bollywood.html'])
    liste.append(['Comédie', URL_MAIN + '4_1_comedie.html'])
    liste.append(['Comédie dramatique', URL_MAIN +
                 '22_1_comedie-dramatique.html'])
    liste.append(['Comédie Musicale', URL_MAIN + '17_1_comedie_musicale.html'])
    liste.append(['Concert', URL_MAIN + '28_1_concert.html'])
    liste.append(['Divers', URL_MAIN + '14_1_divers.html'])
    liste.append(['Documentaire', URL_MAIN + '15_1_documentaire.html'])
    liste.append(['Drame', URL_MAIN + '5_1_drame.html'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 '6_1_epouvante-horreur.html'])
    liste.append(['Erotique', URL_MAIN + '25_1_erotique.html'])
    liste.append(['Espionnage', URL_MAIN + '12_1_espionnage.html'])
    liste.append(['Famille', URL_MAIN + '18_1_famille.html'])
    liste.append(['Fantastique', URL_MAIN + '7_1_fantastique.html'])
    liste.append(['Guerre', URL_MAIN + '21_1_guerre.html'])
    liste.append(['Historique', URL_MAIN + '23_1_historique.html'])
    liste.append(['Musical', URL_MAIN + '16_1_musical.html'])
    liste.append(['Non Classé', URL_MAIN + '26_1_bollywood.html'])
    liste.append(['Opéra', URL_MAIN + '27_1_opera.html'])
    liste.append(['Péplum', URL_MAIN + '20_1_peplum.html'])
    liste.append(['Policier', URL_MAIN + '8_1_policier.html'])
    liste.append(['Romance', URL_MAIN + '9_1_romance.html'])
    liste.append(['Science Fiction', URL_MAIN + '10_1_science-fiction.html'])
    liste.append(['Thriller', URL_MAIN + '11_1_thriller.html'])
    liste.append(['Western', URL_MAIN + '19_1_western.html'])

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


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if 'serie' in url:
        code = 'series/'
    else:
        code = 'animes/'

    liste = []
    liste.append(['Action', URL_MAIN + code + 'action.html'])
    liste.append(['Animation', URL_MAIN + code + 'animation.html'])
    liste.append(['Arts Martiaux', URL_MAIN + code + 'arts-martiaux.html'])
    liste.append(['Aventure', URL_MAIN + code + 'aventure.html'])
    liste.append(['Biopic', URL_MAIN + code + 'biopic.html'])
    liste.append(['Comédie', URL_MAIN + code + 'comedie.html'])
    liste.append(['Comédie dramatique', URL_MAIN +
                 code + 'comedie-dramatique.html'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 code + 'comedie_musicale.html'])
    liste.append(['Divers', URL_MAIN + code + 'divers.html'])
    liste.append(['Documentaire', URL_MAIN + code + 'documentaire.html'])
    liste.append(['Drame', URL_MAIN + code + 'drame.html'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 code + 'epouvante-horreur.html'])
    liste.append(['Espionnage', URL_MAIN + code + 'espionnage.html'])
    liste.append(['Famille', URL_MAIN + code + 'famille.html'])
    liste.append(['Fantastique', URL_MAIN + code + 'fantastique.html'])
    liste.append(['Guerre', URL_MAIN + code + 'guerre.html'])
    liste.append(['Historique', URL_MAIN + code + 'historique.html'])
    liste.append(['Musical', URL_MAIN + code + 'musical.html'])
    liste.append(['Policier', URL_MAIN + code + 'policier.html'])
    liste.append(['Romance', URL_MAIN + code + 'romance.html'])
    liste.append(['Science Fiction', URL_MAIN + code + 'science-fiction.html'])
    liste.append(['Thriller', URL_MAIN + code + 'thriller.html'])
    liste.append(['Western', URL_MAIN + code + 'western.html'])

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


def showMoviesYears():
    gui = Gui()

    for i in reversed(xrange(1921, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films-produit-en-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesYears():
    gui = Gui()

    for i in reversed(xrange(1940, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'series-produit-en-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimsYears():
    gui = Gui()

    for i in reversed(xrange(1969, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'animes-produit-en-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
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

    pattern = 'format-video hentry item-video">.+?<img src="(.+?)".+?<a href="([^<>"]+?)".+?<b>(.+?)<\\/b>'

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

            title = entry[2].decode("utf8")
            title = cUtil().unescape(title)
            try:
                title = title.encode("utf-8")
            except BaseException:
                pass

            url = entry[1]
            thumb = entry[0]
            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '/serie' in url:
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', thumb, '', output_parameter_handler)
            elif '/anime' in url:
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', thumb, '', output_parameter_handler)
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
    pattern = "<div class=\"wp-pagenavi\">.+?</span><a href='([^<>']+?)'"
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        if results[1][0].startswith('http'):
            return results[1][0]
        else:
            return URL_MAIN + results[1][0]

    return False


def showEpisode():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # resume
    desc = ''
    if '/anime' in url:
        pattern = '<span>Synopsis.+?<\\/span><span>([^<]+)<\\/span><\\/p>'
    else:
        pattern = '<span>Résumé.+?<\\/span><span>([^<]+)<\\/span><\\/p>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = results[1][0]

    pattern = '<span>(.aison *\\d+.+?)<\\/span>'
    pattern = pattern + '|href="([^"]+)">(épisode.+?)<\\/a>'
    results = parser.parse(html_content, pattern)
    SaisonNum = '0'

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                SaisonNum = parser.getNumberFromString(entry[0])
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]Saison ' +
                    SaisonNum +
                    '[/COLOR]')
            else:
                if 'aison' in movie_title:
                    title = movie_title + entry[2]
                else:
                    title = movie_title + ' S' + SaisonNum + entry[2]

                url = URL_MAIN[:-1] + entry[1]

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addTV(SITE_IDENTIFIER, 'showLinks', title, '',
                          thumb, desc, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        'HD streaming', '').replace(
        'télécharger sur ', '')

    pattern = '<img src="(\\/images\\/video-coming-soon\\.jpg)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR crimson]Vidéo bientôt disponible[/COLOR]')

    # resume
    desc = ''
    pattern = '<span class="synopsis">([^<]+)<\\/span>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        desc = results[1][0]

    pattern = '<a href="([^"]+)" class="sinactive ilink.+?" rel="nofollow" title="([^"]+)">.+?<span class="quality" title="(.+?)">.+?<span class="langue" title="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            url = entry[0].replace(
                'p=watchers',
                'p=30').replace(
                'p=16do',
                'p=16').replace(
                'p=the23eo',
                'p=23').replace(
                'p=the24',
                'p=24')  # a del si correction sur le site
            if url.endswith(
                    '&c=') or '?p=0&c=' in url:  # vide ou redirection
                continue

            host = entry[1].capitalize()
            qual = entry[2]
            lang = entry[3]
            title = '%s [%s] (%s) [COLOR coral]%s[/COLOR]' % (movie_title,
                                                              qual, lang, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
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
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    # evite redirection vers fausse video hs
    if 'filmsvostfr.vip' in url:
        host = 'www.filmsvostfr.vip'
    elif 'voirstream.org' in url:
        host = 'www.voirstream.org'

    if 'filmsvostfr.vip' in url or 'voirstream.org' in url:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'

        headers = {
            'User-Agent': UA,
            'Host': host,
            'Referer': URL_MAIN,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'text/html; charset=utf-8'}

        request = urllib2.Request(url, None, headers)
        reponse = urllib2.urlopen(request)
        repok = reponse.read()
        reponse.close()

        vUrl = re.search('url=([^"]+)"', repok)
        if vUrl:
            hoster_url = vUrl.group(1)
            if 'vidto.' in hoster_url:
                hoster_url = hoster_url.replace('vidto.', 'vidtodo.')
            elif 'uptobox' in hoster_url:
                hoster_url = re.sub(
                    r'(http://www\.filmsvostfr.+?/uptoboxlink\.php\?link=)',
                    'http://uptobox.com/',
                    hoster_url)
            elif '1fichier' in hoster_url:
                hoster_url = re.sub(
                    r'(http://www\.filmsvostfr.+?/1fichierlink\.php\?link=)',
                    'https://1fichier.com/?',
                    hoster_url)

    else:
        hoster_url = url

    hoster = HosterGui().checkHoster(hoster_url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
