# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import Progress, Addon, dialog, VSupdate, isMatrix, SiteManager
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
    addons = Addon()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'search/movie')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchMovie',
        addons.VSlang(30423),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'movie/now_playing')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30426),
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'movie/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30425),
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'genre/movie/list')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenreMovie',
        addons.VSlang(30428),
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'movie/top_rated')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        addons.VSlang(30427),
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'search/tv')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchSerie',
        addons.VSlang(30424),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'tv/on_the_air')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30430),
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'tv/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30429),
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'genre/tv/list')
    gui.addDir(
        SITE_IDENTIFIER,
        'showGenreTV',
        addons.VSlang(30432),
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'tv/top_rated')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeries',
        addons.VSlang(30431),
        'notes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'search/person')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearchActor',
        addons.VSlang(30450),
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'person/popular')
    gui.addDir(
        SITE_IDENTIFIER,
        'showActors',
        addons.VSlang(30433),
        'actor.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://')
    gui.addDir(
        'topimdb',
        'load',
        'Top Imdb',
        'star.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://')
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
    addons = Addon()

    tmdb_session = addons.getSetting('tmdb_session')
    if tmdb_session == '':
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'https://')
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

            username = result['username']
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', 'https://')
            gui.addText(SITE_IDENTIFIER, (addons.VSlang(30306)) % username)

            # /account/{account_id}/favorite/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/favorite/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30434),
                'films.png',
                output_parameter_handler)

            # /account/{account_id}/rated/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/rated/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30435),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/watchlist/movies
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/watchlist/movies' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                addons.VSlang(30436),
                'views.png',
                output_parameter_handler)

            # /account/{account_id}/favorite/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/favorite/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30437),
                'series.png',
                output_parameter_handler)

            # /account/{account_id}/rated/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/rated/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30438),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/watchlist/tv
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/watchlist/tv' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30440),
                'views.png',
                output_parameter_handler)

            # /account/{account_id}/rated/tv/episodes
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/rated/tv/episodes' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                addons.VSlang(30439),
                'notes.png',
                output_parameter_handler)

            # /account/{account_id}/lists
            output_parameter_handler.addParameter('session_id', tmdb_session)
            output_parameter_handler.addParameter(
                'site_url', 'account/%s/lists' % int(result['id']))
            gui.addDir(
                SITE_IDENTIFIER,
                'showUserLists',
                addons.VSlang(30441),
                'listes.png',
                output_parameter_handler)

            output_parameter_handler.addParameter('site_url', 'http://')
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
    addons = Addon()
    addons.setSetting('tmdb_session', '')
    addons.setSetting('tmdb_account', '')

    dialog().VSinfo(addons.VSlang(30320))
    VSupdate()
    showMyTmdb()
    return


def getContext():
    addons = Addon()
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
        _type = disp[ret]

    return _type


def getAction():
    gui = Gui()
    grab = TMDb()
    dialogs = dialog()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()

    action = ''
    if not action:
        action, sFow, sYn = getContext()
    if not action:
        return

    cat = input_parameter_handler.getValue('cat')
    if not cat:
        cat = getCat()
    if not cat:
        return

    # dans le doute si meta active
    tmdb = input_parameter_handler.getValue('tmdb_id')
    season = input_parameter_handler.getValue('season')
    sEpisode = input_parameter_handler.getValue('sEpisode')

    cat = cat.replace('1', 'movie').replace('2', 'tv')

    if not tmdb:
        tmdb = grab.get_idbyname(
            input_parameter_handler.getValue('file_name'), '', cat)
    if not tmdb:
        return

    if action == 'vote':
        # vote /movie/{movie_id}/rating
        # /tv/{tv_id}/rating
        # /tv/{tv_id}/season/{season_number}/episode/{episode_number}/rating
        numboard = gui.showNumBoard('Min 0.5 - Max 10')
        if numboard is not None:
            if season is not False and sEpisode is not False:
                action = '%s/%s/season/%s/episode/%s/rating' % (
                    cat, tmdb, season, sEpisode)
            else:
                action = '%s/%s/rating' % (cat, tmdb)
            sPost = {"value": numboard}
        else:
            return

    elif action == 'addtolist':
        if cat == 'tv':
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
        action = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": tmdb}

    elif action == 'addtonewlist':
        if cat == 'tv':
            dialogs.VSinfo(
                "Vous ne pouvez pas ajouter une série à une liste de films tmdb")
            return
        # nom de la nouvelle liste
        listname = gui.showKeyBoard()
        if listname == '':
            return
        # creation de la liste
        action = 'list'
        sPost = {
            "name": listname,
            "description": " ",
            "language": "fr"
        }
        rep = grab.getPostUrl(action, sPost)
        # recuperer son id
        if 'success' in rep:
            idliste = rep['list_id']
        else:
            return
        # ajout du film à la nouvelle liste
        action = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": tmdb}

    else:
        sPost = {"media_type": cat, "media_id": tmdb, sFow: sYn}

    data = grab.getPostUrl(action, sPost)

    if len(data) > 0:
        dialogs.VSinfo(data['status_message'])

    return


