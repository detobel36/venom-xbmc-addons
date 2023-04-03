# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'frenchanimes'
SITE_NAME = 'French Animes'
SITE_DESC = 'Mangas en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showAnimes')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showAnimes')
ANIM_MOVIE = (URL_MAIN + 'films-vf-vostfr/', 'showAnimes')
ANIM_GENRES = (True, 'showGenres')

URL_SEARCH = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&story=',
    'showSearch')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showAnimes')
FUNCTION_SEARCH = 'showSearch'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://animes')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
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

    output_parameter_handler.addParameter('site_url', ANIM_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE[1],
        'Animés (Films)',
        'animes.png',
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
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    parser = Parser()

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '</span><b>Animes par genre</b></div>'
    end = '<div class="side-b">'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if results[0]:
        for entry in results[1]:
            url = URL_MAIN[:-1] + entry[0]
            title = entry[1].capitalize()
            TriAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in TriAlpha:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAnimes',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showAnimes(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:sai">([^<]+[0-9]).+?|)Version'
    pattern += '.+?desc">([^<]*).+?Synopsis:.+?desc">(.*?)</d'
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

            thumb = entry[0]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            title = entry[1].replace(' wiflix', '')
            url = entry[2]
            sSaison = entry[3].replace('Saison', 'Saison ')
            lang = entry[4]
            desc = str(entry[5])

            # la langue est parfois dans le titre
            if lang in title:
                title = title.replace(lang, '')

            sDisplaytitle = '%s %s (%s)' % (title, sSaison, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if 'films-vf-vostfr' in url:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplaytitle,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplaytitle,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showAnimes',
                'Page ' + paging,
                output_parameter_handler)

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


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    start = 'class="eps" style="display: none">'
    end = '/div>'
    html_content = parser.abParse(html_content, start, end)
    # Pour les liens myvi
    html_content = html_content.replace(
        '!//', '!https://').replace(',//', ',https://')

    # Besoin des saut de ligne
    html_content = html_content.replace('\n', '@')

    pattern = '([0-9]+)!|(https:.+?)[,|<@]'
    results = parser.parse(html_content, pattern)

    ep = 0

    if results[0]:
        for entry in results[1]:

            if entry[0]:
                ep = 'Episode ' + entry[0]
                gui.addText(SITE_IDENTIFIER, '[COLOR red]' + ep + '[/COLOR]')
            if entry[1]:
                title = movie_title + ' ' + ep
                hoster_url = entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    start = 'class="eps" style="display: none">'
    end = '/div>'
    html_content = parser.abParse(html_content, start, end)
    # Pour les liens myvi
    html_content = html_content.replace(
        '!//', '!https://').replace(',//', ',https://')

    pattern = '(https:.+?)[,|<]'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
