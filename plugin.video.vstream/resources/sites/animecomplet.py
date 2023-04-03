# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import string

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'animecomplet'
SITE_NAME = 'Animecomplet'
SITE_DESC = 'Series Anime'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
# ANIM_NEWS = (URL_MAIN, 'showAnims')
# ANIM_ALPHA = (URL_MAIN, 'showAlpha')

tag_global = '#global'
URL_SEARCH_ANIMS = (URL_MAIN + tag_global + '?s=', 'showAnims')
URL_SEARCH = (URL_MAIN + '?s=', 'showAnims')


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

    # output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers  épisodes récents)', 'series.png', output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', ANIM_ALPHA[0])
    # gui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Liste alphabétique)', 'az.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha():
    gui = Gui()
    sAlpha = string.ascii_lowercase
    listAlpha = list(sAlpha)
    liste = []

    req = ANIM_LIST[0]
    request_handler = RequestHandler(req)
    html_content = request_handler.request()

    # on propose quand meme en premier la liste complete
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_LIST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_LIST[1],
        ' [COLOR coral]' +
        'Animés (Liste complète)' +
        '[/COLOR]',
        'listes.png',
        output_parameter_handler)

    # récupere les chiffres dispos
    pattern = 'href="#gti_(\\d+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        for entry in results[1]:
            liste.append([str(entry), url1 + str(entry)])

    for alpha in listAlpha:
        liste.append([str(alpha).upper(), url1 + str(alpha)])

    # url = 'tagalpha ;alpha'
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnims',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showAnims(url)
        gui.setEndOfDirectory()
        return


def showAnims(search=''):
    gui = Gui()

    is_search_global = False
    if search:
        search_text = search.replace(URL_SEARCH[0], '')
        search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
        search_text = cUtil().CleanName(search_text)
        url = search.replace(' ', '+').replace('%20', '+')
        if tag_global in search:
            url = url.replace(tag_global, '')
            is_search_global = True
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    # pour la liste alpha on peu aussi faire url = alpha (plus rapide)
    # pattern = '<a href="([^"]+)">..' + alpha + '([^<]+).+?style="width'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<article id=".+?img src="([^\"]+)".+?<a href="([^\"]+)"><.+?>(.+?)<'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    iCurrent = 0
    list_simlilar = []

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            iCurrent = iCurrent + 1
            thumb = ''
            desc = ''
            thumb = entry[0]
            url2 = entry[1]
            title = entry[2]
            try:
                title = title.decode('ascii', errors='ignore')
            except BaseException:
                pass
            title = title.replace(
                ' - Episode',
                ' Episode').replace(
                ' VOSTFR',
                '').replace(
                ' VF',
                '')
            if search and not util.CheckOccurence(search_text, title):
                continue    # Filtre de recherche

            lang = ''
            if ' VOSTFR' in title:
                lang = 'VOSTFR'
            if ' VF' in title:
                lang = 'VF'
            if 'http' not in thumb:
                thumb = URL_MAIN + thumb

            # le lien liés a l'episode va nous fournir apres tous
            # les episodes saisons donc inutile de tout afficher si titre
            # semblable
            if is_search_global and iCurrent > 3:
                bValid, sim = similarTitle(title)
                if bValid:
                    if sim not in list_simlilar:
                        list_simlilar.append(sim)
                    else:
                        continue
            sDisplayTtitle = title + ' (' + lang + ')'

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                sDisplayTtitle,
                '',
                thumb,
                desc,
                output_parameter_handler)

    if not is_search_global:
        next_page, paging = __checkForNextPage(html_content)
        if next_page is not False:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showAnims',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '>([^<]+)</a><a class="next page.+?href="([^"]+).+?Suivant'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = URL_MAIN + results[1][0][1]
        number_next = re.search('paged=([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'colo_cont">.+?>([^<]*)</p>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        desc = results[1][0]
        desc = (
            '[I][COLOR coral]%s[/COLOR][/I] %s') % (' SYNOPSIS : \r\n\r\n', desc)
    else:
        desc = ''

    pattern = 'class="item">.+?href="([^"]+)".+?<h2>([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry[0]
            title = movie_title + ' ' + entry[1]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<h2 class="entry-title">.+?b>([^<]+)'
    results = parser.parse(html_content, pattern)

    desc = ('[I][COLOR grey]%s[/COLOR][/I]') % ('Anime Complet')
    if results[0]:
        desc = (
            '[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', results[1][0])

    # inutile (pour l'instant)
    start = html_content.find('<div class="post-content">')
    html_content = html_content[start:]

    pattern = '<h2><a href="([^"]+).+?title="([^"]+).+?src=.([^">]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url2 = entry[0]
            title = entry[1]
            if ' VOSTFR' in title:
                title = title.replace(
                    ' - Episode',
                    ' Episode').replace(
                    ' VOSTFR',
                    '')
            thumb = entry[2]
            if 'http' not in thumb:
                thumb = URL_MAIN + thumb

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        next_page, paging = __checkForNextPage(html_content)
        if next_page is not False:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showEpisodes',
                'Page ' + paging,
                output_parameter_handler)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'iframe.+?src="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = entry

            if 'https' not in url2:
                url2 = 'https:' + url2

            # host = ''
            hoster = HosterGui().checkHoster(url2)
            if not hoster:
                continue
            host = '[COLOR coral]' + hoster.getDisplayName() + '[/COLOR]'

            display_title = movie_title + ' ' + host
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('referer', url)
            gui.addLink(
                SITE_IDENTIFIER,
                'hostersLink',
                display_title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def getHostName(url):
    try:
        if 'www' not in url:
            host = re.search('http.*?\\/\\/([^.]*)', url).group(1)
        else:
            host = re.search('htt.+?\\/\\/(?:www).([^.]*)', url).group(1)
            host = str(host).capitalize()
    except BaseException:
        host = url
    return host


def hostersLink():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    hoster_url = url

    if 'oload.tv' in url:  # https://oload.tv/embed/0rRYBdB_3Xw/# #ace attorney vostfr
        gui.addText(
            SITE_IDENTIFIER,
            ' vStream : Accès refusé : Le site Oload.tv n\'est pas sécurisé')
        gui.setEndOfDirectory()
        return

    # Petit hack pour conserver le nom de domaine du site
    # necessaire pour userload.
    if 'userload' in hoster_url:
        hoster_url = hoster_url + "|Referer=" + URL_MAIN

    hoster = HosterGui().checkHoster(hoster_url)
    if hoster:
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                               input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


def similarTitle(s):
    list_spe = ['&', '\'', ',', '.', ';', '!']

    s = s.strip()
    if ' ' in s:
        try:
            s = str(s).lower()
            sx = s.split(' ')
            snews = sx[0] + ' ' + sx[1]
            for spe in list_spe:
                snews = snews.replace(spe, '')
            return True, snews.lower()
        except BaseException:
            return False, False
    return False, False
