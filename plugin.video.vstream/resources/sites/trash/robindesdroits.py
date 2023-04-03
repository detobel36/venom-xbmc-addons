# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil
from resources.lib.multihost import cJheberg
from resources.lib.multihost import cMultiup
from resources.lib.packer import cPacker
from resources.lib.util import Unquote

SITE_IDENTIFIER = 'robindesdroits'
SITE_NAME = 'Robin des Droits'
SITE_DESC = 'Replay sports'

URL_MAIN = 'http://robindesdroits.me/'

SPORT_NEWS = (URL_MAIN + 'derniers-uploads/', 'showMovies')
SPORT_FOOT = (URL_MAIN + 'football/', 'showMovies')
SPORT_US = (URL_MAIN + 'sports-us/', 'showMovies')
SPORT_AUTO = (URL_MAIN + 'sports-automobiles/', 'showMovies')
SPORT_RUGBY = (URL_MAIN + 'rugby/', 'showMovies')
SPORT_TENNIS = (URL_MAIN + 'tennis/', 'showMovies')
SPORT_HAND = (URL_MAIN + 'handball/', 'showMovies')
SPORT_BASKET = (URL_MAIN + 'basketball/', 'showMovies')
SPORT_DIVERS = (URL_MAIN + 'docus-et-divers/', 'showMovies')
SPORT_SPORTS = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_NEWS[1],
        'Nouveautés',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_SPORTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_SPORTS[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_FOOT[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_FOOT[1],
        'Football',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_RUGBY[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_RUGBY[1],
        'Rugby',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_BASKET[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_BASKET[1],
        'Basketball',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_AUTO[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_AUTO[1],
        'Sport Automobiles',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_US[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_US[1],
        'Sport US',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_TENNIS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_TENNIS[1],
        'Tennis',
        'sport.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_HAND[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_HAND[1],
        'Handball',
        'sport.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Football', SPORT_FOOT[0], 'Matchs de Football'])
    liste.append(['Football (Emissions)', SPORT_FOOT[0],
                 'Emissions de Football'])

    liste.append(['Rugby', SPORT_RUGBY[0], 'Matchs de Rugby'])
    liste.append(['Rugby (Emissions)', SPORT_RUGBY[0], 'Emissions de Rugby'])

    liste.append(['Basketball', SPORT_BASKET[0], 'BASKETBALL'])

    liste.append(['Sports Automobiles', SPORT_AUTO[0],
                 'Courses de Sports Mécaniques'])
    liste.append(['Sports Automobiles (Emissions)',
                 SPORT_AUTO[0], 'Emissions de Sports Mécaniques'])

    liste.append(['Sports US', SPORT_US[0], 'Matchs de Sports US'])
    liste.append(['Sports US (Emissions)', SPORT_US[0],
                 'Emissions de Sports US'])

    liste.append(['Tennis (Grand Chelem)', SPORT_TENNIS[0], 'Grand Chelem'])
    liste.append(['Tennis (ATP)', SPORT_TENNIS[0], 'ATP Masters 1000'])
#     liste.append(['Tennis', SPORT_TENNIS[0], 'ATP Finals'])

    liste.append(['Handball', SPORT_HAND[0], 'HANDBALL'])

    for title, url, sFiltre in liste:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        output_parameter_handler.addParameter('cat', sFiltre)
        gui.addDir(
            SITE_IDENTIFIER,
            'showCat',
            title,
            'genres.png',
            output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_DIVERS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_DIVERS[1],
        'Documentaires',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showCat():

    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    # site_url = input_parameter_handler.getValue('site_url')
    sFiltre = input_parameter_handler.getValue('cat')

    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    html_content = parser.abParse(html_content, sFiltre, '</ul>')
    pattern = 'href="([^"]+)">(.+?)</a>'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)

            if 'Emissions' in sFiltre:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showMovies',
                    title,
                    'sport.png',
                    output_parameter_handler)
            else:
                gui.addDir(
                    SITE_IDENTIFIER,
                    'showLinkGenres',
                    title,
                    'sport.png',
                    output_parameter_handler)
    else:
        gui.addText(SITE_DESC)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<figure class="mh-loop-thumb"><a href="([^"]+)"><img src=".+?" style="background:url\\(\'(.+?)\'\\).+?rel="bookmark">(.+?)</a></h3>'

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:

        for entry in results[1]:
            url = entry[0]
            thumb = entry[1]
            title = entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showLink',
                title,
                'sport.png',
                thumb,
                '',
                output_parameter_handler)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                number +
                ' >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<a class="next page-numbers" href="([^"]+)"'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showLinkGenres():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    thumb = ''
    try:
        pattern = '<p style="text-align: center;"><img src="([^"]+)".+?</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            thumb = results[1][0]
    except BaseException:
        pass

    pattern = '<span style="font-family: Arial, Helvetica,.+?font-size:.+?pt;">([^<>]+)<\\/span>|<li ><a href="([^"]+)" title=".+?">([^<>]+)</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            if entry[0]:
                title = entry[0]
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR gold]' +
                    title +
                    '[/COLOR]')
            else:
                url = entry[1]
                title = entry[2]

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)

                gui.addDir(
                    SITE_IDENTIFIER,
                    'showLink',
                    title,
                    'sport.png',
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showLink():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'a href="([^"]+)">(?:<span.+?|)<b>([^<]+)</b><'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            url = entry[0]
            host = cUtil().removeHtmlTags(entry[1])

            display_title = (
                '%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addDir(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                'sport.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def AdflyDecoder(url):
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()
    pattern = "var ysmm = '([^']+)'"
    results = parser.parse(html_content, pattern)

    if results[0]:

        from base64 import b64decode

        code = results[1][0]

        A = ''
        B = ''
        # First pass
        for num in enumerate(code):
            if num % 2 == 0:
                A += code[num]
            else:
                B = code[num] + B

        code = A + B

        # Second pass
        m = 0
        code = list(code)
        while m < len(code):
            if code[m].isdigit():
                R = m + 1
                while R < len(code):
                    if code[R].isdigit():
                        S = int(code[m]) ^ int(code[R])
                        if (S < 10):
                            code[m] = str(S)
                        m = R
                        R = len(code)
                    R += 1
            m += 1

        code = ''.join(code)
        code = b64decode(code)
        code = code[16:]
        code = code[:-16]

        return code

    return ''


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # D'abord on saute les redirections.
    if 'replay.robindesdroits' in url:
        pattern = 'content="0;URL=([^"]+)">'
        results = parser.parse(html_content, pattern)
        if results:
            url = results[1][0]
            request_handler = RequestHandler(url)
            html_content = request_handler.request()

    # Ensuite les sites a la con
    if (True):
        if 'AdF' in html_content:
            url = AdflyDecoder(url)
            if 'motheregarded' in url:
                pattern = 'href=(.+?)&dp_lp'
                results = parser.parse(url, pattern)
                if results[0]:
                    url = Unquote(''.join(results[1])).decode('utf8')

            request_handler = RequestHandler(url)
            html_content = request_handler.request()

    # clictune / mylink / ect ...
    pattern = '<b><a href=".+?redirect\\/\\?url\\=(.+?)\\&id.+?">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        url = Unquote(results[1][0])

    # Et maintenant le ou les liens

    if 'gounlimited' in url:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        pattern = '(eval\\(function\\(p,a,c,k,e(?:.|\\s)+?\\))<\\/script>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            html_content = cPacker().unpack(results[1][0])

            pattern = '{sources:\\["([^"]+)"'
            results = parser.parse(html_content, pattern)
            if not results[0]:
                pattern = '\\[{src:"([^"]+)"'
                results = parser.parse(html_content, pattern)

            if results[0]:
                hoster_url = results[1][0]
                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    elif 'jheberg' in url:
        results = cJheberg().GetUrls(url)
        if (results):
            for entry in results:
                hoster_url = entry

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    elif 'multiup' in url:
        results = cMultiup().GetUrls(url)

        if (results):
            for entry in results:
                hoster_url = entry

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    else:
        hoster_url = url
        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()
