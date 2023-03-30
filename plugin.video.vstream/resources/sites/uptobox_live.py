# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re

from resources.lib.comaddon import addon, isMatrix, SiteManager
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
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'series' not in sUrl:
        output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
        output_parameter_handler.addParameter('sMovieTitle', 'movie')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Recherche (Films)',
            'search.png',
            output_parameter_handler)

    if 'films' not in sUrl:
        output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
        output_parameter_handler.addParameter('sMovieTitle', 'tv')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Recherche (Séries)',
            'search.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch(path='//'):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrlSearch = sUrl + sSearchText

        if title == 'movie':
            showMovies(sUrlSearch, True)
        else:
            showSeries(sUrlSearch, True)


def getAuthorizedID():
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sHtmlContent = RequestHandler(URL_MAIN).request()
    sPattern = "Authorization': '(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return False


def getContent(sUrl):

    sUrl = sUrl.replace(' ', '%20')
    videoId = getAuthorizedID()

    oRequest = RequestHandler(URL_MAIN + sUrl)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Authorization', videoId)
    sHtmlContent = oRequest.request()

    content = json.loads(sHtmlContent)

#    if content['status'] == 'unauthorized':
    if content['status'] == 'ok':
        return content['items']

    return []


def showMovies(sSearch='', searchLocal=False):
    gui = Gui()
    oUtil = cUtil()

    if not sSearch:
        searchLocal = True
        input_parameter_handler = InputParameterHandler()
        sSearch = input_parameter_handler.getValue('siteUrl')
    sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
    sSearchText = Unquote(sSearchText)
    sSearchText = oUtil.CleanName(sSearchText)

    sUrl = sSearch.replace('-', '\\-').replace('.', '%20')
    content = getContent(sUrl)

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
        sTmdbId, pos = getIdTMDB(title, pos)
        if sTmdbId:
            title = title.replace('.TM%sTM.' % sTmdbId, '')
            pos = len(title)

        sYear, pos = getYear(title, pos)
        sRes, pos = getReso(title, pos)
        sLang, pos = getLang(title, pos)
        title, sa, ep = getSaisonEpisode(title)

        # enlever les séries
        if not sa or not ep:
            title = title[:pos]
            title, sa, ep = getSaisonEpisode(title)
        if sa or ep:
            continue

        sMovieTitle = title[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle).strip()
        sMovieTitle = sMovieTitle.replace('.', ' ')

        if not oUtil.CheckOccurence(sSearchText, sMovieTitle):
            continue    # Filtre de recherche

        # lien de recherche spécifique à chaque film
        siteUrl = URL_SEARCH_MOVIES[0] + sMovieTitle.replace('-', '\\-')
        startWith = sMovieTitle[0].upper()
        if startWith.isdigit():
            startWith = 'number'
        siteUrl += '&start\\-with=' + startWith

        sSearchTitle = oUtil.CleanName(sMovieTitle)
        if sYear:
            sSearchTitle += ' (%s)' % sYear

        if sSearchTitle in movies:
            continue                # film déjà proposé

        movies.add(sSearchTitle)

        output_parameter_handler.clearParameter()
        output_parameter_handler.addParameter('siteUrl', siteUrl)
        output_parameter_handler.addParameter('sMovieTitle', sSearchTitle)
        output_parameter_handler.addParameter('sYear', sYear)
        output_parameter_handler.addParameter('sTmdbId', sTmdbId)
        gui.addMovie(
            SITE_IDENTIFIER,
            'showHosters',
            sMovieTitle,
            'films.png',
            '',
            '',
            output_parameter_handler)

    if searchLocal:
        gui.setEndOfDirectory()


def showAnims(sSearch=''):
    showSeries(sSearch, False, True)


