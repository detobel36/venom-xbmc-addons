# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re
import xbmc
import xbmcgui

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
    from urllib.parse import urlencode

from resources.lib.comaddon import Progress, VSlog, dialog, Addon, isMatrix, SiteManager
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import RequestHandler, MPencode
from resources.lib.parser import Parser
from resources.lib.util import Quote


SITE_IDENTIFIER = 'siteuptobox'
SITE_NAME = '[COLOR dodgerblue]Compte UpToBox[/COLOR]'
SITE_DESC = 'Fichiers sur compte UpToBox'
URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
NB_FILES = 100
BURL = URL_MAIN + '?op=my_files'
API_URL = 'https://uptobox.com/api/user/files?token=none&orderBy=file_date_inserted&dir=desc'
URL_MOVIE = ('&path=//', 'showMedias')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = {'User-Agent': UA}


def load():
    gui = Gui()
    addons = Addon()

    # Même avec un token, on verifies les identifiants
    if (addons.getSetting('hoster_uptobox_username') == '') or (addons.getSetting(
            'hoster_uptobox_password') == '') or not cPremiumHandler('uptobox').getToken():
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]' +
            'Nécessite un Compte Uptobox Premium ou Gratuit' +
            '[/COLOR]')
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', '//')
        gui.addDir(
            SITE_IDENTIFIER,
            'opensetting',
            Addon().VSlang(30023),
            'none.png',
            output_parameter_handler)
        gui.setEndOfDirectory()
        return

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_MOVIE[1],
        'Mes vidéos',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showFile',
        'Mes Fichiers',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def opensetting():
    Addon().openSettings()


def showSearch(path='//'):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sPath = input_parameter_handler.getValue('site_url')
    _type = input_parameter_handler.getValue('movie_title')

    search_text = gui.showKeyBoard()
    if search_text:
        sUrlSearch = ''
        if _type:
            sUrlSearch += '&type=' + _type
        if sPath:
            sUrlSearch += '&path=' + sPath
        else:
            sUrlSearch += '&path=//'
        sUrlSearch += '&searchField=file_name&search=' + search_text

        if _type == 'serie':
            searchSeries(search_text)
        else:
            showMedias(sUrlSearch, _type)


def showFile(search=''):

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    offset = 0
    limit = NB_FILES
    if 'offset=' not in url:
        url = '&offset=0' + url
    else:
        offset = int(re.search('&offset=(\\d+)', url).group(1))

    if 'limit=' not in url:
        url = '&limit=%d' % NB_FILES + url
    else:
        limit = int(re.search('&limit=(\\d+)', url).group(1))

    # Page courante
    numPage = offset // limit

    premium_handler = cPremiumHandler('uptobox')
    sToken = premium_handler.getToken()

    request_handler = RequestHandler(API_URL.replace('none', sToken) + url)
    html_content = request_handler.request()
    content = json.loads(html_content)
    if ('success' in content and content['success']
            == False) or content['statusCode'] != 0:
        dialog().VSinfo(content['data'])
        gui.setEndOfDirectory()
        return

    content = content['data']
    path = content['path'].upper()
    if not content:
        gui.setEndOfDirectory()
        return

    # menu de recherche
    output_parameter_handler = OutputParameterHandler()
    if path == '//' and not search:
        output_parameter_handler.addParameter('site_url', URL_MOVIE[0])
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Rechercher',
            'search.png',
            output_parameter_handler)

    total = len(content)
    sPath = getpath(content)

    # les dossiers en premier, sur la première page seulement
    if not search and numPage == 0 and 'folders' in content:
        folders = sorted(
            content['folders'],
            key=lambda f: f['fld_name'].upper())
        sFoldername = ''
        for folder in folders:
            title = folder['name']
            sFoldername = folder['fld_name']
            if not isMatrix():
                title = title.encode('utf-8')
                sFoldername = sFoldername.encode('utf-8')
            url = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showFile',
                title,
                'genres.png',
                output_parameter_handler)

    # les fichiers
    nbFile = 0
    oHosterGui = HosterGui()
    hoster = oHosterGui.getHoster('uptobox')

    for file in content['files']:
        title = file['file_name']
        if not isMatrix():
            title = title.encode('utf-8')

        hoster_url = URL_MAIN + file['file_code']

        hoster.setDisplayName(title)
        hoster.setFileName(title)
        oHosterGui.showHoster(gui, hoster, hoster_url, '')

        nbFile += 1

    # Next >>>
    if not search and nbFile == NB_FILES:
        sPath = getpath(content)
        next_page_data = numPage + 1
        offset = next_page_data * NB_FILES
        site_url = '&offset=%d&limit=%d&path=%s' % (offset, limit, sPath)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', site_url)
        output_parameter_handler.addParameter('movie_title', 'movie_title')
        gui.addNext(SITE_IDENTIFIER, 'showFile', 'Page %d' %
                    (next_page_data + 1), output_parameter_handler)

    gui.setEndOfDirectory()


