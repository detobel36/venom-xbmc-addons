# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager


SITE_IDENTIFIER = 'neko_sama'
SITE_NAME = 'Neko Sama'
SITE_DESC = 'Animés en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showLastEp')
ANIM_VFS = (URL_MAIN + 'anime-vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime', 'showMovies')

URL_SEARCH = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_ANIMS = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_VF = (ANIM_VFS[0], 'showSearchResult')

FUNCTION_SEARCH = 'showSearchResult'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VOSTFR)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VF)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Dernier ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        showSearchResult(search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchResult(search):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    searchURL = URL_MAIN[:-1] + \
        re.search('var urlsearch = "([^"]+)";', html_content).group(1)

    bGlobal_Search = False
    if search:
        if URL_SEARCH[0] in search:
            bGlobal_Search = True
            search = search.replace(URL_SEARCH[0], '')
    search = search.lower()

    request_handler = RequestHandler(searchURL)
    data = request_handler.request(json_decode=True)

    output_parameter_handler = OutputParameterHandler()
    for dicts in data:
        if search in dicts['title'].lower() or search in dicts['title_english'].lower(
        ) or search in dicts['others'].lower():
            title = dicts['title']
            url2 = URL_MAIN[:-1] + dicts['url']
            thumb = dicts['url_image']
            desc = ''

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addAnime(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showLastEp():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '"episode":"([^"]+)".+?","title":"([^"]+)".+?"lang":"([^"]+)".+?"anime_url":"([^"]+)".+?"url_bg":"([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = URL_MAIN[:-1] + entry[3]
            thumb = entry[4]
            lang = entry[2].upper()
            title = '%s %s [%s]' % (entry[1], entry[0], lang)
            desc = ''

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a href="([^"]+)">.+?src="([^"]+)" alt="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = URL_MAIN[:-1] + entry[0]
            thumb = entry[1]
            title = entry[2]
            desc = ''

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addAnime(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

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
    pattern = '>([^<]+)</a><a href="([^"]+)" class=""><svg'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN[:-1] + results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisonEpisodes():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')

    if url.endswith("vostfr"):
        request_handler = RequestHandler(url.replace('vostfr', 'vf'))
        html_content = request_handler.request()
        if "404 Not Found" not in html_content:
            output_parameter_handler = OutputParameterHandler()
            title = "[COLOR red]Cliquez ici pour accéder à la version VF[/COLOR]"
            output_parameter_handler.addParameter(
                'site_url', url.replace('vostfr', 'vf'))
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisonEpisodes',
                title,
                '',
                output_parameter_handler)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    try:
        pattern = '<p>(.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = '"episode":"([^"]+)".+?"url":"([^"]+)","url_image":"([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = movie_title + ' ' + entry[0].replace('Ep. ', 'E')
            url2 = URL_MAIN[:-1] + entry[1].replace('\\/', '/')
            thumb = entry[2]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showSeriesHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = "video\\[\\d+\\] = \'([^']+)\'"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            # Enlève les faux liens
            # if 'openload' in entry or '.mp4' not in entry:
            if 'openload' in entry or 'mystream.to' in entry or "streamtape" in entry:
                continue

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
