# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress, dialog
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import requests
import re
return False  # Cloudflare 15/01/2021


SITE_IDENTIFIER = 'dpstreaming'
SITE_NAME = 'DP Streaming'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = "https://series.dpstreaming.to/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'serie-category/series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'serie-category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def protectStreamByPass(url):
    if url.startswith('/'):
        url = URL_MAIN[:-1] + url

    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

    session = requests.Session()
    session.headers.update(
        {
            'User-Agent': UA,
            'Referer': URL_MAIN,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('erreur ' + str(e))
        return ''

    html_content = response.text

    parser = Parser()
    pattern = 'var k=\"([^<>\"]*?)\";'
    results = parser.parse(html_content, pattern)

    if results[0]:

        dialog().VSinfo('Décodage en cours', 'Patientez', 5)
        xbmc.sleep(5000)

        postdata = results[1][0]
        headers = {'User-Agent': UA, 'Accept': '*/*', 'Referer': url,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        session.headers.update(headers)
        data = {'k': postdata}

        try:
            response = session.post(URL_MAIN + 'embed_secur.php', data=data)
        except requests.exceptions.RequestException as e:
            print('erreur' + str(e))
            return ''

        data = response.text
        data = data.encode('utf-8', 'ignore')

        # Test de fonctionnement
        results = parser.parse(data, pattern)
        if results[0]:
            dialog().VSinfo('Lien encore protegé', 'Erreur', 5)
            return ''

        # recherche du lien embed
        pattern = '<iframe src=["\']([^<>"\']+?)["\']'
        results = parser.parse(data, pattern)
        if results[0]:
            return results[1][0]

        # recherche d'un lien redirigee
        pattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        results = parser.parse(data, pattern)
        if results[0]:
            return results[1][0]

    return ''


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeriesSearch',
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

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Classique', 'classique'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'],
             ['Dessin animés', 'dessin-anime'], ['Divers', 'divers'], ['Documentaires', 'documentaire'],
             ['Drama', 'drama'], ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Expérimental', 'experimental'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'], ['soap', 'soap'],
             ['Thriller', 'thriller'], ['Websérie', 'webserie'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'serie-category/series/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()

    if search:
        url = search
        url = url.replace('%20', '+').replace(' ', '+')

    else:
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = re.sub(
        'src="https://dpstreaming.to/wp-content/plugins/wp-fastest-cache-premium/pro/images/blank.gif"',
        '',
        html_content)
    pattern = '<div class="moviefilm".+?<a href="([^"]+)".+?<img.+?src="([^"]+)" alt="([^"]+)".+?<p>(.+?)</p>'
    parser = Parser()
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

            url = entry[0]
            thumb = re.sub('-119x125', '', entry[1])
            title = entry[2].replace(' Streaming', '')
            desc = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:  # une seule page par recherche
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSeries():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis plus complet que dans showmovies
    desc = ''
    try:
        pattern = 'class="lab_syn">Synopsis :</span>(.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].decode('utf-8')
            desc = cUtil().unescape(desc).encode('utf-8')
    except BaseException:
        pass

    pattern = '<a href="([^"]+)" class.+?><span>([^<]+)</span></a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = movie_title + ' episode ' + entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace('<iframe src="//www.facebook.com/', '')

    pattern = 'class="lg" width=".+?">(?:(VF|VOSTFR|VO))</td>.+?<td class="lg" width=".+?">([^<]+)</td.+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            lang = entry[0]
            host = entry[1]
            url = entry[2]

            display_title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (movie_title, lang, host)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addLink(
                SITE_IDENTIFIER,
                'serieHosters',
                display_title,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def serieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    hoster_url = protectStreamByPass(url)

    hoster = HosterGui().checkHoster(hoster_url)

    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
