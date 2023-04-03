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
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'voiranime'
SITE_NAME = 'VoirAnime'
SITE_DESC = 'Animés en Streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

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
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_VOSTFR[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VOSTFR)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche d\'animés (VF)',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Par genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ALPHA[1],
        'Animés (Par ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        url = url + Quote(search_text)
        showAnimes(url)
        gui.setEndOfDirectory()
        return


def showAlpha():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    progress_ = Progress().VScreate(SITE_NAME)

    output_parameter_handler = OutputParameterHandler()
    for i in range(-1, 27):
        progress_.VSupdate(progress_, 36)

        if i == -1:
            title = 'ALL'
            output_parameter_handler.addParameter(
                'site_url', url.replace('?start=', ''))
        elif i == 0:
            title = '#'
            output_parameter_handler.addParameter('site_url', url + 'non-char')
        else:
            title = chr(64 + i)
            output_parameter_handler.addParameter('site_url', url + title)

        output_parameter_handler.addParameter('movie_title', title)
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'az.png',
            output_parameter_handler)

    progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []
    liste.append(['Action', url + 'action/'])
    liste.append(['Aventure', url + 'adventure/'])
    liste.append(['Chinois', url + 'chinese/'])
    liste.append(['Comédie', url + 'comdey/'])
    liste.append(['Drama', url + 'drama/'])
    liste.append(['Ecchi', url + 'ecchi/'])
    liste.append(['Fantastique', url + 'fantasy/'])
    liste.append(['Horreur', url + 'horror/'])
    liste.append(['Mahou Shoujo', url + 'mahou-shoujo/'])
    liste.append(['Mécha', url + 'mecha/'])
    liste.append(['Musique', url + 'music/'])
    liste.append(['Mystère', url + 'mystery'])
    liste.append(['Psychologie', url + 'psychological/'])
    liste.append(['Romance', url + 'romance/'])
    liste.append(['Sci-Fi', url + 'sci-fi/'])
    liste.append(['Trance de vie', url + 'slice-of-life/'])
    liste.append(['Sports', url + 'sports/'])
    liste.append(['Surnaturel', url + 'supernatural/'])
    liste.append(['Thriller', url + 'thriller/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showAnimes(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search

        sTypeSearch = parser.parseSingleResult(url, '\\?type=(.+?)&')
        if sTypeSearch[0]:
            sTypeSearch = sTypeSearch[1]
        else:
            sTypeSearch = False

        request = RequestHandler(url)
        request.addHeaderEntry('Referer', URL_MAIN)
        request.addHeaderEntry(
            'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.addHeaderEntry(
            'Accept-Language',
            'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.addHeaderEntry(
            'Content-Type',
            'application/x-www-form-urlencoded')
        html_content = request.request()
        pattern = '<a href="([^"]+)" title="([^"]+)".+?src="([^"]+)".+?Type.+?content.+?>([^<]+)'

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        request_handler = RequestHandler(url)
        html_content = request_handler.request()
        pattern = '<div class="page-item-detail video">.+?a href="([^"]+)" title="([^"]+)".+?src="([^"]+)"'

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

            url = entry[0]
            if 'http' not in url:
                url = URL_MAIN[:-1] + url

            title = entry[1].replace('film ', '').replace(' streaming', '')
            thumb = entry[2]
            if 'http' not in thumb:
                thumb = URL_MAIN + thumb

            if 'VOSTFR' in title:
                title = title.replace('VOSTFR', '')
                lang = 'VOSTFR'
            elif 'VF' in title:
                title = title.replace('VF', '')
                lang = 'VF'
            else:
                lang = 'VOSTFR'

            display_title = '%s (%s)' % (title, lang)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addAnime(
                SITE_IDENTIFIER,
                'showEpisodes',
                display_title,
                thumb,
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.findall('([0-9]+)', next_page)[-1]
            gui.addNext(
                SITE_IDENTIFIER,
                'showAnimes',
                'Page ' + number,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class="nextpostslink".+?href="([^"]+)"'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    # recup description
    pattern = '<div class="summary__content ">.+?<p>([^<]+)'
    results = parser.parse(html_content, pattern)

    desc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[0])

    # Recup lien + titre
    pattern = '<li class="wp-manga-chapter.+?="([^"]+)".+?([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()

        # Dernier épisode
        sUrlEpisode = results[1][0][0]
        title = results[1][0][1]

        output_parameter_handler.addParameter('site_url', sUrlEpisode)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('desc', desc)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showLinks',
            '===] Dernier épisode [===',
            '',
            thumb,
            desc,
            output_parameter_handler)

        # Premier épisode
        sUrlEpisode = results[1][-1][0]
        title = results[1][-1][1]

        output_parameter_handler.addParameter('site_url', sUrlEpisode)
        output_parameter_handler.addParameter('movie_title', title)
        output_parameter_handler.addParameter('desc', desc)
        output_parameter_handler.addParameter('thumb', thumb)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'showLinks',
            '===] Premier épisode [===',
            '',
            thumb,
            desc,
            output_parameter_handler)

        # Liste des épisodes
        for entry in results[1]:
            sUrlEpisode = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', sUrlEpisode)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # Les elements post.
    data = re.search(
        'data-action="bookmark" data-post="([^"]+)" data-chapter="([^"]+)"',
        html_content)
    post = data.group(1)
    chapter = data.group(2)

    # On extrait une partie de la page pour eviter les doublons.
    sData = re.search(
        '<select class="selectpicker host-select">(.+?)</select> </label>',
        html_content,
        re.MULTILINE | re.DOTALL).group(1)

    parser = Parser()
    pattern = '<option data-redirect=.+?value="([^"]+)">LECTEUR.+?</option>'

    results = parser.parse(sData, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            title = movie_title + entry

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('desc', 'salut')
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('sPost', post)
            output_parameter_handler.addParameter('sChapter', chapter)
            output_parameter_handler.addParameter('_type', entry)

            gui.addEpisode(
                SITE_IDENTIFIER,
                'RecapchaBypass',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()


def RecapchaBypass():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    post = input_parameter_handler.getValue('sPost')
    chapter = input_parameter_handler.getValue('sChapter')
    types = input_parameter_handler.getValue('_type')

    # La lib qui gere recaptcha
    from resources.lib import librecaptcha
    test = librecaptcha.get_token(
        api_key="6Ld2q9gUAAAAAP9vNl23kYuST72fYsu494_B2qaZ",
        site_url=url,
        user_agent=UA,
        gui=False,
        debug=False)

    if test is None:
        gui.addText(
            SITE_IDENTIFIER,
            '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

    else:
        # N'affiche pas directement le liens car sinon Kodi crash.
        display_title = "Recaptcha passé avec succès, cliquez pour afficher les liens"
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('movie_title', movie_title)
        output_parameter_handler.addParameter('thumb', thumb)
        output_parameter_handler.addParameter('Token', test)
        output_parameter_handler.addParameter('sPost', post)
        output_parameter_handler.addParameter('sChapter', chapter)
        output_parameter_handler.addParameter('_type', types)
        gui.addEpisode(
            SITE_IDENTIFIER,
            'getHost',
            display_title,
            '',
            thumb,
            '',
            output_parameter_handler)

    gui.setEndOfDirectory()


def getHost():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    test = input_parameter_handler.getValue('Token')
    post = input_parameter_handler.getValue('sPost')
    chapter = input_parameter_handler.getValue('sChapter')
    types = input_parameter_handler.getValue('_type')

    # On valide le token du coté du site
    data = 'action=get_video_chapter_content&grecaptcha=' + test + '&manga=' + \
        post + '&chapter=' + chapter + '&host=' + types.replace(' ', '+')
    request_handler = RequestHandler(
        "https://voiranime.com/wp-admin/admin-ajax.php")
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip')
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', len(str(data)))
    request_handler.addParametersLine(data)
    html_content = request_handler.request()

    pattern = '<iframe src="([^"]+)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        for entry in results[1]:
            hoster_url = entry.replace('\\', '').replace('\\/', '/')
            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()
