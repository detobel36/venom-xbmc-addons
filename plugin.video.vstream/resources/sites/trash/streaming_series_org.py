# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False


SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming Séries'
SITE_DESC = 'Séries en streaming vf gratuitement sur Série Streaming'

URL_MAIN = 'https://www.streamingseries.biz/'

SERIE_NEWS = (URL_MAIN + 'film-archive/',
              'showMovies')  # astuce anti caroussel
SERIE_SERIES = ('http://', 'load')
SERIE_VFS = (URL_MAIN + 'version-francaise-vf/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'version-francaise-vf/?sort=views', 'showMovies')
SERIE_COMMENTS = (
    URL_MAIN +
    'version-francaise-vf/?sort=comments',
    'showMovies')
SERIE_LIST = (True, 'AlphaSearch')


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSerieSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_COMMENTS[1],
        'Séries (Les plus commentées)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def AlphaSearch():
    gui = Gui()

    for i in range(0, 27):

        if (i < 1):
            sLetter = '[0-9]'
        else:
            sLetter = chr(64 + i)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sLetter', sLetter)
        gui.addDir(
            SITE_IDENTIFIER,
            'AlphaDisplay',
            '[COLOR teal] Lettre [COLOR red]' +
            sLetter +
            '[/COLOR][/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def AlphaDisplay():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    sLetter = input_parameter_handler.getValue('sLetter')

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    pattern = '<a href="([^"]+?)" >(' + sLetter + '[^<]+?)<'
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)

            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="movie-poster">.+?href="([^<]+)".+?src="([^<]+)" alt="(.+?)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            thumb = entry[1]
            title = entry[2]

            # Si recherche et trop de resultat, on nettoye
            if search and total > 2:
                if cUtil().CheckOccurence(
                        search.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', thumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

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
    parser = Parser()
    pattern = '<div class="keremiya-loadnavi-.+?href="(.+?)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div class="movie-poster".+?src="([^"]+)".+?href="([^<]+)" title="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            url = entry[1]
            title = entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', thumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # recuperation du hoster de base
    pattern = '<div class="part active".+?class="part-name">(.+?)<\\/div>'
    results = parser.parse(html_content, pattern)

    ListeUrl = []
    if results[0]:
        ListeUrl = [(url, results[1][0])]

    # Recuperation des suivants
    pattern = '<a href="([^<]+)"><div class="part "> *<div class="part-name">([^<]+)<\\/div>'
    results = parser.parse(html_content, pattern)
    ListeUrl = ListeUrl + results[1]

    if results[0]:
        total = len(ListeUrl)
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in ListeUrl:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            title = movie_title + entry[1].replace('Part', 'Episode')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    # si un seul episode
    else:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter(
            'movie_title', movie_title + 'episode 1 ')
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addTV(
            SITE_IDENTIFIER,
            'showHosters',
            movie_title +
            'episode 1 ',
            '',
            thumb,
            '',
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
    html_content = html_content.replace('<iframe src="//www.facebook.com/', '')
    html_content = html_content.replace('\r', '')
    # on réécris pour récupérer la langue
    html_content = html_content.replace(
        'VF</strong>', 'VF</b>').replace('</font></u>', '')
    html_content = html_content.replace(
        '- Version Française',
        '').replace(
        'Version Française',
        'VF')
    # on réécris pour récupérer les hosters
    html_content = html_content.replace('<p><script', '<iframe')

    pattern = '(VF|VF |VOSTFR)<\\/b><\\/p>|<iframe.+?=[\'|"](.+?)[\'|"]'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # langue
            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]')
            # hote
            else:
                hoster_url = entry[1]
                if '//goo.gl' in hoster_url:
                    import urllib2
                    try:

                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                        request = urllib2.Request(hoster_url, None, headers)
                        reponse = urllib2.urlopen(request)
                        hoster_url = reponse.geturl()
                    except BaseException:
                        pass

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
