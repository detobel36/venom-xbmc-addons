# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re

from resources.lib.comaddon import Addon, isMatrix, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil, Unquote


SITE_IDENTIFIER = 'uptobox_live'
SITE_NAME = '[COLOR violet]Uptobox Live[/COLOR]'
SITE_DESC = 'Bibliothèque de liens Uptobox'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = ('search?sort=size&order=desc&q=', 'showMovies')
URL_SEARCH_SERIES = ('search?sort=id&order=asc&q=', 'showSeries')
URL_SEARCH_ANIMS = ('search?sort=id&order=asc&q=', 'showAnims')

MOVIE_MOVIE = ('films', 'load')
SERIE_SERIES = ('series', 'load')


def load():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if 'series' not in url:
        output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
        output_parameter_handler.addParameter('movie_title', 'movie')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Recherche (Films)',
            'search.png',
            output_parameter_handler)

    if 'films' not in url:
        output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
        output_parameter_handler.addParameter('movie_title', 'tv')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Recherche (Séries)',
            'search.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def opensetting():
    Addon().openSettings()


def showSearch(path='//'):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')

    search_text = gui.showKeyBoard()
    if search_text:
        sUrlSearch = url + search_text

        if title == 'movie':
            showMovies(sUrlSearch, True)
        else:
            showSeries(sUrlSearch, True)


def getAuthorizedID():
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    html_content = RequestHandler(URL_MAIN).request()
    pattern = "Authorization': '(.+?)'"
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return False


def getContent(url):

    url = url.replace(' ', '%20')
    videoId = getAuthorizedID()

    request = RequestHandler(URL_MAIN + url)
    request.addHeaderEntry('Referer', URL_MAIN)
    request.addHeaderEntry('Authorization', videoId)
    html_content = request.request()

    content = json.loads(html_content)

#    if content['status'] == 'unauthorized':
    if content['status'] == 'ok':
        return content['items']

    return []


