# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import Parser
# from resources.lib.util import cUtil
import re
import urllib
import base64

SITE_IDENTIFIER = 'papystreaming_org'
SITE_NAME = 'Papystreaming'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'https://papystreaming.org/'

MOVIE_NEWS = (URL_MAIN + 'nouveaux-films-hd/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-streaming-hd-2017/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaire-hd/', 'showMovies')
# MOVIE_VIEWS = (URL_MAIN + 'de-visite/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'de-vote/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series-streaming-hd/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series-streaming-hd/', 'showSeries')
SERIE_COMMENTS = (URL_MAIN + 'populaire-hd/', 'showSeries')
# SERIE_VIEWS = (URL_MAIN + 'de-visite/', 'showSeries')
SERIE_NOTES = (URL_MAIN + 'de-vote/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH2 = (URL_MAIN + '?s=', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
# series et films melangé sur certaine fonction tri obligatoire qui bloque
# l'optimisation
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = {'User-Agent': UA}


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMSearch',
        'Recherche Film',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSSearch',
        'Recherche Série',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuFilms',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuSeries',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuFilms():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_COMMENTS[1],
        'Films (Les plus commentés)',
        'comments.png',
        output_parameter_handler)

#    Résultat des comments et des views identiques
#    output_parameter_handler = OutputParameterHandler()
#    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
#    gui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NOTES[1],
        'Films (Les mieux notés)',
        'notes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuSeries():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_COMMENTS[1],
        'Séries (Les plus commentées)',
        'comments.png',
        output_parameter_handler)

