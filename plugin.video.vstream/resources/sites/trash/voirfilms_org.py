# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import QuoteSafe, Quote
import re

SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms'
SITE_DESC = 'Films, Séries & Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = 'https://wvv.voirfilms.club/'  # url de repli site sans pub

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_LIST = (URL_MAIN + 'alphabet', 'showAlpha')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_LIST = (URL_MAIN + 'series/alphabet', 'showAlpha')
SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_LIST = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?type=film&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?type=serie&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'recherche?type=anime&s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par ordre alphabétique)',
        'az.png',
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
        'Films (Par années)',
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
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
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
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnims():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        url = url + Quote(search_text)
        showMovies(url)
        gui.setEndOfDirectory()
        return


def AlphaSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    progress_ = Progress().VScreate(SITE_NAME)
    output_parameter_handler = OutputParameterHandler()
    for i in range(0, 27):
        progress_.VSupdate(progress_, 36)

        if i > 0:
            title = chr(64 + i)
        else:
            title = '09'

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

    liste = []
    liste.append(['Action', url + 'action_1'])
    liste.append(['Animation', url + 'animation_1'])
    liste.append(['Arts Martiaux', url + 'arts-martiaux_1'])
    liste.append(['Aventure', url + 'aventure_1'])
    liste.append(['Biopic', url + 'biopic_1'])
    liste.append(['Comédie', url + 'film-comedie'])
    liste.append(['Comédie Dramatique', url + 'comedie-dramatique_1'])
    liste.append(['Documentaire', url + 'documentaire_1'])
    liste.append(['Drame', url + 'drame_1'])
    liste.append(['Epouvante Horreur', url + 'epouvante-horreur_1'])
    liste.append(['Erotique', url + 'erotique_1'])
    liste.append(['Espionnage', url + 'espionnage_1'])
    liste.append(['Fantastique', url + 'fantastique_1'])
    liste.append(['Guerre', url + 'guerre_1'])
    liste.append(['Historique', url + 'historique_1'])
    liste.append(['Musical', url + 'musical_1'])
    liste.append(['Policier', url + 'policier_1'])
    liste.append(['Romance', url + 'romance_1'])
    liste.append(['Science Fiction', url + 'science-fiction_1'])
    liste.append(['Série', url + 'series_1'])
    liste.append(['Thriller', url + 'thriller_1'])
    liste.append(['Western', url + 'western_1'])
    liste.append(['Non classé', url + 'non-classe_1'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

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

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1913, 2023)):
        Year = str(i)
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
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2023)):
        Year = str(i)
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

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

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
    parser = Parser()

    if search:
        url = search

        sTypeSearch = parser.parseSingleResult(url, '\\?type=(.+?)&')
        if sTypeSearch[0]:
            sTypeSearch = sTypeSearch[1]
        else:
            sTypeSearch = False

        request = RequestHandler(url)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')

        html_content = request.request()

        pattern = '<div class="unfilm".+?href="([^"]+)" title="([^"]+).+?class="type ([^"]+)".+?<img src="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        html_content = re.sub('alt="title="', 'alt="', html_content)  # anime
        pattern = '<div class="unfilm".+?href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if search:
                title = entry[1]
                _type = entry[2]
                thumb = entry[3]
                year = entry[5]
                qual = entry[6]
                if sTypeSearch:
                    if sTypeSearch != _type:  # genre recherché:  film/serie/anime
                        continue
            else:
                thumb = entry[1]
                title = entry[2]
                year = entry[4]
                qual = entry[5]

            url = entry[0]
            if 'http' not in url:
                url = URL_MAIN[:-1] + url

            title = title.replace('film ', '')  # genre
            title = title.replace(' streaming', '')  # genre

            lang = ''
            if 'Vostfr' in title:
                title = title.replace('Vostfr', '')
                lang = 'VOSTFR'

            display_title = '%s [%s] (%s) (%s)' % (title, qual, lang, year)

            if 'http' not in thumb:
                thumb = URL_MAIN + thumb

            # not found better way
            # title = unicode(title, errors='replace')
            # title = title.encode('ascii', 'ignore').decode('ascii')

            # vStream don't work with unicode url for the moment
            # thumb = unicode(thumb, 'UTF-8')
            # thumb = thumb.encode('ascii', 'ignore').decode('ascii')
            # thumb = thumb.decode('utf8')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('qual', qual)

            if '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showS_E',
                    display_title,
                    thumb,
                    thumb,
                    '',
                    output_parameter_handler)
            elif 'anime' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showS_E',
                    display_title,
                    thumb,
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    thumb,
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

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
    html_content = re.sub(" rel='nofollow'", "", html_content)  # next genre
    pattern = ">([^<]+)</a><a href='([^']+)'>suiv »"
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        if next_page.startswith('/'):
            next_page = URL_MAIN[:-1] + next_page
        number_next = re.findall('([0-9]+)', next_page)[-1]
        paging = str(number_next) + '/' + number_max
        return next_page, paging

    return False, 'none'


