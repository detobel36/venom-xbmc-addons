# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager  # , isMatrix
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'otaku_attitude'
SITE_NAME = 'Otaku-Attitude'
SITE_DESC = 'Animes, Drama et OST en DDL et Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json
OST_MAIN = "https://forum.otaku-attitude.net/musicbox/playlists/"

URL_SEARCH_ANIMS = (URL_MAIN + 'recherche.html?cat=1&q=', 'showAnimes')
URL_SEARCH_DRAMAS = (URL_MAIN + 'recherche.html?cat=2&q=', 'showAnimes')
FUNCTION_SEARCH = 'showAnimes'

ANIM_ANIMS = ('http://', 'load')
ANIM_VOSTFRS = (URL_MAIN + 'liste-dl-animes.php', 'showAnimes')

DRAMA_SERIES = (URL_MAIN + 'liste-dl-dramas.php', 'showAnimes')

OST_ANIME = (True, 'showGenres')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animés)', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Dramas)', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_SERIES[1], 'Dramas (VOSTFR)', 'dramas.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', OST_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, OST_ANIME[1], 'Musicbox (OST)', 'music.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = Gui()

    liste = [['Animés', '1-anime'], ['Dramas', '6-drama'], ['Jeux Vidéo', '7-jeu-vidéo']]

    output_parameter_handler = OutputParameterHandler()
    for sTitle, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', OST_MAIN + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showOst', sTitle, 'music.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return


def showAnimes(sSearch=''):
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    # On mémorise le lien de base ce qui permet d'avoir un nextpage fonctionnel sans modif et peu importe la categorie
    if not sSearch:
        if 'scroll' not in sUrl:
            memorisedUrl = sUrl
            Page = 1
        else:
            memorisedUrl = input_parameter_handler.getValue('memorisedUrl')
            Page = input_parameter_handler.getValue('Page')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_DRAMAS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sPattern = 'href="([^"]+)" class="liste_dl"><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)</.+?>'
    else:
        sPattern = 'href="([^"]+)".+?><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)<br.+?>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = aEntry[1] + "|verifypeer=false"
            sTitle = aEntry[2].replace('-...', '').replace('...', '').replace('!', ' !')
            sDesc = aEntry[3]

            # filtre search
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sDesc', sDesc)
            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        Page = int(Page) + 1
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', memorisedUrl + '?&scroll=' + str(Page))
        # On renvoie l'url memoriser et le numero de page pour l'incrementer a chaque fois
        output_parameter_handler.addParameter('memorisedUrl', memorisedUrl)
        output_parameter_handler.addParameter('Page', Page)
        oGui.addNext(SITE_IDENTIFIER, 'showAnimes', 'Page ' + str(Page), output_parameter_handler)

        oGui.setEndOfDirectory()


def showOst():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if 'page' not in sUrl:
        memorisedUrl = sUrl
        Page = 1
    else:
        memorisedUrl = input_parameter_handler.getValue('memorisedUrl')
        Page = input_parameter_handler.getValue('Page')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "<div class='plWrapper'>.+?href='([^']+)' title='([^']+)'.+?src=\"([^\"]+)\""
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1].replace('- Artiste non défini', '')
            sThumb = aEntry[2]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            oGui.addAnime(SITE_IDENTIFIER, 'showMusic', sTitle, '', sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

        Page = int(Page) + 1
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', memorisedUrl + '?page=' + str(Page))
        # On renvoie l'url memoriser et le numero de page pour l'incrementer a chaque fois
        output_parameter_handler.addParameter('memorisedUrl', memorisedUrl)
        output_parameter_handler.addParameter('Page', Page)
        oGui.addNext(SITE_IDENTIFIER, 'showOst', 'Page ' + str(Page), output_parameter_handler)

        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sDesc = input_parameter_handler.getValue('sDesc')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    # On recupere l'id de l'anime dans l'url
    serieID = re.search('fiche-.+?-(\\d+)-.+?.html', sUrl).group(1)
    sPattern = 'class="(?:download cell_impaire|download)" id="([^"]+)".+?(\\d+).+?class="cell".+?>([^<]+)</td'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in sorted(aResult[1], key=lambda aResult: aResult[1]):
            sQual = aEntry[2]

            # if isMatrix():  # plante sous matrix !!!!!!
            # sQual = sQual.encode('latin-1').decode()

            # Changemement de formats ...x... -> ....P
            if '1920×' in sQual or '1440×' in sQual or '1904×' in sQual:
                sQual = re.sub('(\\d+×\\d+)px', '[1080P]', sQual)
            elif '1728×' in sQual:
                sQual = re.sub('(\\d+×\\d+)px', '[800P]', sQual)
            elif '1280×' in sQual:
                # VSlog(sQual)
                sQual = re.sub('(\\d+×\\d+)px', '[720P]', sQual)
            elif '1024×' in sQual:
                sQual = re.sub('(\\d+×\\d+)px', '[600P]', sQual)
            elif '480×' in sQual:
                sQual = re.sub('(\\d+×\\d+)px', '[360P]', sQual)
            else:
                sQual = re.sub('(\\d+×\\d+)px', '[480P]', sQual)

            sTitle = 'E' + aEntry[1] + ' ' + sMovieTitle
            sDisplayTitle = sTitle + ' ' + sQual
            idEpisode = aEntry[0]

            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('serieID', serieID)
            output_parameter_handler.addParameter('idEpisode', idEpisode)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

    oGui.setEndOfDirectory()


def showMusic():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div data-track-file="([^"]+)".+?data-track-name="([^"]+)".+?"><span.+?>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[2] + ' ' + aEntry[1]
            mp3Url = aEntry[0]

            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('mp3Url', mp3Url)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showMp3', sTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMp3():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    mp3Url = input_parameter_handler.getValue('mp3Url')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

#     if 'mp3' in mp3Url:
#         sHosterUrl = mp3Url

    oHoster = HosterGui().checkHoster('.m3u8')
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(oGui, oHoster, mp3Url + "|verifypeer=false", sThumb)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    serieID = input_parameter_handler.getValue('serieID')
    idEpisode = input_parameter_handler.getValue('idEpisode')

    sHosterUrl = ''
    if 'fiche-anime' in sUrl:
        sHosterUrl = URL_MAIN + 'launch-download-1-' + serieID + '-ddl-' + idEpisode + '.html'
    elif 'fiche-drama' in sUrl:
        sHosterUrl = URL_MAIN + 'launch-download-2-' + serieID + '-ddl-' + idEpisode + '.html'

    oHoster = HosterGui().checkHoster('.m3u8')
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(oGui, oHoster, sHosterUrl + "|verifypeer=false", sThumb)

    oGui.setEndOfDirectory()
