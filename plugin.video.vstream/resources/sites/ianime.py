# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import re
import unicodedata

from resources.lib.comaddon import VSlog, isMatrix, SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil, Unquote, QuotePlus

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

# Make random url
s = 'azertyuiopqsdfghjklmwxcvbn0123456789AZERTYUIOPQSDFGHJKLMWXCVBN'
RandomKey = ''.join(random.choice(s) for i in range(32))


SITE_IDENTIFIER = 'ianime'
SITE_NAME = 'I anime'
SITE_DESC = 'Animés en streaming'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (URL_MAIN + 'films.php?liste=' + RandomKey, 'showAlpha')
MOVIE_GENRES = (URL_MAIN, 'showGenresMovies')

SERIE_SERIES = (URL_MAIN + 'series.php?liste=' + RandomKey, 'showAlpha')

ANIM_NEWS = (URL_MAIN + 'nouveautees.html', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.php?liste=' + RandomKey, 'showAlpha')
ANIM_VFS = (URL_MAIN + 'listing_vf.php', 'showAlpha2')
ANIM_VOSTFRS = (URL_MAIN + 'listing_vostfr.php', 'showAlpha2')
ANIM_GENRES = (URL_MAIN + 'categorie.php?watch=' + RandomKey, 'showGenres')
ANIM_DRAMA = (URL_MAIN + 'drama.php', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH_MOVIES = ('movies=', 'showMovies')
URL_SEARCH_SERIES = ('tvshow=', 'showMovies')
URL_SEARCH_ANIMS = ('anime=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'resultat+', 'showMovies')


def RandomReferer():
    return URL_MAIN + ''.join(random.choice(s) for i in range(32)) + '.htm'


def DecryptMangacity(chain):
    parser = Parser()
    pattern = '(.+?),\\[(.+?)\\],\\[(.+?)\\]\\)'
    aResult2 = parser.parse(chain, pattern)
    d = ''

    if aResult2[0] is True:

        a = aResult2[1][0][0]
        b = aResult2[1][0][1].replace('"', '').split(',')
        c = aResult2[1][0][2].replace('"', '').split(',')

        d = a
        for i in range(0, len(b)):
            d = d.replace(b[i], c[i])

        d = d.replace('%26', '&')
        d = d.replace('%3B', ';')

    return d


def FullUnescape(code):
    pattern = '<script type="text/javascript">document\\.write\\(unescape\\(".+?"\\)\\);</script>'
    results = re.findall(pattern, code)
    if results:
        return Unquote(results[0])
    return code


def ICDecode(html):

    # if 'HTML/JavaScript Encoder' not in html:
    #     return html

    import math

    pattern = 'language=javascript>c="([^"]+)";eval\\(unescape\\("([^"]+)"\\)\\);x\\("([^"]+)"\\);'
    results = re.findall(pattern, html)

    if not results:
        return html

    c = results[0][0]
    # a = results[0][1]
    x = results[0][2]

    # premier decodage
    d = ''
    i = 0
    while i < len(c):
        if i % 3 == 0:
            d = d + '%'
        else:
            d = d + c[i]
        i = i + 1

    # Recuperation du tableau
    results = re.findall('t=Array\\(([0-9,]+)\\);', Unquote(d))
    if not results:
        return ''

    t = results[0].split(',')
    l = len(x)
    b = 1024
    i = p = s = w = 0
    j = math.ceil(float(l) / b)
    r = ''

    while j > 0:

        i = min(l, b)
        while i > 0:
            w |= int(t[ord(x[p]) - 48]) << s
            p = p + 1
            if s:
                r = r + chr(165 ^ w & 255)
                w >>= 8
                s = s - 2
            else:
                s = 6

            i = i - 1
            l = l - 1

        j = j - 1

    return str(r)


def GetHost(_url):
    parts = _url.split('//', 1)
    host = parts[0] + '//' + parts[1].split('/', 1)[0]
    return host

# ------------------------------------------------------------------------------------


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
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

    output_parameter_handler.addParameter('site_url', ANIM_DRAMA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_DRAMA[1],
        'Animés (Drama)',
        'dramas.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        showMovies(url + search_text)
        gui.setEndOfDirectory()
        return


def showGenresMovies():
    gui = Gui()

    liste = []
    liste.append(['Action', 'categorie_action_page1.html'])
    liste.append(['Animation', 'categorie_animation_page1.html'])
    liste.append(['Aventure', 'categorie_aventure_page1.html'])
    liste.append(['Combat', 'categorie_combats_page1.html'])
    liste.append(['Comédie', 'categorie_comedie_page1.html'])
    liste.append(['Drame', 'categorie_drame_page1.html'])
    liste.append(['Espionnage', 'categorie_espionnage_page1.html'])
    liste.append(['Fantastique', 'categorie_fantastique_page1.html'])
    liste.append(['Guerre', 'categorie_guerre_page1.html'])
    liste.append(['Horreur', 'categorie_epouvante_page1.html'])
    liste.append(['Musical', 'categorie_musical_page1.html'])
    liste.append(['Péplum', 'categorie_peplum_page1.html'])
    liste.append(['Policier', 'categorie_policier_page1.html'])
    liste.append(['Romance', 'categorie_romance_page1.html'])
    liste.append(['Thriller', 'categorie_thriller_page1.html'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', URL_MAIN + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


# Retrouve les genres en dynamique dans la page
def showGenres():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    html_content = request_handler.request()

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    if html_content.startswith('<script type="text/javascript">'):
        html_content = FullUnescape(html_content)

    pattern = '<center><a href="(.+?)" onmouseover="this.style.color.+?>(.+?)</a>'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    genres = []
    if results[0]:
        for entry in results[1]:
            title = entry[1]
            title = str(cUtil().unescape(title))
            # on filtre les genres
            if 'Ecchi' in title:
                continue
            url = URL_MAIN + entry[0]
            genres.append((title, url))

        # Trie des genres par ordre alphabétique
        genres = sorted(genres, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in genres:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha2():
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    url2 = URL_MAIN + 'animes.php?liste=' + RandomKey

    _type = 'VF'
    if 'vostfr' in url:
        _type = 'VOSTFR'

    request_handler = RequestHandler(url2)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', URL_MAIN)
    html_content = request_handler.request()

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    if html_content.startswith('<script type="text/javascript">'):
        html_content = FullUnescape(html_content)

    parser = Parser()
    pattern = '<a href=.(listing_(?:vf|vostfr)\\.php\\?affichage=[^<>"]+?). class=.button black pastel light. alt="Voir la liste des animes en ' + _type + '"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        showAlpha(URL_MAIN + results[1][0])


def showAlpha(url=None):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    if url is None:
        url = input_parameter_handler.getValue('site_url')
    else:
        url = url

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', URL_MAIN)
    html_content = request_handler.request()

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    if html_content.startswith('<script type="text/javascript">'):
        html_content = FullUnescape(html_content)

    pattern = "<a href=.([^<>]+?). class=.button (?:red )*light.><headline6>(?:<font color=.black.>)*([A-Z#])(?:</font>)*</headline6></a>"

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = URL_MAIN + entry[0]
            sLetter = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                'Lettre [B][COLOR red]' +
                sLetter +
                '[/COLOR][/B]',
                'listes.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        util = cUtil()
        typeSearch, search = search.split('=')
        search = Unquote(search)
        search = util.CleanName(search)

        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_ANIMS[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')

        # remplace espace par + et passe en majuscule
        search = QuotePlus(search).upper()

        url = URL_SEARCH[0] + search + '.html'

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', URL_MAIN)
        html_content = request_handler.request()
        html_content = cutSearch(html_content, typeSearch)

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', RandomReferer())
        html_content = request_handler.request()
        # html_content = DecryptMangacity(html_content)

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    if html_content.startswith('<script type="text/javascript">'):
        html_content = FullUnescape(html_content)

    if search or 'categorie.php' in url or 'categorie_' in url or 'listing3.php?' in url or 'drama.php' in url:
        pattern = '<center><div style="background: url\\(\'([^\'].+?)\'\\); background-size.+?alt="(.+?)" title.+?<a href=["\']*(.+?)[\'"]* class=.button'
    else:
        pattern = '<center><div style="background: url\\(\'([^\'].+?)\'\\); background-size.+?<a href="([^"]+)".+?alt="(.+?)"'

    html_content = re.sub(
        '<a\\s*href=\"categorie.php\\?watch=\"\\s*class="genre\\s*\"',
        '',
        html_content,
        re.DOTALL)

    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            thumb = entry[0]
            if not thumb.startswith('http'):
                thumb = URL_MAIN + thumb

            if search or 'categorie.php' in url or 'categorie_' in url or 'listing3.php?' in url or 'drama.php' in url:
                title = entry[1]
                url2 = entry[2]
            else:
                title = str(entry[2])
                url2 = entry[1]

            if not url2.startswith('http'):
                url2 = URL_MAIN + url2

            # affichage de la langue
            lang = ''
            if 'VF' in title:
                lang = 'VF'
                title = title.replace(lang, '')
            elif 'VOSTFR' in title:
                lang = 'VOSTFR'
                title = title.replace(lang, '')

            title = title.replace('()', '').strip()

            # affichage de la qualité -> NON, qualité fausse
            # qual = ''
            # if 'DVDRIP' in title:
            # qual = 'DVDRIP'

            # Nettoyer le titre
            title = title.replace(' DVDRIP', '').replace('Visionnez ', '')
            title = title.replace(
                '[Streaming] - ',
                '').replace(
                'gratuitement maintenant',
                '')
            if ' - Episode' in title:
                title = title.replace(' -', '')

            if not isPython3:
                title = util.CleanName(title)

            # Filtre de recherche
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue

            display_title = title

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)

            if 'drama.php' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    'animes.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif (search and typeSearch == 'tvshow') or '?serie=' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '?manga=' in url2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaison',
                    display_title,
                    'animes.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '?film=' in url2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovies',
                    display_title,
                    'films.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
                    'films.png',
                    thumb,
                    '',
                    output_parameter_handler)

    if not search:  # une seule page par recherche
        next_page = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Suivant',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()

    pattern = 'class=.button red light. title=.Voir la page.+?<a href=.(.+?)(?:\'|") class=.button light.'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        pattern = "<.table><center><center><a href='(.+?)' class='button light' title='Voir la page 1'>"
        results = parser.parse(html_content, pattern)

    if results[0]:
        return URL_MAIN + results[1][0]

    return False


def showSaison():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', RandomReferer())
    html_content = request_handler.request()

    try:
        desc = parser.parse(
            html_content,
            '</headline15>.+?<font style=.+?>([^"]+)</font')[1][0]
    except BaseException:
        desc = ""

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    # </a>|href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"'
    pattern = '<headline11>(.+?)</headline11>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            season = entry.replace('00', '0')
            site_url = url + '&season=' + season
            display_title = movie_title + ' ' + season
            output_parameter_handler.addParameter('site_url', site_url)
            output_parameter_handler.addParameter('movie_title', display_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisode',
                display_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url, sSearchSeason = input_parameter_handler.getValue(
        'site_url').split('&season=')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', RandomReferer())
    html_content = request_handler.request()

    try:
        desc = parser.parse(
            html_content,
            '</headline15>.+?<font style=.+?>([^"]+)</font')[1][0]
    except BaseException:
        desc = ""

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    pattern = '<headline11>(.+?)</headline11></a>|href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        season = ''
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                season = entry[0].replace('00', '0')
                continue

            if season != sSearchSeason:
                continue

            if not isPython3:
                title = unicode(entry[2], 'iso-8859-1')
                title = unicodedata.normalize(
                    'NFD', title).encode(
                    'ascii', 'ignore')
                title = title.encode(
                    'ascii',
                    'ignore').decode('ascii').replace(
                    ' VF',
                    '').replace(
                    ' VOSTFR',
                    '')
            else:
                title = entry[2]

            title = cUtil().unescape(title)
            lang = ''
            if 'VF' in title:
                lang = 'VF'
                title = title.replace(lang, '')
            elif 'VOSTFR' in title:
                lang = 'VOSTFR'
                title = title.replace(lang, '')

            url2 = cUtil().unescape(entry[1])
            if not url2.startswith('http'):
                url2 = URL_MAIN + url2

            idx = title.find('Episode')
            if idx > 0:
                title = title.replace(season, '')
                title = '%s %s %s' % (title[:idx], season, title[idx:])

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def extractLink(html):
    # Fake link
    fake1 = 'https://www.youtube.com'
    fake2 = '/api.js'

    final = ''

    parser = Parser()

    pattern = '(?i)src=(?:\'|")(.+?)(?:\'|")'
    results = re.findall(pattern, html, re.DOTALL)

    if results:
        for a in results:
            if ('adnetworkperformance' in a) or ('jquery' in a):
                continue
            if fake1 not in a and fake2 not in a:
                final = a
                break

    pattern = 'encodeURI\\("(.+?)"\\)'
    results = re.findall(pattern, html)
    if results:
        if fake1 not in results[0] and fake2 not in results[0]:
            final = results[0]

    pattern = "'file': '(.+?)',"
    results = parser.parse(html, pattern)
    if results[0]:
        if fake1 not in results[1][0] and fake2 not in results[1][0]:
            final = results[1][0]

    # nouveau codage
    if ';&#' in final:
        final = cUtil().unescape(final)

    if (not final.startswith('http')) and (len(final) > 2):
        final = URL_MAIN + final

    return final.replace(' ', '').replace('\n', '')


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry('Referer', RandomReferer())
    html_content = request_handler.request()

    if 'HTML/JavaScript Encoder' in html_content:
        html_content = ICDecode(html_content)

    html_content = html_content.replace(
        '<iframe src="http://www.promoliens.net', '')
    html_content = html_content.replace("<iframe src='cache_vote.php", '')

    pattern = '<iframe.+?src=\'([^<>"]+?)\''
    results = parser.parse(html_content, pattern)

    text = 'Animés dispo gratuitement et légalement sur :'
    if 'animedigitalnetwork.fr' in str(results[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            text +
            "[/COLOR][COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(results[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            text +
            "[/COLOR][COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(results[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            text +
            "[/COLOR][COLOR coral] wakanim[/COLOR]")
    else:
        list_url = []

        # 1 er methode
        pattern = '<div class="box"><iframe.+?src=[\'|"](.+?)[\'|"]'
        results = parser.parse(html_content, pattern)

        if results[0]:
            for entry in results[1]:
                if re.match(".+?&#[0-9]+;", entry):  # directe mais codé html
                    hoster_url = cUtil().unescape(entry)

                else:  # directe en clair
                    hoster_url = str(entry)

                # Ces liens sont toujours des liens
                if (not hoster_url.startswith('http')) and (
                        len(hoster_url) > 2):
                    hoster_url = URL_MAIN + hoster_url

                list_url.append(hoster_url)

        # 2 eme methode
        pattern = '<script>eval\\(unescape\\((.+?)\\); eval\\(unescape\\((.+?)\\);</script>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:
                # si url cryptee mangacity algo
                hoster_url = DecryptMangacity(entry[1])
                hoster_url = hoster_url.replace('\\', '')
                list_url.append(hoster_url)

        # 3 eme methode
        pattern = 'document\\.write\\(unescape\\("(%3c%.+?)"\\)\\);'
        results = parser.parse(html_content, pattern)
        if results[0]:
            for entry in results[1]:
                tmp = Unquote(entry)

                sPattern2 = 'src=["\']([^"\']+)["\']'
                results = re.findall(sPattern2, tmp)
                if results:
                    list_url.append(results[0])

        if len(list_url) > 0:
            for entry in list_url:

                hoster_url = entry

                # Dans le cas ou l'adresse n'est pas directe,on cherche a
                # l'extraire
                if not hoster_url[:4] == 'http':
                    hoster_url = extractLink(hoster_url)

                # Si aucun lien on arrete ici
                if not hoster_url:
                    continue

                # si openload code
                if 'openload2.php' in hoster_url:
                    # on telecharge la page

                    request_handler = RequestHandler(hoster_url)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    html_content = request_handler.request()
                    # Et on remplace le code
                    html_content = ICDecode(html_content)
                    hoster_url = extractLink(html_content)

                # Passe par lien .asx ??
                pattern = '(https*:\\/\\/www.ianime[^\\/\\]+\\/[0-9a-zA-Z_-]+\\.asx)'
                results = parser.parse(hoster_url, pattern)
                if results[0]:
                    # on telecharge la page
                    request_handler = RequestHandler(hoster_url)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    html_content = request_handler.request()

                    # Si c'est une redirection, on passe juste le vrai lien
                    if 'ianime' not in request_handler.getRealUrl().split(
                            '/')[2]:
                        hoster_url = request_handler.getRealUrl()
                    else:
                        # Sinon on remplace le code
                        html = ICDecode(html_content)
                        hoster_url = extractLink(html)

                # Passe par lien .vxm ??
                # pattern = 'http:\/\/www.ianime[^\/\\]+\/([0-9a-zA-Z_-]+)\.vxm'
                # results = parser.parse(hoster_url, pattern)
                # if results[0] :
                # hoster_url = 'http://embed.nowvideo.sx/embed.php?v=' + results[1][0]

                # redirection tinyurl
                if 'tinyurl' in hoster_url:
                    hoster_url = getTinyUrl(hoster_url)

                # test pr liens raccourcis
                if 'http://goo.gl' in hoster_url:
                    try:
                        request_handler = RequestHandler(hoster_url)
                        request_handler.addHeaderEntry(
                            'User-Agent', "Mozilla 5.10")
                        request_handler.addHeaderEntry('Host', "goo.gl")
                        request_handler.addHeaderEntry(
                            'Connection', 'keep-alive')
                        html_content = request_handler.request()
                        hoster_url = request_handler.getRealUrl()

                    except BaseException:
                        pass

                # Potection visio.php
                if '/visio.php?' in hoster_url:
                    request_handler = RequestHandler(hoster_url)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry('User-Agent', UA)
                    html_content = request_handler.request()

                    html_content = ICDecode(html_content)

                    pattern = 'src=[\'"]([^\'"]+)[\'"]'
                    results = parser.parse(html_content, pattern)
                    if results[0]:
                        hoster_url = results[1][0]

                # Derniere en date
                pattern = "(https*:\\/\\/www.ianime[^\\/\\]+\\/[^']+)"
                results = parser.parse(hoster_url, pattern)
                if results[0]:
                    request_handler = RequestHandler(hoster_url)
                    request_handler.addHeaderEntry('Referer', url)
                    request_handler.addHeaderEntry('User-Agent', UA)

                    html_content = request_handler.request()
                    html_content = ICDecode(html_content)
                    sHosterUrl2 = extractLink(html_content)

                    if 'intern_player.png' in sHosterUrl2 or 'intern_player2.png' in sHosterUrl2:
                        xx = str(random.randint(300, 350))  # 347
                        yy = str(random.randint(200, 255))  # 216

                        # Remove old hoster
                        hoster_url = hoster_url.replace(
                            GetHost(hoster_url), "")
                        # Add new one
                        hoster_url = GetHost(sHosterUrl2) + hoster_url

                        request_handler = RequestHandler(hoster_url)
                        request_handler.setRequestType(
                            RequestHandler.REQUEST_TYPE_POST)
                        # Add params
                        request_handler.addParameters('submit.x', xx)
                        request_handler.addParameters('submit.y', yy)

                        # look for hidden params
                        p1 = re.search(
                            r'name="valeur" value="([^"]+)"', html_content)
                        if p1:
                            request_handler.addParameters(
                                'valeur', p1.group(1))

                        # Set headers
                        request_handler.addHeaderEntry('Referer', url)
                        request_handler.addHeaderEntry('User-Agent', UA)
                        html_content = request_handler.request()

                        sHosterUrl2 = extractLink(html_content)

                    hoster_url = sHosterUrl2

                if 'tinyurl' in hoster_url:
                    hoster_url = getTinyUrl(hoster_url)

                if '///' in hoster_url:
                    hoster_url = 'https://' + \
                        '/'.join(hoster_url.split('/')[5:])

                VSlog(hoster_url)

                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()


# -------------------------------------------------------------------------------------------
def getTinyUrl(url):
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
        request_handler = RequestHandler(url)
        request_handler.disableRedirect()
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry('Referer', URL_MAIN)
        html_content = request_handler.request()

        UrlRedirect = request_handler.getRealUrl()

        if not (UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.getResponseHeader():
            url = reponse.getResponseHeader()['Location']
    return url


def cutSearch(html_content, typeSearch):
    types = {'movies': 'Films et Animations',
             'tvshow': 'Séries et Drama',
             'anime': 'Animes et Mangas'}
    pattern = types.get(typeSearch) + \
        '<.+?alt="separateur"(.+?)alt="separateur"'

    results = Parser().parse(html_content, pattern)
    if results[0]:
        return results[1][0]
    return ''
