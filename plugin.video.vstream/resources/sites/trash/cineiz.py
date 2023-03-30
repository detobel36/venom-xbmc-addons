# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, VSlog
import re
return false

SITE_IDENTIFIER = 'cineiz'
SITE_NAME = 'Cineiz'
SITE_DESC = 'Films, Séries et mangas en streaming'

URL_MAIN = 'https://ww3.cineiz.io/'

URL_SEARCH = ('', 'showMovieSearch')
URL_SEARCH_MOVIES = ('', 'showMovieSearch')
URL_SEARCH_SERIES = ('', 'showMovieSearch')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_GENRES = ('http://film', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = ('http://film', 'showList')

SERIE_NEWS = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_GENRES = ('http://serie', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (True, 'showList')

ANIM_NEWS = (URL_MAIN + 'animes/dernier/', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.htm', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')
ANIM_GENRES = (True, 'showGenres')
ANIM_ANNEES = (True, 'showAnimesYears')
ANIM_ENFANTS = (URL_MAIN + 'animes', 'showMovies')
ANIM_LIST = (True, 'showAnimesList')


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par Années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VIEWS[1],
        'Animés (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Liste)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovieSearch(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'film' in sUrl:
        code = 'films-genre-'
    elif 'serie' in sUrl:
        code = 'series-tv/genre-'
    else:
        code = 'animes-du-genre-'

    liste = []
    liste.append(['Action', URL_MAIN + code + 'action.htm'])
    liste.append(['Animation', URL_MAIN + code + 'animation.htm'])
    liste.append(['Arts Martiaux', URL_MAIN + code + 'arts-martiaux.htm'])
    liste.append(['Aventure', URL_MAIN + code + 'aventure.htm'])
    liste.append(['Biopic', URL_MAIN + code + 'biopic.htm'])
    liste.append(['Classique', URL_MAIN + code + 'classique.htm'])
    liste.append(['Comédie', URL_MAIN + code + 'comedie.htm'])
    liste.append(['Comédie Dramatique', URL_MAIN +
                 code + 'comedie-dramatique.htm'])
    liste.append(['Comédie Musicale', URL_MAIN +
                 code + 'comedie-musicale.htm'])
    liste.append(['Dessin animé', URL_MAIN + code + 'dessin-anime.htm'])
    liste.append(['Divers', URL_MAIN + code + 'divers.htm'])
    liste.append(['Documentaire', URL_MAIN + code + 'documentaire.htm'])
    liste.append(['Drame', URL_MAIN + code + 'drame.htm'])
    liste.append(['Epouvante Horreur', URL_MAIN +
                 code + 'epouvante-horreur.htm'])
    liste.append(['Erotique', URL_MAIN + code + 'erotique.htm'])
    liste.append(['Espionnage', URL_MAIN + code + 'espionnage.htm'])
    liste.append(['Expérimental', URL_MAIN + code + 'experimental.htm'])
    liste.append(['Famille', URL_MAIN + code + 'famille.htm'])
    liste.append(['Fantastique', URL_MAIN + code + 'fantastique.htm'])
    liste.append(['Guerre', URL_MAIN + code + 'guerre.htm'])
    liste.append(['Historique', URL_MAIN + code + 'historique.htm'])
    liste.append(['Judicaire', URL_MAIN + code + 'judiciaire.htm'])
    liste.append(['Musical', URL_MAIN + code + 'musical.htm'])
    liste.append(['Policier', URL_MAIN + code + 'policier.htm'])
    liste.append(['Péplum', URL_MAIN + code + 'peplum.htm'])
    liste.append(['Romance', URL_MAIN + code + 'romance.htm'])
    liste.append(['Science Fiction', URL_MAIN + code + 'science-fiction.htm'])
    liste.append(['Sport event', URL_MAIN + code + 'sport-event.htm'])
    liste.append(['Thriller', URL_MAIN + code + 'thriller.htm'])
    liste.append(['Western', URL_MAIN + code + 'western.htm'])
    liste.append(['Non classé', URL_MAIN + code + 'non-classe.htm'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'film' in sUrl:
        code = 'films-commence-par-'
    else:
        code = 'series-tv/commence-par-'

    liste = []
    liste.append(['0', URL_MAIN + code + '0.htm'])
    liste.append(['1', URL_MAIN + code + '1.htm'])
    liste.append(['2', URL_MAIN + code + '2.htm'])
    liste.append(['3', URL_MAIN + code + '3.htm'])
    liste.append(['4', URL_MAIN + code + '4.htm'])
    liste.append(['5', URL_MAIN + code + '5.htm'])
    liste.append(['6', URL_MAIN + code + '6.htm'])
    liste.append(['7', URL_MAIN + code + '7.htm'])
    liste.append(['8', URL_MAIN + code + '8.htm'])
    liste.append(['9', URL_MAIN + code + '9.htm'])
    liste.append(['A', URL_MAIN + code + 'A.htm'])
    liste.append(['B', URL_MAIN + code + 'b.htm'])
    liste.append(['C', URL_MAIN + code + 'C.htm'])
    liste.append(['D', URL_MAIN + code + 'D.htm'])
    liste.append(['E', URL_MAIN + code + 'E.htm'])
    liste.append(['F', URL_MAIN + code + 'F.htm'])
    liste.append(['G', URL_MAIN + code + 'G.htm'])
    liste.append(['H', URL_MAIN + code + 'H.htm'])
    liste.append(['I', URL_MAIN + code + 'I.htm'])
    liste.append(['J', URL_MAIN + code + 'J.htm'])
    liste.append(['K', URL_MAIN + code + 'K.htm'])
    liste.append(['L', URL_MAIN + code + 'L.htm'])
    liste.append(['M', URL_MAIN + code + 'M.htm'])
    liste.append(['N', URL_MAIN + code + 'N.htm'])
    liste.append(['O', URL_MAIN + code + 'O.htm'])
    liste.append(['P', URL_MAIN + code + 'P.htm'])
    liste.append(['Q', URL_MAIN + code + 'Q.htm'])
    liste.append(['R', URL_MAIN + code + 'R.htm'])
    liste.append(['S', URL_MAIN + code + 'S.htm'])
    liste.append(['T', URL_MAIN + code + 'T.htm'])
    liste.append(['U', URL_MAIN + code + 'U.htm'])
    liste.append(['V', URL_MAIN + code + 'V.htm'])
    liste.append(['W', URL_MAIN + code + 'W.htm'])
    liste.append(['X', URL_MAIN + code + 'X.htm'])
    liste.append(['Y', URL_MAIN + code + 'Y.htm'])
    liste.append(['Z', URL_MAIN + code + 'Z.htm'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimesList():
    gui = Gui()

    liste = []
    liste.append(['09', URL_MAIN + 'animes/alphabet/09'])
    liste.append(['A', URL_MAIN + 'animes/alphabet/A'])
    liste.append(['B', URL_MAIN + 'animes/alphabet/B'])
    liste.append(['C', URL_MAIN + 'animes/alphabet/C'])
    liste.append(['D', URL_MAIN + 'animes/alphabet/D'])
    liste.append(['E', URL_MAIN + 'animes/alphabet/E'])
    liste.append(['F', URL_MAIN + 'animes/alphabet/F'])
    liste.append(['G', URL_MAIN + 'animes/alphabet/G'])
    liste.append(['H', URL_MAIN + 'animes/alphabet/H'])
    liste.append(['I', URL_MAIN + 'animes/alphabet/I'])
    liste.append(['J', URL_MAIN + 'animes/alphabet/J'])
    liste.append(['K', URL_MAIN + 'animes/alphabet/K'])
    liste.append(['L', URL_MAIN + 'animes/alphabet/L'])
    liste.append(['M', URL_MAIN + 'animes/alphabet/M'])
    liste.append(['N', URL_MAIN + 'animes/alphabet/N'])
    liste.append(['O', URL_MAIN + 'animes/alphabet/O'])
    liste.append(['P', URL_MAIN + 'animes/alphabet/P'])
    liste.append(['Q', URL_MAIN + 'animes/alphabet/Q'])
    liste.append(['R', URL_MAIN + 'animes/alphabet/R'])
    liste.append(['S', URL_MAIN + 'animes/alphabet/S'])
    liste.append(['T', URL_MAIN + 'animes/alphabet/T'])
    liste.append(['U', URL_MAIN + 'animes/alphabet/U'])
    liste.append(['V', URL_MAIN + 'animes/alphabet/V'])
    liste.append(['W', URL_MAIN + 'animes/alphabet/W'])
    liste.append(['X', URL_MAIN + 'animes/alphabet/X'])
    liste.append(['Y', URL_MAIN + 'animes/alphabet/Y'])
    liste.append(['Z', URL_MAIN + 'animes/alphabet/Z'])

    for title, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    for i in reversed(xrange(1921, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films-annee-' + Year + '.htm')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    for i in reversed(xrange(1961, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'series-tv/annee-' + Year + '.htm')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieSearch(sSearch=''):
    gui = Gui()

    if not sSearch:
        return
    else:
        sUrl = URL_MAIN + 'recherche'

    oRequestHandler = RequestHandler(sUrl)
    # oRequestHandler.addHeaderEntry('Referer', 'https://www.cineiz.io/recherche')
    oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('action', 'recherche')
    oRequestHandler.addParameters('story', sSearch)

    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="linkfilm">(.+?)</span>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            sThumb = URL_MAIN + str(aEntry[1])
            title = str(aEntry[2])
            desc = ''

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/series-tv/' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            elif '/anime/' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="xquality">(.+?)</span>.+?<span class="xlangue">(.+?)</span>.+?<span class="linkfilm">(.+?)</span>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1])
            if 'films' in sUrl:
                sQual = str(aEntry[2])
                sLang = str(aEntry[3])
            else:
                sQual = ''
                sLang = ''
            title = str(aEntry[4])
            desc = ''

            sDisplayTitle = ('%s (%s) (%s)') % (title, sQual, sLang.upper())

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            elif '/anime' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<a href=\'([^<]+)\' rel=\'nofollow\'>suiv »'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        if aResult[1][0].startswith('/'):
            return URL_MAIN[:-1] + aResult[1][0]
        else:
            return aResult[1][0]

    return False


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unepetitesaisons"><a href="(.+?)" title=.+?<div class="etlelien">(.+?)</div>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            # title = str(aEntry[1]) + sMovieTitle
            title = ('%s %s') % (aEntry[1], sMovieTitle)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="n_episode2".+?href="([^"]+)"><span class="head">(.+?)</span><span class="body">(.+?)</span>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = str(aEntry[1]) + str(aEntry[2]) + ' ' + sMovieTitle
            sUrl2 = str(aEntry[0])
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    import threading
    threads = []

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    # faut post
    oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('levideo', '123456')
    sHtmlContent = oRequestHandler.request().replace(
        '<span class="telecharger_sur_uptobox"></span>', '')

    desc = ''
    try:
        sPattern = '<p>Synopsis.+?</strong> :(.+?)<\\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0]
    except BaseException:
        pass

    sPattern = '<div class="num_link">Lien:.+?<span class="(.+?)".+?span style="width:55px;" class="(.+?)">.+?<input name="levideo" value="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHost = str(aEntry[0]).capitalize()
            if 'Nowvideo' in sHost:
                continue
            sLang = str(aEntry[1])
            sPost = str(aEntry[2])
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sPost', sPost)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            # gui.addMovie(SITE_IDENTIFIER, 'showHosters', title, '', sThumb, desc, output_parameter_handler)
            # dispo a la version 0.6.2
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace(
        'https://streamcomplet.cineiz.io', URL_MAIN)
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sPost = input_parameter_handler.getValue('sPost')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters('levideo', sPost)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '</script></div></div><iframe src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            url = URL_MAIN + aEntry
            oRequestHandler = RequestHandler(url)
            sHtmlContent = oRequestHandler.request()
            sHosterUrl = oRequestHandler.getRealUrl()

            if 'facebook.com' in sHosterUrl:
                continue

            if 'vimple.org' in sHosterUrl:
                oRequestHandler = RequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                sHtmlContent2 = oRequestHandler.request()
                try:
                    sHosterUrl = re.search(
                        'url=([^"]+)"', sHtmlContent2, re.DOTALL).group(1)
                except BaseException:
                    sHosterUrl = str(oRequestHandler.getRealUrl())

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
