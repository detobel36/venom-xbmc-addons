# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'frenchanimes'
SITE_NAME = 'French Animes'
SITE_DESC = 'Mangas en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showAnimes')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showAnimes')
ANIM_MOVIE = (URL_MAIN + 'films-vf-vostfr/', 'showAnimes')
ANIM_GENRES = (True, 'showGenres')

URL_SEARCH = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&story=',
    'showSearch')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showAnimes')
FUNCTION_SEARCH = 'showSearch'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://animes')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche Animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIE[1],
        'Animés (Films)',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showAnimes(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()
    oParser = Parser()

    oRequestHandler = RequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '</span><b>Animes par genre</b></div>'
    sEnd = '<div class="side-b">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            title = aEntry[1].capitalize()
            TriAlpha.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, sUrl in TriAlpha:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showAnimes',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showAnimes(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:sai">([^<]+[0-9]).+?|)Version'
    sPattern += '.+?desc">([^<]*).+?Synopsis:.+?desc">(.*?)</d'
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

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            title = aEntry[1].replace(' wiflix', '')
            sUrl = aEntry[2]
            sSaison = aEntry[3].replace('Saison', 'Saison ')
            sLang = aEntry[4]
            desc = str(aEntry[5])

            # la langue est parfois dans le titre
            if sLang in title:
                title = title.replace(sLang, '')

            sDisplaytitle = '%s %s (%s)' % (title, sSaison, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            if 'films-vf-vostfr' in sUrl:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplaytitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addSeason(
                    SITE_IDENTIFIER,
                    'showEpisodes',
                    sDisplaytitle,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showAnimes',
                'Page ' + sPaging,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sStart = 'class="eps" style="display: none">'
    sEnd = '/div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # Pour les liens myvi
    sHtmlContent = sHtmlContent.replace(
        '!//', '!https://').replace(',//', ',https://')

    # Besoin des saut de ligne
    sHtmlContent = sHtmlContent.replace('\n', '@')

    sPattern = '([0-9]+)!|(https:.+?)[,|<@]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ep = 0

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                ep = 'Episode ' + aEntry[0]
                gui.addText(SITE_IDENTIFIER, '[COLOR red]' + ep + '[/COLOR]')
            if aEntry[1]:
                title = sMovieTitle + ' ' + ep
                sHosterUrl = aEntry[1]

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(title)
                    oHoster.setFileName(title)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = Parser()
    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="eps" style="display: none">'
    sEnd = '/div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # Pour les liens myvi
    sHtmlContent = sHtmlContent.replace(
        '!//', '!https://').replace(',//', ',https://')

    sPattern = '(https:.+?)[,|<]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
