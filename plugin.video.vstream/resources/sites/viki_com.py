# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# uniquement format mpd disponible
# Based on
# https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/viki.py

import hashlib
import hmac
import re
import time

from resources.lib.comaddon import Progress, isMatrix, dialog, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.util import cUtil

# _DEVICE_ID = '86085977d'  # used for android api
# inspiré de github.com / yt-dlp / yt-dlp / blob / master / yt_dlp /
# extractor / viki.py
_DEVICE_ID = '112395910d'
_APP = '100005a'
_APP_VERSION = '6.11.3'
_APP_SECRET = 'd96704b180208dbb2efa30fe44c48bd8690441af9f567ba8fd710a72badc85198f7472'
Base_API = 'https://api.viki.io%s'

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
SITE_IDENTIFIER = 'viki_com'
SITE_NAME = 'Viki'
SITE_DESC = 'Emissions TV, Séries et films asiatiques'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = 'https://api.viki.io/v4/'

DRAMA_DRAMAS = (True, 'load')

# il n'existe qu'une vingtaine de films
MOVIE_GENRES = (True, 'showMovieGenre')
MOVIE_PAYS = (True, 'showMoviePays')
MOVIE_NEWS = (
    URL_API +
    'movies.json?sort=newest_video&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
MOVIE_RECENT = (
    URL_API +
    'movies.json?sort=views_recent&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
MOVIE_POPULAR = (
    URL_API +
    'movies.json?sort=trending&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
MOVIE_BEST = (
    URL_API +
    'movies.json?sort=views&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')

DRAMA_GENRES = (True, 'showSerieGenre')
DRAMA_PAYS = (True, 'showSeriePays')
DRAMA_NEWS = (
    URL_API +
    'series.json?sort=newest_video&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
DRAMA_VIEWS = (
    URL_API +
    'series.json?sort=trending&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
DRAMA_RECENT = (
    URL_API +
    'series.json?sort=views_recent&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')
DRAMA_BEST = (
    URL_API +
    'series.json?sort=views&page=1&per_page=50&app=' +
    _APP +
    '&t=',
    'showMovies')

URL_SEARCH = (
    URL_API +
    'search.json?page=1&per_page=50&app=' +
    _APP +
    '&term=',
    'showMovies')
FUNCTION_SEARCH = 'showMovies'
URL_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')

se = 'true'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'dramas.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Nouveautés)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_POPULAR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_POPULAR[1],
        'Films (Populaires)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_PAYS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_PAYS[1],
        'Films (Pays)',
        'lang.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', DRAMA_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_NEWS[1],
        'Séries (Nouveautés)',
        'dramas.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_RECENT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_RECENT[1],
        'Séries (Récentes)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_VIEWS[1],
        'Séries (Populaires)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_PAYS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_PAYS[1],
        'Séries (Pays)',
        'lang.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_BEST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_BEST[1],
        'Séries (Best)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sUrl = sSearch
        sSearchText = sSearch.replace(URL_SEARCH[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

    url = sUrl
    timestamp = str(int(time.time()))

    if 'search.json' not in url:
        url = url + timestamp

    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    if not jsonrsp:
        gui.addText(SITE_IDENTIFIER)

    output_parameter_handler = OutputParameterHandler()
    if len(jsonrsp['response']) > 0:
        total = len(jsonrsp['response'])
        progress_ = Progress().VScreate(SITE_NAME)
        for movie in range(0, len(jsonrsp['response'])):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if jsonrsp['response'][movie]['type'] == "movie":
                try:
                    title = jsonrsp['response'][movie]['container']['titles']['fr']
                except BaseException:
                    title = jsonrsp['response'][movie]['container']['titles']['en']

                try:
                    sThumb = jsonrsp['response'][movie]['container']['images']['atv_cover']['url']
                except BaseException:
                    sThumb = jsonrsp['response'][movie]['container']['images']['poster']['url']

                sUrl2 = jsonrsp['response'][movie]['id']

            else:
                sUrl2 = URL_API + 'series/' + \
                    jsonrsp['response'][movie]['id'] + '/episodes.json?page=1&per_page=50&app=' + _APP + '&t=' + str(timestamp)

                try:
                    title = jsonrsp['response'][movie]['titles']['fr']
                except BaseException:
                    title = jsonrsp['response'][movie]['titles']['en']

                try:
                    sThumb = jsonrsp['response'][movie]['images']['atv_cover']['url']
                except BaseException:
                    sThumb = jsonrsp['response'][movie]['images']['poster']['url']

            try:
                desc = str(jsonrsp['response'][movie]['descriptions']['fr'])
            except BaseException:
                desc = ''

            output_parameter_handler.addParameter('siteUrl', sUrl2)

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            if not isMatrix():
                output_parameter_handler.addParameter(
                    'sMovieTitle', title.encode('utf-8', 'ignore'))
            else:
                output_parameter_handler.addParameter('sMovieTitle', title)

            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            if jsonrsp['response'][movie]['type'] == "movie":
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        if jsonrsp['more'] is True:
            getpage = re.compile(
                '(.+?)&page=(.+?)&per_page=(.+?)&t=').findall(url)
            for frontUrl, page, backurl in getpage:
                iNumberPage = int(page) + 1
                url = frontUrl + '&page=' + \
                    str(iNumberPage) + '&per_page=' + backurl + '&t='
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', url)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + str(iNumberPage),
                    output_parameter_handler)

        gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    url = sUrl + '&direction=asc'
    timestamp = str(int(time.time()))

    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    output_parameter_handler = OutputParameterHandler()
    for episode in range(0, len(jsonrsp['response'])):
        try:
            if jsonrsp['response'][episode]['blocked'] is False:
                et = ''
                try:
                    et = jsonrsp['response'][episode]['titles']['en']
                except BaseException:
                    pass

                title = jsonrsp['response'][episode]['container']['titles']['en'] + \
                    ' Episode ' + str(jsonrsp['response'][episode]['number'])
                sUrl = jsonrsp['response'][episode]['id']
                sThumb = jsonrsp['response'][episode]['images']['poster']['url'] + '@' + et

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                pass

        except BaseException:
            pass

    if len(jsonrsp['response']) == 0:
        pass

    if jsonrsp['more'] is True:
        getpage = re.compile('(.+?)page=(.+?)&per_page').findall(url)
        for frontUrl, page in getpage:
            newPage = int(page) + 1
            url = frontUrl + 'page=' + \
                str(newPage) + '&per_page=50&app=' + _APP + '&t=' + timestamp
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', url)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieGenre():
    gui = Gui()

    sGenre = 'movies'
    url = URL_API + 'videos/genres.json?app=' + _APP + ''
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    output_parameter_handler = OutputParameterHandler()
    for genre in range(0, len(jsonrsp)):
        # or jsonrsp[genre]['name']['en']
        typeGenre = jsonrsp[genre]['name']['fr']
        urlGenre = URL_API + sGenre + '.json?sort=newest_video&page=1&per_page=50&app=' + \
            _APP + '&genre=' + jsonrsp[genre]['id'] + '&t='

        output_parameter_handler.addParameter('siteUrl', urlGenre)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            typeGenre.capitalize(),
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieGenre():
    gui = Gui()

    sGenre = 'series'
    url = URL_API + 'videos/genres.json?app=' + _APP + ''
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    output_parameter_handler = OutputParameterHandler()
    for genre in range(0, len(jsonrsp)):
        urlGenre = URL_API + sGenre + '.json?sort=newest_video&page=1&per_page=50&app=' + \
            _APP + '&genre=' + jsonrsp[genre]['id'] + '&t='
        typeGenre = jsonrsp[genre]['name']['fr']

        output_parameter_handler.addParameter('siteUrl', urlGenre)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            typeGenre.capitalize(),
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviePays():
    showPays('movies')


def showSeriePays():
    showPays('series')


def showPays(genre):
    gui = Gui()
    url = URL_API + 'videos/countries.json?app=' + _APP + ''
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    output_parameter_handler = OutputParameterHandler()
    for country, subdict in jsonrsp.items():
        urlcountry = URL_API + genre + '.json?sort=newest_video&page=1&per_page=50&app=' + \
            _APP + '&origin_country=' + country + '&t='
        country = jsonrsp[country]['name']['en']
        output_parameter_handler.addParameter('siteUrl', urlcountry)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            country.capitalize(),
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


# Signature des demandes au nom de Flash player
def SIGN(pth, version=4):
    timestamp = int(time.time())
    rawtxt = '/v%d/%s?drms=dt3&device_id=%s&app=%s' % (
        version, pth, _DEVICE_ID, _APP)
    sig = hmac.new(_APP_SECRET.encode('ascii'), ('%s&t=%d' %
                                                 (rawtxt, timestamp)).encode('ascii'), hashlib.sha1).hexdigest()

    # syntaxe reservée au Python 3
    # rawtxt = f'/v{version}/{pth}?drms=dt3&device_id={_DEVICE_ID}&app={_APP}'
    # sig = hmac.new(_APP_SECRET.encode('ascii'), f'{rawtxt}&t={timestamp}'.encode('ascii'), hashlib.sha1).hexdigest()
    return Base_API % rawtxt, timestamp, sig


def GET_URLS_STREAM(url):
    streamUrlList = []
    validq = []

    urlreq, timestamp, sig = SIGN('playback_streams/' + url + '.json', 5)
    oRequestHandler = RequestHandler(urlreq)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('X-Viki-manufacturer', 'vivo')
    oRequestHandler.addHeaderEntry('X-Viki-device-model', 'vivo 1606')
    oRequestHandler.addHeaderEntry('X-Viki-device-os-ver', '6.0.1')
    oRequestHandler.addHeaderEntry('X-Viki-connection-type', 'WIFI')
    oRequestHandler.addHeaderEntry('X-Viki-carrier', '')
    oRequestHandler.addHeaderEntry('X-Viki-as-id', '100005a-1625321982-3932')
    oRequestHandler.addHeaderEntry('timestamp', str(timestamp))
    oRequestHandler.addHeaderEntry('signature', str(sig))
    oRequestHandler.addHeaderEntry('x-viki-app-ver', _APP_VERSION)
    oRequestHandler.addHeaderEntry('origin', 'https://www.viki.com')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    try:
        jsonrsp = jsonrsp['main']
    except BaseException:
        dialog().VSinfo("Contenu payant", 'An error occurred')
        return False

    testeurl = ''
    testeq = ''
    for qual in jsonrsp:
        streamUrlList.append(qual['url'])

    streamUrlList.append(testeurl)
    return streamUrlList


def showLinks():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    dataList = []

    streamList2 = GET_URLS_STREAM(sUrl)

    if not streamList2:
        return

    for item in streamList2:
        dataList.append(item)

    # Conversion en str pour pouvoir facilement le manipuler dans le hoster.
    dataList = ','.join(dataList)

    oHoster = HosterGui().checkHoster('viki')
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, dataList, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