def showMedias(search='', _type=None):

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')

    if search:
        site_url = search
    else:
        site_url = input_parameter_handler.getValue('site_url')

    premium_handler = cPremiumHandler('uptobox')
    sToken = premium_handler.getToken()

    # parcourir un dossier virtuel, séparateur ':'
    searchFolder = ''
    if site_url[-1:] == ':':
        idxFolder = site_url.rindex('/')
        searchFolder = site_url[idxFolder + 1:-1]
        site_url = site_url[:idxFolder]

    offset = 0
    limit = NB_FILES
    if 'offset=' not in site_url:
        site_url = '&offset=0' + site_url
    else:
        offset = int(re.search('&offset=(\\d+)', site_url).group(1))

    if 'limit=' not in site_url:
        site_url = '&limit=%d' % NB_FILES + site_url
    else:
        limit = int(re.search('&limit=(\\d+)', site_url).group(1))

    # Page courante
    numPage = offset // limit

    request_handler = RequestHandler(
        API_URL.replace('none', sToken) + site_url)
    html_content = request_handler.request()
    content = json.loads(html_content)

    if ('success' in content and content['success']
            == False) or content['statusCode'] != 0:
        dialog().VSinfo(content['data'])
        gui.setEndOfDirectory()
        return

    content = content['data']
    if not content:
        gui.setEndOfDirectory()
        return

    isMovie = isTvShow = isSeason = False
    path = content['path'].upper()
    if not isMatrix():
        path = path.encode('utf-8')
    isMovie = 'FILM' in path or 'MOVIE' in path or 'DISNEY' in path or '3D' in path or '4K' in path or 'DOCUMENTAIRE' in path or 'DOCS' in path
    isTvShow = 'SERIE' in path or 'SÉRIE' in path or 'TVSHOW' in path
    isAnime = '/ANIMES' in path or '/ANIMÉS' in path or 'MANGA' in path or 'JAPAN' in path

    # Rechercher Film
    if path == '//' and not search:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', path)
        output_parameter_handler.addParameter('movie_title', 'film')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Rechercher (Films)',
            'search.png',
            output_parameter_handler)

    # Rechercher Séries
    if path == '//' and not search:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', path)
        output_parameter_handler.addParameter('movie_title', 'serie')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearch',
            'Rechercher (Séries)',
            'search.png',
            output_parameter_handler)

    if search and _type == 'film':
        isMovie = True

    # ajout des dossiers en premier, sur la première page seulement
    if not isTvShow and not isAnime and not search and numPage == 0 and 'folders' in content:
        addFolders(gui, content, searchFolder)

    nbFile = 0
    if isTvShow or isAnime:
        season = False
        if 'season' in site_url:
            season = site_url.split('season=')[1]

        if len(content['files']) > 0:
            nbFile = showEpisodes(gui, movie_title, content, site_url, season)
        else:
            nbFile = showSeries(gui, content, searchFolder, numPage)
    elif isMovie:
        nbFile = showMovies(gui, content, _type)
    else:
        for file in content['files']:
            title = file['file_name']
            hoster_url = URL_MAIN + file['file_code']
            showMovie(gui, title, hoster_url, 'film')

    # Lien Suivant >>
    if not search and nbFile == NB_FILES:
        sPath = getpath(content)
        next_page_data = numPage + 1
        offset = next_page_data * NB_FILES
        site_url = '&offset=%d&limit=%d&path=%s' % (offset, limit, sPath)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', site_url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        gui.addNext(SITE_IDENTIFIER, 'showMedias', 'Page %d' %
                    (next_page_data + 1), output_parameter_handler)

    gui.setEndOfDirectory()


