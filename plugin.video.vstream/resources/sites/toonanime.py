# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import urlEncode

try:
    xrange
except NameError:
    xrange = range

SITE_IDENTIFIER = 'toonanime'
SITE_NAME = 'Toon Anime'
SITE_DESC = 'anime en VF/VOSTFR'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_VFS = (URL_MAIN + 'anime-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-vostfr/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'films/', 'showMovies')
ANIM_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        "Recherche d'animés",
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_FILM[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_FILM[1],
        "Film d'animation japonais (Derniers ajouts)",
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Dernier ajouts)',
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

    output_parameter_handler.addParameter('site_url', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = [
        [
            'Action', 'Action'], [
            'Animation', 'Action'], [
                'Aventure', 'Aventure'], [
                    'Comédie', 'Comédie'], [
                        'Tranche de Vie', 'Tranche de vie'], [
                            'Drame', 'Drame'], [
                                'Fantasy', 'Fantasy'], [
                                    'Surnaturel', 'Surnaturel'], [
                                        'Mystère', 'Mystère'], [
                                            'Shonen', 'Shonen'], [
                                                'Psychologique', 'Psychologique'], [
                                                    'Romance', 'Romance'], [
                                                        'Science-Fiction', 'Sci-Fi']]

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'xfsearch/genre/' + url + '/')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(xrange(1982, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'xfsearch/year/' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    bGlobal_Search = False
    if search:
        if URL_SEARCH[0] in search:
            bGlobal_Search = True
            search = search.replace(URL_SEARCH[0], '')

        query_args = (('do', 'search'), ('subaction', 'search'),
                      ('story', search), ('titleonly', '0'), ('full_search', '1'))
        data = urlEncode(query_args)

        request_handler = RequestHandler(URL_SEARCH[0])
        request_handler.setRequestType(1)
        request_handler.addParametersLine(data)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', URL_SEARCH[0])
        request_handler.addHeaderEntry(
            'Content-Type', 'application/x-www-form-urlencoded')
        request_handler.addHeaderEntry('Content-Length', str(len(data)))
        html_content = request_handler.request()
    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    if "/films/" in url:
        pattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" alt="([^"]+).+?pg">([^<]+).+?text">([^<]+)'
    else:
        pattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" alt="([^"]+).+?pg">([^<]+).+?cat">([^<]+).+?text">([^<]+)'

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

            url2 = entry[0]
            thumb = entry[1]
            if thumb.startswith('/'):
                thumb = URL_MAIN[:-1] + thumb
            if "/films/" in url:
                title = entry[2]
                qual = entry[3]
                desc = entry[4]
                lang = ""
            else:
                lang = entry[2].split(" ")[-1]
                title = re.sub('Saison \\d+',
                               '',
                               entry[2][:entry[2].rfind('')].replace(lang,
                                                                       "")) + " " + entry[4]
                qual = entry[3]
                desc = entry[5]

            display_title = ('%s [%s] (%s)') % (title, qual, lang.upper())

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            gui.addAnime(
                SITE_IDENTIFIER,
                'ShowSxE',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a href="([^"]+)"><span class="md__icon md-arrowr"></span>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def ShowSxE():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    # movie_title = input_parameter_handler.getValue('movie_title')
    # movie_title = re.sub('Episode \d+', '', movie_title)

    sID = url.split('/')[3].split('-')[0]

    request_handler = RequestHandler(
        URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    html_content = request_handler.request(json_decode=True)['html']

    pattern = 'href="(.+?)".+?title="(.+?)">'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = entry[1]
            url2 = entry[0]

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('id', sID)

            gui.addAnime(
                SITE_IDENTIFIER,
                'seriesHosters',
                title,
                'animes.png',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def seriesHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    sID = input_parameter_handler.getValue('id')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'data-class="(.+?) ".+?data-server-id="(.+?)"'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    request_handler = RequestHandler(
        URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    html_content = request_handler.request(json_decode=True)['html']

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            pattern = '<div id="content_player_' + entry[1] + '".+?>(.+?)<'
            aResult1 = parser.parse(html_content, pattern)
            hostClass = entry[0]

            for aEntry1 in aResult1[1]:
                # title = movie_title  + " [COLOR coral]" + hostClass.capitalize() + "[/COLOR]"

                if "https" in aEntry1[0]:
                    hoster_url = aEntry1[0]
                elif hostClass == "cdnt":
                    hoster_url = "https://lb.toonanime.xyz/playlist/" + \
                        aEntry1 + "/" + str(round(time.time() * 1000))
                else:
                    request_handler = RequestHandler(
                        URL_MAIN + "/templates/toonanime/js/anime.js")
                    sHtmlContent1 = request_handler.request()

                    pattern = 'player_type=="toonanimeplayer_' + \
                        hostClass + '".+?src=\\\\"([^\\\\]+)\\\\"'
                    urlBase = parser.parse(sHtmlContent1, pattern)[1][0]
                    hoster_url = urlBase.replace('"+player_content+"', aEntry1)

                if "toonanime" in hoster_url:
                    hoster = HosterGui().checkHoster(".mp4")
                else:
                    hoster = HosterGui().checkHoster(hoster_url)

                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()