def showMovies(search='', searchLocal=False):
    gui = Gui()
    util = cUtil()

    if not search:
        searchLocal = True
        input_parameter_handler = InputParameterHandler()
        search = input_parameter_handler.getValue('site_url')
    search_text = search.replace(URL_SEARCH_MOVIES[0], '')
    search_text = Unquote(search_text)
    search_text = util.CleanName(search_text)

    url = search.replace('-', '\\-').replace('.', '%20')
    content = getContent(url)

    output_parameter_handler = OutputParameterHandler()
    movies = set()
    bMatrix = isMatrix()
    for movie in content:
        title = movie['title']
        if not bMatrix:
            title = title.encode('utf-8')

        # seulement les formats vidéo
        if title[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
            continue
        # enlever l'extension
        title = title[:-4]

        title = title.replace('CUSTOM', '')
        if '1XBET' in title:  # or 'HDCAM'
            continue

        # recherche des métadonnées
        pos = len(title)
        tmdb_id, pos = getIdTMDB(title, pos)
        if tmdb_id:
            title = title.replace('.TM%sTM.' % tmdb_id, '')
            pos = len(title)

        year, pos = getYear(title, pos)
        resolution, pos = getReso(title, pos)
        lang, pos = getLang(title, pos)
        title, sa, ep = getSaisonEpisode(title)

        # enlever les séries
        if not sa or not ep:
            title = title[:pos]
            title, sa, ep = getSaisonEpisode(title)
        if sa or ep:
            continue

        movie_title = title[:pos]
        movie_title = util.unescape(movie_title).strip()
        movie_title = movie_title.replace('.', ' ')

        if not util.CheckOccurence(search_text, movie_title):
            continue    # Filtre de recherche

        # lien de recherche spécifique à chaque film
        site_url = URL_SEARCH_MOVIES[0] + movie_title.replace('-', '\\-')
        startWith = movie_title[0].upper()
        if startWith.isdigit():
            startWith = 'number'
        site_url += '&start\\-with=' + startWith

        search_title = util.CleanName(movie_title)
        if year:
            search_title += ' (%s)' % year

        if search_title in movies:
            continue                # film déjà proposé

        movies.add(search_title)

        output_parameter_handler.clearParameter()
        output_parameter_handler.addParameter('site_url', site_url)
        output_parameter_handler.addParameter('movie_title', search_title)
        output_parameter_handler.addParameter('year', year)
        output_parameter_handler.addParameter('tmdb_id', tmdb_id)
        gui.addMovie(
            SITE_IDENTIFIER,
            'showHosters',
            movie_title,
            'films.png',
            '',
            '',
            output_parameter_handler)

    if searchLocal:
        gui.setEndOfDirectory()


def showAnims(search=''):
    showSeries(search, False, True)


def showSeries(search='', searchLocal=False, isAnime=False):
    gui = Gui()
    util = cUtil()

    search_title = search.replace(URL_SEARCH_SERIES[0], '')
    search_title = Unquote(search_title)
    search_title = util.CleanName(search_title)

    url = search.replace('-', '\\-')

    series = set()
    output_parameter_handler = OutputParameterHandler()

    # deux url pour plus de résultats
    urls = [url, url.replace('order=asc', 'order=desc')]
    bMatrix = isMatrix()
    for url in urls:
        content = getContent(url)
        for file in content:
            title = file['title']
            if not bMatrix:
                title = title.encode('utf-8')

            if title[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            title = title[:-4]

            # recherche des métadonnées
            pos = len(title)
            tmdb_id, pos = getIdTMDB(title, pos)
            if tmdb_id:
                title = title.replace('.TM%sTM.' % tmdb_id, '')
                pos = len(title)
            year, pos = getYear(title, pos)
            resolution, pos = getReso(title, pos)
            lang, pos = getLang(title, pos)
            title, saison, episode, pos = getSaisonEpisode(title, pos)

            # Recherche des noms de séries
            if not saison or not episode:
                title = title[:pos]
                pos = len(title)
                title, saison, episode, pos = getSaisonEpisode(title, pos)

            if saison:
                if int(saison) > 100:
                    continue
                title = title[:pos]
                display_title = util.unescape(title).strip()
                display_title = display_title.replace('.', ' ')

                if not util.CheckOccurence(search_title, display_title):
                    continue    # Filtre de recherche

                movie_title = util.CleanName(display_title)
                if year:
                    movie_title += ' (%s)' % year
                if movie_title in series:
                    continue
                series.add(movie_title)

                output_parameter_handler.clearParameter()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('year', year)
                output_parameter_handler.addParameter(
                    'tmdb_id', tmdb_id)  # Utilisé par TMDB
                if isAnime:
                    gui.addAnime(
                        SITE_IDENTIFIER,
                        'showSaisons',
                        display_title,
                        '',
                        '',
                        '',
                        output_parameter_handler)
                else:
                    gui.addTV(
                        SITE_IDENTIFIER,
                        'showSaisons',
                        display_title,
                        '',
                        '',
                        '',
                        output_parameter_handler)

    if searchLocal:
        gui.setEndOfDirectory()


def showSaisons():
    # deux url pour plus de résultats
    gui = Gui()
    saisons = {}
    util = cUtil()

    input_parameter_handler = InputParameterHandler()
    # url = input_parameter_handler.getValue('site_url')
    search_title = input_parameter_handler.getValue('movie_title')
    sSearchYear, pos = getYear(search_title, len(search_title))
    if sSearchYear:
        search_title = search_title[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('year')

    # recherche depuis le titre sélectionné, pas depuis les mots clefs
    # recherchés
    url = URL_SEARCH_SERIES[0] + search_title.replace('-', '\\-')
    startWith = search_title[0].upper()
    if startWith.isdigit():
        startWith = 'number'
    url += '&start\\-with=' + startWith

    # deux url pour plus de résultats
    urls = [url, url.replace('order=asc', 'order=desc')]

    bMatrix = isMatrix()
    for url in urls:
        content = getContent(url)

        # Recherche des saisons
        for file in content:
            title = file['title']
            if not bMatrix:
                title = title.encode('utf-8')

            if title[-4] == '.':
                if title[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                    continue
                # enlever l'extension
                title = title[:-4]

            # recherche des métadonnées
            pos = len(title)
            tmdb_id, pos = getIdTMDB(title, pos)
            if tmdb_id:
                title = title.replace('.TM%sTM.' % tmdb_id, '')
                pos = len(title)
            year, pos = getYear(title, pos)
            resolution, pos = getReso(title, pos)
            lang, pos = getLang(title, pos)
            title, saison, episode, pos = getSaisonEpisode(title, pos)

            # vérifier l'année pour les homonymes
            if sSearchYear:
                if year:
                    if sSearchYear != year:
                        continue
                else:
                    continue
            elif year:
                continue

            # Recherche des noms de séries
            if not saison or not episode:
                title = title[:pos]
                pos = len(title)
                title, saison, episode, pos = getSaisonEpisode(title, pos)

            if saison:
                title = title[:pos]
                movie_title = util.unescape(title).strip()
                movie_title = util.CleanName(movie_title)
                if movie_title == search_title:
                    saisons[saison] = url

    output_parameter_handler = OutputParameterHandler()
    for saison, url in sorted(saisons.items(), key=lambda s: s[0]):
        display_title = '%s S%s' % (search_title, saison)
        site_url = '%s|%s' % (url, saison)
        output_parameter_handler.addParameter('site_url', site_url)
        sSaisonTitle = '%s S%s' % (search_title, saison)
        if sSearchYear:
            sSaisonTitle = '%s (%s)' % (sSaisonTitle, sSearchYear)
            output_parameter_handler.addParameter('year', sSearchYear)
        output_parameter_handler.addParameter('movie_title', sSaisonTitle)
        gui.addSeason(
            SITE_IDENTIFIER,
            'showEpisodes',
            display_title,
            '',
            '',
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():

    gui = Gui()
    util = cUtil()

    input_parameter_handler = InputParameterHandler()
    url, sSearchSaison = input_parameter_handler.getValue(
        'site_url').split('|')
    search_title = input_parameter_handler.getValue('movie_title')
    search_title = search_title.replace(' S%s' % sSearchSaison, '')

    sSearchYear, pos = getYear(search_title, len(search_title))
    if sSearchYear:
        search_title = search_title[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('year')

    content = getContent(url)

    # Recherche des épisodes
    bMatrix = isMatrix()
    episodes = set()
    for file in content:
        title = file['title']
        if not bMatrix:
            title = title.encode('utf-8')

        if title[-4] == '.':
            if title[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            title = title[:-4]

        # recherche des métadonnées
        pos = len(title)
        lang, pos = getLang(title, pos)
        resolution, pos = getReso(title, pos)
        year, pos = getYear(title, pos)
        title, saison, episode, pos = getSaisonEpisode(title, pos)

        # Vérifier la saison
        if not saison or not episode:
            title = title[:pos]
            pos = len(title)
            title, saison, episode, pos = getSaisonEpisode(title, pos)
        if not saison or saison != sSearchSaison:
            continue

        # Vérifier l'année
        if sSearchYear:
            if year:
                if sSearchYear != year:
                    continue
            else:
                continue
        elif year:
            continue

        movie_title = title[:pos]
        movie_title = util.unescape(movie_title).strip()
        movie_title = util.CleanName(movie_title)

        if movie_title != search_title:
            continue

        episodes.add(episode)

    output_parameter_handler = OutputParameterHandler()
    for episode in sorted(episodes):
        display_title = '%s S%sE%s' % (search_title, sSearchSaison, episode)

        site_url = '%s|%s|%s' % (url, sSearchSaison, episode)
        output_parameter_handler.addParameter('site_url', site_url)
        sEpTitle = '%s S%sE%s' % (search_title, sSearchSaison, episode)
        output_parameter_handler.addParameter('movie_title', sEpTitle)
        output_parameter_handler.addParameter('year', sSearchYear)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            display_title,
            '',
            '',
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():

    from resources.lib.gui.hoster import HosterGui
    gui = Gui()
    oHosterGui = HosterGui()
    hoster = oHosterGui.getHoster('lien_direct')
    util = cUtil()

    input_parameter_handler = InputParameterHandler()
    # sSearchTmdbId = input_parameter_handler.getValue('tmdb_id')
    search_title = input_parameter_handler.getValue('movie_title')
    sSearchYear, pos = getYear(search_title, len(search_title))
    if sSearchYear:
        search_title = search_title[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('year')

    url = input_parameter_handler.getValue('site_url')
    sSearchSaison = ''
    if '|' in url:
        url, sSearchSaison, sSearchEpisode = url.split('|')
        search_title = search_title.replace(
            ' S%sE%s' %
            (sSearchSaison, sSearchEpisode), '')
    search_title = util.CleanName(search_title)

    content = getContent(url)
    # retourne le bon débrideur en fonction de son compte premmium
    hoster = oHosterGui.checkHoster('uptobox')

    # Recherche les liens
    bMatrix = isMatrix()
    for file in content:
        title = file['title']
        if not bMatrix:
            title = title.encode('utf-8')

        if title[-4] == '.':
            if title[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            title = title[:-4]

        title = title.replace('CUSTOM', '')
        if '1XBET' in title:
            continue

        # Recherche des metadonnées
        pos = len(title)
        tmdb_id, pos = getIdTMDB(title, pos)
        lang, pos = getLang(title, pos)
        resolution, pos = getReso(title, pos)
        year, pos = getYear(title, pos)

        # identifier une série
        title, saison, episode, pos = getSaisonEpisode(title, pos)
        if not saison or not episode:
            title = title[:pos]
            pos = len(title)
            title, saison, episode, pos = getSaisonEpisode(title, pos)

        if sSearchSaison:   # recherche de série
            if not saison or saison != sSearchSaison:
                continue
            if not episode or episode != sSearchEpisode:
                continue
        else:  # recherche de film
            if saison or episode:
                continue

        # vérifier l'année pour les homonymes
        if sSearchYear:
            if year:
                if sSearchYear != year:
                    continue
            else:
                continue
        elif year:
            continue

        title = title[:pos]
        movie_title = util.unescape(title).strip()
        movie_title = movie_title.replace('.', ' ').lower()
        if util.CleanName(movie_title) != search_title:
            continue

        display_title = movie_title
        if saison:
            display_title += ' S%sE%s' % (saison, episode)
        if resolution:
            display_title += ' [%s]' % resolution
        if lang:
            display_title += ' (%s)' % lang
        if year:
            display_title += ' (%s)' % year
            movie_title += ' (%s)' % year
        hoster_url = file['link']

        hoster.setDisplayName(display_title)
        hoster.setFileName(movie_title)
        oHosterGui.showHoster(gui, hoster, hoster_url, '')

    gui.setEndOfDirectory()


# Recherche saisons et episodes
def getSaisonEpisode(title, pos=0):
    title = title.replace('x264', '').replace('x265', '').strip()
    sa = ep = terme = ''
    m = re.search(
        '(^S| S|\\.S|\\[S|saison|\\s+|\\.)(\\s?|\\.)(\\d+)( *- *|\\s?|\\.)(E|Ep|x|\\wpisode|Épisode)(\\s?|\\.)(\\d+)',
        title,
        re.UNICODE | re.IGNORECASE)
    if m:
        sa = m.group(3)
        if int(sa) < 100:
            ep = m.group(7)
            terme = m.group(0)
        else:
            sa = ''
    else:  # Juste l'épisode
        m = re.search(
            '(^|\\s|\\.)(E|Ep|\\wpisode)(\\s?|\\.)(\\d+)',
            title,
            re.UNICODE | re.IGNORECASE)
        if m:
            ep = m.group(4)
            sa = '01'  # si la saison n'est pas précisée, c'est qu'il n'y a sans doute qu'une saison
            terme = m.group(0)
        else:  # juste la saison
            m = re.search(
                '( S|\\.S|\\[S|saison)(\\s?|\\.)(\\d+)',
                title,
                re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''
                else:
                    terme = m.group(0)

    if terme:
        p = title.index(terme)

        if p < 5:             # au début, on retire directement l'élement recherché
            title = title.replace(terme, '')
            if pos:
                pos -= len(terme)
            if title.startswith(']'):
                title = title[1:]
                pos -= 1
        elif p < pos:
            pos = p

    if pos == 0:
        return title, sa, ep
    return title, sa, ep, pos


def getYear(title, pos):
    pattern = ['[^\\w]([0-9]{4})[^\\w]']
    return _getTag(title, pattern, pos)


def getLang(movie_title, pos):
    pattern = [
        'VFI',
        'VFF',
        'VFQ',
        'SUBFRENCH',
        'TRUEFRENCH',
        'FRENCH',
        'VF',
        'VOSTFR',
        '[^\\w](VOST)[^\\w]',
        '[^\\w](VO)[^\\w]',
        'QC',
        '[^\\w](MULTI)[^\\w]',
        'FASTSUB']
    return _getTag(movie_title, pattern, pos)


def getReso(movie_title, pos):
    pattern = [
        'HDCAM',
        '[^\\w](CAM)[^\\w]',
        '[^\\w](R5)[^\\w]',
        '.(3D)',
        '.(DVDSCR)',
        '.(TVRIP)',
        '.(FHD)',
        '.(HDLIGHT)',
        '\\d{3,4}P',
        '.(4K)',
        '.(UHD)',
        '.(BDRIP)',
        '.(BRRIP)',
        '.(DVDRIP)',
        '.(HDTV)',
        '.(BLURAY)',
        '.(WEB-DL)',
        '.(WEBRIP)',
        '[^\\w](WEB)[^\\w]',
        '.(DVDRIP)']
    resolution, pos = _getTag(movie_title, pattern, pos)
    if resolution:
        resolution = resolution.replace('2160P', '4K')
    return resolution, pos


def getIdTMDB(movie_title, pos):
    pattern = ['.TM(\\d+)TM.']
    return _getTag(movie_title, pattern, pos)


def _getTag(movie_title, tags, pos):
    for t in tags:
        results = re.search(t, movie_title, re.IGNORECASE)
        if results:
            l = len(results.groups())
            ret = results.group(l)
            if not ret and l > 1:
                ret = results.group(l - 1)
            terme = results.group(0)
            p = movie_title.index(terme)
            if pos > p > 2:  # si ce n'est pas au début
                pos = p
            return ret.upper(), pos
    return False, pos
