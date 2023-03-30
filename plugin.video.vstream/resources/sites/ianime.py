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
    oParser = Parser()
    sPattern = '(.+?),\\[(.+?)\\],\\[(.+?)\\]\\)'
    aResult2 = oParser.parse(chain, sPattern)
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
    sPattern = '<script type="text/javascript">document\\.write\\(unescape\\(".+?"\\)\\);</script>'
    aResult = re.findall(sPattern, code)
    if aResult:
        return Unquote(aResult[0])
    return code


def ICDecode(html):

    # if 'HTML/JavaScript Encoder' not in html:
    #     return html

    import math

    sPattern = 'language=javascript>c="([^"]+)";eval\\(unescape\\("([^"]+)"\\)\\);x\\("([^"]+)"\\);'
    aResult = re.findall(sPattern, html)

    if not aResult:
        return html

    c = aResult[0][0]
    # a = aResult[0][1]
    x = aResult[0][2]

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
    aResult = re.findall('t=Array\\(([0-9,]+)\\);', Unquote(d))
    if not aResult:
        return ''

    t = aResult[0].split(',')
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
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche animés',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animés (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés (Liste)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
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

    output_parameter_handler.addParameter('siteUrl', ANIM_DRAMA[0])
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
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        showMovies(sUrl + sSearchText)
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
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + sUrl)
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
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = '<center><a href="(.+?)" onmouseover="this.style.color.+?>(.+?)</a>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    genres = []
    if aResult[0]:
        for aEntry in aResult[1]:
            title = aEntry[1]
            title = str(cUtil().unescape(title))
            # on filtre les genres
            if 'Ecchi' in title:
                continue
            sUrl = URL_MAIN + aEntry[0]
            genres.append((title, sUrl))

        # Trie des genres par ordre alphabétique
        genres = sorted(genres, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, sUrl in genres:
            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showAlpha2():
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sUrl2 = URL_MAIN + 'animes.php?liste=' + RandomKey

    sType = 'VF'
    if 'vostfr' in sUrl:
        sType = 'VOSTFR'

    oRequestHandler = RequestHandler(sUrl2)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    oParser = Parser()
    sPattern = '<a href=.(listing_(?:vf|vostfr)\\.php\\?affichage=[^<>"]+?). class=.button black pastel light. alt="Voir la liste des animes en ' + sType + '"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        showAlpha(URL_MAIN + aResult[1][0])


def showAlpha(url=None):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    if url is None:
        sUrl = input_parameter_handler.getValue('siteUrl')
    else:
        sUrl = url

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = "<a href=.([^<>]+?). class=.button (?:red )*light.><headline6>(?:<font color=.black.>)*([A-Z#])(?:</font>)*</headline6></a>"

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sLetter = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                'Lettre [B][COLOR red]' +
                sLetter +
                '[/COLOR][/B]',
                'listes.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()
    oParser = Parser()

    if sSearch:
        oUtil = cUtil()
        typeSearch, sSearch = sSearch.split('=')
        sSearch = Unquote(sSearch)
        sSearch = oUtil.CleanName(sSearch)

        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')

        # remplace espace par + et passe en majuscule
        sSearch = QuotePlus(sSearch).upper()

        sUrl = URL_SEARCH[0] + sSearch + '.html'

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = cutSearch(sHtmlContent, typeSearch)

    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', RandomReferer())
        sHtmlContent = oRequestHandler.request()
        # sHtmlContent = DecryptMangacity(sHtmlContent)

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl or 'drama.php' in sUrl:
        sPattern = '<center><div style="background: url\\(\'([^\'].+?)\'\\); background-size.+?alt="(.+?)" title.+?<a href=["\']*(.+?)[\'"]* class=.button'
    else:
        sPattern = '<center><div style="background: url\\(\'([^\'].+?)\'\\); background-size.+?<a href="([^"]+)".+?alt="(.+?)"'

    sHtmlContent = re.sub(
        '<a\\s*href=\"categorie.php\\?watch=\"\\s*class="genre\\s*\"',
        '',
        sHtmlContent,
        re.DOTALL)

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl or 'drama.php' in sUrl:
                title = aEntry[1]
                sUrl2 = aEntry[2]
            else:
                title = str(aEntry[2])
                sUrl2 = aEntry[1]

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            # affichage de la langue
            sLang = ''
            if 'VF' in title:
                sLang = 'VF'
                title = title.replace(sLang, '')
            elif 'VOSTFR' in title:
                sLang = 'VOSTFR'
                title = title.replace(sLang, '')

            title = title.replace('()', '').strip()

            # affichage de la qualité -> NON, qualité fausse
            # sQual = ''
            # if 'DVDRIP' in title:
            # sQual = 'DVDRIP'

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
                title = oUtil.CleanName(title)

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sDisplayTitle = title

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)

            if 'drama.php' in sUrl:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    sDisplayTitle,
                    'animes.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif (sSearch and typeSearch == 'tvshow') or '?serie=' in sUrl2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaison',
                    sDisplayTitle,
                    'series.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif '?manga=' in sUrl2:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showSaison',
                    sDisplayTitle,
                    'animes.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif '?film=' in sUrl2:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showMovies',
                    sDisplayTitle,
                    'films.png',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    sDisplayTitle,
                    'films.png',
                    sThumb,
                    '',
                    output_parameter_handler)

    if not sSearch:  # une seule page par recherche
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Suivant',
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()

    sPattern = 'class=.button red light. title=.Voir la page.+?<a href=.(.+?)(?:\'|") class=.button light.'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        sPattern = "<.table><center><center><a href='(.+?)' class='button light' title='Voir la page 1'>"
        aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False


