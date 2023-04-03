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
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'otakufr_com'
SITE_NAME = 'OtakuFR'
SITE_DESC = 'OtakuFR animés en streaming et téléchargement'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = (URL_MAIN, 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'film', 'showMovies')
ANIM_GENRES = (True, 'ShowGenre')
ANIM_LIST = (URL_MAIN + 'liste-anime/', 'showAlpha')

URL_SEARCH = (URL_MAIN + 'toute-la-liste-affiches/?q=', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'site_url')
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

    output_parameter_handler.addParameter('site_url', ANIM_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIES[1],
        'Animés (Film)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    if search or '/genre/' in url or '/film' in url:  # news
        pattern = '<figure class="m-0">.+?ref="([^"]+).+?(?:src="(.+?)"|\\.?) class.+?</i>([^<]+).+?Synopsis:.+?>([^<]+)'
    else:  # populaire et search
        pattern = '<article class=".+?ref="([^"]+).+?src="([^"]+).+?title="([^"]+)'

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

            url2 = entry[0]
            thumb = entry[1]
            title = entry[2]
            lang = ''
            if 'Vostfr' in title:
                lang = 'VOSTFR'
                title = title.replace('Vostfr', '')
            desc = ''
            if search or '/genre/' in url or '/film' in url:
                desc = entry[3]

            display_title = title + ' (' + lang + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if search or '/genre/' in url or '/film' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    'animes.png',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    'animes.png',
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
    pattern = '>([^<]+)</a></li><li class="page-item"> <a class="next page-link" href="([^"]+)">Next'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def ShowGenre():
    gui = Gui()

    liste = [
        'action',
        'aventure',
        'comedie',
        'crime',
        'demons',
        'drame',
        'Ecchi',
        'espace',
        'fantastique',
        'gore',
        'harem',
        'historique',
        'horreur',
        'jeu',
        'lecole',
        'magie',
        'martial-arts',
        'mecha',
        'militaire',
        'musique',
        'mysterieux',
        'Parodie',
        'police',
        'psychologique',
        'romance',
        'samurai',
        'sci-fi',
        'seinen',
        'shoujo',
        'shoujo-ai',
        'shounen',
        'shounen-ai',
        'sport',
        'super-power',
        'surnaturel',
        'suspense',
        'thriller',
        'tranche-de-vie']

    output_parameter_handler = OutputParameterHandler()
    for igenre in liste:
        title = igenre.capitalize().replace('-', ' ')
        if 'Jeu' in igenre:
            title = 'Jeux'
        url = URL_MAIN + 'genre/' + igenre + '/'
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a href="([^<]+)">([A-Z#])</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            sLetter = entry[1]
            Link = entry[0]

            output_parameter_handler.addParameter('site_url', URL_MAIN + Link)
            output_parameter_handler.addParameter('AZ', sLetter)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAZ',
                'Lettre [COLOR coral]' +
                sLetter +
                '[/COLOR]',
                'animes.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAZ():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    dAZ = input_parameter_handler.getValue('AZ')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = 'has-large-font-size.+?<strong>([^<]+)|<li><a href="([^"]+).+?>([^<]+)'
    results = parser.parse(html_content, pattern)
    bValid = False
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                bValid = False
                if dAZ in entry[0]:
                    bValid = True
                    continue
            if bValid:
                url = entry[1]
                title = entry[2]
                display_title = title + ' (' + 'VOSTFR' + ')'
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    display_title,
                    'animes.png',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    pattern = 'Synopsis:(.*?)(?:<ul|class="|Autre Nom)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = results[1][0]
        desc = cleanDesc(desc)

    thumb = ''
    pattern = 'ImageObject.*?primaryimage.+?"(https.*?jpg)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        thumb = results[1][0]

    pattern = '(?:right">|<\\/a>)\\s*<a href="(https.+?\\/episode\\/.+?)".+?list-group-item.+?item-action">([^<]+)(?:Vostfr|Vf)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):
            url = entry[0]
            Ep = entry[1].split(' ')[-2]
            title = entry[1].replace(Ep, '') + ' E' + Ep

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                'animes.png',
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

    list_hostname = []
    pattern = 'aria-selected="true">([^<]+)'
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:
            list_hostname.append(entry)

    # list_host = []
    # normalement on devrait correler le valeur de l'id avec list_hostname
    pattern = 'iframe.+?src="([^"]*).+?id="([^"]*)'
    results = parser.parse(html_content, pattern)
    i = 0
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            if 'https:' not in url2:
                url2 = 'https:' + url2

            if len(results[1]) == len(list_hostname):
                host = list_hostname[i]
            else:
                host = GetHostname(url2)
            i = i + 1
            sFilter = host.lower()
            if 'brightcove' in sFilter or 'purevid' in sFilter or 'videomega' in sFilter:
                continue

            display_title = '%s [COLOR coral]%s[/COLOR]' % (movie_title, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('siteRefer', url)
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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    siteRefer = input_parameter_handler.getValue('siteRefer')

    hoster_url = url
    if 'parisanime' in url:

        html_content = unCap(url, siteRefer)

        pattern = "data-url='([^']+)'"
        results = parser.parse(html_content, pattern)
        if results[0]:
            hoster_url = results[1][0]

    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def unCap(hoster_url, url):

    request = RequestHandler(hoster_url)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
    request.addHeaderEntry('Referer', url)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    # Requete pour récupérer le cookie
    request.request()
    Cookie = request.GetCookies()

    xbmc.sleep(1000)

    request = RequestHandler(hoster_url)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
    request.addHeaderEntry('Host', 'parisanime.com')
    request.addHeaderEntry('Referer', hoster_url)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request.addHeaderEntry('Cookie', Cookie)
    request.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    request.addHeaderEntry('Connection', 'keep-alive')
    html_content = request.request()
    return html_content


def GetHostname(url):
    hoster = HosterGui().checkHoster(url)
    if hoster:
        return hoster.getDisplayName()
    try:
        if 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
    except BaseException:
        host = url
    return host.capitalize()


def cleanDesc(desc):
    parser = Parser()
    pattern = '(<.+?>)'
    results = parser.parse(desc, pattern)
    if results[0]:
        for entry in results[1]:
            desc = desc.replace(entry, '')
    return desc
