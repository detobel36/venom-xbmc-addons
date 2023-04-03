# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.comaddon import Progress, SiteManager
import re
return False  # l'adresse a changé mais plus du tout le meme site, le 06/06/22


SITE_IDENTIFIER = 'zustream'
SITE_NAME = 'ZuStream'
SITE_DESC = 'Retrouvez un énorme répertoire de films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuFilms')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/mangas/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (True, 'showYearsSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
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


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche films',
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
        'Recherche séries',
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

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_MANGAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_MANGAS[1],
        'Séries (Mangas)',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/' + url])
    liste.append(['Animation', URL_MAIN + 'genre/animation/' + url])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/' + url])
    liste.append(['Biopic', URL_MAIN + 'genre/biographie/' + url])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/' + url])
    liste.append(['Comédie musicale', URL_MAIN + 'genre/musique/' + url])
    liste.append(['Comédie romantique', URL_MAIN + 'genre/romance/' + url])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/' + url])
    liste.append(['Drame', URL_MAIN + 'genre/drame/' + url])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/' + url])
    liste.append(['Famille', URL_MAIN + 'genre/familial/' + url])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/' + url])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/' + url])
    liste.append(['Historique', URL_MAIN + 'genre/histoire/' + url])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/' + url])
    liste.append(['Noël', URL_MAIN + 'genre/noel/' + url])
    liste.append(['Science Fiction', URL_MAIN +
                 'genre/science-fiction/' + url])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/' + url])
    liste.append(['Western', URL_MAIN + 'genre/western/' + url])

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


def showNetwork():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    output_parameter_handler.addParameter('tmdb_id', 213)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_CANAL[0])
    output_parameter_handler.addParameter('tmdb_id', 285)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_AMAZON[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1024)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_DISNEY[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2739)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_APPLE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2552)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_YOUTUBE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (YouTube Originals)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1995, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'sortie/' + Year + '/?post_types=movies')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYearsSeries():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1997, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'sortie/' + Year + '/?post_types=tvshows')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()
    util = cUtil()

    if search:
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
        pattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)</p>'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        pattern = 'article id="post-\\d+".+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)href="([^"]+).+?class="texto">(.*?)</div>'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
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

            lang = ''
            year = ''
            desc = ''
            if search:
                url = entry[0]
                thumb = entry[1]
                title = entry[2]
                desc = entry[3]

                # Filtre de recherche
                if not util.CheckOccurence(search_text, title):
                    continue
            else:
                thumb = entry[0]
                title = entry[1]
                if entry[2]:
                    lang = entry[2]
                if entry[3]:
                    year = entry[3]
                url = entry[4]
                if entry[5]:
                    desc = entry[5]

            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = util.unescape(desc).encode(
                    'utf-8')    # retire les balises HTML
            except BaseException:
                pass

            display_title = ('%s (%s) (%s)') % (title, lang, year)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    '',
                    thumb,
                    desc,
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
    parser = Parser()
    pattern = '<span>Page.+?de ([^<]+)</span.+?href="([^"]+)(?:"><i id=\'nextpaginat|" ><span class="icon-chevron-rig)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaison():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "<span class='title'>Saisons (.+?) *<i>"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sNumSaison = entry[0].strip()
            title = movie_title + ' saison ' + sNumSaison
            sUrlSaison = url + "?sNumSaison=" + sNumSaison
            output_parameter_handler.addParameter('site_url', sUrlSaison)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(SITE_IDENTIFIER, 'showSxE', title, '',
                          thumb, desc, output_parameter_handler)

    gui.setEndOfDirectory()


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')
    url, sNumSaison = url.split('?sNumSaison=')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "class='numerando'>(\\d+) - (\\d+)</div><div class='episodiotitle'><a href='([^']+)'"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            s = entry[0]
            if s != sNumSaison:
                continue
            e = entry[1]
            url = entry[2]
#            SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', entry[0])
            title = movie_title + ' Saison %s Episode %s' % (s, e)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()
    pattern = "dooplay_player_option.+?data-post='(\\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        # trie par numéro de serveur
        sortedList = sorted(results[1], key=lambda item: item[2])
        for entry in sortedList:

            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            # fonctionne pour Film ou Série (pour info : série -> dtype = 'tv')
            dtype = 'movie'
            dpost = entry[0]
            dnum = entry[1]
            pdata = 'action=doo_player_ajax&post=' + \
                dpost + '&nume=' + dnum + '&type=' + dtype
            lang = entry[2].replace(
                'Serveur',
                '').replace(
                'Télécharger',
                '').replace(
                '(',
                '').replace(
                ')',
                '')

            if 'VIP - ' in lang:  # Les liens VIP ne fonctionnent pas
                continue

            title = ('%s [%s]') % (movie_title, lang)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('pdata', pdata)
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
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry('User-Agent', UA)
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParametersLine(pdata)

    html_content = request.request()

    # 1
    pattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=[\'|"]([^\'"|]+)'
    aResult1 = re.findall(pattern, html_content)

    # 2
    pattern = '<a href="([^"]+)">'
    aResult2 = re.findall(pattern, html_content)

    # fusion
    results = aResult1 + aResult2

    if results:
        for entry in results:

            hoster_url = entry
            if 'zustreamv2/viplayer' in hoster_url:
                return

            if 're.zu-lien.com' in hoster_url:
                request_handler = RequestHandler(hoster_url)
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Referer', 'https://re.zu-lien.com')
                request_handler.request()
                sUrl1 = request_handler.getRealUrl()
                if not sUrl1 or sUrl1 == hoster_url:
                    request_handler = RequestHandler(hoster_url)
                    request_handler.disableRedirect()
                    request_handler.addHeaderEntry('User-Agent', UA)
                    request_handler.addHeaderEntry(
                        'Referer', 'https://re.zu-lien.com')
                    request_handler.request()

                    getreal = hoster_url

                    if request_handler.statusCode() == 302:
                        redirection_target = reponse.getResponseHeader()[
                            'Location']
                else:
                    hoster_url = sUrl1

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
