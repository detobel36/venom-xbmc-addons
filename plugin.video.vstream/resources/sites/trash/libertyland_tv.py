# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # de nouveau en panne au 08/07/22


SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et séries récentes en streaming et en téléchargement'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + 'v2/recherche/', 'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    'v2/recherche/categorie=films&mot_search=',
    'showMovies')
URL_SEARCH_SERIES = (
    URL_MAIN +
    'v2/recherche/categorie=series&mot_search=',
    'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/nouveautes/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/plus-vus-mois/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films/les-mieux-notes/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus vus)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
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
        'Recherche série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
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


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovieGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biographie', 'biographie'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Drame', 'drame'], ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Historique', 'historique'], ['Horreur', 'horreur'],
             ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Sport', 'sport'], ['Thriller', 'thriller'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films/genre/' + sUrl + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animé', 'anime'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['DC Comics', 'dc-comics'], ['Documentaire', 'documentaire'], ['Drama', 'drama'], ['Drame', 'drame'],
             ['Emission TV', 'emission-tv'], ['Epouvante-Horreur', 'epouvante-horreur'], ['Fantastique', 'fantastique'],
             ['Gore', 'gore'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Mystère', 'mystere'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Série TV', 'serie-tv'], ['Thriller', 'thriller'], ['Télé-réalité', 'tele-realite']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'v2/series/genre/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieAnnees():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1914, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieAnnees():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1989, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'v2/series/annee/' + Year + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        sUrl = sSearch
        sPattern = '<img class="img-responsive" *src="([^"]+)".+?<div class="divtelecha.+?href="([^"]+)">([^<>]+)<'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        if '/series' in sUrl:
            sPattern = '<div class="divtelecha.+?href="([^"]+)"><strong>([^<]+)</strong>.+?<img class="img-responsive".+?src="([^"]+).+?serie de (\\d{4})<.+?Synopsis :([^<]+)'
        else:  # films
            sPattern = '<h2 class="heading"> *<a href="[^"]+">([^<]+).+?<img class="img-responsive" *src="([^"]+)" *alt.+?(?:<font color="#.+?">([^<]+)</font>.+?).+?>film de (\\d{4})<.+?Synopsis : ([^<]+).+?<div class="divtelecha.+?href="([^"]+)'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
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

            desc = ''
            sYear = ''
            if sSearch:
                sQual = ''
                sThumb = URL_MAIN[:-1] + aEntry[0]
                title = aEntry[2].replace(
                    'télécharger ', '').replace(
                    'en Streaming', '')
                title = title.replace(
                    ' TELECHARGEMENT GRATUIT', '').replace(
                    'gratuitement', '')
                sUrl2 = aEntry[1]
            elif '/series' in sUrl:
                sQual = ''
                sUrl2 = aEntry[0]
                title = aEntry[1].replace(
                    'Regarder ', '').replace(
                    'en Streaming', '')
                sThumb = URL_MAIN[:-1] + aEntry[2]
                sYear = aEntry[3]

                try:
                    desc = aEntry[4].decode('utf-8')
                except AttributeError:
                    pass

                desc = cUtil().unescape(desc).encode('utf-8')
            else:
                title = aEntry[0]
                sThumb = URL_MAIN[:-1] + aEntry[1]
                sYear = aEntry[3]

                try:
                    desc = aEntry[4].decode('utf-8')
                except AttributeError:
                    pass

                desc = cUtil().unescape(desc).encode('utf-8')
                sUrl2 = aEntry[5]

                sQual = aEntry[2]
                if sQual:

                    try:
                        sQual = sQual.decode("utf-8")
                    except AttributeError:
                        pass

                    sQual = sQual.replace(
                        u' qualit\u00E9', '').replace(
                        'et ', '/').replace(
                        'Haute', 'HD') .replace(
                        ' ', '').replace(
                        'Bonne', 'DVD').replace(
                        'Mauvaise', 'SD').encode("utf-8")

            if 'https' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sUrl2 = sUrl2.replace('telecharger', 'streaming')

            try:
                title = title.decode("utf-8")
            except AttributeError:
                pass

            title = title.replace(
                u'T\u00E9l\u00E9charger ',
                '').encode("utf-8")

            # Remplace tout les decodage en python 3
            try:
                title = str(title, 'utf-8')
                sQual = str(sQual, 'utf-8')
                desc = str(desc, 'utf-8')
            except BaseException:
                pass

            sDisplayTitle = ('%s [%s] (%s)') % (title, sQual, sYear)

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('sYear', sYear)
            output_parameter_handler.addParameter('sQual', sQual)

            if '/series/' in sUrl or '/series/' in sUrl2 or '/series_co/' in sThumb:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisonsEpisodes',
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

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.findall('([0-9]+)', sNextPage)[-1]
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<li><a href="([^"]+)" class="next">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN[:-1] + aResult[1][0]

    return False


def ReformatUrl(link):
    if '/v2/mangas' in link:
        return link
    if '/telecharger/' in link:
        return link.replace('telecharger', 'streaming')
    if '-telecharger-' in link:
        f = link.split('/')[-1]
        return '/'.join(link.split('/')[:-1]) + \
            '/streaming/' + f.replace('-telecharger', '')
    # if ('/v2/' in link) and ('/streaming/' in link):
        # return link.replace('/v2/', '/')
    # if ('/v2/' in link) and ('/genre/' in link):
        # return link
    # if '/v2/' in link:
        # return link.replace('/v2/', '/streaming/')
    return link


def showSaisonsEpisodes():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')
    sYear = input_parameter_handler.getValue('sYear')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(?:<h2 class="heading-small">(Saison .+?)<)|(?:<li><a title=".+? \\| (.+?)" class="num_episode" href="([^"]+)")'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]')
            else:
                ePisode = aEntry[1].replace(',', '')
                title = sMovieTitle + ' ' + ePisode
                sUrl = aEntry[2]
                if 'https' not in sUrl:
                    sUrl = URL_MAIN[:-1] + sUrl

                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter(
                    'sYear', sYear)  # utilisé par le skin
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showLinks',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    # reformatage url
    sUrl = ReformatUrl(sUrl)

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sType = ''
    if '/films' in sUrl:
        sType = 'films'
    elif 'saison' in sUrl or 'episode' in sUrl:
        sType = 'series'

    sUrl2 = sUrl.rsplit('/', 1)[1]
    idMov = re.sub('-.+', '', sUrl2)

    sPattern = '<div title="([^"]+)".+?streaming="([^"]+)" heberger="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            if 'VF' in aEntry[0]:
                sLang = 'VF'
            elif 'VOSTFR' in aEntry[0]:
                sLang = 'VOSTFR'
            else:
                sLang = 'VO'

            idHeb = aEntry[1]
            sHost = aEntry[2].capitalize()
            title = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)
            output_parameter_handler.addParameter('sHost', sHost)
            output_parameter_handler.addParameter('sType', sType)
            output_parameter_handler.addParameter('idMov', idMov)
            output_parameter_handler.addParameter('idHeb', idHeb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                sThumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    sType = input_parameter_handler.getValue('sType')
    idHeb = input_parameter_handler.getValue('idHeb')

    if input_parameter_handler.exist('idMov'):  # film
        idMov = input_parameter_handler.getValue('idMov')
        pdata = 'id=' + idHeb + '&id_movie=' + idMov + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'
    else:  # serie pas d'idmov
        pdata = 'id=' + idHeb + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'

    pUrl = pUrl + '?' + pdata

    oRequest = RequestHandler(pUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<iframe.+?src="([^"]+)".+?"qualite":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            sQual = aEntry[1]

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    else:
        # au cas où pas de qualité
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
