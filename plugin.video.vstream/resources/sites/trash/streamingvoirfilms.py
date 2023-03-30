# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons 9bed026547
import json
import re
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/66.0'

SITE_IDENTIFIER = 'streamingvoirfilms'
SITE_NAME = 'Streamingvoirfilms'
SITE_DESC = ' StreamingVoirfilms Vous propose un large choix des nouveaux et vieux films.'

URL_MAIN = 'https://streamingvoirfilms.com/'
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (URL_MAIN + 'wp-json/dooplay/glossary/?term=$$&nonce=9bed026547&type=movies', 'showAlpha')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_LIST = (URL_MAIN + 'wp-json/dooplay/glossary/?term=$$&nonce=9bed026547&type=tvshows', 'showAlpha')
SERIE_SEASONS = (URL_MAIN + 'saisons/', 'showMovies')

FUNCTION_SEARCH = 'showList'
URL_SEARCH = (URL_MAIN + 'wp-json/dooplay/search/?keyword=', 'showList')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showList')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showList')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'listes.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Episode derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SEASONS[0])
    oGui.addDir(
        SITE_IDENTIFIER,
        SERIE_SEASONS[1],
        'Séries (Saison derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Toutes les séries)', 'series.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'listes.png', output_parameter_handler)
    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showList(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/'])
    liste.append(['Action & Adventure', URL_MAIN + 'genre/action-adventure/'])
    liste.append(['Animation', URL_MAIN + 'genre/animation/'])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/'])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/'])
    liste.append(['Crime', URL_MAIN + 'genre/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'genre/drame/'])
    liste.append(['Familial', URL_MAIN + 'genre/familial/'])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'genre/histoire/'])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/'])
    liste.append(['Musique', URL_MAIN + 'genre/musique/'])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/'])
    liste.append(['Romance', URL_MAIN + 'genre/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'genre/science-fiction/'])
    liste.append(['Science Fiction & Fantastique', URL_MAIN + 'genre/science-fiction-fantastique/'])
    liste.append(['Téléfilm', URL_MAIN + 'genre/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/'])
    liste.append(['Western', URL_MAIN + 'genre/western/'])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    # liste.append( ['#', sUrl.replace('$$','09')] ) fonctionne pas sur le site
    liste.append(['A', sUrl.replace('$$', 'a')])
    liste.append(['B', sUrl.replace('$$', 'b')])
    liste.append(['C', sUrl.replace('$$', 'c')])
    liste.append(['D', sUrl.replace('$$', 'd')])
    liste.append(['E', sUrl.replace('$$', 'e')])
    liste.append(['F', sUrl.replace('$$', 'f')])
    liste.append(['G', sUrl.replace('$$', 'g')])
    liste.append(['H', sUrl.replace('$$', 'h')])
    liste.append(['I', sUrl.replace('$$', 'i')])
    liste.append(['J', sUrl.replace('$$', 'j')])
    liste.append(['K', sUrl.replace('$$', 'k')])
    liste.append(['L', sUrl.replace('$$', 'l')])
    liste.append(['M', sUrl.replace('$$', 'm')])
    liste.append(['N', sUrl.replace('$$', 'n')])
    liste.append(['O', sUrl.replace('$$', 'o')])
    liste.append(['P', sUrl.replace('$$', 'p')])
    liste.append(['Q', sUrl.replace('$$', 'q')])
    liste.append(['R', sUrl.replace('$$', 'r')])
    liste.append(['S', sUrl.replace('$$', 's')])
    liste.append(['T', sUrl.replace('$$', 't')])
    liste.append(['U', sUrl.replace('$$', 'u')])
    liste.append(['V', sUrl.replace('$$', 'v')])
    liste.append(['W', sUrl.replace('$$', 'w')])
    liste.append(['X', sUrl.replace('$$', 'x')])
    liste.append(['Y', sUrl.replace('$$', 'y')])
    liste.append(['Z', sUrl.replace('$$', 'z')])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(
            SITE_IDENTIFIER,
            'showList',
            'Lettre [COLOR coral]' +
            sTitle +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    oGui.setEndOfDirectory()


def showList(sSearch=''):
    oGui = Gui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+') + '&nonce=9bed026547'
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    page = json.loads(sHtmlContent)

    if page:
        for x in page:
            sUrl = page[x]["url"]
            sTitle = page[x]["title"].encode('utf-8')

            sThumb = page[x]["img"].replace('90x135', '185x278')  # pas mieux

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if 'series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, '', output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showMovies():
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '/films' in sUrl or '/series' in sUrl:
        sPattern = 'data-src="([^"]+)" alt="([^"]+)">.+?<a href="([^"]+)".+?<div class="texto">([^<]+)<\\/div>'
    else:
        sPattern = 'data-src="([^"]+)" alt="([^"]+)">.+?<a href="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            sDesc = ''

            if '/films' in sUrl or '/series' in sUrl:
                sDesc = aEntry[3]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/series' in sUrl2 or '/saisons' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, output_parameter_handler)
            elif '/episodes' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', output_parameter_handler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class=\'arrow_pag\' href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSaisonEpisodes():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "<span class='title'>([^<]+)<i>|<div class='numerando'>(\\d+) - (\\d+)</div>.+?class='episodiotitle'><a href='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[3]
                sTitle = 'Saison ' + aEntry[1] + ' Episode' + aEntry[2] + ' ' + sMovieTitle

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter('sMovieTitle', sTitle)
                output_parameter_handler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = cParser()
    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern2 = "data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)'>.+?<span class='title'>([^<]+)<\\/span><span class='server'>([^<]+)<\\/span>.+?<img src='([^']+)'>"
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHost = aEntry[4].capitalize()
            sLang = aEntry[5].split('/')[-1].replace('.png', '').capitalize()
            sQual = aEntry[3]

            postdata = 'action=doo_player_ajax&post=' + aEntry[1] + '&nume=' + aEntry[2] + '&type=' + aEntry[0]

            sDisplayTitle = ('%s (%s %s %s)') % (sMovieTitle, sLang, sQual, sHost)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('postdata', postdata)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    postdata = input_parameter_handler.getValue('postdata')

    oRequest = RequestHandler(URL_MAIN + '/wp-admin/admin-ajax.php')
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    # oRequest.addHeaderEntry('Accept', '*/*')
    # oRequest.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
    # oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addParametersLine(postdata)
    sHtmlContent = oRequest.request()

    sPattern = "<iframe.+?src='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