"""
# comme le cat change pour le type ont refait
def getWatchlist():
    grab = TMDb()
    addons = Addon()

    tmdb_session = addons.getSetting('tmdb_session')
    tmdb_account = addons.getSetting('tmdb_account')

    if not tmdb_session:
        return

    if not tmdb_account:
        return

    input_parameter_handler = InputParameterHandler()
    cat = input_parameter_handler.getValue('cat')
    if not cat:
        return

    cat = cat.replace('1', 'movie').replace('2', 'tv')

    # dans le doute si meta active
    tmdb = input_parameter_handler.getValue('tmdb_id')
    title = input_parameter_handler.getValue('file_name')

# import re
#     if cat == "tv":
#         season = re.search('aison (\\d+)',title).group(1)
#         sEpisode = re.search('pisode (\\d+)',title).group(1)

    if not tmdb:
        tmdb = grab.get_idbyname(title, '', cat)
    if not tmdb:
        return

    sPost = {"media_type": cat, "media_id": tmdb, 'watchlist': True}
    action = 'account/%s/watchlist' % tmdb_account

    data = grab.getPostUrl(action, sPost)

    if len(data) > 0:
        dialog().VSinfo(data['status_message'])

    return

"""


def getToken():
    grab = TMDb()
    return grab.getToken()


