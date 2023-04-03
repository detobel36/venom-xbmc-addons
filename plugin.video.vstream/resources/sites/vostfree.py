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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if search:
        pattern = '<span class="image"><img src="([^"]+)" alt="([^"]+).+?<a href="([^"]+).+?desc">([^<]+)'
    elif '/films-vf-vostfr/' in url:
        pattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+)'
    else:
        pattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+).+?</i>Saison</span><b>([^<]+).+?Ep</span><b>([^<]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if search:
                thumb = entry[0]
                if 'http' not in thumb:
                    thumb = URL_MAIN + thumb
                url2 = entry[2]
            else:
                url2 = entry[0]
                thumb = entry[2]
                if 'http' not in thumb:
                    thumb = URL_MAIN + thumb

            movie_title = entry[1]
            desc = entry[3]

            lang = ''
            if 'FRENCH' in movie_title or 'French' in movie_title:
                lang = 'VF'
            if 'VOSTFR' in movie_title:
                lang = 'VOSTFR'

            movie_title = movie_title.replace(
                ' VOSTFR',
                '').replace(
                ' FRENCH',
                '').replace(
                ' French',
                '')
            display_title = movie_title + ' (' + lang + ')'
            if len(entry) > 4:
                display_title = display_title + \
                    ' S' + entry[4] + ' E' + entry[5]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>([^<]+)</a>\\s*</div>\\s*<a href="([^"]+)">\\s*<span class="next-page">Suivant</span>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def seriesHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    url = URL_MAIN + 'templates/Animix/js/anime.js'

    request_handler = RequestHandler(url)
    playerContent = request_handler.request()

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # On récupère l'id associé à l'épisode
    pattern = '<option value="buttons_([0-9]+)">([^<]+)</option>'

    parser = Parser()
    results = parser.parse(html_content, pattern)
    epNumber = ''
    hoster_url = ''
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Streaming
            title = movie_title + ' ' + entry[1]
            if epNumber != entry[1]:
                epNumber = entry[1]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    epNumber +
                    '[/COLOR]')

            # On récupère l'info du player
            pattern = '<div id="buttons_' + \
                entry[0] + '" class="button_box">(.+?)/div></div>'
            htmlCut = parser.parse(html_content, pattern)[1][0]

            pattern = '<div id="player_([0-9]+)".+?class="new_player_([^"]+)'
            data = parser.parse(htmlCut, pattern)

            for aEntry1 in data[1]:

                pattern = '<div id="content_player_' + \
                    aEntry1[0] + '" class="player_box">([^<]+)</div>'
                playerData = parser.parse(html_content, pattern)[1][0]

                if 'http' not in playerData:
                    pattern = 'player_type[^;]*=="new_player_' + aEntry1[1].lower(
                    ) + '"\\|.+?(?:src=\\\\")([^"]*).*?player_content.*?"([^\\\\"]*)'
                    aResult2 = parser.parse(playerContent, pattern)
                    if aResult2[0] is True:
                        hoster_url = aResult2[1][0][0] + \
                            playerData + aResult2[1][0][1]
                        if 'http' not in hoster_url:
                            hoster_url = 'https:' + hoster_url

                else:
                    hoster_url = playerData

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

            pattern = '<div class="lien-episode">.+?<b>' + \
                epNumber + '<.+?href="([^"]+).+?<b>([^<]+)<'
            ddlData = parser.parse(html_content, pattern)

            output_parameter_handler = OutputParameterHandler()
            for aEntry2 in ddlData[1]:
                title = movie_title + ' ' + epNumber + ' ' + aEntry2[1]
                url = aEntry2[0]

                if 'ouo' in url:
                    output_parameter_handler.addParameter('site_url', url)
                    output_parameter_handler.addParameter(
                        'movie_title', movie_title)
                    output_parameter_handler.addParameter('thumb', thumb)
                    gui.addLink(
                        SITE_IDENTIFIER,
                        'DecryptOuo',
                        title,
                        thumb,
                        '',
                        output_parameter_handler,
                        input_parameter_handler)
                else:
                    hoster_url = url
                    hoster = HosterGui().checkHoster(hoster_url)
                    if hoster:
                        hoster.setDisplayName(title)
                        hoster.setFileName(title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                               input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def DecryptOuo():
    from resources.lib.recaptcha import ResolveCaptcha
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    urlOuo = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    if '/fbc/' not in urlOuo:
        urlOuo = urlOuo.replace(
            'io/', 'io/fbc/').replace('press/', 'press/fbc/')

    request_handler = RequestHandler(urlOuo)
    html_content = request_handler.request()
    Cookie = request_handler.GetCookies()

    key = re.search('sitekey: "([^"]+)', str(html_content)).group(1)
    OuoToken = re.search(
        '<input name="_token" type="hidden" value="([^"]+).+?id="v-token" name="v-token" type="hidden" value="([^"]+)',
        str(html_content),
        re.MULTILINE | re.DOTALL)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + \
        OuoToken.group(1) + '&g-recaptcha-response=' + gToken + '&v-token=' + OuoToken.group(2)

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Referer', urlOuo)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', str(len(params)))
    request_handler.addHeaderEntry('Cookie', Cookie)
    request_handler.addParametersLine(params)
    html_content = request_handler.request()

    final = re.search(
        '<form method="POST" action="(.+?)" accept-charset=.+?<input name="_token" type="hidden" value="(.+?)">',
        str(html_content))

    url = final.group(1)
    params = '_token=' + final.group(2) + '&x-token=' + ''

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Referer', urlOuo)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', str(len(params)))
    request_handler.addHeaderEntry('Cookie', Cookie)
    request_handler.addParametersLine(params)
    # html_content = request_handler.request()

    hoster_url = request_handler.getRealUrl()
    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
