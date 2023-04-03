# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

"""
Pour rappel.
Problème avec les DNS en ipv6 il faut utiliser les suivantes
CloudFlare DNS:
Préféré : 2606:4700:4700::1111
Auxiliaire : 2606:4700:4700::1001
Ou:
Google DNS:
Préféré : 2001:4860:4860::8888
Auxiliaire : 2001:4860:4860::8844
"""

import re
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, dialog, SiteManager
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'series_en_streaming'
SITE_NAME = 'Series-en-Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'category/series/?orderby=date', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
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

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showMovies(URL_SEARCH[0] + search_text)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Classique', 'classique'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'],
             ['Dessin animés', 'dessin-anime'], ['Divers', 'divers'], ['Documentaire', 'documentaire'],
             ['Drama', 'drama'], ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'],
             ['Historique', 'historique'], ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'],
             ['Péplum', 'peplum'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science-fiction', 'science-fiction'], ['Soap', 'soap'], ['Thriller', 'thriller'],
             ['Webséries', 'webserie'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'category/series/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        util = cUtil()
        url = search.replace(' ', '+')
        search = util.CleanName(search.replace(URL_SEARCH[0], ''))
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="video\\s.+?href="([^"]+).+?class="izimg".+?src="([^"]+).+?title="([^"]+)'
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

            url = entry[0]
            title = entry[2].replace(' Streaming', '')

            thumb = entry[1]
            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb

            # tris search
            if search and total > 3:
                if not util.CheckOccurence(search, title):
                    continue

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', thumb, '', output_parameter_handler)

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
    pattern = '>([^<]+)</a></div><span class="son bg"><a href="([^"]+)" *>Suivante'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération des Synopsis
    desc = ''
    try:
        pattern = '<b>Synopsis :</b>(.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
            desc = desc.replace('\\', '')
    except BaseException:
        pass

    pattern = '<a href="([^"]+)" class="post-page-numbers".+?<span>([^<>]+)</span></a>'
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

    pattern = '<span class="lg">(.+?)</span>|myLecteur">Lecteur (?:<b>)*([a-z]+)(?:</b>)* *:</span> <a href="([^"]+)"'
    results = parser.parse(html_content, pattern)
    lang = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                # lang = entry[0].replace('Langue(', 'Langue -')
                lang = entry[0].replace('(', '- ').replace(')', '').strip()
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    lang +
                    '[/COLOR]')
            else:
                host = entry[1].capitalize()
                url = entry[2]
                if url.startswith('/'):
                    url = URL_MAIN[:-1] + url

                display_title = (
                    '%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('lang', lang)
                output_parameter_handler.addParameter('host', host)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    hoster_url = protectStreamByPass(url)
    hoster = HosterGui().checkHoster(hoster_url)

    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def protectStreamByPass(url):

    # lien commençant par VID_
    Codedurl = url
    request_handler = RequestHandler(Codedurl)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'var k=\"([^<>\"]*?)\";'
    results = parser.parse(html_content, pattern)

    if results[0]:
        postdata = 'k=' + results[1][0]

        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        xbmc.sleep(5000)

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

        request = RequestHandler(URL_MAIN + 'embed_secur.php')
        request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        # request.addHeaderEntry('Host', 'www.protect-stream.com')
        request.addHeaderEntry('Referer', Codedurl)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(postdata)
        html_content = request.request()

        # Test de fonctionnement
        results = parser.parse(html_content, pattern)
        if results[0]:
            dialog().VSinfo('Lien encore protégé', "Erreur", 5)
            return ''

        # recherche du lien embed
        pattern = '<iframe src=["\']([^<>"\']+?)["\']'
        results = parser.parse(html_content, pattern)
        if results[0]:
            return results[1][0]

        # recherche d'un lien redirigé
        pattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            return results[1][0]

    return ''
