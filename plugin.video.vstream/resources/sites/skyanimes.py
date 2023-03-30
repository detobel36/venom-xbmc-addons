# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

SITE_IDENTIFIER = 'skyanimes'
SITE_NAME = 'Sky-Animes'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

STREAM = 'index.php?file=Media&nuked_nude=index&op=do_dl&dl_id='

INDEX = 'index.php?file=Search&op=mod_search&searchtype=matchand&autor=&module=Download&limit=100&main='
URL_SEARCH_ANIMS = (URL_MAIN + INDEX, 'showEpisode')
# URL_SEARCH_DRAMAS = (URL_MAIN + INDEX, 'showEpisode')
FUNCTION_SEARCH = 'showEpisode'

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_GENRES = (True, 'showGenresA')
ANIM_VOSTFRS = (URL_MAIN + 'streaming-films', 'showSeries')
ANIM_OAVS = (URL_MAIN + 'streaming-oavs', 'showSeries')

DRAMA_DRAMAS = (True, 'showMenuDramas')
DRAMA_GENRES = (True, 'showGenresD')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_DRAMAS[1],
        'Dramas',
        'dramas.png',
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

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (Films)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'streaming-animes-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-animes-termines?p=-1'])

    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'animes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuDramas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Dramas (Genres)',
        'genres.png',
        output_parameter_handler)

    # contenu à contrôler
    # output_parameter_handler.addParameter('siteUrl', ANIM_OAVS[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_OAVS[1], 'Dramas (OAVS)', 'dramas.png', output_parameter_handler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'download-dramas-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-dramas-termines?p=-1'])

    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'dramas.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenresA():
    gui = Gui()
    oParser = Parser()

    sUrl = URL_MAIN + 'streaming-animes-en-cours'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = 'id="id_genre"'
    sEnd = '<select id="triGenre"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

        gui.setEndOfDirectory()


def showGenresD():
    gui = Gui()
    oParser = Parser()

    sUrl = URL_MAIN + 'download-dramas-en-cours?p=-1'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = 'id="id_genre"'
    sEnd = '<select id="triGenre"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            title = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', title)
            gui.addDir(
                SITE_IDENTIFIER,
                'showSeries',
                title,
                'genres.png',
                output_parameter_handler)

        gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showEpisode(sUrl)
        gui.setEndOfDirectory()
        return


def showSeries():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl').replace(
        '+',
        '%2B').replace(
        'é',
        'e').replace(
            'ô',
            'o') .replace(
                'É',
                'E').replace(
                    'ï',
                    'i').replace(
                        'è',
        'e')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    sPattern = '<a href="([^"]+)"><img src="([^"]+)" width.+?alt="([^"]+).+?></a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME, large=(total > 50))
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = aEntry[2]
            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1].replace(' ', '%20')
            desc = ''

            title = title.replace(', telecharger en ddl', '')

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '-animes-' in sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

        gui.setEndOfDirectory()


def showEpisode(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    if sThumb:
        sThumb = sThumb.replace(' ', '%20')

    if sSearch:
        sUrl = sSearch

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    if sSearch:
        sPattern = '<a href=".+?id=([^"]+)"><b>(.+?)</b>'
    else:
        sPattern = '<td style="padding-left: 12px;"><a href="([^"]+).+?><b><img.+?>(.+?)</b>.+?</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sorted(aResult[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                title = aEntry[1]
                title, sTitle1 = title.replace(
                    '1080p', '').replace(
                    'BD', '').replace(
                    'V2', '').replace(
                    'FIN', '') .replace(
                    'Fin', '').replace(
                        'fin', '').replace(
                            'OAV', '').replace(
                                'Bluray', '') .replace(
                                    'Blu-Ray', '').rstrip().rsplit(
                                        ' ', 1)
                title = 'E' + sTitle1 + ' ' + title
                sUrl2 = URL_MAIN + STREAM + aEntry[0]
                sThumb = ''
            else:
                title = aEntry[1]
                title, sTitle1 = title.replace(
                    '1080p', '').replace(
                    'BD', '').replace(
                    'V2', '').replace(
                    'FIN', '') .replace(
                    'Fin', '').replace(
                        'fin', '').replace(
                            'OAV', '').replace(
                                'Bluray', '') .replace(
                                    'Blu-Ray', '').rstrip().rsplit(
                                        ' ', 1)
                title = 'E' + sTitle1 + ' ' + title
                sUrl2 = URL_MAIN + STREAM + aEntry[0]
                sUrl2 = sUrl2.replace('#', '')

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)
    if not sSearch:
        gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    if sThumb:
        sThumb = sThumb.replace(' ', '%20')
    oHoster = HosterGui().checkHoster('.m3u8')

    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
