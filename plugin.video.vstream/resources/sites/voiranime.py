# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'voiranime'
SITE_NAME = 'VoirAnime'
SITE_DESC = 'Animés en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + '?filter=subbed', 'showAnimes')
ANIM_VFS = (URL_MAIN + '?filter=dubbed', 'showAnimes')
ANIM_GENRES = (URL_MAIN + 'anime-genre/', 'showGenres')
ANIM_ALPHA = (URL_MAIN + 'liste-danimes/?start=', 'showAlpha')

FUNCTION_SEARCH = 'showAnimes'
URL_SEARCH = (URL_MAIN + '?post_type=wp-manga&m_orderby=views', 'showAnimes')
URL_SEARCH_ANIMS = (URL_SEARCH[0] + '&s=', 'showAnimes')

URL_SEARCH_VOSTFR = (URL_SEARCH[0] + '&language=vostfr&s=', 'showAnimes')
URL_SEARCH_VF = (URL_SEARCH[0] + '&language=vf&s=', 'showAnimes')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VOSTFR)', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_VF[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VF)', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Par genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Par ordre alphabétique)', 'az.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return


def showAlpha():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    progress_ = progress().VScreate(SITE_NAME)

    output_parameter_handler = OutputParameterHandler()
    for i in range(-1, 27):
        progress_.VSupdate(progress_, 36)

        if i == -1:
            sTitle = 'ALL'
            output_parameter_handler.addParameter('siteUrl', sUrl.replace('?start=', ''))
        elif i == 0:
            sTitle = '#'
            output_parameter_handler.addParameter('siteUrl', sUrl + 'non-char')
        else:
            sTitle = chr(64 + i)
            output_parameter_handler.addParameter('siteUrl', sUrl + sTitle)

        output_parameter_handler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            'Lettre [COLOR coral]' +
            sTitle +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Aventure', sUrl + 'adventure/'])
    liste.append(['Chinois', sUrl + 'chinese/'])
    liste.append(['Comédie', sUrl + 'comdey/'])
    liste.append(['Drama', sUrl + 'drama/'])
    liste.append(['Ecchi', sUrl + 'ecchi/'])
    liste.append(['Fantastique', sUrl + 'fantasy/'])
    liste.append(['Horreur', sUrl + 'horror/'])
    liste.append(['Mahou Shoujo', sUrl + 'mahou-shoujo/'])
    liste.append(['Mécha', sUrl + 'mecha/'])
    liste.append(['Musique', sUrl + 'music/'])
    liste.append(['Mystère', sUrl + 'mystery'])
    liste.append(['Psychologie', sUrl + 'psychological/'])
    liste.append(['Romance', sUrl + 'romance/'])
    liste.append(['Sci-Fi', sUrl + 'sci-fi/'])
    liste.append(['Trance de vie', sUrl + 'slice-of-life/'])
    liste.append(['Sports', sUrl + 'sports/'])
    liste.append(['Surnaturel', sUrl + 'supernatural/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

    output_parameter_handler = OutputParameterHandler()
    for sTitle, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showAnimes(sSearch=''):
    oGui = Gui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch

        sTypeSearch = oParser.parseSingleResult(sUrl, '\\?type=(.+?)&')
        if sTypeSearch[0]:
            sTypeSearch = sTypeSearch[1]
        else:
            sTypeSearch = False

        oRequest = RequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        sHtmlContent = oRequest.request()
        sPattern = '<a href="([^"]+)" title="([^"]+)".+?src="([^"]+)".+?Type.+?content.+?>([^<]+)'

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')
        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="page-item-detail video">.+?a href="([^"]+)" title="([^"]+)".+?src="([^"]+)"'

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

            sUrl = aEntry[0]
            if 'http' not in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = aEntry[1].replace('film ', '').replace(' streaming', '')
            sThumb = aEntry[2]
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            if 'VOSTFR' in sTitle:
                sTitle = sTitle.replace('VOSTFR', '')
                sLang = 'VOSTFR'
            elif 'VF' in sTitle:
                sTitle = sTitle.replace('VF', '')
                sLang = 'VF'
            else:
                sLang = 'VOSTFR'

            sDisplayTitle = '%s (%s)' % (sTitle, sLang)

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, sThumb, sThumb, '', output_parameter_handler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.findall('([0-9]+)', sNextPage)[-1]
            oGui.addNext(SITE_IDENTIFIER, 'showAnimes', 'Page ' + number, output_parameter_handler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink".+?href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showEpisodes():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="summary__content ">.+?<p>([^<]+)'  # recup description
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[0])

    sPattern = '<li class="wp-manga-chapter.+?="([^"]+)".+?([^<]+)'  # Recup lien + titre
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()

        # Dernier épisode
        sUrlEpisode = aResult[1][0][0]
        sTitle = aResult[1][0][1]

        output_parameter_handler.addParameter('siteUrl', sUrlEpisode)
        output_parameter_handler.addParameter('sMovieTitle', sTitle)
        output_parameter_handler.addParameter('sDesc', sDesc)
        output_parameter_handler.addParameter('sThumb', sThumb)
        oGui.addEpisode(
            SITE_IDENTIFIER,
            'showLinks',
            '===] Dernier épisode [===',
            '',
            sThumb,
            sDesc,
            output_parameter_handler)

        # Premier épisode
        sUrlEpisode = aResult[1][-1][0]
        sTitle = aResult[1][-1][1]

        output_parameter_handler.addParameter('siteUrl', sUrlEpisode)
        output_parameter_handler.addParameter('sMovieTitle', sTitle)
        output_parameter_handler.addParameter('sDesc', sDesc)
        output_parameter_handler.addParameter('sThumb', sThumb)
        oGui.addEpisode(
            SITE_IDENTIFIER,
            'showLinks',
            '===] Premier épisode [===',
            '',
            sThumb,
            sDesc,
            output_parameter_handler)

        # Liste des épisodes
        for aEntry in aResult[1]:
            sUrlEpisode = aEntry[0]
            sTitle = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrlEpisode)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sDesc', sDesc)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, output_parameter_handler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Les elements post.
    data = re.search('data-action="bookmark" data-post="([^"]+)" data-chapter="([^"]+)"', sHtmlContent)
    post = data.group(1)
    chapter = data.group(2)

    # On extrait une partie de la page pour eviter les doublons.
    sData = re.search('<select class="selectpicker host-select">(.+?)</select> </label>',
                      sHtmlContent, re.MULTILINE | re.DOTALL).group(1)

    oParser = cParser()
    sPattern = '<option data-redirect=.+?value="([^"]+)">LECTEUR.+?</option>'

    aResult = oParser.parse(sData, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = sMovieTitle + aEntry

            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sDesc', 'salut')
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sPost', post)
            output_parameter_handler.addParameter('sChapter', chapter)
            output_parameter_handler.addParameter('sType', aEntry)

            oGui.addEpisode(SITE_IDENTIFIER, 'RecapchaBypass', sTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def RecapchaBypass():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    post = input_parameter_handler.getValue('sPost')
    chapter = input_parameter_handler.getValue('sChapter')
    types = input_parameter_handler.getValue('sType')

    # La lib qui gere recaptcha
    from resources.lib import librecaptcha
    test = librecaptcha.get_token(api_key="6Ld2q9gUAAAAAP9vNl23kYuST72fYsu494_B2qaZ", site_url=sUrl,
                                  user_agent=UA, gui=False, debug=False)

    if test is None:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

    else:
        # N'affiche pas directement le liens car sinon Kodi crash.
        sDisplayTitle = "Recaptcha passé avec succès, cliquez pour afficher les liens"
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
        output_parameter_handler.addParameter('sThumb', sThumb)
        output_parameter_handler.addParameter('Token', test)
        output_parameter_handler.addParameter('sPost', post)
        output_parameter_handler.addParameter('sChapter', chapter)
        output_parameter_handler.addParameter('sType', types)
        oGui.addEpisode(SITE_IDENTIFIER, 'getHost', sDisplayTitle, '', sThumb, '', output_parameter_handler)

    oGui.setEndOfDirectory()


def getHost():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    test = input_parameter_handler.getValue('Token')
    post = input_parameter_handler.getValue('sPost')
    chapter = input_parameter_handler.getValue('sChapter')
    types = input_parameter_handler.getValue('sType')

    # On valide le token du coté du site
    data = 'action=get_video_chapter_content&grecaptcha=' + test + '&manga=' + \
        post + '&chapter=' + chapter + '&host=' + types.replace(' ', '+')
    oRequestHandler = RequestHandler("https://voiranime.com/wp-admin/admin-ajax.php")
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry.replace('\\', '').replace('\\/', '/')
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
