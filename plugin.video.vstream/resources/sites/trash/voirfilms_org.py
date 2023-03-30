# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import QuoteSafe, Quote
import re

SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms'
SITE_DESC = 'Films, Séries & Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = 'https://wvv.voirfilms.club/'  # url de repli site sans pub

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_LIST = (URL_MAIN + 'alphabet', 'showAlpha')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_LIST = (URL_MAIN + 'series/alphabet', 'showAlpha')
SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_LIST = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?type=film&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?type=serie&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'recherche?type=anime&s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_LIST[1],
        'Films (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_ANNEES[1],
        'Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnims():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        'Animés (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def AlphaSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    progress_ = Progress().VScreate(SITE_NAME)
    output_parameter_handler = OutputParameterHandler()
    for i in range(0, 27):
        progress_.VSupdate(progress_, 36)

        if i > 0:
            title = chr(64 + i)
        else:
            title = '09'

        output_parameter_handler.addParameter('siteUrl', sUrl + title.upper())
        output_parameter_handler.addParameter('sMovieTitle', title)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action_1'])
    liste.append(['Animation', sUrl + 'animation_1'])
    liste.append(['Arts Martiaux', sUrl + 'arts-martiaux_1'])
    liste.append(['Aventure', sUrl + 'aventure_1'])
    liste.append(['Biopic', sUrl + 'biopic_1'])
    liste.append(['Comédie', sUrl + 'film-comedie'])
    liste.append(['Comédie Dramatique', sUrl + 'comedie-dramatique_1'])
    liste.append(['Documentaire', sUrl + 'documentaire_1'])
    liste.append(['Drame', sUrl + 'drame_1'])
    liste.append(['Epouvante Horreur', sUrl + 'epouvante-horreur_1'])
    liste.append(['Erotique', sUrl + 'erotique_1'])
    liste.append(['Espionnage', sUrl + 'espionnage_1'])
    liste.append(['Fantastique', sUrl + 'fantastique_1'])
    liste.append(['Guerre', sUrl + 'guerre_1'])
    liste.append(['Historique', sUrl + 'historique_1'])
    liste.append(['Musical', sUrl + 'musical_1'])
    liste.append(['Policier', sUrl + 'policier_1'])
    liste.append(['Romance', sUrl + 'romance_1'])
    liste.append(['Science Fiction', sUrl + 'science-fiction_1'])
    liste.append(['Série', sUrl + 'series_1'])
    liste.append(['Thriller', sUrl + 'thriller_1'])
    liste.append(['Western', sUrl + 'western_1'])
    liste.append(['Non classé', sUrl + 'non-classe_1'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:

        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1913, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'series/annee-' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'series' in sUrl:
        code = 'series/alphabet/'
    else:
        code = 'alphabet/'

    liste = []
    liste.append(['0', URL_MAIN + code + '0'])
    liste.append(['1', URL_MAIN + code + '1'])
    liste.append(['2', URL_MAIN + code + '2'])
    liste.append(['3', URL_MAIN + code + '3'])
    liste.append(['4', URL_MAIN + code + '4'])
    liste.append(['5', URL_MAIN + code + '5'])
    liste.append(['6', URL_MAIN + code + '6'])
    liste.append(['7', URL_MAIN + code + '7'])
    liste.append(['8', URL_MAIN + code + '8'])
    liste.append(['9', URL_MAIN + code + '9'])
    liste.append(['A', URL_MAIN + code + 'A'])
    liste.append(['B', URL_MAIN + code + 'B'])
    liste.append(['C', URL_MAIN + code + 'C'])
    liste.append(['D', URL_MAIN + code + 'D'])
    liste.append(['E', URL_MAIN + code + 'E'])
    liste.append(['F', URL_MAIN + code + 'F'])
    liste.append(['G', URL_MAIN + code + 'G'])
    liste.append(['H', URL_MAIN + code + 'H'])
    liste.append(['I', URL_MAIN + code + 'I'])
    liste.append(['J', URL_MAIN + code + 'J'])
    liste.append(['K', URL_MAIN + code + 'K'])
    liste.append(['L', URL_MAIN + code + 'L'])
    liste.append(['M', URL_MAIN + code + 'M'])
    liste.append(['N', URL_MAIN + code + 'N'])
    liste.append(['O', URL_MAIN + code + 'O'])
    liste.append(['P', URL_MAIN + code + 'P'])
    liste.append(['Q', URL_MAIN + code + 'Q'])
    liste.append(['R', URL_MAIN + code + 'R'])
    liste.append(['S', URL_MAIN + code + 'S'])
    liste.append(['T', URL_MAIN + code + 'T'])
    liste.append(['U', URL_MAIN + code + 'U'])
    liste.append(['V', URL_MAIN + code + 'V'])
    liste.append(['W', URL_MAIN + code + 'W'])
    liste.append(['X', URL_MAIN + code + 'X'])
    liste.append(['Y', URL_MAIN + code + 'Y'])
    liste.append(['Z', URL_MAIN + code + 'Z'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:

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


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        sUrl = sSearch

        sTypeSearch = oParser.parseSingleResult(sUrl, '\\?type=(.+?)&')
        if sTypeSearch[0]:
            sTypeSearch = sTypeSearch[1]
        else:
            sTypeSearch = False

        oRequest = RequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')

        sHtmlContent = oRequest.request()

        sPattern = '<div class="unfilm".+?href="([^"]+)" title="([^"]+).+?class="type ([^"]+)".+?<img src="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = re.sub('alt="title="', 'alt="', sHtmlContent)  # anime
        sPattern = '<div class="unfilm".+?href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                title = aEntry[1]
                sType = aEntry[2]
                sThumb = aEntry[3]
                sYear = aEntry[5]
                sQual = aEntry[6]
                if sTypeSearch:
                    if sTypeSearch != sType:  # genre recherché:  film/serie/anime
                        continue
            else:
                sThumb = aEntry[1]
                title = aEntry[2]
                sYear = aEntry[4]
                sQual = aEntry[5]

            sUrl = aEntry[0]
            if 'http' not in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            title = title.replace('film ', '')  # genre
            title = title.replace(' streaming', '')  # genre

            sLang = ''
            if 'Vostfr' in title:
                title = title.replace('Vostfr', '')
                sLang = 'VOSTFR'

            sDisplayTitle = '%s [%s] (%s) (%s)' % (title, sQual, sLang, sYear)

            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            # not found better way
            # title = unicode(title, errors='replace')
            # title = title.encode('ascii', 'ignore').decode('ascii')

            # vStream don't work with unicode url for the moment
            # sThumb = unicode(sThumb, 'UTF-8')
            # sThumb = sThumb.encode('ascii', 'ignore').decode('ascii')
            # sThumb = sThumb.decode('utf8')

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sQual', sQual)

            if '/serie' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showS_E',
                    sDisplayTitle,
                    sThumb,
                    sThumb,
                    '',
                    output_parameter_handler)
            elif 'anime' in sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showS_E',
                    sDisplayTitle,
                    sThumb,
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    sThumb,
                    sThumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sPaging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sHtmlContent = re.sub(" rel='nofollow'", "", sHtmlContent)  # next genre
    sPattern = ">([^<]+)</a><a href='([^']+)'>suiv »"
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        if sNextPage.startswith('/'):
            sNextPage = URL_MAIN[:-1] + sNextPage
        sNumberNext = re.findall('([0-9]+)', sNextPage)[-1]
        sPaging = str(sNumberNext) + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    # patch for unicode url
    sUrl = QuoteSafe(sUrl)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-src="([^"]+)" target="filmPlayer".+?span class="([^"]+)"></span>.+?class="([^"]+)"></span>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sHost = aEntry[1].capitalize()
            if 'apidgator' in sHost or 'dl_to' in sHost:
                continue

            sLang = aEntry[2].upper().replace('L', '')
            title = '%s (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle,
                                                          sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)

            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    sPattern = 'href="(https:\\/\\/cineactu.co\\/.+?").*?span class="([^"]+).*?class="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sHost = aEntry[1]
            if 'fichier' in sHost:
                sHost = '1 Fichier'
            if 'uptobox' in sHost:
                sHost = 'Uptobox'
            sHost = sHost.capitalize()  # ou autres ?

            sLang = aEntry[2].upper().replace('L', '')
            title = '%s (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle,
                                                          sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('siteReferer', sUrl)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHostersDL',
                title,
                sThumb,
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showS_E():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sHtmlContent = sHtmlContent.replace("\r\t", "")
    if '-saison-' in sUrl or 'anime' in sUrl:
        sPattern = '<a class="n_episode2" title=".+?, *([A-Z]+) *,.+?" *href="([^"]+)">(.+?)</a></li>'
    else:
        sPattern = '<div class="unepetitesaisons">[^<>]*?<a href="([^"]+)" title="([^"]+)">'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            # Si plusieurs langues sont disponibles, une seule est affichée ici.
            # Ne rien mettre, la langue sera ajoutée avec le host
            if 'anime' in sUrl:
                sUrl2 = aEntry[1]
                sNM = aEntry[2].replace('<span>', '').replace('</span>', '')
                title = sMovieTitle + ' E' + sNM
                sDisplayTitle = title
            elif '-saison-' in sUrl:
                sUrl2 = aEntry[1]
                sNM = aEntry[2].replace('<span>', ' ').replace('</span>', '')
                title = sMovieTitle + sNM
                sDisplayTitle = title
            else:
                sUrl2 = aEntry[0]
                title = re.sub('\\d x ', 'E', aEntry[1])
                title = title.replace('EP ', 'E')
                sDisplayTitle = title

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN + sUrl2

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '-episode-' in sUrl2 or '/anime' in sUrl:
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showS_E',
                    sDisplayTitle,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    host = sUrl.split('/')[0:3]
    host = host[0] + '//' + host[2] + '/'

    # VSlog('org > ' + sUrl)

    # Attention ne marche pas dans tout les cas, certain site retourne aussi
    # un 302 et la lib n'en gere qu'un
    if False:
        # On recupere la redirection
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', host)
        sHtmlContent = oRequestHandler.request()
        redirection_target = oRequestHandler.getRealUrl()

    else:
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', host)
        sHtmlContent = oRequestHandler.request()

        redirection_target = sUrl

        if oRequestHandler.statusCode() == 302:
            redirection_target = reponse.getResponseHeader()['Location']

    # attention fake redirection
    sUrl = redirection_target
    try:
        m = re.search(r'url=([^"]+)', sHtmlContent)
    except BaseException:
        m = re.search(r'url=([^"]+)', str(sHtmlContent))

    if m:
        sUrl = m.group(1)

    # Modifications
    sUrl = sUrl.replace('1wskdbkp.xyz', 'youwatch.org')
    if '1fichier' in sUrl:
        sUrl = re.sub('(http.+?\\?link=)', 'https://1fichier.com/?', sUrl)

    sHosterUrl = sUrl
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHostersDL():
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    siteReferer = input_parameter_handler.getValue('siteReferer')

    if 'cineactu.co' in sUrl:  # tjrs vrai mais au cas ou autre pattern fait sur host DL
        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', siteReferer)
        oRequestHandler.request()
        redirection_target = oRequestHandler.getRealUrl()
        if 'shortn.co' in redirection_target:
            bvalid, shost = Hoster_shortn(redirection_target, sUrl)
            if bvalid:
                sHosterUrl = shost
                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def Hoster_shortn(url, refer):
    shost = ''
    # url="https://shortn.co/f/6183943"
    url = url.replace('%22', '')
    oRequestHandler = RequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', refer)
    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    sPattern = "type.*?name=.*?value='([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        token = aResult[0]
        data = '_token=' + token
        oRequestHandler = RequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry(
            'Accept',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry(
            'Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParametersLine(data)
        sHtmlContent = oRequestHandler.request()

        # https://1fichier.com/?jttay6v60izpcu3rank7
        # https://uptobox.com/vy7g5a6itlgj?aff_id=10831504
        sPattern = 'href="([^"]+).+?target="_blank'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            shost = aResult[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
