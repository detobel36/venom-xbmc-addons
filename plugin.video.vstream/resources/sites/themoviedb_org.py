# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import Progress, addon, dialog, VSupdate, isMatrix, SiteManager
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.tmdb import TMDb

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = '[COLOR orange]TheMovieDB[/COLOR]'
SITE_DESC = 'Base de données video.'

# doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

API_VERS = '3'
API_URL = URL_MAIN + API_VERS

# FANART_URL = 'https://image.tmdb.org/t/p/original/'
# https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

view = '500'
tmdb_session = ''
tmdb_account = ''


def load():
    gui = Gui()
    addons = addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'search/movie')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        addons.VSlang(30423),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'movie/now_playing')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30426),
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'movie/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30425),
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'genre/movie/list')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenreMovie',
        addons.VSlang(30428),
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'movie/top_rated')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30427),
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'search/tv')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        addons.VSlang(30424),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'tv/on_the_air')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30430),
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'tv/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30429),
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'genre/tv/list')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenreTV',
        addons.VSlang(30432),
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'tv/top_rated')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30431),
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'search/person')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchActor',
        addons.VSlang(30450),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'person/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showActors',
        addons.VSlang(30433),
        'actor.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        'topimdb',
        'load',
        'Top Imdb',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://')
    gui.addDir(
        SITE_IDENTIFIER,
        'showFolderList',
        'Listes TMDB',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMyTmdb():
    gui = Gui()
    grab = TMDb()
    addons = addon()

    tmdb_session = addons.getSetting('tmdb_session')
    if tmdb_session == '':
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'https://')
        gui.addDir(
            SITE_IDENTIFIER,
            'getToken',
            addons.VSlang(30305),
            'tmdb.png',
            output_parameter_handler)
    else:
        # pas de deco possible avec l'api donc on test l'username sinon ont
        # supprime tous
        result = grab.getUrl('account', '1', 'session_id=' + tmdb_session)

        if 'username' in result and result['username']:

            # pas de menu sans ID user c'est con
            addons.setSetting('tmdb_account', str(result['id']))

            sUsername = result['username']
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', 'https://')
            gui.addText(SITE_IDENTIFIER, (addons.VSlang(30306)) % sUsername)

            # /account/{account_id}/favorite/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/favorite/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30434),
                'films.png',
                output_parameter_handler)

            # /account/{account_id}/rated/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/rated/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30435),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/watchlist/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/watchlist/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30436),
                'views.png',
                output_parameter_handler)

            # /account/{account_id}/favorite/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/favorite/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30437),
                'series.png',
                output_parameter_handler)

            # /account/{account_id}/rated/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/rated/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30438),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/watchlist/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/watchlist/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30440),
                'views.png',
                output_parameter_handler)

            # /account/{account_id}/rated/tv/episodes
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/rated/tv/episodes' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30439),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/lists
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'siteUrl', 'account/%s/lists' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showUserLists',
                addons.VSlang(30441),
                'listes.png',
                output_parameter_handler)

            output_parameter_handler.addParameter('siteUrl', 'http://')
            gui.addDir(
                SITE_IDENTIFIER,
                'ouTMyTmdb',
                addons.VSlang(30309),
                'listes.png',
                output_parameter_handler)

        else:
            ouTMyTmdb()

    gui.setEndOfDirectory()


def ouTMyTmdb():
    addons = addon()
    addons.setSetting('tmdb_session', '')
    addons.setSetting('tmdb_account', '')

    dialog().VSinfo(addons.VSlang(30320))
    VSupdate()
    showMyTmdb()
    return


def getContext():
    addons = addon()
    dialogs = dialog()

    tmdb_account = addons.getSetting('tmdb_account')
    if tmdb_account == "":
        dialogs.VSerror(addons.VSlang(30442))
        return False, False, False

    disp = []
    lang = []
    fow = []
    yn = []

    disp.append('vote')
    fow.append('vote')
    yn.append(True)
    lang.append(addons.VSlang(30443))

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(True)
    lang.append(addons.VSlang(30444))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(True)
    lang.append(addons.VSlang(30445))

    disp.append('addtolist')
    fow.append('addtolist')
    yn.append(True)
    lang.append(addons.VSlang(31211))

    disp.append('addtonewlist')
    fow.append('addtonewlist')
    yn.append(True)
    lang.append(addons.VSlang(31210))

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(False)
    lang.append(addons.VSlang(30446))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(False)
    lang.append(addons.VSlang(30447))

    ret = dialogs.VSselect(lang, 'TMDB')
    if ret > -1:
        return disp[ret], fow[ret], yn[ret]

    return False


