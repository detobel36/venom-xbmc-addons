# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 08 update 14/01/2021
# return False
from resources.lib.comaddon import SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
import re
import string

TimeOut = 10  # requetes avec time out utilisées seulement dans show movies : on attend plus 30s
SITE_IDENTIFIER = 'mystream_zone'
SITE_NAME = 'My Stream'
SITE_DESC = 'Films et Series en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
imdmovies = '#movies'  # tag request
imdseries = '#series'

# variables globales
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')
# variables internes
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'movies/', 'showMovies')
# serie&movie a revoir
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_NOTES = (URL_MAIN + 'imdb/' + imdmovies, 'showMovies')
MOVIE_LIST = (True, 'showAlphaMovies')
MOVIE_TENDANCE = (URL_MAIN + 'tendance/', 'showMovies')
MOVIE_FEATURED = (URL_MAIN, 'showMovies')
MOVIE_TOP_IMD = (
    URL_MAIN + 'imdb/' + imdmovies,
    'showMovies')  # = globale MOVIE_NOTES

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tvshows/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
SERIE_ALPHA = (True, 'showAlphaSeries')
SERIE_TOP_IMD = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
SERIE_NEWS_SAISONS = (URL_MAIN + 'seasons/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films & Séries',
        'search.png',
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

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films & Séries (Par Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_FEATURED[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_FEATURED[1],
        'Films & Séries (En vedette)',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TENDANCE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TENDANCE[1],
        'Films & Séries (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films & Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        ' Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TOP_IMD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP_IMD[1],
        'Films (Top IMDb)',
        'tmdb.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS_SAISONS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_SAISONS[1],
        'Séries (Saisons récentes)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_TOP_IMD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_TOP_IMD[1],
        'Séries (Top IMDd)',
        'tmdb.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ALPHA[1],
        'Séries (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '%20')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + key_search_series + \
            search_text.replace(' ', '%20')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + key_search_movies + \
            search_text.replace(' ', '%20')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Action & Adventure', 'action-adventure'], ['Adventure', 'adventure'],
             ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comedie', 'comedie'], ['Comedy', 'comedie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Documentary', 'documentary'], ['Drama', 'drama'],
             ['Drame', 'drame'], ['Familial', 'familial'], ['Family', 'family'], ['Fantastique', 'fantastique'],
             ['Fantasy', 'fantasy'], ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['History', 'history'],
             ['Horreur', 'horreur'], ['Horror', 'horror'], ['Kids', 'kids'], ['Music', 'music'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['Mystery', 'mystery'], ['Reality', 'reality'], ['Romance', 'romance'],
             ['Sci-Fi & Fantasy', 'sci-fi-fantasy'], ['Sci-Fi', 'science-fiction'],
             ['Sci-Fi & Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Talk', 'talk'],
             ['Telefilm', 'telefilm'], ['Thriller', 'thriller'], ['Tv Movie', 'tv-movie'], ['Guerre', 'war'],
             ['Guerre & politique', 'war-politics'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrlGenre in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'genre/' + sUrlGenre + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)
    gui.setEndOfDirectory()


def showAlphaMovies():
    showAlpha('movies')


def showAlphaSeries():
    showAlpha('tvshows')


def showAlpha(stype):
    gui = Gui()
    # requete json 20 resultat max
    # https://www3.mystream.zone/wp-json/dooplay/glossary/?term=g&nonce=2132c17353&type=tvshows
    url1 = URL_MAIN + 'wp-json/dooplay/glossary/?term='
    url2 = '&nonce='
    snonce = '2132c17353'  # a surveiller si jamais cela change
    url3 = '&type='

    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = []
    for alpha in listalpha:
        liste.append([str(alpha).upper(), url1 + str(alpha) +
                     url2 + snonce + url3 + stype])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    # https://www3.mystream.zone/release/2020
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1982, 2023)):
        year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'release/' + year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False

    if search:
        url = search.replace(' ', '%20')
        if key_search_movies in url:
            url = str(url).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in url:
            url = str(url).replace(key_search_series, '')
            bSearchSerie = True

        util = cUtil()
        search_text = util.CleanName(url.split(URL_SEARCH[0])[1])
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    if 'wp-json' in url and not search:
        try:
            request_handler = RequestHandler(url)
            request_handler.setTimeout(TimeOut)
            jsonrsp = request_handler.request(json_decode=True)
        except Exception as e:
            if str(e) == "('The read operation timed out',)":
                gui.addText(SITE_IDENTIFIER, 'site Inaccessible')
                gui.setEndOfDirectory()
                return
            else:
                gui.addText(SITE_IDENTIFIER, 'Request Failed')
                gui.setEndOfDirectory()
                return

        output_parameter_handler = OutputParameterHandler()
        for i, idict in jsonrsp.items():
            title = str(
                jsonrsp[i]['title'].encode(
                    'utf-8',
                    'ignore')).replace(
                ' mystream',
                '')  # I Know This Much Is True mystream
            title = title[2:-1]
            url2 = str(jsonrsp[i]['url'])
            thumb = str(jsonrsp[i]['img'])
            thumb = re.sub(
                'https:..ml2o99dkuow5.i.optimole.+?/https',
                'https',
                thumb)
            year = str(jsonrsp[i]['year'])
            display_title = title + ' (' + year + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if 'type=tvshows' in url:
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
        # 1 result with <= 20 items
        gui.setEndOfDirectory()
        return

    if '/tendance/' in url:  # title; thumb; url; year #regex ok
        pattern = 'class="item (?:movies|tvshows)".+?alt="([^"]+).+?src="([^"]+).+?href="([^"]+).+?span>([^<]+)'

    elif url == URL_MAIN:  # thumb; title; url; year #regex ok
        pattern = 'post-featured.+?src="(h[^"]+).+?alt="([^"]+).+?href="([^"]+).+?<span>([^<]*)'

    elif '/seasons/' in url:  # thumb; url; number; title #regex ok
        pattern = 'se seasons.+?src="(h[^"]*).+?href="([^"]*).+?class="b">([^<]*).+?c">([^<]*)'

    elif '/episodes/' in url:  # thumb; url; 'S* E*'; title; #regex ok
        pattern = 'se episodes".+?src="(h[^"]*).+?href="([^"]+).+?<span>([^/]+).+?">([^<]+)'

    elif '?s=' in url:  # url; title; thumb; year; desc #regex ok
        pattern = 'animation-2".+?href="([^"]+).+?alt="([^"]+).+?src="([^"]+)" .+?(?:|year">([^<]*)<.+?)<p>(.*?)<'

    elif '/genre/' in url or '/release/' in url:  # thumb; url; title; year; desc #regex ok
        pattern = 'class="item (?:movies|tvshows)".+?alt="([^"]+).+?src="([^"]+).+?href="([^"]+).+?span>(\\d+)<.+?texto">(.+?)<'

    elif '/imdb/' in url:  # url; thumb; title; rate #regex ok
        pattern = "poster'.+?ref='([^']*).+?src='(h[^']*).+?alt='([^']*).+?rating'>([^<]*)"

    elif '/tvshows/' in url or '/movies/' in url:  # thumb; title; url; year; desc #regex ok
        pattern = 'noscript>.+?src="([^"]+).+?alt="([^"]+).+?href="([^"]+).+?class="metadata".+?<span>(\\d+).+?class="texto">([^<]*)'

    request_handler = RequestHandler(url)
    request_handler.setTimeout(TimeOut)
    html_content = request_handler.request()
    parser = Parser()
    # filtrage html_content
    start = '<h2>Recently added</h2>'
    end = 'class="pagination"><span>'
    html_content = parser.abParse(html_content, start, end)
    # pour les thumb
    # html_content = re.sub('https:..ml2o99dkuow5.i.optimole.+?/https', 'https', html_content)

    if search and 'no-result animation-2' in html_content:  # Pas de résultats
        gui.addText(SITE_IDENTIFIER)
        return

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        desc = ''
        year = ''
        for entry in results[1]:
            if '/tendance/' in url:  # thumb; title; url; year
                title = entry[0].replace(' mystream', '')
                thumb = entry[1]
                url2 = entry[2]
                year = entry[3]
                if year != '':
                    year = re.search('(\\d{4})', year).group(1)
                display_title = title + ' (' + year + ')'

            elif url == URL_MAIN:  # thumb; title; url; year
                thumb = entry[0]
                title = entry[1].replace(' mystream', '')
                url2 = entry[2]
                year = entry[3]
                display_title = title + ' (' + year + ')'

            elif '/seasons/' in url:  # thumb; url; number; title
                thumb = entry[0]
                url2 = entry[1]
                title = entry[3].replace(' mystream', '')
                display_title = title + ' Saison ' + entry[2]

            elif '/episodes/' in url:  # thumb; url; 'S* E*'; title
                thumb = entry[0]
                url2 = entry[1]
                year = ''  # inutile pour les séries
                title = entry[3] + ' ' + entry[2]
                display_title = title + '(' + year + ')'

            elif '?s=' in url:  # thumb; url; title; year; desc
                url2 = entry[0]
                title = entry[1].replace(' mystream', '')
                thumb = entry[2]
                year = entry[3]
                desc = entry[4]
                display_title = title + ' (' + year + ')'

            elif '/genre/' in url or '/release/' in url:  # thumb; url; title; year; desc
                thumb = entry[1]
                url2 = entry[2]
                title = entry[0].replace(' mystream', '')
                year = entry[3]
                desc = entry[4]
                display_title = title + ' (' + year + ')'

            elif '/imdb/' in url:  # url; thumb; title; rate
                if 'movies' in str(
                        entry[0]) and 'mystream.zone/imdb/' + imdmovies in url:
                    url2 = entry[0]
                    title = str(entry[2]).replace(' mystream', '')
                    thumb = entry[1]
                    display_title = title + ' [ Imdb ' + str(entry[3]) + ' ]'
                elif 'tvshows' in str(entry[0]) and 'mystream.zone/imdb/' + imdseries in url:
                    url2 = entry[0]
                    title = str(entry[2]).replace(' mystream', '')
                    thumb = entry[1]
                    display_title = title + ' [ Imdb ' + str(entry[3]) + ' ]'
                else:
                    continue

            elif '/tvshows/' in url or '/movies/' in url:  # thumb; title; url; year; desc
                thumb = entry[0]
                title = entry[1].replace(' mystream', '')
                url2 = entry[2]
                year = entry[3]
                if year != '':
                    year = re.search('(\\d{4})', year).group(1)
                desc = entry[4]
                display_title = title + ' (' + year + ')'

            if search or '/release/' in url or '/genre/' in url or '/tendance/' in url:
                if 'movies' in url2 and not bSearchMovie:
                    display_title = display_title + ' (Film)'
                if 'tvshows' in url2 and not bSearchSerie:
                    display_title = display_title + ' (Série)'

            # filtre recherche par type
            if bSearchMovie:
                if 'tvshows' in url2:
                    continue
                else:
                    display_title = display_title
            if bSearchSerie:
                if 'movies' in url2:
                    continue
                else:
                    display_title = title

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre les résultats

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if 'mystream.zone/tvshows' in url2:  # inutile mais ne pas enlever resoudre regex
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            elif 'mystream.zone/seasons' in url2:
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
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
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
    pattern = 'pagination"><span>Page \\d+ de (\\d+)</span>.+?current">\\d+</span><ahref=.([^"|\']+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    movie_title = input_parameter_handler.getValue('movie_title')
    year = input_parameter_handler.getValue('year')
    # probleme temps de la requete aleatoire normale, lent, ou tps de
    # connexion > max autorisé
    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # temps qui peu depasser 10 secondes parfois

    # on passe ts les liens des épisodes dans chaque dossier saisons créés ds un liste
    # car pas de liens existants ds la page pour acceder aux pages de chaque
    # saison
    if not desc:
        try:
            pattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            results = parser.parse(html_content, pattern)
            if results[0]:
                desc = results[1][0]
        except BaseException:
            pass

    # '2 - 11'   href   title
    # class='numerando'>([^<]*).+?href='([^']*).>([^<]*) #
    pattern = "class='numerando'>(\\d+) - (\\d+)<.+?href='([^']*)"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            iSaison = entry[0]
            iEpisode = entry[1]
            url = entry[2]

            title = movie_title + ' Saison ' + \
                str(iSaison) + ' Episode ' + str(iEpisode)

            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showListEpisodes():  # plus utilisé
    # parent https://www3.mystream.zone/tvshows
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')
    listeUrlEpisode = input_parameter_handler.getValue('listeUrlEpisode')
    listeStitle = input_parameter_handler.getValue('listeStitle')

    listeUrlEpisode2 = []
    listetitle2 = []
    pattern = "'([^']*)'"
    parser = Parser()

    results = parser.parse(listeUrlEpisode, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    if results[0]:
        for entry in results[1]:
            listeUrlEpisode2.append(entry)

    results = parser.parse(listeStitle, pattern)
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    if results[0]:
        for entry in results[1]:
            listetitle2.append(entry)
    i = 0
    output_parameter_handler = OutputParameterHandler()
    for itemurl in listeUrlEpisode2:
        title = listetitle2[i]
        i = i + 1
        output_parameter_handler.addParameter('site_url', itemurl)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('desc', desc)
        output_parameter_handler.addParameter('year', year)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            title,
            '',
            thumb,
            desc,
            output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    # parents https://www3.mystream.zone/saisons/    # SERIE_NEWS_SAISONS
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')
    movie_title = input_parameter_handler.getValue('movie_title')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if not desc:
        try:
            pattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            results = parser.parse(html_content, pattern)
            if results[0]:
                desc = results[1][0]
        except BaseException:
            pass
    # '2 - 11'   url
    pattern = "class='numerando'>([^<]*).+?href='([^']*)"
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            iSaison = re.search('([0-9]+)', entry[0]).group(1)
            iEpisode = re.search('([0-9]+)$', entry[0]).group(1)
            url = entry[1]
            display_title = movie_title + ' ' + ' Saison ' + \
                str(iSaison) + ' Episode ' + str(iEpisode)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
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
    title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')
    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # if False: no desc MOVIE_TENDANCE
    if not desc:
        try:
            pattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            results = parser.parse(html_content, pattern)
            if results[0]:
                desc = results[1][0]
        except BaseException:
            pass

    pattern = "data-type='([^']*).*?post='([^']*).*?nume='([^']*).*?title'>([^<]*)"
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            datatype = entry[0]
            datapost = entry[1]
            datanum = entry[2]
            host = entry[3]
            url2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            pdata = 'action=doo_player_ajax&post=' + datapost + \
                '&nume=' + datanum + '&type=' + datatype
            display_title = (
                '%s [COLOR coral]%s[/COLOR]') % (title, host.capitalize())

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
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
    year = input_parameter_handler.getValue('year')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParametersLine(pdata)
    html_content = request.request(json_decode=True)

    hoster_url = html_content["embed_url"]

    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()
