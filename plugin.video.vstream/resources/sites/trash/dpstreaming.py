# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress, dialog
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmc
import requests
import re
return False  # Cloudflare 15/01/2021


SITE_IDENTIFIER = 'dpstreaming'
SITE_NAME = 'DP Streaming'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = "https://series.dpstreaming.to/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'serie-category/series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'serie-category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def protectStreamByPass(url):
    if url.startswith('/'):
        url = URL_MAIN[:-1] + url

    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

    session = requests.Session()
    session.headers.update(
        {
            'User-Agent': UA,
            'Referer': URL_MAIN,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('erreur ' + str(e))
        return ''

    sHtmlContent = response.text

    oParser = Parser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        dialog().VSinfo('Décodage en cours', 'Patientez', 5)
        xbmc.sleep(5000)

        postdata = aResult[1][0]
        headers = {'User-Agent': UA, 'Accept': '*/*', 'Referer': url,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        session.headers.update(headers)
        data = {'k': postdata}

        try:
            response = session.post(URL_MAIN + 'embed_secur.php', data=data)
        except requests.exceptions.RequestException as e:
            print('erreur' + str(e))
            return ''

        data = response.text
        data = data.encode('utf-8', 'ignore')

        # Test de fonctionnement
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            dialog().VSinfo('Lien encore protegé', 'Erreur', 5)
            return ''

        # recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            return aResult[1][0]

        # recherche d'un lien redirigee
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            return aResult[1][0]

    return ''


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeriesSearch',
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

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Classique', 'classique'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'],
             ['Dessin animés', 'dessin-anime'], ['Divers', 'divers'], ['Documentaires', 'documentaire'],
             ['Drama', 'drama'], ['Drame', 'drame'], ['Epouvante-Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Expérimental', 'experimental'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'], ['soap', 'soap'],
             ['Thriller', 'thriller'], ['Websérie', 'webserie'], ['Western', 'western']]

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter(
            'siteUrl', URL_MAIN + 'serie-category/series/' + sUrl + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    input_parameter_handler = InputParameterHandler()

    if sSearch:
        sUrl = sSearch
        sUrl = sUrl.replace('%20', '+').replace(' ', '+')

    else:
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = re.sub(
        'src="https://dpstreaming.to/wp-content/plugins/wp-fastest-cache-premium/pro/images/blank.gif"',
        '',
        sHtmlContent)
    sPattern = '<div class="moviefilm".+?<a href="([^"]+)".+?<img.+?src="([^"]+)" alt="([^"]+)".+?<p>(.+?)</p>'
    oParser = Parser()
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

            sUrl = aEntry[0]
            sThumb = re.sub('-119x125', '', aEntry[1])
            title = aEntry[2].replace(' Streaming', '')
            desc = aEntry[3]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addTV(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:  # une seule page par recherche
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="([^"]+)">»</a>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSeries():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis plus complet que dans showmovies
    desc = ''
    try:
        sPattern = 'class="lab_syn">Synopsis :</span>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0].decode('utf-8')
            desc = cUtil().unescape(desc).encode('utf-8')
    except BaseException:
        pass

    sPattern = '<a href="([^"]+)" class.+?><span>([^<]+)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            title = sMovieTitle + ' episode ' + aEntry[1]

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

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    sPattern = 'class="lg" width=".+?">(?:(VF|VOSTFR|VO))</td>.+?<td class="lg" width=".+?">([^<]+)</td.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sLang = aEntry[0]
            sHost = aEntry[1]
            sUrl = aEntry[2]

            sDisplayTitle = (
                '%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addLink(
                SITE_IDENTIFIER,
                'serieHosters',
                sDisplayTitle,
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def serieHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    sHosterUrl = protectStreamByPass(sUrl)

    oHoster = HosterGui().checkHoster(sHosterUrl)

    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()
