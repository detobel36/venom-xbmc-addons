# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'wiflix'
SITE_NAME = 'Wiflix'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_EXCLU = (URL_MAIN + 'film-en-streaming/exclue', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
SERIE_NEWS = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN, 'showSearch')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showSearch'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://film')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://serie')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Séries',
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

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_EXCLU[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLU[1],
        'Films et Séries (Exclus)',
        'news.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:

        if 'film' in url:
            showMovies(search_text)
        else:
            showSeries(search_text)

        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()

    url = URL_MAIN
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '</span><b>Films par genre</b></div>'
    end = '<div class="side-b">'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if results[0]:
        for entry in results[1]:
            url = URL_MAIN + entry[0]
            title = entry[1].capitalize()
            TriAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in TriAlpha:
            output_parameter_handler.addParameter('site_url', url)
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
        search_text = util.CleanName(search.replace('%20', ' '))

        pdata = 'do=search&subaction=search&story=' + \
            search_text.replace(' ', '+') + '&titleonly=3&all_word_seach=1&catlist[]=1'

        request = RequestHandler(URL_SEARCH[0])
        # request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry('Origin', URL_MAIN)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(pdata)
        html_content = request.request()

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    pattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:|bloc1">([^<]+).+?)(?:|bloc2">([^<]*).+?)'
    pattern += 'ml-desc"> (?:([0-9]+)| )</div.+?Synopsis:.+?ml-desc">(.*?)</div'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:
            thumb = entry[0]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + entry[0]
            title = entry[1].replace(' wiflix', '')
            url = entry[2]
            lang = entry[3]
            qual = entry[4]
            year = entry[5]
            if year in title:  # double affichage de l'année
                title = re.sub('\\(' + year + '\\)', '', title)

            # Filtre de recherche
            if search and not util.CheckOccurence(search_text, title):
                continue

            # Nettoyage du synopsis
            desc = str(entry[6])
            desc = desc.replace('en streaming ', '')
            desc = desc.replace('Regarder film ' + title + ';', '')
            desc = desc.replace('Regarder film ' + title + ':', '')
            desc = desc.replace('Voir film ' + title + ';', '')
            desc = desc.replace('Voir film ' + title + ':', '')
            desc = desc.replace('Voir Film ' + title + ':', '')
            desc = desc.replace('Voir film ' + title + ' :', '')
            desc = desc.replace('Regarder ' + title + ';', '')
            desc = desc.replace('Regarder ' + title + ' :', '')
            desc = desc.replace('Regarder ' + title + ':', '')
            desc = desc.replace('voir ' + title + ';', '')
            desc = desc.replace('voir ' + title + ':', '')
            desc = desc.replace('Voir ' + title + ':', '')
            desc = desc.replace('Regarder film ', '')
            desc = desc.strip()

            display_title = '%s [%s] (%s)' % (title, qual, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter('qual', qual)

            if 'serie-en-streaming' in url:
                gui.addSeason(
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

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)
    else:
        gui.addText(SITE_IDENTIFIER)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSeries(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        util = cUtil()
        search_text = util.CleanName(search.replace('%20', ' '))
        url = search.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + url + \
            '&titleonly=3&all_word_seach=1&catlist[]=31&catlist[]=35'

        request = RequestHandler(URL_SEARCH[0])
        # request.setRequestType(1)
        request.addHeaderEntry('User-Agent', UA)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        request.addParametersLine(pdata)
        html_content = request.request()

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    pattern = 'mov clearfix.+?src="([^"]+)" *alt="([^"]+).+?data-link="([^"]+).+?block-sai">([^<]+).+?ml-desc">(.+?)</div>'

    results = parser.parse(html_content, pattern)
    if results[0]:
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:
            thumb = entry[0]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + entry[0]

            title = entry[1].replace(
                '- Saison',
                'saison').replace(
                ' wiflix',
                '')

            # Filtre de recherche
            if search and not util.CheckOccurence(search_text, title):
                continue

            # lang = re.sub('Saison \d+', '', entry[3]).replace(' ', '')
            display_title = title
            url = entry[2]
            desc = entry[4]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                display_title,
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
                'showSeries',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<div class="(ep.+?)"|<a href="([^"]+)"[^><]+target="x_player"'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    # Afficher le numero de l episode et la saison dans le titre
    # permet de marquer vu avec trakt automatiquement.
    ep = 0
    lang = ''

    if results[0]:
        for entry in results[1]:
            if entry[0]:

                if 'vs' in entry[0]:
                    lang = ' (VOSTFR)'
                elif 'vf' in entry[0]:
                    lang = ' (VF)'

                if 'epblocks' in entry[0]:
                    continue

                ep = entry[0].replace(
                    'ep',
                    'Episode ').replace(
                    'vs',
                    '').replace(
                    'vf',
                    '')

            if entry[1]:
                title = movie_title + ' ' + ep + lang
                hoster_url = entry[1].replace('/vd.php?u=', '')
                if 'players.wiflix.' in hoster_url:
                    request_handler = RequestHandler(hoster_url)
                    request_handler.request()
                    hoster_url = request_handler.getRealUrl()

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a href="\\/vd.php\\?u=([^"]+)"[^<>]+target="x_player_wfx"><span>([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]  # .replace('/wiflix.cc/', '')
            if 'wiflix.' in hoster_url:
                request_handler = RequestHandler(hoster_url)
                request_handler.request()
                hoster_url = request_handler.getRealUrl()
            else:
                hoster_url = entry[0].replace('/wiflix.cc/', '')
            lang = entry[1].replace('2', '').replace('3', '')
            if 'Vost' in entry[1]:
                display_title = ('%s (%s)') % (movie_title, lang)
            else:
                display_title = movie_title
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(display_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
