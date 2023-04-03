# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # de nouveau en panne au 08/07/22


SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et séries récentes en streaming et en téléchargement'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + 'v2/recherche/', 'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    'v2/recherche/categorie=films&mot_search=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'v2/recherche/categorie=series&mot_search=',
    'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/nouveautes/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/plus-vus-mois/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films/les-mieux-notes/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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
        'Recherche film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
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
        'Recherche série',
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
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biographie', 'biographie'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Drame', 'drame'], ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Historique', 'historique'], ['Horreur', 'horreur'],
             ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Sport', 'sport'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/genre/' + url + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animé', 'anime'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['DC Comics', 'dc-comics'], ['Documentaire', 'documentaire'], ['Drama', 'drama'], ['Drame', 'drame'],
             ['Emission TV', 'emission-tv'], ['Epouvante-Horreur', 'epouvante-horreur'], ['Fantastique', 'fantastique'],
             ['Gore', 'gore'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Mystère', 'mystere'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Série TV', 'serie-tv'], ['Thriller', 'thriller'], ['Télé-réalité', 'tele-realite']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'v2/series/genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieAnnees():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1914, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'films/annee/' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieAnnees():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1989, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'v2/series/annee/' + Year + '/')
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

    if search:
        url = search
        pattern = '<img class="img-responsive" *src="([^"]+)".+?<div class="divtelecha.+?href="([^"]+)">([^<>]+)<'
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        if '/series' in url:
            pattern = '<div class="divtelecha.+?href="([^"]+)"><strong>([^<]+)</strong>.+?<img class="img-responsive".+?src="([^"]+).+?serie de (\\d{4})<.+?Synopsis :([^<]+)'
        else:  # films
            pattern = '<h2 class="heading"> *<a href="[^"]+">([^<]+).+?<img class="img-responsive" *src="([^"]+)" *alt.+?(?:<font color="#.+?">([^<]+)</font>.+?).+?>film de (\\d{4})<.+?Synopsis : ([^<]+).+?<div class="divtelecha.+?href="([^"]+)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
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

            desc = ''
            year = ''
            if search:
                qual = ''
                thumb = URL_MAIN[:-1] + entry[0]
                title = entry[2].replace(
                    'télécharger ', '').replace(
                    'en Streaming', '')
                title = title.replace(
                    ' TELECHARGEMENT GRATUIT', '').replace(
                    'gratuitement', '')
                url2 = entry[1]
            elif '/series' in url:
                qual = ''
                url2 = entry[0]
                title = entry[1].replace(
                    'Regarder ', '').replace(
                    'en Streaming', '')
                thumb = URL_MAIN[:-1] + entry[2]
                year = entry[3]

                try:
                    desc = entry[4].decode('utf-8')
                except AttributeError:
                    pass

                desc = cUtil().unescape(desc).encode('utf-8')
            else:
                title = entry[0]
                thumb = URL_MAIN[:-1] + entry[1]
                year = entry[3]

                try:
                    desc = entry[4].decode('utf-8')
                except AttributeError:
                    pass

                desc = cUtil().unescape(desc).encode('utf-8')
                url2 = entry[5]

                qual = entry[2]
                if qual:

                    try:
                        qual = qual.decode("utf-8")
                    except AttributeError:
                        pass

                    qual = qual.replace(
                        u' qualit\u00E9', '').replace(
                        'et ', '/').replace(
                        'Haute', 'HD') .replace(
                        ' ', '').replace(
                        'Bonne', 'DVD').replace(
                        'Mauvaise', 'SD').encode("utf-8")

            if 'https' not in url2:
                url2 = URL_MAIN[:-1] + url2

            url2 = url2.replace('telecharger', 'streaming')

            try:
                title = title.decode("utf-8")
            except AttributeError:
                pass

            title = title.replace(
                u'T\u00E9l\u00E9charger ',
                '').encode("utf-8")

            # Remplace tout les decodage en python 3
            try:
                title = str(title, 'utf-8')
                qual = str(qual, 'utf-8')
                desc = str(desc, 'utf-8')
            except BaseException:
                pass

            display_title = ('%s [%s] (%s)') % (title, qual, year)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            if '/series/' in url or '/series/' in url2 or '/series_co/' in thumb:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisonsEpisodes',
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

    if not search:
        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.findall('([0-9]+)', next_page)[-1]
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<li><a href="([^"]+)" class="next">Suivant'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return URL_MAIN[:-1] + results[1][0]

    return False


def ReformatUrl(link):
    if '/v2/mangas' in link:
        return link
    if '/telecharger/' in link:
        return link.replace('telecharger', 'streaming')
    if '-telecharger-' in link:
        f = link.split('/')[-1]
        return '/'.join(link.split('/')[:-1]) + \
            '/streaming/' + f.replace('-telecharger', '')
    # if ('/v2/' in link) and ('/streaming/' in link):
        # return link.replace('/v2/', '/')
    # if ('/v2/' in link) and ('/genre/' in link):
        # return link
    # if '/v2/' in link:
        # return link.replace('/v2/', '/streaming/')
    return link


def showSaisonsEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '(?:<h2 class="heading-small">(Saison .+?)<)|(?:<li><a title=".+? \\| (.+?)" class="num_episode" href="([^"]+)")'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            else:
                ePisode = entry[1].replace(',', '')
                title = movie_title + ' ' + ePisode
                url = entry[2]
                if 'https' not in url:
                    url = URL_MAIN[:-1] + url

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter(
                    'year', year)  # utilisé par le skin
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    # reformatage url
    url = ReformatUrl(url)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    _type = ''
    if '/films' in url:
        _type = 'films'
    elif 'saison' in url or 'episode' in url:
        _type = 'series'

    url2 = url.rsplit('/', 1)[1]
    idMov = re.sub('-.+', '', url2)

    pattern = '<div title="([^"]+)".+?streaming="([^"]+)" heberger="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            if 'VF' in entry[0]:
                lang = 'VF'
            elif 'VOSTFR' in entry[0]:
                lang = 'VOSTFR'
            else:
                lang = 'VO'

            idHeb = entry[1]
            host = entry[2].capitalize()
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('_type', _type)
            output_parameter_handler.addParameter('idMov', idMov)
            output_parameter_handler.addParameter('idHeb', idHeb)
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
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    _type = input_parameter_handler.getValue('_type')
    idHeb = input_parameter_handler.getValue('idHeb')

    if input_parameter_handler.exist('idMov'):  # film
        idMov = input_parameter_handler.getValue('idMov')
        pdata = 'id=' + idHeb + '&id_movie=' + idMov + '&type=' + _type
        pUrl = URL_MAIN + 'v2/video.php'
    else:  # serie pas d'idmov
        pdata = 'id=' + idHeb + '&type=' + _type
        pUrl = URL_MAIN + 'v2/video.php'

    pUrl = pUrl + '?' + pdata

    request = RequestHandler(pUrl)
    request.addHeaderEntry('Referer', url)
    html_content = request.request()
    html_content = html_content.replace('\\', '')

    pattern = '<iframe.+?src="([^"]+)".+?"qualite":"([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]
            if hoster_url.startswith('//'):
                hoster_url = 'http:' + hoster_url

            qual = entry[1]

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                display_title = ('%s [%s]') % (movie_title, qual)
                hoster.setDisplayName(display_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        # au cas où pas de qualité
        pattern = '<iframe.+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:
                hoster_url = entry
                if hoster_url.startswith('//'):
                    hoster_url = 'http:' + hoster_url

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
