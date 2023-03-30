# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Progress
from resources.lib.util import cUtil
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False


SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming Séries'
SITE_DESC = 'Séries en streaming vf gratuitement sur Série Streaming'

URL_MAIN = 'https://www.streamingseries.biz/'

SERIE_NEWS = (URL_MAIN + 'film-archive/',
              'showMovies')  # astuce anti caroussel
SERIE_SERIES = ('http://', 'load')
SERIE_VFS = (URL_MAIN + 'version-francaise-vf/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'version-francaise-vf/?sort=views', 'showMovies')
SERIE_COMMENTS = (
    URL_MAIN +
    'version-francaise-vf/?sort=comments',
    'showMovies')
SERIE_LIST = (True, 'AlphaSearch')


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSerieSearch',
        'Recherche',
        'search.png',
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
    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Les plus vues)',
        'views.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_COMMENTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_COMMENTS[1],
        'Séries (Les plus commentées)',
        'comments.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_LIST[1],
        'Séries (Liste)',
        'listes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def AlphaSearch():
    gui = Gui()

    for i in range(0, 27):

        if (i < 1):
            sLetter = '[0-9]'
        else:
            sLetter = chr(64 + i)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sLetter', sLetter)
        gui.addDir(
            SITE_IDENTIFIER,
            'AlphaDisplay',
            '[COLOR teal] Lettre [COLOR red]' +
            sLetter +
            '[/COLOR][/COLOR]',
            'az.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def AlphaDisplay():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sLetter = input_parameter_handler.getValue('sLetter')

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+?)" >(' + sLetter + '[^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            title = aEntry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)

            gui.addDir(
                SITE_IDENTIFIER,
                'showSaisons',
                title,
                'series.png',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="movie-poster">.+?href="([^<]+)".+?src="([^<]+)" alt="(.+?)"'
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

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            title = aEntry[2]

            # Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(
                        sSearch.replace(
                            URL_SEARCH[0],
                            ''),
                        title) == 0:
                    continue

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addTV(SITE_IDENTIFIER, 'showEpisodes', title,
                      '', sThumb, '', output_parameter_handler)

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
    sPattern = '<div class="keremiya-loadnavi-.+?href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="movie-poster".+?src="([^"]+)".+?href="([^<]+)" title="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            title = aEntry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
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
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # recuperation du hoster de base
    sPattern = '<div class="part active".+?class="part-name">(.+?)<\\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ListeUrl = []
    if aResult[0]:
        ListeUrl = [(sUrl, aResult[1][0])]

    # Recuperation des suivants
    sPattern = '<a href="([^<]+)"><div class="part "> *<div class="part-name">([^<]+)<\\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if aResult[0]:
        total = len(ListeUrl)
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in ListeUrl:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            title = sMovieTitle + aEntry[1].replace('Part', 'Episode')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    # si un seul episode
    else:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter(
            'sMovieTitle', sMovieTitle + 'episode 1 ')
        output_parameter_handler.addParameter('sThumb', sThumb)
        gui.addTV(
            SITE_IDENTIFIER,
            'showHosters',
            sMovieTitle +
            'episode 1 ',
            '',
            sThumb,
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')
    sHtmlContent = sHtmlContent.replace('\r', '')
    # on réécris pour récupérer la langue
    sHtmlContent = sHtmlContent.replace(
        'VF</strong>', 'VF</b>').replace('</font></u>', '')
    sHtmlContent = sHtmlContent.replace(
        '- Version Française',
        '').replace(
        'Version Française',
        'VF')
    # on réécris pour récupérer les hosters
    sHtmlContent = sHtmlContent.replace('<p><script', '<iframe')

    sPattern = '(VF|VF |VOSTFR)<\\/b><\\/p>|<iframe.+?=[\'|"](.+?)[\'|"]'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # langue
            if aEntry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]')
            # hote
            else:
                sHosterUrl = aEntry[1]
                if '//goo.gl' in sHosterUrl:
                    import urllib2
                    try:

                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                        request = urllib2.Request(sHosterUrl, None, headers)
                        reponse = urllib2.urlopen(request)
                        sHosterUrl = reponse.geturl()
                    except BaseException:
                        pass

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
