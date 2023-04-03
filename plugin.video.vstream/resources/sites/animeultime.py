# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto et Arias800 02/06/2019
import re

from resources.lib.comaddon import Addon, isMatrix, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'animeultime'
SITE_NAME = 'Anime Ultime'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

URL_SEARCH_DRAMAS = (URL_MAIN + 'search-0-1+', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'search-0-1+', 'showSeries')

ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_ANNEES = (True, 'ShowYearsAnimes')
ANIM_GENRES = (True, 'ShowGenreAnimes')
ANIM_ALPHA = (True, 'ShowAlphaAnimes')

DRAMA_DRAMAS = (True, 'showMenuDramas')
DRAMA_ANNEES = (True, 'ShowYearsDramas')
DRAMA_GENRES = (True, 'ShowGenreDramas')
DRAMA_ALPHA = (True, 'ShowAlphaDramas')

TOKUSATSU_TOKUSATSUS = (True, 'showMenuTokusatsu')
TOKUSATSU = (URL_MAIN + 'series-0-1/tokusatsu/0---', 'showSeries')
TOKUSATSU_ALPHA = ('true', 'ShowAlphaTokusatsu')

adulteContent = Addon().getSetting('contenu_adulte')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_DRAMAS[1],
        'Dramas',
        'dramas.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', TOKUSATSU_TOKUSATSUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU_TOKUSATSUS[1],
        'Tokusatsu',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnimes():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ALPHA[1],
        'Animés  (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuDramas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DRAMA_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_ALPHA[1],
        'Dramas (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Dramas (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DRAMA_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_ANNEES[1],
        'Dramas (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTokusatsu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', TOKUSATSU[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU[1],
        'Tokusatsu',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', TOKUSATSU_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU_ALPHA[1],
        'Tokusatsu (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def loadTypelist(typemovie, typelist):
    # typelist genre ou year
    # <select name="genre"
    # <select name="year"
    url = URL_MAIN + 'series-0-1/' + typemovie

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = '<select name="([^"]+)|<option value=\'([^\']+).*?>([^<]+)'
    results = parser.parse(html_content, pattern)

    list_typelist = {}

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                if entry[0] == typelist:
                    bfind = True
                else:
                    bfind = False

            if bfind and entry[1]:
                if not isMatrix():
                    title = entry[2].decode('iso-8859-1').encode('utf8')
                else:
                    title = entry[2]
                title = title.replace('e', 'E').strip()
                list_typelist[title] = entry[1]

    list_typelist = sorted(
        list_typelist.items(),
        key=lambda typeList: typeList[0])

    return list_typelist


def ShowGenreAnimes():
    ShowGenre('anime')


def ShowGenreDramas():
    ShowGenre('drama')


def ShowGenre(typemovie):
    gui = Gui()
    list_listgenre = loadTypelist(typemovie, 'genre')
    output_parameter_handler = OutputParameterHandler()
    for ilist in list_listgenre:
        url = URL_MAIN + 'series-0-1/' + typemovie + '/-' + ilist[1] + '---'
        title = ilist[0].title()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowYearsAnimes():
    ShowYears('anime')


def ShowYearsDramas():
    ShowYears('drama')


def ShowYears(typemovie):
    gui = Gui()
    list_year = loadTypelist(typemovie, 'year')
    # http://www.anime-ultime.net/series-0-1/anime/--626--    2019
    output_parameter_handler = OutputParameterHandler()
    for liste in reversed(list_year):
        url = URL_MAIN + 'series-0-1/' + typemovie + '/--' + liste[1] + '--'
        title = liste[0]
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowAlphaAnimes():
    ShowAlpha('anime')


def ShowAlphaDramas():
    ShowAlpha('drama')


def ShowAlphaTokusatsu():
    ShowAlpha('tokusatsu')


def ShowAlpha(typemovie):
    gui = Gui()

    import string
    # http://www.anime-ultime.net/series-0-1/tokusatsu/c---
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = [['#', URL_MAIN + 'series-0-1/' + typemovie + '/' + '1---']]
    for alpha in listalpha:
        liste.append([str(alpha).upper(), URL_MAIN +
                     'series-0-1/' + typemovie + '/' + alpha + '---'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text
        showSeries(url)
        gui.setEndOfDirectory()
        return


def showSeries(search=''):
    gui = Gui()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_DRAMAS[0], '')
        search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
        search_text = util.CleanName(search_text)
        url = search.replace(' ', '+').replace('%20', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    if search:
        pattern = '<td class=".+?<a href="([^"]+)".+?<img src=.+?img=([^>]+)\\/>.+?onMouseOut.+?>(.+?)<\\/a>.+?<td class="" align="center">([^<]+)<'
    else:
        pattern = '<td class=".+?<a href="([^"]+)".+?<img src=([^>]+)\\/>.+?alt="([^"]+).+?align="center">([^<]+)<'

    results = parser.parse(html_content, pattern)

    # Si il y a qu'un seule resultat alors le site fait une redirection.
    if not results[0]:
        output_parameter_handler = OutputParameterHandler()
        if search and "sultats anime" not in html_content:
            title = ''
            try:
                title = re.search('<h1>([^<]+)', html_content).group(1)
            except BaseException:
                pass
            if title:
                url2 = url
                thumb = ''

                # Enleve le contenu pour adultes.
                if 'Public Averti' in title or 'Interdit' in title:
                    if adulteContent == "false":
                        gui.addText(
                            SITE_IDENTIFIER,
                            '[COLOR red]Contenu pour adultes désactivé[/COLOR]')
                        return

                output_parameter_handler.addParameter('site_url', url2)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)

                if '/anime/' in url:
                    gui.addAnime(
                        SITE_IDENTIFIER,
                        'showEpisode',
                        title,
                        '',
                        thumb,
                        '',
                        output_parameter_handler)
                else:
                    gui.addDrama(
                        SITE_IDENTIFIER,
                        'showEpisode',
                        title,
                        '',
                        thumb,
                        '',
                        output_parameter_handler)

            else:
                gui.addText(SITE_IDENTIFIER)
        else:
            gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry[2]
            if search:
                # Enleve les balise.
                try:
                    title = re.sub('<.*?>', '', title)
                except BaseException:
                    pass

            try:
                title = title.decode('iso-8859-1').encode('utf8')
            except BaseException:
                pass

            url2 = URL_MAIN + entry[0]
            thumb = entry[1]

            if adulteContent == "false":
                # Enleve le contenu pour adulte.
                if 'Public Averti' in title or 'Interdit' in title:
                    continue

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            _type = entry[3].strip()
            title += ' [%s]' % _type

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if _type != 'Episode':
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '/anime/' in url:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    desc = ''
    try:
        pattern = 'src="images.+?(?:<br />)(.+?)(?:<span style|TITRE ORIGINAL|ANNÉE DE PRODUCTION|STUDIO|GENRES)'

        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0].replace('<br>', '').replace('<br />', '')
            desc = desc.replace(
                'Synopsis',
                '').replace(
                'synopsis',
                '').replace(
                ':',
                ' ')
            desc = ('[I][COLOR coral]%s[/COLOR][/I] %s') % ('Synopsis :', desc)

            # Enleve les balises.
            try:
                desc = re.sub('<.*?>', '', desc)
            except BaseException:
                pass
    except BaseException:
        pass

    pattern = '<tr.+?align="left">.+?align="left">([^"]+)</td>.+?nowrap>+?<.+?</td>.+?<.+?/td>.+?<.+?<a href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            title = entry[0]
            try:
                title = title.decode('iso-8859-1').encode('utf8')
            except BaseException:
                pass

            lang = ''
            if ' vostfr' in title:
                lang = 'VOSTFR'
            if ' vf' in title:
                lang = 'VF'
            title = entry[0].replace(
                '[',
                '').replace(
                ']',
                '').replace(
                'FHD',
                '').replace(
                'vostfr',
                '').replace(
                    'vf',
                    '').replace(
                        'HD',
                        '').replace(
                            'HQ',
                '').strip()
            if '(saison' in title:
                title = title.replace('(', '').replace(')', '')
            sEpisode = title.split(' ')[-1]
            title = title.replace(sEpisode, ' Episode ' + sEpisode).strip()
            sDisplayTtitle = title + ' [' + lang + ']'

            url2 = URL_MAIN + entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTtitle,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'id="stream">Streaming <span itemprop="name">([^<]+)<.+?thumbnailUrl" content="([^\"]+)".+?contentURL" content="([^\"]+)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            title = entry[0].strip()
            if ' vostfr' in title:
                lang = 'VOSTFR'
            if ' vf' in title:
                lang = 'VF'
            title = ('%s - [%s]') % (movie_title, lang)

            thumb = entry[1]
            hoster_url = entry[2]
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
