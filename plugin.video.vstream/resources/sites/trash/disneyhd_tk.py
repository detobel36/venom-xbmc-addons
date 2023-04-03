# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.util import Unquote
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False  # au 18/03/2020


SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'https://disneyhd.cf/'
URL_LISTE = URL_MAIN + '?page=liste.php'
ANIM_ENFANTS = ('http://', 'load')

FUNCTION_SEARCH = 'sHowResultSearch'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = ('', FUNCTION_SEARCH)

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'

##########################################################################
# DECODE TORRENT : https://effbot.org/zone/bencode.htm
##########################################################################


def tokenize(text, match=re.compile("([idel])|(\\d+):|(-?\\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i + int(s)]
            i = i + int(s)
        else:
            yield s


def decode_item(nextItem, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(next())
        if next() != "e":
            raise ValueError
    elif token == "s":
        # string: "s" value (virtual tokens)
        data = next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != "e":
            data.append(decode_item(nextItem, tok))
            tok = next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data


def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.next, src.next())
        for token in src:  # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data

##########################################################################


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
    output_parameter_handler.addParameter('site_url', URL_MAIN)
    output_parameter_handler.addParameter('filtre', 'ajouts')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Ajouts récents',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_MAIN)
    output_parameter_handler.addParameter('filtre', 'populaires')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Populaires',
        'enfants.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_LISTE)
    output_parameter_handler.addParameter('filtre', 'liste')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Liste des films',
        'enfants.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        sHowResultSearch(str(search_text))
        gui.setEndOfDirectory()
        return


def sHowResultSearch(search=''):
    gui = Gui()

    search = Unquote(search)

    request_handler = RequestHandler(URL_MAIN + 'movies_list.php')
    html_content = request_handler.request()

    parser = Parser()
    pattern = '<a class="item" href="([^"]+)" title="([^"]+)"> *<img src="([^"]+)">'
    results = parser.parse(html_content, pattern)

    if results[0]:

        progress_ = Progress().VScreate(SITE_NAME)
        for entry in results[1]:
            title = entry[1]
            if search.lower() not in title.lower():
                continue

            url = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN + entry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'enfants.png',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        gui.setEndOfDirectory()


def order(sList, sIndex):
    # remet en ordre le résultat du parser par un index ici par le titre qui est en position 2
    # exemple: ('http://venom', 'thumb', 'title')
    #          results = order(results[1], 2)
    results = sorted(sList, key=lambda a: a[sIndex])
    # retourne au format du parser
    return True, results


def showMovies():
    gui = Gui()
    parser = Parser()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if input_parameter_handler.exist('filtre'):
        sFiltre = input_parameter_handler.getValue('filtre')
    else:
        sFiltre = "none"

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if 'ajouts' in sFiltre:
        html_content = parser.abParse(
            html_content, '</i> Derniers ajouts', '</section>')
        results = parser.parse(html_content, sPattern1)
    elif 'populaires' in sFiltre:
        html_content = parser.abParse(
            html_content,
            '</i> Les plus populaires',
            '</i> Visionnés en ce moment')
        results = parser.parse(html_content, sPattern1)
    else:
        html_content = parser.abParse(html_content, 'style', '</html>')
        results = parser.parse(html_content, sPattern1)
        results = order(results[1], 2)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = URL_MAIN[:-1] + entry[0]
            thumb = URL_MAIN + entry[1]
            title = entry[2].replace(
                'streaming',
                '').replace(
                ' 1080p',
                '').replace(
                '_',
                ' ')

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            if entry[0].startswith('s-'):
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'enfants.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    'enfants.png',
                    thumb,
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()

# Non utilisé


def ShowList():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    results = parser.parse(html_content,
                            '<li data-arr_pos="([0-9]+)">([^<]+)<')

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            title = entry[1]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'enfants.png',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    parser = Parser()

    # film
    if '<ol id="playlist">' in html_content:
        pattern = '<li data-trackurl="([^"]+)">(.+?)<\\/li>'
    elif 'data-ws=' in html_content:
        pattern = 'data-ws="([^"]+)">(.+?)</span>'
    else:
        pattern = 'class="qualiteversion" data-qualurl="([^"]+)">([^"]+)</span>'

    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry[0]
            sFinalTitle = movie_title + ' ' + entry[1]

            if '/mp4/' in hoster_url and 'http' not in hoster_url:
                hoster_url = 'http://disneyhd.tk%s' % hoster_url

            if '//goo.gl' in hoster_url:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response
                        https_response = http_response

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append(('User-Agent', UA))
                    opener.addheaders.append(('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    hoster_url = HttpReponse.headers['Location']
                    hoster_url = hoster_url.replace('https', 'http')
                except BaseException:
                    pass

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(sFinalTitle)
                hoster.setFileName(sFinalTitle)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)
    else:
        # playlist-serie lien direct http pour le moment
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:
                hoster_url = entry[0]
                title = entry[1]

                hoster = HosterGui().checkHoster(hoster_url)
                if (hoster):
                    hoster.setDisplayName(title)
                    hoster.setFileName(title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        else:
            # Dernier essai avec les torrent
            results = parser.parse(html_content, 'data-maglink="([^"]+)')
            if results[0]:
                match = Unquote(results[1][0])

                folder = re.findall('ws=(https[^&]+)', match)[0] + '/'
                torrent = re.findall('xs=(https[^&]+)', match)[0]

                oRequestHandler2 = RequestHandler(torrent)
                torrent = decode(oRequestHandler2.request())

                files = torrent['info']['files']
                name = torrent['info']['name']

                count = 0
                for i in files:
                    hoster_url = (folder + name + '/' + i['path'][0])
                    count = count + 1

                    hoster = HosterGui().checkHoster(hoster_url)
                    if (hoster):
                        hoster.setDisplayName(
                            movie_title + " " + name + "E" + str(count))
                        hoster.setFileName(
                            movie_title + " " + name + "E" + str(count))
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb)

            else:
                gui.addText(SITE_IDENTIFIER)

    gui.setEndOfDirectory()
