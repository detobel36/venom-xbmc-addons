# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager

import re

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = 'https://gum-gum-streaming.co/'  # sans pub

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showNews')
ANIM_VFS = (URL_MAIN + 'vf/', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'vostfr/', 'showAnimes')
ANIM_MOVIES = (URL_MAIN + 'films/', 'showMovies')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
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

    output_parameter_handler.addParameter(
        'site_url', 'https://gum-gum-streaming.com/vostfr1/')
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR) (A-F)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', 'https://gum-gum-streaming.com/vostfr2/')
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR) (G-L)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', 'https://gum-gum-streaming.com/vostfr3/')
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR) (M-R)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter(
        'site_url', 'https://gum-gum-streaming.com/vostfr4/')
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR) (S-Z)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_MOVIES[1],
        'Films',
        'animes.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showNews():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # pattern = 'Dernier (VF|VOSTFR|OAV|Film)\s*: (?:<a |<a title="([^"]+)" )href="([^"]+)" data-wpel-link="internal">([^<]+)'
    pattern = 'Dernier (VF|VOSTFR|OAV|Film)\\s*: (<a|<a title="([^"]+)") href="([^"]+)" data-wpel-link="internal">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if '' == entry[2]:  # titre absent donc on le recup dans l'url
                num = entry[4]
                title = re.sub(URL_MAIN, '', entry[3])
                title = title.replace(
                    '-', ' ')[:-1] + ' ' + num.replace('N°', 'E')
                url = entry[3]
            else:
                title = entry[2]
                url = entry[3]

            # traitement pour affichage de la langue
            lang = ''
            if 'VF' in title or 'vf' in title:
                lang = 'VF'
            elif 'VOSTFR' in title:
                lang = 'VOSTFR'

            title = title.replace(
                ' VOSTFR',
                '').replace(
                ' VF',
                '').replace(
                ' vf',
                '')
            display_title = ('%s (%s)') % (title, lang)

            sFilter = re.search('(\\d+)-(\\d+)', url)
            if sFilter:
                continue

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                '',
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showAnimes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'Synopsis:([^"]+)" href="([^"]+).+?">([^<]+).+?data-lazy-src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME, large=True)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            desc = entry[0]
            url = entry[1]
            title = entry[2]
            thumb = entry[3]

            # traitement du titre pour compatibilite
            title = title.replace('(', ' ').replace(')', ' ')
            title = re.sub('([0-9]+) .. ([0-9\\?]+)', '\\1-\\2', title)
            title = re.sub('([0-9]+) & ([0-9\\?]+)', '\\1-\\2', title)

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)

            gui.addAnime(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                'animes.png',
                thumb,
                desc,
                output_parameter_handler)
        progress_.VSclose(progress_)
    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    sSerieTitle = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace('><span', '').replace('span></', '')
    pattern = '<header class="entry-header">(.+?)<footer class="entry-footer">'
    results = parser.parse(html_content, pattern)
    sUsentContent = results[1][0]

    # récupération du synopsis
    desc = ''
    pattern = 'Synopsis:</span>(.+?)</h5>'
    aSynResult = parser.parse(sUsentContent, pattern)
    if aSynResult[0]:
        desc = aSynResult[1][0]
        desc = desc.replace('<br />', '').replace('&#8216;', '\'')

    # récupération du poster
    thumb = ''
    pattern = '<h4 style=".+?"><img class="alignright".+?data-lazy-src="(.+?)"'
    sThumbResult = parser.parse(sUsentContent, pattern)
    if sThumbResult[0]:
        thumb = sThumbResult[1][0]

    pattern = '<h2 style="color: #.+?">([^<]+)|href="http([^"]+)".+?>([^<]+)<\\/a>'
    results = parser.parse(sUsentContent, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        sSaison = ''
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                sSaison = entry[0]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    sSaison +
                    '[/COLOR]')
                if ':' in sSaison:
                    sSaison = sSaison[:sSaison.index(':')]
                sSaison = sSaison.capitalize().strip()
            else:
                aUrl = 'http' + entry[1]
                display_title = entry[2].replace('•', '').strip()
                if display_title.endswith(':'):
                    display_title = display_title[:-1]

                title = sSerieTitle + ' ' + display_title

                output_parameter_handler.addParameter('site_url', aUrl)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('thumb', thumb)
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'style="width: 280px;"><h2><a title="Synopsis: (.+?)" href="([^"]+).+?>([^<]+).+?data-lazy-src="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME, large=True)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            desc = entry[0]
            url = entry[1]
            title = entry[2]
            thumb = entry[3]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            if title.lower().find('les films') != -1:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovieList',
                    title,
                    'animes.png',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'animes.png',
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)
    gui.setEndOfDirectory()


