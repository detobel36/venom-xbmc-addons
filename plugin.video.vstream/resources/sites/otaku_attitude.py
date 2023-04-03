# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager  # , isMatrix
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'otaku_attitude'
SITE_NAME = 'Otaku-Attitude'
SITE_DESC = 'Animes, Drama et OST en DDL et Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json
OST_MAIN = "https://forum.otaku-attitude.net/musicbox/playlists/"

URL_SEARCH_ANIMS = (URL_MAIN + 'recherche.html?cat=1&q=', 'showAnimes')
URL_SEARCH_DRAMAS = (URL_MAIN + 'recherche.html?cat=2&q=', 'showAnimes')
FUNCTION_SEARCH = 'showAnimes'

ANIM_ANIMS = ('http://', 'load')
ANIM_VOSTFRS = (URL_MAIN + 'liste-dl-animes.php', 'showAnimes')

DRAMA_SERIES = (URL_MAIN + 'liste-dl-dramas.php', 'showAnimes')

OST_ANIME = (True, 'showGenres')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Animés)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche (Dramas)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_SERIES[1],
        'Dramas (VOSTFR)',
        'dramas.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', OST_ANIME[0])
    gui.addDir(
        SITE_IDENTIFIER,
        OST_ANIME[1],
        'Musicbox (OST)',
        'music.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = [['Animés', '1-anime'], ['Dramas', '6-drama'],
             ['Jeux Vidéo', '7-jeu-vidéo']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', OST_MAIN + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showOst',
            title,
            'music.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text.replace(' ', '+')
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showAnimes(search=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search

    # On mémorise le lien de base ce qui permet d'avoir un nextpage
    # fonctionnel sans modif et peu importe la categorie
    if not search:
        if 'scroll' not in url:
            memorisedUrl = url
            Page = 1
        else:
            memorisedUrl = input_parameter_handler.getValue('memorisedUrl')
            Page = input_parameter_handler.getValue('Page')

    request_handler = RequestHandler(url)
    request_handler.disableSSL()
    html_content = request_handler.request()

    parser = Parser()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_DRAMAS[0], '')
        search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
        search_text = util.CleanName(search_text)
        pattern = 'href="([^"]+)" class="liste_dl"><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)</.+?>'
    else:
        pattern = 'href="([^"]+)".+?><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)<br.+?>'

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

            url2 = URL_MAIN + entry[0]
            thumb = entry[1] + "|verifypeer=false"
            title = entry[2].replace(
                '-...',
                '').replace(
                '...',
                '').replace(
                '!',
                ' !')
            desc = entry[3]

            # filtre search
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addAnime(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        Page = int(Page) + 1
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', memorisedUrl + '?&scroll=' + str(Page))
        # On renvoie l'url memoriser et le numero de page pour l'incrementer a
        # chaque fois
        output_parameter_handler.addParameter('memorisedUrl', memorisedUrl)
        output_parameter_handler.addParameter('Page', Page)
        gui.addNext(
            SITE_IDENTIFIER,
            'showAnimes',
            'Page ' + str(Page),
            output_parameter_handler)

        gui.setEndOfDirectory()


def showOst():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'page' not in url:
        memorisedUrl = url
        Page = 1
    else:
        memorisedUrl = input_parameter_handler.getValue('memorisedUrl')
        Page = input_parameter_handler.getValue('Page')

    request_handler = RequestHandler(url)
    request_handler.disableSSL()
    html_content = request_handler.request()

    parser = Parser()
    pattern = "<div class='plWrapper'>.+?href='([^']+)' title='([^']+)'.+?src=\"([^\"]+)\""
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
            title = entry[1].replace('- Artiste non défini', '')
            thumb = entry[2]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addAnime(
                SITE_IDENTIFIER,
                'showMusic',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        Page = int(Page) + 1
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'site_url', memorisedUrl + '?page=' + str(Page))
        # On renvoie l'url memoriser et le numero de page pour l'incrementer a
        # chaque fois
        output_parameter_handler.addParameter('memorisedUrl', memorisedUrl)
        output_parameter_handler.addParameter('Page', Page)
        gui.addNext(
            SITE_IDENTIFIER,
            'showOst',
            'Page ' + str(Page),
            output_parameter_handler)

        gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    request_handler.disableSSL()
    html_content = request_handler.request()

    # On recupere l'id de l'anime dans l'url
    serieID = re.search('fiche-.+?-(\\d+)-.+?.html', url).group(1)
    pattern = 'class="(?:download cell_impaire|download)" id="([^"]+)".+?(\\d+).+?class="cell".+?>([^<]+)</td'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in sorted(results[1], key=lambda results: results[1]):
            qual = entry[2]

            # if isMatrix():  # plante sous matrix !!!!!!
            # qual = qual.encode('latin-1').decode()

            # Changemement de formats ...x... -> ....P
            if '1920×' in qual or '1440×' in qual or '1904×' in qual:
                qual = re.sub('(\\d+×\\d+)px', '[1080P]', qual)
            elif '1728×' in qual:
                qual = re.sub('(\\d+×\\d+)px', '[800P]', qual)
            elif '1280×' in qual:
                # VSlog(qual)
                qual = re.sub('(\\d+×\\d+)px', '[720P]', qual)
            elif '1024×' in qual:
                qual = re.sub('(\\d+×\\d+)px', '[600P]', qual)
            elif '480×' in qual:
                qual = re.sub('(\\d+×\\d+)px', '[360P]', qual)
            else:
                qual = re.sub('(\\d+×\\d+)px', '[480P]', qual)

            title = 'E' + entry[1] + ' ' + movie_title
            display_title = title + ' ' + qual
            idEpisode = entry[0]

            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('serieID', serieID)
            output_parameter_handler.addParameter('idEpisode', idEpisode)
            output_parameter_handler.addParameter('qual', qual)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMusic():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    parser = Parser()
    request_handler = RequestHandler(url)
    request_handler.disableSSL()
    html_content = request_handler.request()
    pattern = '<div data-track-file="([^"]+)".+?data-track-name="([^"]+)".+?"><span.+?>([^<]+)</span>'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry[2] + ' ' + entry[1]
            mp3Url = entry[0]

            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('mp3Url', mp3Url)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showMp3',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMp3():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    mp3Url = input_parameter_handler.getValue('mp3Url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

#     if 'mp3' in mp3Url:
#         hoster_url = mp3Url

    hoster = HosterGui().checkHoster('.m3u8')
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, mp3Url + "|verifypeer=false",
                               thumb, input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    serieID = input_parameter_handler.getValue('serieID')
    idEpisode = input_parameter_handler.getValue('idEpisode')

    hoster_url = ''
    if 'fiche-anime' in url:
        hoster_url = URL_MAIN + 'launch-download-1-' + \
            serieID + '-ddl-' + idEpisode + '.html'
    elif 'fiche-drama' in url:
        hoster_url = URL_MAIN + 'launch-download-2-' + \
            serieID + '-ddl-' + idEpisode + '.html'

    hoster = HosterGui().checkHoster('.m3u8')
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url + "|verifypeer=false",
                               thumb, input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