def showSearchMovie():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showMovies(search_text.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showSearchSerie():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showSeries(search_text.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showSearchActor():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        showActors(search_text.replace(' ', '+'))
        # gui.setEndOfDirectory()
        return


def showGenreMovie():
    gui = Gui()
    grab = TMDb()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    result = grab.getUrl(url)
    total = len(result)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in result['genres']:
            s_id, title = i['id'], i['name']

            if not isMatrix():
                title = title.encode("utf-8")
            url = 'genre/' + str(s_id) + '/movies'
            output_parameter_handler.addParameter('site_url', url)
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
    url = input_parameter_handler.getValue('site_url')

    result = grab.getUrl(url)
    total = len(result)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in result['genres']:
            s_id, title = i['id'], i['name']

            if not isMatrix():
                title = title.encode("utf-8")
            # url = API_URL + '/genre/' + str(s_id) + '/tv'
            url = 'discover/tv'
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('genre', s_id)
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

    url = input_parameter_handler.getValue('site_url')
    result = grab.getUrl(url, iPage, term)
    results = result['results']
    # Compter le nombre de pages
    nbpages = result['total_pages']
    page = 2
    while page <= nbpages:
        result = grab.getUrl(url, page, term)
        results += result['results']
        page += 1
    total = len(results)
    if total > 0:
        output_parameter_handler = OutputParameterHandler()
        for i in results:
            s_id, title = i['id'], i['name']

            # url = API_URL + '/genre/' + str(s_id) + '/tv'
            output_parameter_handler.addParameter('site_url', s_id)
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showLists',
            title,
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    grab = TMDb()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    term = ''
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('search'):
        search = input_parameter_handler.getValue('search')

    if search:
        result = grab.getUrl('search/movie', iPage, 'query=' + search)
        url = ''

    else:
        if input_parameter_handler.exist('session_id'):
            term += 'session_id=' + \
                input_parameter_handler.getValue('session_id')

        url = input_parameter_handler.getValue('site_url')
        result = grab.getUrl(url, iPage, term)

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

                s_id, title, sGenre, thumb, sFanart, desc, year = i['tmdb_id'], i['title'], i[
                    'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    title = title.encode("utf-8")

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'site_url', 'http://tmdb/%s' % s_id)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('tmdb_id', s_id)
                output_parameter_handler.addParameter('type', 'film')

                if isMatrix():
                    output_parameter_handler.addParameter('searchtext', title)
                else:
                    output_parameter_handler.addParameter(
                        'searchtext', cUtil().CleanName(title))

                Gui.CONTENT = "movies"
                gui_element = GuiElement()
                gui_element.setTmdbId(s_id)
                gui_element.setSiteName('globalSearch')
                gui_element.setFunction('showSearch')
                gui_element.setTitle(title)
                gui_element.setFileName(title)
                gui_element.setIcon('films.png')
                gui_element.setMeta(1)
                gui_element.setThumbnail(thumb)
                gui_element.setPoster(thumb)
                gui_element.setFanart(sFanart)
                gui_element.setCat(1)
                gui_element.setDescription(desc)
                gui_element.setYear(year)
                gui_element.setGenre(sGenre)

                gui.addFolder(gui_element, output_parameter_handler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                output_parameter_handler = OutputParameterHandler()
                if search:
                    output_parameter_handler.addParameter('search', search)

                output_parameter_handler.addParameter('site_url', url)
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


def showSeries(search=''):
    grab = TMDb()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    term = ''
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('search'):
        search = input_parameter_handler.getValue('search')

    if search:
        result = grab.getUrl('search/tv', iPage, 'query=' + search)
        url = ''

    else:
        url = input_parameter_handler.getValue('site_url')

        if input_parameter_handler.exist('genre'):
            term = 'with_genres=' + input_parameter_handler.getValue('genre')

        if input_parameter_handler.exist('session_id'):
            term += 'session_id=' + \
                input_parameter_handler.getValue('session_id')

        result = grab.getUrl(url, iPage, term)

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
                s_id, title, sGenre, thumb, sFanart, desc, year = i['tmdb_id'], i['title'], i[
                    'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    title = title.encode("utf-8")

                site_url = 'tv/' + str(s_id)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', site_url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('s_id', s_id)
                output_parameter_handler.addParameter('sFanart', sFanart)
                output_parameter_handler.addParameter('tmdb_id', s_id)

                if isMatrix():
                    output_parameter_handler.addParameter('searchtext', title)
                else:
                    output_parameter_handler.addParameter(
                        'searchtext', cUtil().CleanName(title))

                Gui.CONTENT = "tvshows"
                gui_element = GuiElement()
                gui_element.setTmdbId(s_id)
                # à activer pour saisons
                gui_element.setSiteName(SITE_IDENTIFIER)
                gui_element.setFunction('showSeriesSaison')
                gui_element.setTitle(title)
                gui_element.setFileName(title)
                gui_element.setIcon('series.png')
                gui_element.setMeta(2)
                gui_element.setThumbnail(thumb)
                gui_element.setPoster(thumb)
                gui_element.setFanart(sFanart)
                gui_element.setCat(2)
                gui_element.setDescription(desc)
                gui_element.setYear(year)
                gui_element.setGenre(sGenre)

                gui.addFolder(gui_element, output_parameter_handler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('page', iNextPage)
                if search:
                    output_parameter_handler.addParameter('search', search)
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
    addons = Addon()

    input_parameter_handler = InputParameterHandler()

    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    sFanart = input_parameter_handler.getValue('sFanart')
    tmdb_id = input_parameter_handler.getValue('tmdb_id')
    s_id = input_parameter_handler.getValue('s_id')

    if s_id is False:
        s_id = url.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    # recherche la serie complete
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', movie_title)
    # output_parameter_handler.addParameter('type', 'serie')
    # output_parameter_handler.addParameter('searchtext', movie_title)
    if not isMatrix():
        output_parameter_handler.addParameter(
            'searchtext', cUtil().CleanName(movie_title))
    else:
        output_parameter_handler.addParameter('searchtext', movie_title)

    gui_element = GuiElement()
    gui_element.setSiteName('globalSearch')
    gui_element.setFunction('searchMovie')
    gui_element.setTitle(addons.VSlang(30414))
    gui_element.setCat(2)
    gui_element.setIcon("searchtmdb.png")
    gui.addFolder(gui_element, output_parameter_handler)

    result = grab.getUrl(url)
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
            title, sGenre, thumb, sFanart, desc, year = i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            title = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            url = 'tv/' + str(s_id) + '/season/' + str(SSeasonNum)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('s_id', s_id)
            output_parameter_handler.addParameter('season', SSeasonNum)
            output_parameter_handler.addParameter('sFanart', sFanart)
            output_parameter_handler.addParameter('tmdb_id', tmdb_id)

            Gui.CONTENT = "tvshows"
            gui_element = GuiElement()
            gui_element.setTmdbId(tmdb_id)
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setFunction('showSeriesEpisode')
            gui_element.setTitle(title)
            gui_element.setFileName(movie_title)
            gui_element.setIcon('series.png')
            gui_element.setMeta(2)
            gui_element.setThumbnail(thumb)
            gui_element.setPoster(thumb)
            gui_element.setFanart(sFanart)
            gui_element.setCat(7)
            gui_element.setDescription(desc)
            gui_element.setYear(year)
            gui_element.setGenre(sGenre)

            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showSeriesEpisode():
    grab = TMDb()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    sFanart = input_parameter_handler.getValue('sFanart')
    tmdb_id = input_parameter_handler.getValue('tmdb_id')

    season = input_parameter_handler.getValue('season')
    # s_id = input_parameter_handler.getValue('s_id')
    if season is False:
        season = url.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    gui = Gui()

    # recherche saison complète
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', movie_title)
    # output_parameter_handler.addParameter('type', 'serie')
    search = '%s S%02d' % (movie_title, int(season))
    # output_parameter_handler.addParameter('searchtext', search)

    if not isMatrix():
        output_parameter_handler.addParameter(
            'searchtext', cUtil().CleanName(search))
    else:
        output_parameter_handler.addParameter('searchtext', search)

    gui_element = GuiElement()
    gui_element.setSiteName('globalSearch')
    gui_element.setFunction('searchMovie')
    gui_element.setTitle(addons.VSlang(30415))
    gui_element.setCat(2)
    gui_element.setIcon("searchtmdb.png")
    gui.addFolder(gui_element, output_parameter_handler)

    result = grab.getUrl(url)

    total = len(result)
    if total > 0 and 'episodes' in result:
        total = len(result['episodes'])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for i in result['episodes']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # s_id, title, sOtitle, thumb, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sEpNumber = i['episode_number']

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '')
            title, sGenre, thumb, sFanart, desc, year = i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            title = 'S%s E%s %s' % (season, str(sEpNumber), title)

            sExtraTitle = ' S' + \
                "%02d" % int(season) + 'E' + "%02d" % int(sEpNumber)

            output_parameter_handler.addParameter(
                'site_url', movie_title + '|' + sExtraTitle)  # Pour compatibilite Favoris
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('tmdb_id', tmdb_id)
            output_parameter_handler.addParameter('season', season)
            output_parameter_handler.addParameter('sEpisode', sEpNumber)
            output_parameter_handler.addParameter('type', 'serie')

            if not isMatrix():
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(movie_title))
            else:
                output_parameter_handler.addParameter(
                    'searchtext', movie_title)

            Gui.CONTENT = "tvshows"
            gui_element = GuiElement()
            gui_element.setTmdbId(tmdb_id)
            gui_element.setSiteName('globalSearch')
            gui_element.setFunction('showSearch')
            gui_element.setTitle(title)
            gui_element.setFileName(movie_title)
            gui_element.setIcon('series.png')
            gui_element.setMeta(2)
            gui_element.setThumbnail(thumb)
            gui_element.setFanart(sFanart)
            gui_element.setCat(2)
            gui_element.setDescription(desc)
            gui_element.setYear(year)
            gui_element.setGenre(sGenre)

            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')
    gui.setEndOfDirectory(view)


def showActors(search=''):
    gui = Gui()
    grab = TMDb()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    if input_parameter_handler.exist('search'):
        search = input_parameter_handler.getValue('search')

    if search:
        # format obligatoire évite de modif le format de l'url dans la lib >> _call
        # à cause d'un ? pas ou il faut pour ça >> invalid api key
        result = grab.getUrl(url, iPage, 'query=' + search)

    else:
        result = grab.getUrl(url, iPage)

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

            sName, thumb = i['name'], i['profile_path']

            if thumb:
                POSTER_URL = grab.poster
                thumb = POSTER_URL + thumb
            else:
                thumb = ''

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)

            if not isMatrix():
                sName = sName.encode('utf-8')

            output_parameter_handler.addParameter(
                'site_url', 'person/' + str(i['id']) + '/movie_credits')
            title = str(sName)

            gui_element = GuiElement()
            gui_element.setSiteName(SITE_IDENTIFIER)
            gui_element.setFunction('showFilmActor')
            gui_element.setTitle(title)
            gui_element.setFileName(sName)
            gui_element.setIcon('actors.png')
            gui_element.setMeta(0)
            gui_element.setThumbnail(thumb)
            gui_element.setPoster(thumb)
            gui_element.setCat(7)

            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

        if int(iPage) < int(nbrpage):
            iNextPage = int(iPage) + 1
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('page', iNextPage)

            # ajoute param search pour garder le bon format d'url avec grab
            # url
            if search:
                output_parameter_handler.addParameter('search', search)

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
    addons = Addon()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    result = grab.getUrl(url, iPage)

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

            s_id, title, sGenre, thumb, sFanart, desc, year = i['tmdb_id'], i['title'], i[
                'genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            output_parameter_handler.addParameter(
                'site_url', 'http://tmdb/%s' % s_id)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('tmdb_id', s_id)
            output_parameter_handler.addParameter('type', 'film')

            if not isMatrix():
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(title))
            else:
                output_parameter_handler.addParameter('searchtext', title)

            Gui.CONTENT = "movies"
            gui_element = GuiElement()
            gui_element.setTmdbId(s_id)
            gui_element.setSiteName('globalSearch')
            gui_element.setFunction('showSearch')
            gui_element.setTitle(title)
            gui_element.setFileName(title)
            gui_element.setIcon('films.png')
            gui_element.setMeta(1)
            gui_element.setThumbnail(thumb)
            gui_element.setPoster(thumb)
            gui_element.setFanart(sFanart)
            gui_element.setCat(1)
            gui_element.setDescription(desc)
            gui_element.setYear(year)
            gui_element.setGenre(sGenre)

            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def showLists():
    gui = Gui()
    grab = TMDb()
    addons = Addon()

    input_parameter_handler = InputParameterHandler()

    iPage = 1
    if input_parameter_handler.exist('page'):
        iPage = input_parameter_handler.getValue('page')

    url = input_parameter_handler.getValue('site_url')
    result = grab.getUrl('list/' + url, iPage, '')
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

            s_id, title, _type, thumb, sFanart, sVote, desc, year = i['tmdb_id'], i['title'], i[
                'media_type'], i['poster_path'], i['backdrop_path'], i['rating'], i['plot'], i['year']

            if not isMatrix():
                title = title.encode("utf-8")

            display_title = "%s (%s)" % (title, sVote)

            output_parameter_handler.addParameter(
                'site_url', 'http://tmdb/%s' % s_id)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('s_id', s_id)
            output_parameter_handler.addParameter('sFanart', sFanart)
            output_parameter_handler.addParameter('tmdb_id', s_id)

            if isMatrix():
                output_parameter_handler.addParameter('searchtext', title)
            else:
                output_parameter_handler.addParameter(
                    'searchtext', cUtil().CleanName(title))

            Gui.CONTENT = "movies"
            gui_element = GuiElement()
            gui_element.setTmdbId(s_id)
            gui_element.setSiteName('globalSearch')
            gui_element.setFunction('showSearch')
            gui_element.setTitle(display_title)
            gui_element.setFileName(title)
            if _type == 'movie':
                gui_element.setIcon('films.png')
                gui_element.setMeta(1)
                gui_element.setCat(1)
            elif _type == 'tv':
                gui_element.setIcon('series.png')
                gui_element.setMeta(2)
                gui_element.setCat(2)
            gui_element.setThumbnail(thumb)
            gui_element.setPoster(thumb)
            gui_element.setFanart(sFanart)
            gui_element.setDescription(desc)
            gui_element.setYear(year)
            if 'genre' in i:
                gui_element.setGenre(i['genre'])

            gui.addFolder(gui_element, output_parameter_handler)

        progress_.VSclose(progress_)

    view = addons.getSetting('visuel-view')

    gui.setEndOfDirectory(view)


def __checkForNextPage(html_content):
    return False