def showSaison():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', RandomReferer())
    sHtmlContent = oRequestHandler.request()

    try:
        desc = oParser.parse(
            sHtmlContent,
            '</headline15>.+?<font style=.+?>([^"]+)</font')[1][0]
    except BaseException:
        desc = ""

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    # </a>|href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"'
    sPattern = '<headline11>(.+?)</headline11>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sSeason = aEntry.replace('00', '0')
            siteUrl = sUrl + '&season=' + sSeason
            sDisplayTitle = sMovieTitle + ' ' + sSeason
            output_parameter_handler.addParameter('siteUrl', siteUrl)
            output_parameter_handler.addParameter('sMovieTitle', sDisplayTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisode',
                sDisplayTitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sUrl, sSearchSeason = input_parameter_handler.getValue(
        'siteUrl').split('&season=')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', RandomReferer())
    sHtmlContent = oRequestHandler.request()

    try:
        desc = oParser.parse(
            sHtmlContent,
            '</headline15>.+?<font style=.+?>([^"]+)</font')[1][0]
    except BaseException:
        desc = ""

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sPattern = '<headline11>(.+?)</headline11></a>|href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sSeason = ''
        isPython3 = isMatrix()

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sSeason = aEntry[0].replace('00', '0')
                continue

            if sSeason != sSearchSeason:
                continue

            if not isPython3:
                title = unicode(aEntry[2], 'iso-8859-1')
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
                title = aEntry[2]

            title = cUtil().unescape(title)
            sLang = ''
            if 'VF' in title:
                sLang = 'VF'
                title = title.replace(sLang, '')
            elif 'VOSTFR' in title:
                sLang = 'VOSTFR'
                title = title.replace(sLang, '')

            sUrl2 = cUtil().unescape(aEntry[1])
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            idx = title.find('Episode')
            if idx > 0:
                title = title.replace(sSeason, '')
                title = '%s %s %s' % (title[:idx], sSeason, title[idx:])

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def extractLink(html):
    # Fake link
    fake1 = 'https://www.youtube.com'
    fake2 = '/api.js'

    final = ''

    oParser = Parser()

    sPattern = '(?i)src=(?:\'|")(.+?)(?:\'|")'
    aResult = re.findall(sPattern, html, re.DOTALL)

    if aResult:
        for a in aResult:
            if ('adnetworkperformance' in a) or ('jquery' in a):
                continue
            if fake1 not in a and fake2 not in a:
                final = a
                break

    sPattern = 'encodeURI\\("(.+?)"\\)'
    aResult = re.findall(sPattern, html)
    if aResult:
        if fake1 not in aResult[0] and fake2 not in aResult[0]:
            final = aResult[0]

    sPattern = "'file': '(.+?)',"
    aResult = oParser.parse(html, sPattern)
    if aResult[0]:
        if fake1 not in aResult[1][0] and fake2 not in aResult[1][0]:
            final = aResult[1][0]

    # nouveau codage
    if ';&#' in final:
        final = cUtil().unescape(final)

    if (not final.startswith('http')) and (len(final) > 2):
        final = URL_MAIN + final

    return final.replace(' ', '').replace('\n', '')


def showHosters(input_parameter_handler=False):
    gui = Gui()
    oParser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', RandomReferer())
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sHtmlContent = sHtmlContent.replace(
        '<iframe src="http://www.promoliens.net', '')
    sHtmlContent = sHtmlContent.replace("<iframe src='cache_vote.php", '')

    sPattern = '<iframe.+?src=\'([^<>"]+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    sText = 'Animés dispo gratuitement et légalement sur :'
    if 'animedigitalnetwork.fr' in str(aResult[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            sText +
            "[/COLOR][COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(aResult[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            sText +
            "[/COLOR][COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(aResult[1]):
        gui.addText(
            SITE_IDENTIFIER,
            "[COLOR red]" +
            sText +
            "[/COLOR][COLOR coral] wakanim[/COLOR]")
    else:
        list_url = []

        # 1 er methode
        sPattern = '<div class="box"><iframe.+?src=[\'|"](.+?)[\'|"]'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:
                if re.match(".+?&#[0-9]+;", aEntry):  # directe mais codé html
                    sHosterUrl = cUtil().unescape(aEntry)

                else:  # directe en clair
                    sHosterUrl = str(aEntry)

                # Ces liens sont toujours des liens
                if (not sHosterUrl.startswith('http')) and (
                        len(sHosterUrl) > 2):
                    sHosterUrl = URL_MAIN + sHosterUrl

                list_url.append(sHosterUrl)

        # 2 eme methode
        sPattern = '<script>eval\\(unescape\\((.+?)\\); eval\\(unescape\\((.+?)\\);</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                # si url cryptee mangacity algo
                sHosterUrl = DecryptMangacity(aEntry[1])
                sHosterUrl = sHosterUrl.replace('\\', '')
                list_url.append(sHosterUrl)

        # 3 eme methode
        sPattern = 'document\\.write\\(unescape\\("(%3c%.+?)"\\)\\);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                tmp = Unquote(aEntry)

                sPattern2 = 'src=["\']([^"\']+)["\']'
                aResult = re.findall(sPattern2, tmp)
                if aResult:
                    list_url.append(aResult[0])

        if len(list_url) > 0:
            for aEntry in list_url:

                sHosterUrl = aEntry

                # Dans le cas ou l'adresse n'est pas directe,on cherche a
                # l'extraire
                if not sHosterUrl[:4] == 'http':
                    sHosterUrl = extractLink(sHosterUrl)

                # Si aucun lien on arrete ici
                if not sHosterUrl:
                    continue

                # si openload code
                if 'openload2.php' in sHosterUrl:
                    # on telecharge la page

                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()
                    # Et on remplace le code
                    sHtmlContent = ICDecode(sHtmlContent)
                    sHosterUrl = extractLink(sHtmlContent)

                # Passe par lien .asx ??
                sPattern = '(https*:\\/\\/www.ianime[^\\/\\]+\\/[0-9a-zA-Z_-]+\\.asx)'
                aResult = oParser.parse(sHosterUrl, sPattern)
                if aResult[0]:
                    # on telecharge la page
                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()

                    # Si c'est une redirection, on passe juste le vrai lien
                    if 'ianime' not in oRequestHandler.getRealUrl().split(
                            '/')[2]:
                        sHosterUrl = oRequestHandler.getRealUrl()
                    else:
                        # Sinon on remplace le code
                        html = ICDecode(sHtmlContent)
                        sHosterUrl = extractLink(html)

                # Passe par lien .vxm ??
                # sPattern = 'http:\/\/www.ianime[^\/\\]+\/([0-9a-zA-Z_-]+)\.vxm'
                # aResult = oParser.parse(sHosterUrl, sPattern)
                # if aResult[0] :
                # sHosterUrl = 'http://embed.nowvideo.sx/embed.php?v=' + aResult[1][0]

                # redirection tinyurl
                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = getTinyUrl(sHosterUrl)

                # test pr liens raccourcis
                if 'http://goo.gl' in sHosterUrl:
                    try:
                        oRequestHandler = RequestHandler(sHosterUrl)
                        oRequestHandler.addHeaderEntry(
                            'User-Agent', "Mozilla 5.10")
                        oRequestHandler.addHeaderEntry('Host', "goo.gl")
                        oRequestHandler.addHeaderEntry(
                            'Connection', 'keep-alive')
                        sHtmlContent = oRequestHandler.request()
                        sHosterUrl = oRequestHandler.getRealUrl()

                    except BaseException:
                        pass

                # Potection visio.php
                if '/visio.php?' in sHosterUrl:
                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()

                    sHtmlContent = ICDecode(sHtmlContent)

                    sPattern = 'src=[\'"]([^\'"]+)[\'"]'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        sHosterUrl = aResult[1][0]

                # Derniere en date
                sPattern = "(https*:\\/\\/www.ianime[^\\/\\]+\\/[^']+)"
                aResult = oParser.parse(sHosterUrl, sPattern)
                if aResult[0]:
                    oRequestHandler = RequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)

                    sHtmlContent = oRequestHandler.request()
                    sHtmlContent = ICDecode(sHtmlContent)
                    sHosterUrl2 = extractLink(sHtmlContent)

                    if 'intern_player.png' in sHosterUrl2 or 'intern_player2.png' in sHosterUrl2:
                        xx = str(random.randint(300, 350))  # 347
                        yy = str(random.randint(200, 255))  # 216

                        # Remove old hoster
                        sHosterUrl = sHosterUrl.replace(
                            GetHost(sHosterUrl), "")
                        # Add new one
                        sHosterUrl = GetHost(sHosterUrl2) + sHosterUrl

                        oRequestHandler = RequestHandler(sHosterUrl)
                        oRequestHandler.setRequestType(
                            RequestHandler.REQUEST_TYPE_POST)
                        # Add params
                        oRequestHandler.addParameters('submit.x', xx)
                        oRequestHandler.addParameters('submit.y', yy)

                        # look for hidden params
                        p1 = re.search(
                            r'name="valeur" value="([^"]+)"', sHtmlContent)
                        if p1:
                            oRequestHandler.addParameters(
                                'valeur', p1.group(1))

                        # Set headers
                        oRequestHandler.addHeaderEntry('Referer', sUrl)
                        oRequestHandler.addHeaderEntry('User-Agent', UA)
                        sHtmlContent = oRequestHandler.request()

                        sHosterUrl2 = extractLink(sHtmlContent)

                    sHosterUrl = sHosterUrl2

                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = getTinyUrl(sHosterUrl)

                if '///' in sHosterUrl:
                    sHosterUrl = 'https://' + \
                        '/'.join(sHosterUrl.split('/')[5:])

                VSlog(sHosterUrl)

                oHoster = HosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
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
        oRequestHandler = RequestHandler(url)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        UrlRedirect = oRequestHandler.getRealUrl()

        if not (UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.getResponseHeader():
            url = reponse.getResponseHeader()['Location']
    return url


def cutSearch(sHtmlContent, typeSearch):
    types = {'movies': 'Films et Animations',
             'tvshow': 'Séries et Drama',
             'anime': 'Animes et Mangas'}
    sPattern = types.get(typeSearch) + \
        '<.+?alt="separateur"(.+?)alt="separateur"'

    aResult = Parser().parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