def addFolders(gui, content, searchFolder=None):

    # dossiers trier par ordre alpha
    folders = sorted(content['folders'], key=lambda f: f['fld_name'].upper())

    sFoldername = ''

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    output_parameter_handler = OutputParameterHandler()

    for folder in folders:

        title = folder['name']
        sFoldername = folder['fld_name']
        folderPath = folder['path']
        if not isMatrix():
            title = title.encode('utf-8')
            sFoldername = sFoldername.encode('utf-8')
            folderPath = folderPath.encode('utf-8')

        if searchFolder and not title.startswith(searchFolder):
            continue

        isSubFolder = False
        if title.startswith('REP_') or title.startswith('00_'):
            isSubFolder = True

        if isSubFolder and ':' in title:
            subName, subFolder = title.split(':')
            if folderPath.endswith(subName):
                title = subFolder.strip()
            else:
                if searchFolder:
                    if subName == searchFolder:
                        title = subFolder
                else:
                    if subName in subFolders:
                        continue
                    subFolders.add(subName)
                    title = subName
                    sFoldername = sFoldername.replace(subFolder, '')

        if title.startswith('REP_'):
            title = title.replace('REP_', '')
        if title.startswith('00_'):
            title = title.replace('00_', '')

        # format du genre "REP_:"
        if not title:
            return addFolders(gui, content, subName)

        if title.startswith('RES-') and title.endswith('-RES'):
            title = title.replace('RES-', '[').replace('-RES', ']')

        if 'SERIE' in title.upper() or 'SÉRIE' in title.upper() or 'TVSHOW' in title.upper():
            thumb = 'series.png'
        elif 'DOCUMENTAIRE' in title.upper() or 'DOCS' in title.upper():
            thumb = 'doc.png'
        elif 'SPECTACLE' in title.upper():
            thumb = 'star.png'
        elif 'CONCERT' in title.upper():
            thumb = 'music.png'
        elif 'SPORT' in title.upper():
            thumb = 'sport.png'
        elif 'FILM' in title.upper() or 'MOVIE' in title.upper():
            thumb = 'films.png'
        elif 'ANIMES' in title.upper() or 'ANIMÉS' in title.upper() or 'MANGA' in title.upper() or 'JAPAN' in title.upper():
            thumb = 'animes.png'
        else:
            thumb = 'genres.png'

        url = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')

        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', title)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMedias',
            title,
            thumb,
            output_parameter_handler)


def showMovies(gui, content, _type=None):

    numFile = 0

    # ajout des fichiers
    for file in content['files']:
        title = file['file_name']
        hoster_url = URL_MAIN + file['file_code']
        showMovie(gui, title, hoster_url, _type)
        numFile += 1

    return numFile


def showMovie(gui, title, hoster_url, _type=None):
    # seulement les formats vidéo (ou sans extensions)
    if title[-4] == '.':
        if title[-4:] not in '.mkv.avi.mp4.m4v.iso':
            return
        # enlever l'extension
        title = title[:-4]

    # enlever les séries
    if _type == 'film':
        sa, ep = searchEpisode(title)
        if sa or ep:
            return

    if not isMatrix():
        title = title.encode('utf-8')

    # recherche des métadonnées
    movie_title = title
    pos = len(movie_title)
    year, pos = getYear(movie_title, pos)
    resolution, pos = getReso(movie_title, pos)
    tmdb_id, pos = getIdTMDB(movie_title, pos)
    lang, pos = getLang(movie_title, pos)

    movie_title = movie_title[:pos].replace('.', ' ').replace('_', ' ').strip()

    # un peu de nettoyage
    if 'customer' not in movie_title.lower():
        movie_title = re.sub('(?i)' + re.escape('custom'), '', movie_title)

    title = movie_title
    if resolution:
        movie_title += ' [%s]' % resolution
    if lang:
        movie_title += ' (%s)' % lang

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', hoster_url)
    output_parameter_handler.addParameter('movie_title', movie_title)
    output_parameter_handler.addParameter('year', year)
    output_parameter_handler.addParameter('resolution', resolution)
    output_parameter_handler.addParameter('lang', lang)
    output_parameter_handler.addParameter('tmdb_id', tmdb_id)
    gui.addMovie(
        SITE_IDENTIFIER,
        'showHosters',
        title,
        'films.png',
        '',
        '',
        output_parameter_handler)


