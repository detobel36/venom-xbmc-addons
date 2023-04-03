# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'skyanimes'
SITE_NAME = 'Sky-Animes'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

STREAM = 'index.php?file=Media&nuked_nude=index&op=do_dl&dl_id='

INDEX = 'index.php?file=Search&op=mod_search&searchtype=matchand&autor=&module=Download&limit=100&main='
URL_SEARCH_ANIMS = (URL_MAIN + INDEX, 'showEpisode')
# URL_SEARCH_DRAMAS = (URL_MAIN + INDEX, 'showEpisode')
FUNCTION_SEARCH = 'showEpisode'

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_GENRES = (True, 'showGenresA')
ANIM_VOSTFRS = (URL_MAIN + 'streaming-films', 'showSeries')
ANIM_OAVS = (URL_MAIN + 'streaming-oavs', 'showSeries')

DRAMA_DRAMAS = (True, 'showMenuDramas')
DRAMA_GENRES = (True, 'showGenresD')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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


def showMenuAnims():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (Films)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'streaming-animes-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-animes-termines?p=-1'])

    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'animes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuDramas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Dramas (Genres)',
        'genres.png',
        output_parameter_handler)

    # contenu à contrôler
    # output_parameter_handler.addParameter('site_url', ANIM_OAVS[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_OAVS[1], 'Dramas (OAVS)', 'dramas.png', output_parameter_handler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'download-dramas-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-dramas-termines?p=-1'])

    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'dramas.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenresA():
    gui = Gui()
    parser = Parser()

    url = URL_MAIN + 'streaming-animes-en-cours'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = 'id="id_genre"'
    end = '<select id="triGenre"'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

        gui.setEndOfDirectory()


def showGenresD():
    gui = Gui()
    parser = Parser()

    url = URL_MAIN + 'download-dramas-en-cours?p=-1'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = 'id="id_genre"'
    end = '<select id="triGenre"'
    html_content = parser.abParse(html_content, start, end)

    pattern = '<a href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN + entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

        gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text.replace(' ', '+')
        showEpisode(url)
        gui.setEndOfDirectory()
        return


def showSeries():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url').replace(
        '+',
        '%2B').replace(
        'é',
        'e').replace(
            'ô',
            'o') .replace(
                'É',
                'E').replace(
                    'ï',
                    'i').replace(
                        'è',
        'e')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a href="([^"]+)"><img src="([^"]+)" width.+?alt="([^"]+).+?></a>'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME, large=(total > 50))
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = entry[2]
            url2 = URL_MAIN + entry[0]
            thumb = URL_MAIN + entry[1].replace(' ', '%20')
            desc = ''

            title = title.replace(', telecharger en ddl', '')

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)

            if '-animes-' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()


def showEpisode(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    if thumb:
        thumb = thumb.replace(' ', '%20')

    if search:
        url = search

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    if search:
        pattern = '<a href=".+?id=([^"]+)"><b>(.+?)</b>'
    else:
        pattern = '<td style="padding-left: 12px;"><a href="([^"]+).+?><b><img.+?>(.+?)</b>.+?</a>'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in sorted(results[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if search:
                title = entry[1]
                title, sTitle1 = title.replace(
                    '1080p', '').replace(
                    'BD', '').replace(
                    'V2', '').replace(
                    'FIN', '') .replace(
                    'Fin', '').replace(
                        'fin', '').replace(
                            'OAV', '').replace(
                                'Bluray', '') .replace(
                                    'Blu-Ray', '').rstrip().rsplit(
                                        ' ', 1)
                title = 'E' + sTitle1 + ' ' + title
                url2 = URL_MAIN + STREAM + entry[0]
                thumb = ''
            else:
                title = entry[1]
                title, sTitle1 = title.replace(
                    '1080p', '').replace(
                    'BD', '').replace(
                    'V2', '').replace(
                    'FIN', '') .replace(
                    'Fin', '').replace(
                        'fin', '').replace(
                            'OAV', '').replace(
                                'Bluray', '') .replace(
                                    'Blu-Ray', '').rstrip().rsplit(
                                        ' ', 1)
                title = 'E' + sTitle1 + ' ' + title
                url2 = URL_MAIN + STREAM + entry[0]
                url2 = url2.replace('#', '')

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)
    if not search:
        gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    if thumb:
        thumb = thumb.replace(' ', '%20')
    hoster = HosterGui().checkHoster('.m3u8')

    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
