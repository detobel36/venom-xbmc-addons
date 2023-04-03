# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import unicodedata

from resources.lib.comaddon import Progress
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil, Quote

try:
    xrange
except NameError:
    xrange = range

SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnees videos.'

URL_MAIN = 'https://www.imdb.com/'
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'

MOVIE_WORLD = (
    URL_MAIN +
    'search/title?groups=top_1000&sort=user_rating,desc&start=1',
    'showMovies')
MOVIE_TOP250 = (
    URL_MAIN +
    'search/title?count=100&groups=top_250',
    'showMovies')
MOVIE_ANNEES = (True, 'showMovieYears')


def unescape(text):
    try:  # python 2
        import htmlentitydefs
    except ImportError:  # Python 3
        import html.entities as htmlentitydefs

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\\w+;", fixup, text)


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_WORLD[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_WORLD[1],
        'Top Films Mondial',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_TOP250[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP250[1],
        'Top 250',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Top (Par Années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()

    import datetime
    now = datetime.datetime.now()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(xrange(1903, int(now.year) + 1)):
        output_parameter_handler.addParameter(
            'site_url',
            URL_MAIN +
            'search/title?year=' +
            str(i) +
            ',' +
            str(i) +
            '&title_type=feature&explore=languages')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            str(i),
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    # bGlobal_Search = False

    input_parameter_handler = InputParameterHandler()
    if search:
        url = search
    else:
        url = input_parameter_handler.getValue('site_url')
    # if URL_SEARCH[0] in search:
        # bGlobal_Search = True

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry(
        'Accept-Language',
        'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    html_content = request_handler.request()

    pattern = 'img alt="([^"]+).+?loadlate="([^"]+).+?primary">([^<]+).+?unbold">([^<]+).+?(?:|rated this(.+?)\\s.+?)muted">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # title = unicode(entry[0], 'utf-8')  # converti en unicode
            # title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore')  # vire accent
            # title = unescape(str(entry[1]))
            # title = title.encode( "utf-8")

            title = (
                '%s %s [COLOR fuchsia]%s[/COLOR]') % (entry[2], entry[0], entry[4])
            thumb = entry[1].replace(
                'UX67',
                'UX328').replace(
                'UY98',
                'UY492').replace(
                '67',
                '0').replace(
                '98',
                '0')
            year = re.search('([0-9]{4})', entry[3]).group(1)
            desc = entry[5]

            output_parameter_handler.addParameter('site_url', 'none')
            output_parameter_handler.addParameter(
                'movie_title', str(entry[0]))
            output_parameter_handler.addParameter('year', year)
            output_parameter_handler.addParameter(
                'searchtext', showTitle(str(entry[0]), str('none')))
            gui.addMovie('globalSearch', 'showSearch', title, '',
                         thumb, desc, output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Suivant',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory('500')


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'href="([^"]+?)"class="lister-page-next'
    results = parser.parse(html_content, pattern)

    if results[0]:
        url = ('%s/%s') % (URL_MAIN, results[1][0])
        return url

    return False


def showTitle(movie_title, url):

    sExtraTitle = ''
    # si c'est une série
    if url != 'none':
        sExtraTitle = url.split('|')[1]
        movie_title = url.split('|')[0]

    movie_title = cUtil().CleanName(movie_title)

    # modif ici
    if sExtraTitle:
        movie_title = movie_title + sExtraTitle
    else:
        movie_title = movie_title

    return movie_title
