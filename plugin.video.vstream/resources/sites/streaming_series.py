# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import xbmc

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.comaddon import dialog, SiteManager


SITE_IDENTIFIER = 'streaming_series'
SITE_NAME = 'Streaming-Séries'
SITE_DESC = 'Regarder toutes vos séries en Streaming Gratuit'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()
    gui.addText(
        SITE_IDENTIFIER,
        'Information: Modification des DNS obligatoire pour utiliser cette source.')

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSerieSearch',
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


def showSerieSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'action'], [
            'Animation', 'animation'], [
                'Aventure', 'aventure'], [
                    'Comédie', 'comedie'], [
                        'Documentaire', 'documentaire'], [
                            'Drame', 'drame'], [
                                'Epouvante Horreur', 'epouvante-horreur'], [
                                    'Espionnage', 'espionnage'], [
                                        'Famille', 'famille'], [
                                            'Fantastique', 'fantastique'], [
                                                'Guerre', 'guerre'], [
                                                    'Historique', 'historique'], [
                                                        'Judiciaire', 'judiciaire'], [
                                                            'Medical', 'medical'], [
                                                                'Musical', 'musical'], [
                                                                    'Policier', 'policier'], [
                                                                        'Romance', 'romance'], [
                                                                            'Science Fiction', 'science-fiction'], [
                                                                                'Soap', 'soap'], [
                                                                                    'Thriller', 'thriller'], [
                                                                                        'Western', 'western']]

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
    pattern = 'class="post-thumbnail">.+?href="([^"]+)" *title="([^"]+).+?src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            thumb = entry[2]
            title = entry[1]

            if search:
                if not util.CheckOccurence(search, title):
                    continue

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    if not search:  # une seule page par recherche
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
    pattern = '>([^<]+)</a></li><li class="pg-item"><a class="next page-numbers" href="([^"]+)">Suivant'
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

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    desc = ''
    try:
        pattern = 'style="text-align:justify">(.+?)<'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
            desc = desc.replace('&#8220;', '\"').replace('&#8221;', '\"')
    except BaseException:
        pass

    # filtre pour ne prendre que sur une partie
    start = '<span>Informations</span>'
    end = '<div class="content ">'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)".+?<span>([^<]+)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = movie_title + ' Episode ' + entry[1]

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
    else:
        gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    parser = Parser()
    request = RequestHandler(url)
    html_content = request.request()
    pattern = '<span class="lg">([^<]+)<|<span class="myLecteur">.+?<b>([^<]+)</b>.+?href="([^"]+)'
    results = parser.parse(html_content, pattern)
    lang = ''

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            # langue
            if entry[0]:
                lang = entry[0].replace('(', '').replace(')', '')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    lang +
                    '[/COLOR]')
            # hote
            else:
                host = entry[1]
                url = URL_MAIN[:-1] + entry[2]
                title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('lang', lang)
                output_parameter_handler.addParameter('host', host)

                gui.addLink(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    thumb,
                    desc,
                    output_parameter_handler,
                    input_parameter_handler)

    else:
        gui.addText(SITE_IDENTIFIER)

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

    # lien commencant par VID_
    Codedurl = url
    request_handler = RequestHandler(Codedurl)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'var k=\"([^<>\"]*?)\";'
    results = parser.parse(html_content, pattern)

    if results[0]:
        postdata = 'k=' + results[1][0]

        dialog().VSinfo('Décodage en cours', 'Patientez', 5)
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

        # recherche d'un lien redirige
        pattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            return results[1][0]

    return ''