def showSeries(sSearch='', searchLocal=False, isAnime=False):
    gui = Gui()
    oUtil = cUtil()

    sSearchTitle = sSearch.replace(URL_SEARCH_SERIES[0], '')
    sSearchTitle = Unquote(sSearchTitle)
    sSearchTitle = oUtil.CleanName(sSearchTitle)

    sUrl = sSearch.replace('-', '\\-')

    series = set()
    output_parameter_handler = OutputParameterHandler()

    # deux url pour plus de résultats
    urls = [sUrl, sUrl.replace('order=asc', 'order=desc')]
    bMatrix = isMatrix()
    for sUrl in urls:
        content = getContent(sUrl)
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
            sTmdbId, pos = getIdTMDB(title, pos)
            if sTmdbId:
                title = title.replace('.TM%sTM.' % sTmdbId, '')
                pos = len(title)
            sYear, pos = getYear(title, pos)
            sRes, pos = getReso(title, pos)
            sLang, pos = getLang(title, pos)
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
                sDisplayTitle = oUtil.unescape(title).strip()
                sDisplayTitle = sDisplayTitle.replace('.', ' ')

                if not oUtil.CheckOccurence(sSearchTitle, sDisplayTitle):
                    continue    # Filtre de recherche

                sMovieTitle = oUtil.CleanName(sDisplayTitle)
                if sYear:
                    sMovieTitle += ' (%s)' % sYear
                if sMovieTitle in series:
                    continue
                series.add(sMovieTitle)

                output_parameter_handler.clearParameter()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('sYear', sYear)
                output_parameter_handler.addParameter(
                    'sTmdbId', sTmdbId)  # Utilisé par TMDB
                if isAnime:
                    gui.addAnime(
                        SITE_IDENTIFIER,
                        'showSaisons',
                        sDisplayTitle,
                        '',
                        '',
                        '',
                        output_parameter_handler)
                else:
                    gui.addTV(
                        SITE_IDENTIFIER,
                        'showSaisons',
                        sDisplayTitle,
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
    oUtil = cUtil()

    input_parameter_handler = InputParameterHandler()
    # sUrl = input_parameter_handler.getValue('siteUrl')
    sSearchTitle = input_parameter_handler.getValue('sMovieTitle')
    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('sYear')

    # recherche depuis le titre sélectionné, pas depuis les mots clefs
    # recherchés
    sUrl = URL_SEARCH_SERIES[0] + sSearchTitle.replace('-', '\\-')
    startWith = sSearchTitle[0].upper()
    if startWith.isdigit():
        startWith = 'number'
    sUrl += '&start\\-with=' + startWith

    # deux url pour plus de résultats
    urls = [sUrl, sUrl.replace('order=asc', 'order=desc')]

    bMatrix = isMatrix()
    for sUrl in urls:
        content = getContent(sUrl)

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
            sTmdbId, pos = getIdTMDB(title, pos)
            if sTmdbId:
                title = title.replace('.TM%sTM.' % sTmdbId, '')
                pos = len(title)
            sYear, pos = getYear(title, pos)
            sRes, pos = getReso(title, pos)
            sLang, pos = getLang(title, pos)
            title, saison, episode, pos = getSaisonEpisode(title, pos)

            # vérifier l'année pour les homonymes
            if sSearchYear:
                if sYear:
                    if sSearchYear != sYear:
                        continue
                else:
                    continue
            elif sYear:
                continue

            # Recherche des noms de séries
            if not saison or not episode:
                title = title[:pos]
                pos = len(title)
                title, saison, episode, pos = getSaisonEpisode(title, pos)

            if saison:
                title = title[:pos]
                sMovieTitle = oUtil.unescape(title).strip()
                sMovieTitle = oUtil.CleanName(sMovieTitle)
                if sMovieTitle == sSearchTitle:
                    saisons[saison] = sUrl

    output_parameter_handler = OutputParameterHandler()
    for saison, sUrl in sorted(saisons.items(), key=lambda s: s[0]):
        sDisplayTitle = '%s S%s' % (sSearchTitle, saison)
        siteUrl = '%s|%s' % (sUrl, saison)
        output_parameter_handler.addParameter('siteUrl', siteUrl)
        sSaisonTitle = '%s S%s' % (sSearchTitle, saison)
        if sSearchYear:
            sSaisonTitle = '%s (%s)' % (sSaisonTitle, sSearchYear)
            output_parameter_handler.addParameter('sYear', sSearchYear)
        output_parameter_handler.addParameter('sMovieTitle', sSaisonTitle)
        gui.addSeason(
            SITE_IDENTIFIER,
            'showEpisodes',
            sDisplayTitle,
            '',
            '',
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():

    gui = Gui()
    oUtil = cUtil()

    input_parameter_handler = InputParameterHandler()
    sUrl, sSearchSaison = input_parameter_handler.getValue(
        'siteUrl').split('|')
    sSearchTitle = input_parameter_handler.getValue('sMovieTitle')
    sSearchTitle = sSearchTitle.replace(' S%s' % sSearchSaison, '')

    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('sYear')

    content = getContent(sUrl)

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
        sLang, pos = getLang(title, pos)
        sRes, pos = getReso(title, pos)
        sYear, pos = getYear(title, pos)
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
            if sYear:
                if sSearchYear != sYear:
                    continue
            else:
                continue
        elif sYear:
            continue

        sMovieTitle = title[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle).strip()
        sMovieTitle = oUtil.CleanName(sMovieTitle)

        if sMovieTitle != sSearchTitle:
            continue

        episodes.add(episode)

    output_parameter_handler = OutputParameterHandler()
    for episode in sorted(episodes):
        sDisplayTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)

        siteUrl = '%s|%s|%s' % (sUrl, sSearchSaison, episode)
        output_parameter_handler.addParameter('siteUrl', siteUrl)
        sEpTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)
        output_parameter_handler.addParameter('sMovieTitle', sEpTitle)
        output_parameter_handler.addParameter('sYear', sSearchYear)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showHosters',
            sDisplayTitle,
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
    oUtil = cUtil()

    input_parameter_handler = InputParameterHandler()
    # sSearchTmdbId = input_parameter_handler.getValue('sTmdbId')
    sSearchTitle = input_parameter_handler.getValue('sMovieTitle')
    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = input_parameter_handler.getValue('sYear')

    sUrl = input_parameter_handler.getValue('siteUrl')
    sSearchSaison = ''
    if '|' in sUrl:
        sUrl, sSearchSaison, sSearchEpisode = sUrl.split('|')
        sSearchTitle = sSearchTitle.replace(
            ' S%sE%s' %
            (sSearchSaison, sSearchEpisode), '')
    sSearchTitle = oUtil.CleanName(sSearchTitle)

    content = getContent(sUrl)
    # retourne le bon débrideur en fonction de son compte premmium
    oHoster = oHosterGui.checkHoster('uptobox')

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
        sTmdbId, pos = getIdTMDB(title, pos)
        sLang, pos = getLang(title, pos)
        sRes, pos = getReso(title, pos)
        sYear, pos = getYear(title, pos)

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
            if sYear:
                if sSearchYear != sYear:
                    continue
            else:
                continue
        elif sYear:
            continue

        title = title[:pos]
        sMovieTitle = oUtil.unescape(title).strip()
        sMovieTitle = sMovieTitle.replace('.', ' ').lower()
        if oUtil.CleanName(sMovieTitle) != sSearchTitle:
            continue

        sDisplayTitle = sMovieTitle
        if saison:
            sDisplayTitle += ' S%sE%s' % (saison, episode)
        if sRes:
            sDisplayTitle += ' [%s]' % sRes
        if sLang:
            sDisplayTitle += ' (%s)' % sLang
        if sYear:
            sDisplayTitle += ' (%s)' % sYear
            sMovieTitle += ' (%s)' % sYear
        sHosterUrl = file['link']

        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        oHosterGui.showHoster(gui, oHoster, sHosterUrl, '')

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
    sPattern = ['[^\\w]([0-9]{4})[^\\w]']
    return _getTag(title, sPattern, pos)


def getLang(sMovieTitle, pos):
    sPattern = [
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
    return _getTag(sMovieTitle, sPattern, pos)


def getReso(sMovieTitle, pos):
    sPattern = [
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
    sRes, pos = _getTag(sMovieTitle, sPattern, pos)
    if sRes:
        sRes = sRes.replace('2160P', '4K')
    return sRes, pos


def getIdTMDB(sMovieTitle, pos):
    sPattern = ['.TM(\\d+)TM.']
    return _getTag(sMovieTitle, sPattern, pos)


def _getTag(sMovieTitle, tags, pos):
    for t in tags:
        aResult = re.search(t, sMovieTitle, re.IGNORECASE)
        if aResult:
            l = len(aResult.groups())
            ret = aResult.group(l)
            if not ret and l > 1:
                ret = aResult.group(l - 1)
            terme = aResult.group(0)
            p = sMovieTitle.index(terme)
            if pos > p > 2:  # si ce n'est pas au début
                pos = p
            return ret.upper(), pos
    return False, pos