#    Résultat des comments et des views identiques
#    output_parameter_handler = OutputParameterHandler()
#    output_parameter_handler.addParameter('siteUrl', SERIE_VIEWS[0])
#    gui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NOTES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NOTES[1],
        'Séries (Les mieux notées)',
        'notes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/action/'])
    liste.append(['Animation', URL_MAIN + 'category/animation/'])
    liste.append(['Aventure', URL_MAIN + 'category/aventure/'])
    liste.append(['Comédie', URL_MAIN + 'category/comedie/'])
    liste.append(['Crime', URL_MAIN + 'category/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'category/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'category/drame/'])
    liste.append(['Étranger', URL_MAIN + 'category/etranger/'])
    liste.append(['Familial', URL_MAIN + 'category/familial/'])
    liste.append(['Fantastique', URL_MAIN + 'category/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'category/histoire/'])
    liste.append(['Horreur', URL_MAIN + 'category/papystreaming_horreur/'])
    liste.append(['Musique', URL_MAIN + 'category/musique/'])
    liste.append(['Mystère', URL_MAIN + 'category/mystere/'])
    liste.append(['Romance', URL_MAIN + 'category/romance/'])
    liste.append(['Science-Fiction', URL_MAIN + 'category/science-fiction/'])
    liste.append(['Soap', URL_MAIN + 'category/soap/'])
    liste.append(['Sport', URL_MAIN + 'category/Sport/'])
    liste.append(['Téléfilm', URL_MAIN + 'category/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'category/thriller/'])
    liste.append(['Western', URL_MAIN + 'category/western/'])

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


def showMSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showSSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH2[0] + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<a class="poster" href="([^"]+)"\\s+title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            if '/serie/' in sUrl:
                continue
            sThumb = aEntry[2]
            title = aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('thumbnail', sThumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'films.png',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

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
    sPattern = '<span class="current">.+?<\\/span><\\/li><li><a href="([^"]+)"'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSeries(sSearch=''):
    gui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<a class="poster" href="([^"]+)"\\s+title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            if 'film' in sUrl:
                continue
            sThumb = aEntry[2]
            title = aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('thumbnail', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                sThumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showSeries',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sSyn = ''
    sPattern = '<p class=".+?">([^<]+)<\\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sSyn = aResult[1][0]

    sPattern = '<a class="expand-season-trigger" data-toggle="collapse".+?href="([^"]+)".+?<\\/span>([^<]+)<\\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            vUrl = sUrl + aEntry[0]
            sSaison = sMovieTitle + aEntry[1]
            sSaison = sSaison.replace('N/A', '')
            sFilter = oParser.getNumberFromString(aEntry[1])
            sFilter = 'saison-' + sFilter + '/'

            sDisplayTitle = sSaison
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', vUrl)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('thumbnail', thumbnail)
            output_parameter_handler.addParameter('sSyn', sSyn)
            output_parameter_handler.addParameter('sFilter', sFilter)
            gui.addTV(
                SITE_IDENTIFIER,
                'showEpisodes',
                sDisplayTitle,
                '',
                thumbnail,
                sSyn,
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')
    sFilter = input_parameter_handler.getValue('sFilter')
    sSyn = input_parameter_handler.getValue('sSyn')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<div class="larr episode-header">.+?<a href="([^"]+)"\\s+title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            title = sMovieTitle + aEntry[1]
            title = title.replace('N/A', '').replace(',', '')
            if sFilter not in sUrl:
                continue
            # sDisplayTitle = cUtil().DecoTitle(title)
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('thumbnail', thumbnail)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            gui.addTV(SITE_IDENTIFIER, 'showHosters', title, '',
                      thumbnail, sSyn, output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showHosters():

    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        'http://www.google.com/s2/favicons?domain=',
        '').replace(
        '\\',
        '')
    oParser = Parser()

    sPattern1 = '{"link":"([^"]+)","type":".+?"}'
    sPattern2 = 'src="([^"]+)"/><\\/td>.+?<td>(.+?)<\\/td>'

    aResult1 = re.findall(sPattern1, sHtmlContent, re.DOTALL)
    aResult2 = re.findall(sPattern2, sHtmlContent, re.DOTALL)

    aResult = zip(aResult1, aResult2)
    if (aResult):
        for aEntry in aResult:
            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = 'http:' + sUrl

            sQual = aEntry[1][1]
            if 'vf' in aEntry[1][0]:
                sLang = 'VF'
            else:
                sLang = 'VOSTFR'

            if 'papystreaming' in sUrl or 'mmfilmes.com' in sUrl or 'belike.pw' in sUrl:
                sDisplayTitle = sMovieTitle + \
                    ' [' + sQual + '/' + sLang + ']' + ' [COLOR skyblue]Papyplayer[/COLOR]'
                # sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]Papyplayer[/COLOR]'
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', sMovieTitle)
                output_parameter_handler.addParameter('thumbnail', thumbnail)
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'ShowPapyLink',
                    sDisplayTitle,
                    'films.png',
                    thumbnail,
                    '',
                    output_parameter_handler)

            else:
                sHosterUrl = sUrl

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    sDisplayTitle = sMovieTitle + \
                        ' [' + aEntry[1][1] + '/' + sLang + ']'
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)

    gui.setEndOfDirectory()


def ShowPapyLink():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')
    oParser = Parser()

    if 'papystreaming' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'var player.+?"([^"]+mp4)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)
            else:
                gui.addText(SITE_IDENTIFIER,
                            '[COLOR red]Lien vidéo Non géré[/COLOR]')
        else:
            gui.addText(
                SITE_IDENTIFIER,
                '[COLOR red]Lien vidéo Non géré[/COLOR]')

    elif 'belike.pw' in sUrl:
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'file: *"([^"]+)",label:"(\\d+p)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                label = aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    sDisplayTitle = sMovieTitle + ' [' + label + ']'
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)
    else:

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sHtmlContent = sHtmlContent.replace('\\', '')

        sPattern = '"label":"([0-9p]+)"[^<>]+?"file":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            listurl = []
            listqual = []

            listurl.append(aResult[1][0][1])
            listqual.append(aResult[1][0][0])

            tab = zip(listurl, listqual)

            for url, qual in tab:
                sHosterUrl = url

                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http' + sHosterUrl

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    sDisplayTitle = sMovieTitle + ' [' + qual + ']'
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)
        else:
            gui.addText(SITE_IDENTIFIER, '[COLOR red]Lien vidéo HS[/COLOR]')

    gui.setEndOfDirectory()
