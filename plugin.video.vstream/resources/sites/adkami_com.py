# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import Progress, isMatrix, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'ADKami'
SITE_DESC = 'Animés & Dramas en streaming.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'showAnimMenu')
ANIM_NEWS = (URL_MAIN + 'anime', 'showSeries')
ANIM_LIST = (
    URL_MAIN +
    'video?search=&n=&g=&s=&v=&t=0&p=&order=&d1=&d2=&e=&m=&q=&l=',
    'showAZ')
ANIM_VIEWS = (URL_MAIN + 'video?search=&t=0&order=3', 'showSeries')

DRAMA_DRAMAS = (True, 'showDramaMenu')
DRAMA_LIST = (
    URL_MAIN +
    'video?search=&n=&g=&s=&v=&t=5&p=&order=&d1=&d2=&e=&m=&q=&l=',
    'showAZ')
DRAMA_VIEWS = (URL_MAIN + 'video?search=&t=5&order=3', 'showSeries')

URL_SEARCH = (URL_MAIN + 'video?search=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'video?t=0&order=0&search=', 'showSeries')
URL_SEARCH_DRAMAS = (URL_MAIN + 'video?t=5&order=0&search=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


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

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_DRAMAS[1],
        'Dramas',
        'dramas.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchAnim',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Liste alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VIEWS[1],
        'Animés (Populaire)',
        'views.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showDramaMenu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchDrama',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_LIST[1],
        'Dramas (Liste alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_VIEWS[1],
        'Dramas (Populaire)',
        'views.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearchSerie():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_SERIES[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSearchAnim():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_ANIMS[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSearchDrama():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH_DRAMAS[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sType2 = input_parameter_handler.getValue('type2')

    liste = []
    liste.append(
        ['Action', URL_MAIN + 'video?recherche=&genre3=1&type2=' + sType2])
    liste.append(
        ['Aventure', URL_MAIN + 'video?recherche=&genre3=2&type2=' + sType2])
    liste.append(['Amour & Amitié', URL_MAIN +
                 'video?recherche=&genre3=3&type2=' + sType2])
    liste.append(
        ['Combat', URL_MAIN + 'video?recherche=&genre3=4&type2=' + sType2])
    liste.append(
        ['Comédie', URL_MAIN + 'video?recherche=&genre3=5&type2=' + sType2])
    liste.append(['Contes & Récits', URL_MAIN +
                 'video?recherche=&genre3=6&type2=' + sType2])
    liste.append(['Cyber & Mecha', URL_MAIN +
                 'video?recherche=&genre3=7&type2=' + sType2])
    liste.append(['Dark Fantasy', URL_MAIN +
                 'video?recherche=&genre3=8&type2=' + sType2])
    liste.append(
        ['Drame', URL_MAIN + 'video?recherche=&genre3=9&type2=' + sType2])
    liste.append(
        ['Ecchi', URL_MAIN + 'video?recherche=&genre3=10&type2=' + sType2])
    liste.append(
        ['Éducatif', URL_MAIN + 'video?recherche=&genre3=11&type2=' + sType2])
    liste.append(['Énigme & Policier', URL_MAIN +
                 'video?recherche=&genre3=12&type2=' + sType2])
    liste.append(['Épique & Héroique', URL_MAIN +
                 'video?recherche=&genre3=13&type2=' + sType2])
    liste.append(['Espace & Sci-Fiction', URL_MAIN +
                 'video?recherche=&genre3=14&type2=' + sType2])
    liste.append(['Familial & Jeunesse', URL_MAIN +
                 'video?recherche=&genre3=15&type2=' + sType2])
    liste.append(['Fantastique & Mythe', URL_MAIN +
                 'video?recherche=&genre3=16&type2=' + sType2])
    liste.append(
        ['Hentai', URL_MAIN + 'video?recherche=&genre3=17&type2=' + sType2])
    liste.append(['Historique', URL_MAIN +
                 'video?recherche=&genre3=18&type2=' + sType2])
    liste.append(
        ['Horreur', URL_MAIN + 'video?recherche=&genre3=19&type2=' + sType2])
    liste.append(['Magical Girl', URL_MAIN +
                 'video?recherche=&genre3=20&type2=' + sType2])
    liste.append(
        ['Musical', URL_MAIN + 'video?recherche=&genre3=21&type2=' + sType2])
    liste.append(['Psychologique', URL_MAIN +
                 'video?recherche=&genre3=22&type2=' + sType2])
    liste.append(
        ['Sport', URL_MAIN + 'video?recherche=&genre3=23&type2=' + sType2])
    liste.append(['Tranche de vie', URL_MAIN +
                 'video?recherche=&genre3=24&type2=' + sType2])
    liste.append(
        ['Shôjo-Ai', URL_MAIN + 'video?recherche=&genre3=25&type2=' + sType2])
    liste.append(['Shônen-Ai', URL_MAIN +
                 'video?recherche=&genre3=26&type2=' + sType2])
    liste.append(
        ['Yaoi/BL', URL_MAIN + 'video?recherche=&genre3=27&type2=' + sType2])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAZ():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    # pas d'url pour les non alpha, on utilise l'ancienne méthode épurée.
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', url)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNoAlpha',
        '[COLOR teal] Lettre [COLOR red]123[/COLOR]',
        'az.png',
        output_parameter_handler)

    import string
    for i in string.ascii_lowercase:
        url2 = url + str(i)

        output_parameter_handler.addParameter('site_url', url2)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            '[COLOR teal] Lettre [COLOR red]' +
            str(i).upper() +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showNoAlpha():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Decoupage pour cibler la partie non alpha
    pattern = 'class="video-item-list-days"><h5>Lettre 123</h5>(.+?)<div id="A"'
    html_content = parser.parse(html_content, pattern)

    # regex pour listage sur la partie decoupée
    pattern = 'data-original="([^"]+)".+?<span class="top"><a href="([^"]+)"><span class="title">([^<]+)</span>'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:

            thumb = entry[0]
            url2 = entry[1]
            title = entry[2]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if 't=1' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif 't=5' in url:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'dramas.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'animes.png',
                    thumb,
                    '',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showSeries(search=''):
    gui = Gui()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_ANIMS[0], '')
        search_text = search_text.replace(URL_SEARCH_DRAMAS[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'data-original="([^"]+)".+?class="top">.+?<a href="([^"]+)">.+?<span class="title">([^<]+)'
    results = re.findall(pattern, html_content, re.DOTALL)

    if not results:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(results)
        progress_ = Progress().VScreate(SITE_NAME, large=total > 50)
        output_parameter_handler = OutputParameterHandler()

        for entry in results:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            url2 = entry[1]
            title = entry[2]

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if 't=1' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif 't=5' in url:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'dramas.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaison',
                    title,
                    'animes.png',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if next_page is not False:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('page=([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<button class=\'actuel\'>[0-9]+</button><a href="([^"]+?)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSaison():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    # info anime et serie
    desc = ''
    try:
        pattern = '<p class="description.+?">([^<]+)<a title'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
            desc = desc.replace('<br />', '').replace('&apos;', '\'')
    except BaseException:
        pass

    pattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        gui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        pattern = '<li class="saison">.+?(\\d+)<\\/li>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            output_parameter_handler = OutputParameterHandler()
            for entry in results[1]:

                sNumSaison = entry[0]
                sSaison = 'Saison ' + entry[0]
                sUrlSaison = url + "?sNumSaison=" + sNumSaison
                display_title = movie_title + ' ' + sSaison
                title = movie_title

                output_parameter_handler.addParameter('site_url', sUrlSaison)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)

                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    display_title,
                    'series.png',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    url, sNumSaison = url.split('?sNumSaison=')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        gui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        start = 'class="saison">saison ' + sNumSaison
        end = '<div class="saison-container">'
        html_content = parser.abParse(html_content, start, end)
        pattern = '<a href="(https://www\\.adkami\\.com[^"]+)"[^<>]+>([^<]+)</a></li>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            output_parameter_handler = OutputParameterHandler()
            for entry in results[1]:
                url = entry[0]
                sEpisode = entry[1]
                Saison = 'Saison ' + sNumSaison
                title = movie_title + ' ' + Saison + ' ' + sEpisode
                title = re.sub(' vf', ' (VF)', title, re.IGNORECASE)
                display_title = re.sub(
                    ' vostfr', ' (VOSTFR)', title, re.IGNORECASE)

                lang = ''
                if '(VOSTFR)' in display_title:
                    lang = 'VOSTFR'
                elif '(VF)' in display_title:
                    lang = 'VF'

                title = display_title.replace(
                    ' (VF)', '').replace(
                    ' (VOSTFR)', '')

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('lang', lang)

                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    'series.png',
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

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    pattern = '<div class="video-iframe.+?url="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if not results[0]:
        pattern = 'class="video-video">.+?src="([^"]+)"'
        results = parser.parse(html_content, pattern)

    if "crunchyroll" in str(html_content) or "wakanim" in str(
            html_content) or "animedigitalnetwork" in str(html_content):
        pattern = 'encrypted-media.+?src="([^"]+)"'
        aResult2 = parser.parse(html_content, pattern)

        if not results[0]:
            results = aResult2
        else:
            if aResult2[0]:
                f = results[1] + aResult2[1]
                results[1] = f

    for entry in results[1]:

        url = entry.replace('+', 'plus')
        if 'youtube' in url and 'hl=fr' not in url:
            url = decodex(url)

        if url.startswith('//'):
            url = 'https:' + url

        hoster_url = url.replace('plus', '+')
        hoster = HosterGui().checkHoster(hoster_url)
        if hoster:
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                   input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def decodex(x):
    from itertools import chain
    import base64

    x = x.replace('https://www.youtube.com/embed/', '')

    missing_padding = len(x) % 4
    if missing_padding:
        x += '=' * (4 - missing_padding)

    try:
        e = base64.b64decode(x)
        t = ''
        r = "ETEfazefzeaZa13MnZEe"
        a = 0

        px = chain(e)
        for y in list(px):
            if isMatrix():
                t += chr(int(175 ^ y) - ord(r[a]))
            else:
                t += chr(int(175 ^ ord(y[0])) - ord(r[a]))
            a = 0 if a > len(r) - 2 else a + 1
        return t
    except BaseException:
        return ''

    return ''