def showSeries(gui, content, searchFolder, numPage):

    # dossiers trier par ordre alpha
    folders = content['folders']
    if len(folders) == 0:
        return 0

    folders = sorted(folders, key=lambda f: f['fld_name'].upper())

    movie_title = content['currentFolder']['name'] if 'name' in content['currentFolder'] else 'Rechercher'
    if not isMatrix():
        movie_title = movie_title.encode('utf-8')

    numSeries = 0
    nbSeries = 0
    offset = numPage * NB_FILES

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    output_parameter_handler = OutputParameterHandler()

    for folder in folders:

        title = folder['name']
        sFoldername = folder['fld_name']
        if not isMatrix():
            title = title.encode('utf-8')
            sFoldername = sFoldername.encode('utf-8')

        # if searchFolder and not title.startswith(searchFolder):
        if searchFolder and searchFolder.upper() not in title.upper():
            continue

        if 'REP_' in title:
            addFolders(gui, content, title.split(':')[0])
            continue

        numSeries += 1
        if numSeries <= offset:
            continue

        # dossier
        isSubFolder = False
        if title.startswith('REP_') or title.startswith('00_'):
            isSubFolder = True

        if isSubFolder and ':' in title:
            subName, subFolder = title.split(':')
            if folder['path'].endswith(subName):
                title = subFolder.strip()
            else:
                if searchFolder:
                    if subName == searchFolder:
                        title = subFolder
                else:
                    if subName in subFolders:
                        continue
                    subFolders.add(subName)
                    title = subName
                    sFoldername = sFoldername.replace(subFolder, '')

        if title.startswith('REP_'):
            title = title.replace('REP_', '')
        if title.startswith('00_'):
            title = title.replace('00_', '')

        pos = len(title)

        year, pos = getYear(title, pos)
        tmdb_id, pos = getIdTMDB(title, pos)
        title = title[:pos]

        url = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')

        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('year', year)
        output_parameter_handler.addParameter('tmdb_id', tmdb_id)

        if isSubFolder:   # dossier
            gui.addDir(
                SITE_IDENTIFIER,
                'showMedias',
                title,
                'genres.png',
                output_parameter_handler)
        else:           # série
            saison = None
            if 'SAISON' in title.upper() or 'SEASON' in title.upper():
                saison = re.search('(\\d+)', title)
                if saison:
                    saison = int(saison.group(1))
            if not saison:
                saison = re.search('S(\\d+)', title)
                if saison:
                    saison = int(saison.group(1))
            if saison:
                pos = len(movie_title)
                year, pos = getYear(movie_title, pos)
                tmdb_id, pos = getIdTMDB(movie_title, pos)
                movie_title = movie_title[:pos]

                url += '&season=%d' % saison
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('year', year)
                output_parameter_handler.addParameter('tmdb_id', tmdb_id)

                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showMedias',
                    movie_title +
                    ' ' +
                    title,
                    '',
                    '',
                    '',
                    output_parameter_handler)
            elif movie_title.upper() == 'ANIMES' or movie_title.upper() == 'ANIMÉS' or 'MANGA' in movie_title.upper() or 'JAPAN' in movie_title.upper():
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showMedias',
                    title,
                    '',
                    '',
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showMedias', title,
                          '', '', '', output_parameter_handler)

        nbSeries += 1
        if nbSeries == NB_FILES:
            break

    return nbSeries