def getCat():

    disp = ['1', '2']
    dialogs = dialog()
    dialog_select = 'Films', 'Series'

    ret = dialogs.select('TMDB', dialog_select)
    if ret > -1:
        sType = disp[ret]

    return sType


def getAction():
    gui = Gui()
    grab = TMDb()
    dialogs = dialog()
    addons = addon()

    input_parameter_handler = InputParameterHandler()

    sAction = ''
    if not sAction:
        sAction, sFow, sYn = getContext()
    if not sAction:
        return

    sCat = input_parameter_handler.getValue('sCat')
    if not sCat:
        sCat = getCat()
    if not sCat:
        return

    # dans le doute si meta active
    sTMDB = input_parameter_handler.getValue('sTmdbId')
    sSeason = input_parameter_handler.getValue('sSeason')
    sEpisode = input_parameter_handler.getValue('sEpisode')

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    if not sTMDB:
        sTMDB = grab.get_idbyname(
            input_parameter_handler.getValue('sFileName'), '', sCat)
    if not sTMDB:
        return

    if sAction == 'vote':
        # vote /movie/{movie_id}/rating
        # /tv/{tv_id}/rating
        # /tv/{tv_id}/season/{season_number}/episode/{episode_number}/rating
        numboard = gui.showNumBoard('Min 0.5 - Max 10')
        if numboard is not None:
            if sSeason is not False and sEpisode is not False:
                sAction = '%s/%s/season/%s/episode/%s/rating' % (
                    sCat, sTMDB, sSeason, sEpisode)
            else:
                sAction = '%s/%s/rating' % (sCat, sTMDB)
            sPost = {"value": numboard}
        else:
            return

    elif sAction == 'addtolist':
        if sCat == 'tv':
            dialogs.VSinfo(
                "Vous ne pouvez pas ajouter une série à une liste de films tmdb")
            return
        result = grab.getUrl(
            'account/%s/lists' %
            addons.getSetting('tmdb_account'),
            term='session_id=%s' %
            addons.getSetting('tmdb_session'))
        total = len(result)
        if total == 0:
            return
        labels = []
        for i in result['results']:
            labels.append(i['name'])
        idliste = dialogs.VSselect(labels, addons.VSlang(31212))
        if idliste == -1:
            return

        idliste = result['results'][idliste]['id']
        sAction = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": sTMDB}

    elif sAction == 'addtonewlist':
        if sCat == 'tv':
            dialogs.VSinfo(
                "Vous ne pouvez pas ajouter une série à une liste de films tmdb")
            return
        # nom de la nouvelle liste
        listname = gui.showKeyBoard()
        if listname == '':
            return
        # creation de la liste
        sAction = 'list'
        sPost = {
            "name": listname,
            "description": " ",
            "language": "fr"
        }
        rep = grab.getPostUrl(sAction, sPost)
        # recuperer son id
        if 'success' in rep:
            idliste = rep['list_id']
        else:
            return
        # ajout du film à la nouvelle liste
        sAction = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": sTMDB}

    else:
        sPost = {"media_type": sCat, "media_id": sTMDB, sFow: sYn}

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        dialogs.VSinfo(data['status_message'])

    return


"""
# comme le cat change pour le type ont refait
def getWatchlist():
    grab = TMDb()
    addons = addon()

    tmdb_session = addons.getSetting('tmdb_session')
    tmdb_account = addons.getSetting('tmdb_account')

    if not tmdb_session:
        return

    if not tmdb_account:
        return

    input_parameter_handler = InputParameterHandler()
    sCat = input_parameter_handler.getValue('sCat')
    if not sCat:
        return

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    # dans le doute si meta active
    sTMDB = input_parameter_handler.getValue('sTmdbId')
    title = input_parameter_handler.getValue('sFileName')

# import re
#     if sCat == "tv":
#         sSeason = re.search('aison (\\d+)',title).group(1)
#         sEpisode = re.search('pisode (\\d+)',title).group(1)

    if not sTMDB:
        sTMDB = grab.get_idbyname(title, '', sCat)
    if not sTMDB:
        return

    sPost = {"media_type": sCat, "media_id": sTMDB, 'watchlist': True}
    sAction = 'account/%s/watchlist' % tmdb_account

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        dialog().VSinfo(data['status_message'])

    return

"""


def getToken():
    grab = TMDb()
    return grab.getToken()