def showLinks(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    # patch for unicode url
    url = QuoteSafe(url)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'data-src="([^"]+)" target="filmPlayer".+?span class="([^"]+)"></span>.+?class="([^"]+)"></span>'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            host = entry[1].capitalize()
            if 'apidgator' in host or 'dl_to' in host:
                continue

            lang = entry[2].upper().replace('L', '')
            title = '%s (%s) [COLOR coral]%s[/COLOR]' % (movie_title,
                                                         lang, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('lang', lang)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                thumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    pattern = 'href="(https:\\/\\/cineactu.co\\/.+?").*?span class="([^"]+).*?class="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            host = entry[1]
            if 'fichier' in host:
                host = '1 Fichier'
            if 'uptobox' in host:
                host = 'Uptobox'
            host = host.capitalize()  # ou autres ?

            lang = entry[2].upper().replace('L', '')
            title = '%s (%s) [COLOR coral]%s[/COLOR]' % (movie_title,
                                                         lang, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('siteReferer', url)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('lang', lang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersDL',
                title,
                thumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showS_E():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # html_content = html_content.replace("\r\t", "")
    if '-saison-' in url or 'anime' in url:
        pattern = '<a class="n_episode2" title=".+?, *([A-Z]+) *,.+?" *href="([^"]+)">(.+?)</a></li>'
    else:
        pattern = '<div class="unepetitesaisons">[^<>]*?<a href="([^"]+)" title="([^"]+)">'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1][::-1]:

            # Si plusieurs langues sont disponibles, une seule est affichée ici.
            # Ne rien mettre, la langue sera ajoutée avec le host
            if 'anime' in url:
                url2 = entry[1]
                sNM = entry[2].replace('<span>', '').replace('</span>', '')
                title = movie_title + ' E' + sNM
                display_title = title
            elif '-saison-' in url:
                url2 = entry[1]
                sNM = entry[2].replace('<span>', ' ').replace('</span>', '')
                title = movie_title + sNM
                display_title = title
            else:
                url2 = entry[0]
                title = re.sub('\\d x ', 'E', entry[1])
                title = title.replace('EP ', 'E')
                display_title = title

            if 'http' not in url2:
                url2 = URL_MAIN + url2

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '-episode-' in url2 or '/anime' in url:
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showS_E',
                    display_title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    host = url.split('/')[0:3]
    host = host[0] + '//' + host[2] + '/'

    # VSlog('org > ' + url)

    # Attention ne marche pas dans tout les cas, certain site retourne aussi
    # un 302 et la lib n'en gere qu'un
    if False:
        # On recupere la redirection
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', host)
        html_content = request_handler.request()
        redirection_target = request_handler.getRealUrl()

    else:
        request_handler = RequestHandler(url)
        request_handler.disableRedirect()
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', host)
        html_content = request_handler.request()

        redirection_target = url

        if request_handler.statusCode() == 302:
            redirection_target = reponse.getResponseHeader()['Location']

    # attention fake redirection
    url = redirection_target
    try:
        m = re.search(r'url=([^"]+)', html_content)
    except BaseException:
        m = re.search(r'url=([^"]+)', str(html_content))

    if m:
        url = m.group(1)

    # Modifications
    url = url.replace('1wskdbkp.xyz', 'youwatch.org')
    if '1fichier' in url:
        url = re.sub('(http.+?\\?link=)', 'https://1fichier.com/?', url)

    hoster_url = url
    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHostersDL():
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    siteReferer = input_parameter_handler.getValue('siteReferer')

    if 'cineactu.co' in url:  # tjrs vrai mais au cas ou autre pattern fait sur host DL
        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', siteReferer)
        request_handler.request()
        redirection_target = request_handler.getRealUrl()
        if 'shortn.co' in redirection_target:
            bvalid, shost = Hoster_shortn(redirection_target, url)
            if bvalid:
                hoster_url = shost
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def Hoster_shortn(url, refer):
    shost = ''
    # url="https://shortn.co/f/6183943"
    url = url.replace('%22', '')
    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', refer)
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

        # https://1fichier.com/?jttay6v60izpcu3rank7
        # https://uptobox.com/vy7g5a6itlgj?aff_id=10831504
        pattern = 'href="([^"]+).+?target="_blank'
        results = re.findall(pattern, html_content)
        if results:
            shost = results[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