def showEpisodes(gui, movie_title, content, site_url, season):

    if not season:
        nbFile = 0
        saisons = set()

        # Recherche des saisons
        for file in content['files']:
            nbFile += 1
            title = file['file_name']
            if not isMatrix():
                title = title.encode('utf-8')

            # Recherche saisons et episodes
            sa, ep = searchEpisode(title)
            if sa:
                saisons.add(int(sa))

        # plusieurs saisons, on les découpe
        if len(saisons) > 0:
            output_parameter_handler = OutputParameterHandler()
            for saison in saisons:
                url = site_url + '&season=%d' % saison
                title = 'Saison %d ' % saison + movie_title
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showMedias',
                    title,
                    '',
                    '',
                    '',
                    output_parameter_handler)
            return nbFile

    pos = len(movie_title)
    year, pos = getYear(movie_title, pos)
    movie_title = movie_title[:pos]

    # ajout des fichiers
    nbFile = 0
    output_parameter_handler = OutputParameterHandler()
    for file in content['files']:
        file_name = file['file_name']
        if not isMatrix():
            file_name = file_name.encode('utf-8')

        # Recherche saisons et episodes
        sa, ep = searchEpisode(file_name)
        if season:
            if sa:
                if int(sa) != int(season):
                    continue
            else:
                sa = season

        if ep:
            title = 'E' + ep + ' ' + movie_title
            if sa:
                title = 'S' + sa + title

        pos = len(file_name)
        resolution, pos = getReso(file_name, pos)
        lang, pos = getLang(file_name, pos)

        if not ep:
            title = file_name[:pos]

        display_title = title
        if resolution:
            display_title += '[%s]' % resolution
        if lang:
            display_title += '(%s)' % lang

        hoster_url = URL_MAIN + file['file_code']

        nbFile += 1
        output_parameter_handler.addParameter('site_url', hoster_url)
        output_parameter_handler.addParameter('movie_title', display_title)
        output_parameter_handler.addParameter('year', year)
        gui.addEpisode(SITE_IDENTIFIER, 'showHosters', title,
                       '', '', '', output_parameter_handler)

    return nbFile