def showSearchMovie():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showSeries(sSearchText.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showSearchActor():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showActors(sSearchText.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showGenreMovie():
    gui = Gui()
    grab = TMDb()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in result['genres']:
            sId, title = i['id'], i['name']

            if not isMatrix():
                title = title.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                str(title),
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenreTV():
    gui = Gui()
    grab = TMDb()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in result['genres']:
            sId, title = i['id'], i['name']

            if not isMatrix():
                title = title.encode("utf-8")
            # sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            sUrl = 'discover/tv'
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('genre', sId)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showUserLists():
    gui = Gui()
    grab = TMDb()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    term = ''
    if input_parameter_handler.exist('session_id'):
        term += 'session_id=' + input_parameter_handler.getValue('session_id')

    sUrl = input_parameter_handler.getValue('siteUrl')
    result = grab.getUrl(sUrl, iPage, term)
    results = result['results']
    # Compter le nombre de pages
    nbpages = result['total_pages']
    page = 2
    while page <= nbpages:
        result = grab.getUrl(sUrl, page, term)
        results += result['results']
        page += 1
    total = len(results)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in results:
            sId, title = i['id'], i['name']

            # sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            output_parameter_handler.addParameter('siteUrl', sId)
            gui.addDir(
                SITE_IDENTIFIER,
                'showLists',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showFolderList():
    gui = Gui()

    liste = []
    liste.append(['Top 50 des plus grands films', '10'])
    liste.append(['Gagnants des Oscars', '31670'])
    liste.append(['Les films fascinants ', '43'])
    liste.append(['science-fiction', '3945'])
    liste.append(['Les adaptations', '9883'])
    liste.append(['Disney Classic', '338'])
    liste.append(['Pixar', '3700'])
    liste.append(['Marvel', '1'])
    liste.append(['DC Comics Universe', '3'])
    liste.append(['Top Manga', '31665'])
    liste.append(['Top Manga 2', '31695'])
    liste.append(['Best séries', '36788'])
    liste.append(['Films de Noel', '40944'])
    # liste.append(['nom de la liste', 'ID de la liste'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showLists',
            title,
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    term = ''
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('sSearch'):
        sSearch = input_parameter_handler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if input_parameter_handler.exist('session_id'):
            term += 'session_id=' + \
                input_parameter_handler.getValue('session_id')

        sUrl = input_parameter_handler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        if total > 0:
            total = len(result['results'])
            progress_ = Progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                # Mise en forme des infos (au format meta imdb)
                i = grab._format(i, '', "movie")

                sId, title, sGenre, sThumb, sFanart, desc, sYear = i['tmdb_id'], i['title'], i[
                    'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    title = title.encode("utf-8")

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'siteUrl', 'http://tmdb/%s' % sId)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sTmdbId', sId)
                output_parameter_handler.addParameter('type', 'film')

                if isMatrix():
                    output_parameter_handler.addParameter('searchtext', title)
                else:
                    output_parameter_handler.addParameter(
                        'searchtext', cUtil().CleanName(title))

                Gui.CONTENT = "movies"
                oGuiElement = GuiElement()
                oGuiElement.setTmdbId(sId)
                oGuiElement.setSiteName('globalSearch')
                oGuiElement.setFunction('showSearch')
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon('films.png')
                oGuiElement.setMeta(1)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setFanart(sFanart)
                oGuiElement.setCat(1)
                oGuiElement.setDescription(desc)
                oGuiElement.setYear(sYear)
                oGuiElement.setGenre(sGenre)

                gui.addFolder(oGuiElement, output_parameter_handler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                output_parameter_handler = OutputParameterHandler()
                if sSearch:
                    output_parameter_handler.addParameter('sSearch', sSearch)

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('page', iNextPage)
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showMovies',
                    'Page ' + str(iNextPage),
                    output_parameter_handler)

    except TypeError as e:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showSeries(sSearch=''):
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    term = ''
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('sSearch'):
        sSearch = input_parameter_handler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = input_parameter_handler.getValue('siteUrl')

        if input_parameter_handler.exist('genre'):
            term = 'with_genres=' + input_parameter_handler.getValue('genre')

        if input_parameter_handler.exist('session_id'):
            term += 'session_id=' + \
                input_parameter_handler.getValue('session_id')

        result = grab.getUrl(sUrl, iPage, term)

    gui = Gui()

    try:
        total = len(result)

        if total > 0:
            total = len(result['results'])
            progress_ = Progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                # Mise en forme des infos (au format meta imdb)
                i = grab._format(i, '', "tvshow")
                sId, title, sGenre, sThumb, sFanart, desc, sYear = i['tmdb_id'], i['title'], i[
                    'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    title = title.encode("utf-8")

                sSiteUrl = 'tv/' + str(sId)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sSiteUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('sId', sId)
                output_parameter_handler.addParameter('sFanart', sFanart)
                output_parameter_handler.addParameter('sTmdbId', sId)

                if isMatrix():
                    output_parameter_handler.addParameter('searchtext', title)
                else:
                    output_parameter_handler.addParameter(
                        'searchtext', cUtil().CleanName(title))

                Gui.CONTENT = "tvshows"
                oGuiElement = GuiElement()
                oGuiElement.setTmdbId(sId)
                # à activer pour saisons
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeriesSaison')
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon('series.png')
                oGuiElement.setMeta(2)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setFanart(sFanart)
                oGuiElement.setCat(2)
                oGuiElement.setDescription(desc)
                oGuiElement.setYear(sYear)
                oGuiElement.setGenre(sGenre)

                gui.addFolder(oGuiElement, output_parameter_handler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('page', iNextPage)
                if sSearch:
                    output_parameter_handler.addParameter('sSearch', sSearch)
                if input_parameter_handler.exist('genre'):
                    output_parameter_handler.addParameter(
                        'genre', input_parameter_handler.getValue('genre'))
                gui.addNext(
                    SITE_IDENTIFIER,
                    'showSeries',
                    'Page ' + str(iNextPage),
                    output_parameter_handler)

    except TypeError:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showSeriesSaison():
    gui = Gui()
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()

    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sFanart = input_parameter_handler.getValue('sFanart')
    sTmdbId = input_parameter_handler.getValue('sTmdbId')
    sId = input_parameter_handler.getValue('sId')

    if sId is False:
        sId = sUrl.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    # recherche la serie complete
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sMovieTitle)
    # output_parameter_handler.addParameter('type', 'serie')
    # output_parameter_handler.addParameter('searchtext', sMovieTitle)
    if not isMatrix():
        output_parameter_handler.addParameter(
            'searchtext', cUtil().CleanName(sMovieTitle))
    else:
        output_parameter_handler.addParameter('searchtext', sMovieTitle)

    oGuiElement = GuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(addons.VSlang(30414))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    gui.addFolder(oGuiElement, output_parameter_handler)

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        total = len(result['seasons'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for i in result['seasons']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sNbreEp, SSeasonNum = i['episode_count'], i['season_number']

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '', "season")
            title, sGenre, sThumb, sFanart, desc, sYear = i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            title = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + str(sId) + '/season/' + str(SSeasonNum)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sId', sId)
            output_parameter_handler.addParameter('sSeason', SSeasonNum)
            output_parameter_handler.addParameter('sFanart', sFanart)
            output_parameter_handler.addParameter('sTmdbId', sTmdbId)

            Gui.CONTENT = "tvshows"
            oGuiElement = GuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeriesEpisode')
            oGuiElement.setTitle(title)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(7)
            oGuiElement.setDescription(desc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showSeriesEpisode():
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sFanart = input_parameter_handler.getValue('sFanart')
    sTmdbId = input_parameter_handler.getValue('sTmdbId')

    sSeason = input_parameter_handler.getValue('sSeason')
    # sId = input_parameter_handler.getValue('sId')
    if sSeason is False:
        sSeason = sUrl.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    gui = Gui()

    # recherche saison complète
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', sMovieTitle)
    # output_parameter_handler.addParameter('type', 'serie')
    search = '%s S%02d' % (sMovieTitle, int(sSeason))
    # output_parameter_handler.addParameter('searchtext', search)

    if not isMatrix():
        output_parameter_handler.addParameter(
            'searchtext', cUtil().CleanName(search))
    else:
        output_parameter_handler.addParameter('searchtext', search)

    oGuiElement = GuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(addons.VSlang(30415))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    gui.addFolder(oGuiElement, output_parameter_handler)

    result = grab.getUrl(sUrl)

    total = len(result)
    if total > 0 and 'episodes' in result:
        total = len(result['episodes'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for i in result['episodes']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # sId, title, sOtitle, sThumb, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sEpNumber = i['episode_number']

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '')
            title, sGenre, sThumb, sFanart, desc, sYear = i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            title = 'S%s E%s %s' % (sSeason, str(sEpNumber), title)

            sExtraTitle = ' S' + \
                "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            output_parameter_handler.addParameter(
                'siteUrl', sMovieTitle + '|' + sExtraTitle)  # Pour compatibilite Favoris
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sTmdbId', sTmdbId)
            output_parameter_handler.addParameter('sSeason', sSeason)
            output_parameter_handler.addParameter('sEpisode', sEpNumber)
            output_parameter_handler.addParameter('type', 'serie')

            if not isMatrix():
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(sMovieTitle))
            else:
                output_parameter_handler.addParameter(
                    'searchtext', sMovieTitle)

            Gui.CONTENT = "tvshows"
            oGuiElement = GuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(title)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)
            oGuiElement.setDescription(desc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')
    gui.setEndOfDirectory(view)


def showActors(sSearch=''):
    gui = Gui()
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('sSearch'):
        sSearch = input_parameter_handler.getValue('sSearch')

    if sSearch:
        # format obligatoire évite de modif le format de l'url dans la lib >> _call
        # à cause d'un ? pas ou il faut pour ça >> invalid api key
        result = grab.getUrl(sUrl, iPage, 'query=' + sSearch)

    else:
        result = grab.getUrl(sUrl, iPage)

    total = len(result)

    if total > 0:
        total = len(result['results'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        # récup le nombre de page pour NextPage
        nbrpage = result['total_pages']

        for i in result['results']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sName, sThumb = i['name'], i['profile_path']

            if sThumb:
                POSTER_URL = grab.poster
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if not isMatrix():
                sName = sName.encode('utf-8')

            output_parameter_handler.addParameter(
                'siteUrl', 'person/' + str(i['id']) + '/movie_credits')
            title = str(sName)

            oGuiElement = GuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showFilmActor')
            oGuiElement.setTitle(title)
            oGuiElement.setFileName(sName)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setCat(7)

            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

        if int(iPage) < int(nbrpage):
            iNextPage = int(iPage) + 1
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('page', iNextPage)

            # ajoute param sSearch pour garder le bon format d'url avec grab
            # url
            if sSearch:
                output_parameter_handler.addParameter('sSearch', sSearch)

            gui.addNext(
                SITE_IDENTIFIER,
                'showActors',
                'Page ' + str(iNextPage),
                output_parameter_handler)

    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showFilmActor():
    gui = Gui()
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    if total > 0:
        total = len(result['cast'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for i in result['cast']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '', "person")

            sId, title, sGenre, sThumb, sFanart, desc, sYear = i['tmdb_id'], i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            output_parameter_handler.addParameter(
                'siteUrl', 'http://tmdb/%s' % sId)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sTmdbId', sId)
            output_parameter_handler.addParameter('type', 'film')

            if not isMatrix():
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(title))
            else:
                output_parameter_handler.addParameter('searchtext', title)

            Gui.CONTENT = "movies"
            oGuiElement = GuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(title)
            oGuiElement.setFileName(title)
            oGuiElement.setIcon('films.png')
            oGuiElement.setMeta(1)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            oGuiElement.setDescription(desc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showLists():
    gui = Gui()
    grab = TMDb()
    addons = addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    sUrl = input_parameter_handler.getValue('siteUrl')
    result = grab.getUrl('list/' + sUrl, iPage, '')
    total = len(result)
    if total > 0:
        total = len(result['items'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for i in result['items']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '')

            sId, title, sType, sThumb, sFanart, sVote, desc, sYear = i['tmdb_id'], i['title'], i[
                'media_type'], i['poster_path'], i['backdrop_path'], i['rating'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            sDisplayTitle = "%s (%s)" % (title, sVote)

            output_parameter_handler.addParameter(
                'siteUrl', 'http://tmdb/%s' % sId)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sId', sId)
            output_parameter_handler.addParameter('sFanart', sFanart)
            output_parameter_handler.addParameter('sTmdbId', sId)

            if isMatrix():
                output_parameter_handler.addParameter('searchtext', title)
            else:
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(title))

            Gui.CONTENT = "movies"
            oGuiElement = GuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sDisplayTitle)
            oGuiElement.setFileName(title)
            if sType == 'movie':
                oGuiElement.setIcon('films.png')
                oGuiElement.setMeta(1)
                oGuiElement.setCat(1)
            elif sType == 'tv':
                oGuiElement.setIcon('series.png')
                oGuiElement.setMeta(2)
                oGuiElement.setCat(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setDescription(desc)
            oGuiElement.setYear(sYear)
            if 'genre' in i:
                oGuiElement.setGenre(i['genre'])

            gui.addFolder(oGuiElement, output_parameter_handler)

        progress_.VSclose(progress_)

    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def __checkForNextPage(sHtmlContent):
    return False
