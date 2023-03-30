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

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'vostfree'
SITE_NAME = 'Vostfree'
SITE_DESC = 'anime en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (
    URL_MAIN +
    '?do=search&subaction=search&speedsearch=1&story=',
    'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films-vf-vostfr/', 'showMovies')

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN + 'lastnews/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
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

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if sSearch:
        sPattern = '<span class="image"><img src="([^"]+)" alt="([^"]+).+?<a href="([^"]+).+?desc">([^<]+)'
    elif '/films-vf-vostfr/' in sUrl:
        sPattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+)'
    else:
        sPattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+).+?</i>Saison</span><b>([^<]+).+?Ep</span><b>([^<]+)'

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

            if sSearch:
                sThumb = aEntry[0]
                if 'http' not in sThumb:
                    sThumb = URL_MAIN + sThumb
                sUrl2 = aEntry[2]
            else:
                sUrl2 = aEntry[0]
                sThumb = aEntry[2]
                if 'http' not in sThumb:
                    sThumb = URL_MAIN + sThumb

            sMovieTitle = aEntry[1]
            desc = aEntry[3]

            sLang = ''
            if 'FRENCH' in sMovieTitle or 'French' in sMovieTitle:
                sLang = 'VF'
            if 'VOSTFR' in sMovieTitle:
                sLang = 'VOSTFR'

            sMovieTitle = sMovieTitle.replace(
                ' VOSTFR',
                '').replace(
                ' FRENCH',
                '').replace(
                ' French',
                '')
            sDisplayTitle = sMovieTitle + ' (' + sLang + ')'
            if len(aEntry) > 4:
                sDisplayTitle = sDisplayTitle + \
                    ' S' + aEntry[4] + ' E' + aEntry[5]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sMovieTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                sDisplayTitle,
                '',
                sThumb,
                desc,
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
    oParser = Parser()
    sPattern = '>([^<]+)</a>\\s*</div>\\s*<a href="([^"]+)">\\s*<span class="next-page">Suivant</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def seriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    url = URL_MAIN + 'templates/Animix/js/anime.js'

    oRequestHandler = RequestHandler(url)
    playerContent = oRequestHandler.request()

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # On récupère l'id associé à l'épisode
    sPattern = '<option value="buttons_([0-9]+)">([^<]+)</option>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    epNumber = ''
    sHosterUrl = ''
    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Streaming
            title = sMovieTitle + ' ' + aEntry[1]
            if epNumber != aEntry[1]:
                epNumber = aEntry[1]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    epNumber +
                    '[/COLOR]')

            # On récupère l'info du player
            sPattern = '<div id="buttons_' + \
                aEntry[0] + '" class="button_box">(.+?)/div></div>'
            htmlCut = oParser.parse(sHtmlContent, sPattern)[1][0]

            sPattern = '<div id="player_([0-9]+)".+?class="new_player_([^"]+)'
            data = oParser.parse(htmlCut, sPattern)

            for aEntry1 in data[1]:

                sPattern = '<div id="content_player_' + \
                    aEntry1[0] + '" class="player_box">([^<]+)</div>'
                playerData = oParser.parse(sHtmlContent, sPattern)[1][0]

                if 'http' not in playerData:
                    sPattern = 'player_type[^;]*=="new_player_' + aEntry1[1].lower(
                    ) + '"\\|.+?(?:src=\\\\")([^"]*).*?player_content.*?"([^\\\\"]*)'
                    aResult2 = oParser.parse(playerContent, sPattern)
                    if aResult2[0] is True:
                        sHosterUrl = aResult2[1][0][0] + \
                            playerData + aResult2[1][0][1]
                        if 'http' not in sHosterUrl:
                            sHosterUrl = 'https:' + sHosterUrl

                else:
                    sHosterUrl = playerData

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(title)
                    oHoster.setFileName(title)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                           input_parameter_handler=input_parameter_handler)

            sPattern = '<div class="lien-episode">.+?<b>' + \
                epNumber + '<.+?href="([^"]+).+?<b>([^<]+)<'
            ddlData = oParser.parse(sHtmlContent, sPattern)

            output_parameter_handler = OutputParameterHandler()
            for aEntry2 in ddlData[1]:
                title = sMovieTitle + ' ' + epNumber + ' ' + aEntry2[1]
                url = aEntry2[0]

                if 'ouo' in url:
                    output_parameter_handler.addParameter('siteUrl', url)
                    output_parameter_handler.addParameter(
                        'sMovieTitle', sMovieTitle)
                    output_parameter_handler.addParameter('sThumb', sThumb)
                    gui.addLink(
                        SITE_IDENTIFIER,
                        'DecryptOuo',
                        title,
                        sThumb,
                        '',
                        output_parameter_handler,
                        input_parameter_handler)
                else:
                    sHosterUrl = url
                    oHoster = HosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(title)
                        oHoster.setFileName(title)
                        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                               input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def DecryptOuo():
    from resources.lib.recaptcha import ResolveCaptcha
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    urlOuo = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    if '/fbc/' not in urlOuo:
        urlOuo = urlOuo.replace(
            'io/', 'io/fbc/').replace('press/', 'press/fbc/')

    oRequestHandler = RequestHandler(urlOuo)
    sHtmlContent = oRequestHandler.request()
    Cookie = oRequestHandler.GetCookies()

    key = re.search('sitekey: "([^"]+)', str(sHtmlContent)).group(1)
    OuoToken = re.search(
        '<input name="_token" type="hidden" value="([^"]+).+?id="v-token" name="v-token" type="hidden" value="([^"]+)',
        str(sHtmlContent),
        re.MULTILINE | re.DOTALL)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + \
        OuoToken.group(1) + '&g-recaptcha-response=' + gToken + '&v-token=' + OuoToken.group(2)

    oRequestHandler = RequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    final = re.search(
        '<form method="POST" action="(.+?)" accept-charset=.+?<input name="_token" type="hidden" value="(.+?)">',
        str(sHtmlContent))

    url = final.group(1)
    params = '_token=' + final.group(2) + '&x-token=' + ''

    oRequestHandler = RequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    # sHtmlContent = oRequestHandler.request()

    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = HosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