def showMovieList():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<a title=".+?" href="([^"]+)">(.+?)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                '',
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<div class="video-container"> ?<iframe.+?data-lazy-src="([^"]+)'
    results = parser.parse(html_content, pattern)

    sTexte = "[COLOR red]Animés dispo gratuitement et légalement sur :[/COLOR]"
    if 'animedigitalnetwork.fr' in str(results[1]):
        gui.addText(SITE_IDENTIFIER, sTexte +
                    "[COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(results[1]):
        gui.addText(
            SITE_IDENTIFIER,
            sTexte +
            "[COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(results[1]):
        gui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] wakanim[/COLOR]")
    else:
        if results[0]:
            for entry in results[1]:
                hoster_url = entry
                if not hoster_url.startswith('http'):
                    hoster_url = 'http:' + hoster_url

                if 'tinyurl' in hoster_url:
                    hoster_url = GetTinyUrl(hoster_url)

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, '',
                                           input_parameter_handler=input_parameter_handler)
    gui.setEndOfDirectory()


def GetTinyUrl(url):
    if 'tinyurl' not in url:
        return url

    # Lien deja connu ?
    if '://tinyurl.com/h7c9sr7' in url:
        url = url.replace('://tinyurl.com/h7c9sr7/', '://vidwatch.me/')
    elif '://tinyurl.com/jxblgl5' in url:
        url = url.replace('://tinyurl.com/jxblgl5/', '://streamin.to/')
    elif '://tinyurl.com/q44uiep' in url:
        url = url.replace('://tinyurl.com/q44uiep/', '://openload.co/')
    elif '://tinyurl.com/jp3fg5x' in url:
        url = url.replace('://tinyurl.com/jp3fg5x/', '://allmyvideos.net/')
    elif '://tinyurl.com/kqhtvlv' in url:
        url = url.replace('://tinyurl.com/kqhtvlv/', '://openload.co/embed/')
    elif '://tinyurl.com/lr6ytvj' in url:
        url = url.replace('://tinyurl.com/lr6ytvj/', '://netu.tv/')
    elif '://tinyurl.com/kojastd' in url:
        url = url.replace(
            '://tinyurl.com/kojastd/',
            '://www.rapidvideo.com/embed/')
    elif '://tinyurl.com/l3tjslm' in url:
        url = url.replace('://tinyurl.com/l3tjslm/', '://hqq.tv/player/')
    elif '://tinyurl.com/n34gtt7' in url:
        url = url.replace('://tinyurl.com/n34gtt7/', '://vidlox.tv/')
    elif '://tinyurl.com/kdo4xuk' in url:
        url = url.replace('://tinyurl.com/kdo4xuk/', '://watchers.to/')
    elif '://tinyurl.com/kjvlplm' in url:
        url = url.replace('://tinyurl.com/kjvlplm/', '://streamango.com/')
    elif '://tinyurl.com/kt3owzh' in url:
        url = url.replace('://tinyurl.com/kt3owzh/', '://estream.to/')

    # On va chercher le vrai lien
    else:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
        request_handler = RequestHandler(url)
        request_handler.disableRedirect(1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', URL_MAIN)
        reponse = request_handler.request()
        UrlRedirect = reponse.GetRealUrl()

        if not (UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.getResponseHeader():
            url = reponse.getResponseHeader()['Location']

    return url
