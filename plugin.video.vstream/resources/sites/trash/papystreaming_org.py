# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import Parser
# from resources.lib.util import cUtil
import re
import urllib
import base64

SITE_IDENTIFIER = 'papystreaming_org'
SITE_NAME = 'Papystreaming'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'https://papystreaming.org/'

MOVIE_NEWS = (URL_MAIN + 'nouveaux-films-hd/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-streaming-hd-2017/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaire-hd/', 'showMovies')
# MOVIE_VIEWS = (URL_MAIN + 'de-visite/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'de-vote/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series-streaming-hd/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series-streaming-hd/', 'showSeries')
SERIE_COMMENTS = (URL_MAIN + 'populaire-hd/', 'showSeries')
# SERIE_VIEWS = (URL_MAIN + 'de-visite/', 'showSeries')
SERIE_NOTES = (URL_MAIN + 'de-vote/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH2 = (URL_MAIN + '?s=', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
# series et films melangé sur certaine fonction tri obligatoire qui bloque
# l'optimisation
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = {'User-Agent': UA}


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSSearch',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_COMMENTS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

#    Résultat des comments et des views identiques
#    output_parameter_handler = OutputParameterHandler()
#    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
#    gui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_COMMENTS[1],
        'Séries (Les plus commentées)',
        'comments.png',
        output_parameter_handler)

#    Résultat des comments et des views identiques
#    output_parameter_handler = OutputParameterHandler()
#    output_parameter_handler.addParameter('site_url', SERIE_VIEWS[0])
#    gui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NOTES[1],
        'Séries (Les mieux notées)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/action/'])
    liste.append(['Animation', URL_MAIN + 'category/animation/'])
    liste.append(['Aventure', URL_MAIN + 'category/aventure/'])
    liste.append(['Comédie', URL_MAIN + 'category/comedie/'])
    liste.append(['Crime', URL_MAIN + 'category/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'category/drame/'])
    liste.append(['Étranger', URL_MAIN + 'category/etranger/'])
    liste.append(['Familial', URL_MAIN + 'category/familial/'])
    liste.append(['Fantastique', URL_MAIN + 'category/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'category/histoire/'])
    liste.append(['Horreur', URL_MAIN + 'category/papystreaming_horreur/'])
    liste.append(['Musique', URL_MAIN + 'category/musique/'])
    liste.append(['Mystère', URL_MAIN + 'category/mystere/'])
    liste.append(['Romance', URL_MAIN + 'category/romance/'])
    liste.append(['Science-Fiction', URL_MAIN + 'category/science-fiction/'])
    liste.append(['Soap', URL_MAIN + 'category/soap/'])
    liste.append(['Sport', URL_MAIN + 'category/Sport/'])
    liste.append(['Téléfilm', URL_MAIN + 'category/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'category/thriller/'])
    liste.append(['Western', URL_MAIN + 'category/western/'])

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


def showMSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showSSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH2[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<a class="poster" href="([^"]+)"\\s+title="([^"]+)".+?<img src="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            if '/serie/' in url:
                continue
            thumb = entry[2]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'films.png',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

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
    pattern = '<span class="current">.+?<\\/span><\\/li><li><a href="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSeries(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a class="poster" href="([^"]+)"\\s+title="([^"]+)".+?<img src="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            if 'film' in url:
                continue
            thumb = entry[2]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumbnail', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    sSyn = ''
    pattern = '<p class=".+?">([^<]+)<\\/p>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        sSyn = results[1][0]

    pattern = '<a class="expand-season-trigger" data-toggle="collapse".+?href="([^"]+)".+?<\\/span>([^<]+)<\\/a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            vUrl = url + entry[0]
            sSaison = movie_title + entry[1]
            sSaison = sSaison.replace('N/A', '')
            sFilter = parser.getNumberFromString(entry[1])
            sFilter = 'saison-' + sFilter + '/'

            display_title = sSaison
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', vUrl)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumbnail', thumbnail)
            output_parameter_handler.addParameter('sSyn', sSyn)
            output_parameter_handler.addParameter('sFilter', sFilter)
            gui.addTV(
                SITE_IDENTIFIER,
                'showEpisodes',
                display_title,
                '',
                thumbnail,
                sSyn,
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')
    sFilter = input_parameter_handler.getValue('sFilter')
    sSyn = input_parameter_handler.getValue('sSyn')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<div class="larr episode-header">.+?<a href="([^"]+)"\\s+title="([^"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = entry[0]
            title = movie_title + entry[1]
            title = title.replace('N/A', '').replace(',', '')
            if sFilter not in url:
                continue
            # display_title = cUtil().DecoTitle(title)
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumbnail', thumbnail)
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addTV(SITE_IDENTIFIER, 'showHosters', title, '',
                      thumbnail, sSyn, output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showHosters():

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        'http://www.google.com/s2/favicons?domain=',
        '').replace(
        '\\',
        '')
    parser = Parser()

    sPattern1 = '{"link":"([^"]+)","type":".+?"}'
    sPattern2 = 'src="([^"]+)"/><\\/td>.+?<td>(.+?)<\\/td>'

    aResult1 = re.findall(sPattern1, html_content, re.DOTALL)
    aResult2 = re.findall(sPattern2, html_content, re.DOTALL)

    results = zip(aResult1, aResult2)
    if (results):
        for entry in results:
            url = entry[0]
            if not url.startswith('http'):
                url = 'http:' + url

            qual = entry[1][1]
            if 'vf' in entry[1][0]:
                lang = 'VF'
            else:
                lang = 'VOSTFR'

            if 'papystreaming' in url or 'mmfilmes.com' in url or 'belike.pw' in url:
                display_title = movie_title + \
                    ' [' + qual + '/' + lang + ']' + ' [COLOR skyblue]Papyplayer[/COLOR]'
                # display_title = display_title + ' [COLOR skyblue]Papyplayer[/COLOR]'
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumbnail', thumbnail)
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'ShowPapyLink',
                    display_title,
                    'films.png',
                    thumbnail,
                    '',
                    output_parameter_handler)

            else:
                hoster_url = url

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    display_title = movie_title + \
                        ' [' + entry[1][1] + '/' + lang + ']'
                    hoster.setDisplayName(display_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()


def ShowPapyLink():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')
    parser = Parser()

    if 'papystreaming' in url:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        pattern = 'var player.+?"([^"]+mp4)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            hoster_url = results[1][0]
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)
            else:
                gui.addText(SITE_IDENTIFIER,
                            '[COLOR red]Lien vidéo Non géré[/COLOR]')
        else:
            gui.addText(
                SITE_IDENTIFIER,
                '[COLOR red]Lien vidéo Non géré[/COLOR]')

    elif 'belike.pw' in url:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = 'file: *"([^"]+)",label:"(\\d+p)"'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:
                hoster_url = entry[0]
                label = entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    display_title = movie_title + ' [' + label + ']'
                    hoster.setDisplayName(display_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)
    else:

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        html_content = html_content.replace('\\', '')

        pattern = '"label":"([0-9p]+)"[^<>]+?"file":"([^"]+)"'
        results = parser.parse(html_content, pattern)

        if (results[0]):
            listurl = []
            listqual = []

            listurl.append(results[1][0][1])
            listqual.append(results[1][0][0])

            tab = zip(listurl, listqual)

            for url, qual in tab:
                hoster_url = url

                if not hoster_url.startswith('http'):
                    hoster_url = 'http' + hoster_url

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    display_title = movie_title + ' [' + qual + ']'
                    hoster.setDisplayName(display_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)
        else:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Lien vidéo HS[/COLOR]')

    gui.setEndOfDirectory()