# Recherche saisons et episodes
def searchEpisode(title):
    sa = ep = ''
    m = re.search(
        '( S|\\.S|\\[S|saison|\\s+|\\.)(\\s?|\\.)(\\d+)( *- *|\\s?|\\.)(E|Ep|x|\\wpisode|Épisode)(\\s?|\\.)(\\d+)',
        title,
        re.UNICODE | re.IGNORECASE)
    if m:
        sa = m.group(3)
        if int(sa) < 100:
            ep = m.group(7)
        else:
            sa = ''
    else:  # Juste l'épisode
        m = re.search(
            '(^|\\s|\\.)(E|Ep|\\wpisode)(\\s?|\\.)(\\d+)',
            title,
            re.UNICODE | re.IGNORECASE)
        if m:
            ep = m.group(4)
        else:  # juste la saison
            m = re.search(
                '( S|\\.S|\\[S|saison)(\\s?|\\.)(\\d+)',
                title,
                re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''

    return sa, ep

# recherche d'une serie par son nom en parcourant tous les dossiers


def searchSeries(searchName):

    gui = Gui()
    sToken = cPremiumHandler('uptobox').getToken()
    url = API_URL.replace('none', sToken) + '&offset=0&limit=20&path='

    # recherches des dossiers "series" à la racine
    request_handler = RequestHandler(url + '//')
    html_content = request_handler.request()
    content = json.loads(html_content)
    content = content['data']
    if content:
        folders = content['folders']
        for folder in folders:
            path = folder['fld_name'].upper()
            if not isMatrix():
                path = path.encode('utf-8')
            isTvShow = 'SERIE' in path or 'SÉRIE' in path or 'TVSHOW' in path
            if isTvShow:
                searchSerie(gui, url, path, searchName)

    gui.setEndOfDirectory()
    return


def searchSerie(gui, url, path, searchName):
    request_handler = RequestHandler(url + path)
    html_content = request_handler.request()
    content = json.loads(html_content)
    content = content['data']
    if content:
        showSeries(gui, content, searchName, 0)
        folders = content['folders']

        # recherche dans les sous-dossiers qui ne sont pas des séries
        for folder in folders:
            subFolderName = folder['name'].upper()
            if subFolderName.startswith(
                    'REP_') or subFolderName.startswith('00_'):
                path = folder['fld_name'].upper()
                searchSerie(gui, url, path, searchName)


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    hoster_url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(title)
        hoster.setFileName(title)
        HosterGui().showHoster(gui, hoster, hoster_url, '')
    gui.setEndOfDirectory()


def getYear(movie_title, pos):
    pattern = ['[^\\w]([0-9]{4})[^\\w]']
    return _getTag(movie_title, pattern, pos)


def getLang(movie_title, pos):
    pattern = [
        'VFI',
        'VFF',
        'VFQ',
        'SUBFRENCH',
        'TRUEFRENCH',
        '.(FRENCH)',
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
    pattern = ['TM(\\d+)TM']
    return _getTag(movie_title, pattern, pos)


def _getTag(movie_title, tags, pos):
    for t in tags:
        results = re.search(t, movie_title, re.IGNORECASE)
        if results:
            l = len(results.groups())
            ret = results.group(l)
            if not ret and l > 1:
                ret = results.group(l - 1)
            p = movie_title.index(results.group(0))
            if p < pos:
                pos = p
            return ret.upper(), pos
    return False, pos


def getpath(content):
    for x in content:
        if x == 'path':
            sPath = Quote(content[x].encode('utf-8')).replace('//', '%2F%2F')
            return sPath


def AddmyAccount():
    upToMyAccount()


def upToMyAccount():
    addons = Addon()

    # on n'utilise pas le token car il se prete, il faut fournir les
    # identifiants pour ajouter à son compte
    if (addons.getSetting('hoster_uptobox_username') == '') and (
            addons.getSetting('hoster_uptobox_password') == ''):
        return

    input_parameter_handler = InputParameterHandler()
    media_url = input_parameter_handler.getValue('media_url')
    movie_title = input_parameter_handler.getValue('title')

    premium_handler = cPremiumHandler('uptobox')
    html_content = premium_handler.GetHtml(URL_MAIN)
    cookies = GestionCookie().Readcookie('uptobox')

    results = re.search(
        '<form id="fileupload" action="([^"]+)"',
        html_content,
        re.DOTALL)
    if results:

        upUrl = results.group(1).replace('upload?', 'remote?')

        if upUrl.startswith('//'):
            upUrl = 'https:' + upUrl

        fields = {'urls': '["' + media_url + '"]'}
        mpartdata = list(MPencode(fields))

        if isMatrix():
            mpartdata[1] = mpartdata[1].encode("utf-8")

        req = urllib2.Request(upUrl, mpartdata[1], headers)
        req.add_header('Content-Type', mpartdata[0].replace(',', ';'))
        req.add_header('Cookie', cookies)
        req.add_header('Content-Length', len(mpartdata[1]))

        # pénible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')

        try:
            rep = urllib2.urlopen(req)
            xbmcgui.Dialog().notification(
                'Demande envoyée',
                'Vous pouvez faire autre chose.',
                xbmcgui.NOTIFICATION_INFO,
                3000,
                False)
        except UrlError as e:
            xbmcgui.Dialog().notification(
                'Demande rejetée',
                'Essayez de nouveau.',
                xbmcgui.NOTIFICATION_INFO,
                3000,
                False)
            VSlog(str(e))
            return ''

        html_content = rep.read()
        rep.close()

        pattern = '{"id":.+?,(?:"size":|"Progress":)([0-9]+)'
        results = Parser().parse(html_content, pattern)
        if results[0]:
            xbmcgui.Dialog().notification(
                'Uptobox', 'Fichier ajouté - %s' %
                movie_title, xbmcgui.NOTIFICATION_INFO, 2000, False)
        else:
            # pénible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification(
                'Uptobox',
                'Fichier introuvable',
                xbmcgui.NOTIFICATION_INFO,
                2000,
                False)
    else:
        # pénible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcgui.Dialog().notification(
            'Uptobox',
            "Impossible d'ajouter le fichier",
            xbmcgui.NOTIFICATION_ERROR,
            2000,
            False)
