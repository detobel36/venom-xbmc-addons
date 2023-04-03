# -*- coding: utf-8 -*-
# Venom.
from resources.lib.gui.hoster import HosterGui  # system de recherche pour l'hote
# system de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import Gui  # system d'affichage pour xbmc
from resources.lib.gui.guiElement import GuiElement  # system d'affichage pour xbmc
# entrer des parametres
from resources.lib.handler.inputParameterHandler import InputParameterHandler
# sortis des parametres
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler  # requete url
from resources.lib.config import cConfig  # config
from resources.lib.parser import Parser  # recherche de code
from resources.lib.util import cUtil
import urllib2
import urllib
import re
import unicodedata
import htmlentitydefs
import time

# Si vous créer une source et la déposer dans le dossier sites elle seras
# directement visible sous xbmc

SITE_IDENTIFIER = 'cacastream_com'
SITE_NAME = 'Cacastream.com'
SITE_DESC = 'Series/Films/Animes en streaming'

URL_MAIN = 'http://www.cacastream.com'  # url de votre source

# definis les url pour les catégories principale ceci et automatique si la
# deffition et présente elle seras afficher.
MOVIE_NEWS = (
    'http://www.cacastream.com/films-en-streaming.html',
    'showMovies')
SERIE_SERIES = (
    'http://www.cacastream.com/series-en-streaming.html',
    'showAlpha')
ANIM_ANIMS = (
    'http://www.cacastream.com/mangas-en-streaming.html',
    'showAlpha')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def unescape(text):
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


def _DecryptProtectStream(url):

    videoId = re.findall(
        'protect-stream\\.com\\/PS_DL_([A-Za-z0-9\\-_]+)', url)
    # print(videoId[0])

    request_handler = RequestHandler(
        "http://www.protect-stream.com/w.php?u=" + videoId[0])
    html_content = request_handler.request()

    cheap = re.findall('var k=\"([^<>\"]*?)\";', html_content)

    if not cheap:
        return ''

    # Need to wait
    time.sleep(10)

    query_args = {'k': cheap[0]}
    data = urllib.urlencode(query_args)
    headers = {'User-Agent': 'Mozilla 5.10'}
    url = 'http://www.protect-stream.com/secur.php'
    request = urllib2.Request(url, data, headers)

    try:
        reponse = urllib2.urlopen(request)
    except URLError as e:
        print e.read()
        print e.reason

    html = reponse.read()

    DecryptedUrl = re.findall('href=\"(http[^<>\"]*?)\"', html)

    if DecryptedUrl:
        return DecryptedUrl[0]

    return False


def load():  # function charger automatiquement par l'addon l'index de votre navigation.
    gui = Gui()  # ouvre l'affichage

    # apelle la function pour sortir un parametre
    output_parameter_handler = OutputParameterHandler()
    # sortis du parametres site_url oublier pas la Majuscule
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Liste Series',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Liste Animes',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Liste Films',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()  # ferme l'affichage


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        showMovies(str(search_text))
        gui.setEndOfDirectory()
        return


def showAlpha(sLettre=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    sLettre = input_parameter_handler.getValue('sLettre')

    dialog = cConfig().createDialog(SITE_NAME)

    if not sLettre:
        for i in range(0, 27):
            cConfig().updateDialog(dialog, 27)
            if dialog.iscanceled():
                break

            title = chr(64 + i)
            if title == '@':
                title = '[0-9]'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('sLettre', title)
            output_parameter_handler.addParameter('site_url', url)
            gui.addTV(
                SITE_IDENTIFIER,
                'showAlpha',
                '[COLOR teal] Lettre [COLOR red]' +
                title +
                '[/COLOR][/COLOR]',
                '',
                '',
                '',
                output_parameter_handler)
    else:

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        pattern = 'font-size:10px;font-weight:bold;" href="([^<]+)" class="b">(' + str(
            sLettre) + '.*?)<\\/a>'

        parser = Parser()
        results = parser.parse(html_content, pattern)

        if results[0]:
            total = len(results[1])
            dialog = cConfig().createDialog(SITE_NAME)

            for entry in results[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break

                title = entry[1]

                # Unicode convertion
                title = unicode(title, 'iso-8859-1')
                title = unicodedata.normalize(
                    'NFD', title).encode(
                    'ascii', 'ignore')
                title = unescape(title)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'site_url', str(URL_MAIN) + '/' + str(entry[0]))
                output_parameter_handler.addParameter('movie_title', title)
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', '', '', output_parameter_handler)

    cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()

    if search:
        # on redecode la recherhce codé il y a meme pas une seconde par l'addon
        search = urllib2.unquote(search)

        sDisp = input_parameter_handler.getValue('disp')
        # print search

        if (sDisp == 'search3'):  # anime
            url = 'http://www.cacastream.com/rechercher-un-manga.html'
            query_args = {'searchm': str(search)}
        elif (sDisp == 'search2'):  # serie
            url = 'http://www.cacastream.com/rechercher-une-serie.html'
            query_args = {'searchs': str(search)}
        else:
            url = 'http://www.cacastream.com/rechercher-un-film.html'
            query_args = {'searchf': str(search)}

        data = urllib.urlencode(query_args)
        headers = {'User-Agent': 'Mozilla 5.10'}

        request = urllib2.Request(url, data, headers)

        try:
            reponse = urllib2.urlopen(request)
        except URLError as e:
            print e.read()
            print e.reason

        html_content = reponse.read()

        pattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?<i>(.+?)<.i>(?:.|\n)+?<a href="([^<]+)" class='
        # pattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?Synopsis : <.b> <i>(.+?)<.i>(.|\n)+?<a href="([^<]+)" class='

    else:

        url = input_parameter_handler.getValue('site_url')

        request_handler = RequestHandler(url)
        html_content = request_handler.request()

        pattern = 'Tip\\(\'<center><b>(.+?)<.b>.+?Synopsis : <.b> <i>(.+?)<.i>(?:.|\n)+?<a href="(.+?)"><img src="(.+?)" alt'

    # fh = open('c:\\serie.txt', "w")
    # fh.write(html_content)
    # fh.close()

    parser = Parser()
    results = parser.parse(html_content, pattern)

    print results

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if search:
                title = entry[1]
                thumb = str(entry[0])
                sCom = entry[2]
                url2 = str(URL_MAIN) + '/' + str(entry[3])
            else:
                title = entry[0]
                thumb = str(entry[3])
                sCom = entry[1]
                url2 = str(URL_MAIN) + '/' + str(entry[2])

            # Nettoyage titre
            title = unicode(title, errors='replace')
            title = title.encode('ascii', 'ignore').decode('ascii')

            # Nettoyage commentaires
            sCom = unicode(sCom, 'iso-8859-1')  # converti en unicode
            sCom = unicodedata.normalize('NFD', sCom).encode(
                'ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
            sCom = unescape(sCom)  # decode html
            sCom = re.sub('<.*?>', '', sCom)  # remove html tags

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', str(title))
            output_parameter_handler.addParameter('thumbnail', thumb)

            if ('-episode-' in url2):
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    thumb,
                    sCom,
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showListHosters', title,
                          '', thumb, sCom, output_parameter_handler)

        cConfig().finishDialog(dialog)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            # print next_page
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter(
                'site_url', str(URL_MAIN) + next_page)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                'next.png',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<td width="124" class="page_tab"><a href="(.+?)" class="b">Page Suivante<.a><.td>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showEpisode():
    gui = Gui()  # ouvre l'affichage

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # print url

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # fh = open('c:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    parser = Parser()

    # image
    pattern = '<div class="tvshow_image">.+?src="(.+?)"'
    results = parser.parse(html_content, pattern)

    if results[0]:
        thumbnail = results[1][0]
    else:
        thumbnail = ''

    # commentaire
    pattern = '<span class="infos01">Synopsis : <\\/span>(.+?)<\\/div>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        sCom = results[1][0]
        # Nettoyage commentaires
        sCom = unicode(sCom, 'iso-8859-1')  # converti en unicode
        sCom = unicodedata.normalize('NFD', sCom).encode(
            'ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
        sCom = unescape(sCom)  # decode html
        sCom = re.sub('<.*?>', '', sCom)  # remove html tags

    else:
        sCom = ''

    # liens par saisons
    pattern = '(?:<a name="s[0-9]+" >(Saison.+?)<\\/a>)|(?:<a class="e" href="(.+?)">(.+?)<\\/a>)'
    results = parser.parse(html_content, pattern)

    # si pas trouvé par episode
    if not results[0]:
        pattern = '(ABXY)*<a (class)="e" href="(.+?episode.+?html)">(.+?)<\\/a>'
        results = parser.parse(html_content, pattern)

    # print results

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = entry[2]

            # Nettoyage titre
            title = unicode(title, errors='replace')
            title = title.encode('ascii', 'ignore').decode('ascii')

            if entry[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', str(title))

                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    '[COLOR red]' +
                    entry[0] +
                    '[/COLOR]',
                    '',
                    thumbnail,
                    '',
                    output_parameter_handler)
            else:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'site_url', str(URL_MAIN) + '/' + entry[1])
                output_parameter_handler.addParameter(
                    'movie_title', str(title))
                output_parameter_handler.addParameter('thumbnail', thumbnail)

                gui.addTV(
                    SITE_IDENTIFIER,
                    'showListHosters',
                    title,
                    '',
                    thumbnail,
                    sCom,
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

        gui.setEndOfDirectory()


def showListHosters():
    gui = Gui()  # ouvre l'affichage

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    print url

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # fh = open('c:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    pattern = '(?:<a href="(http:..www.protect-stream.com.+?)" target="_blank" class="b"><b><span class="(.+?)">(.+?)<\\/span>)|(?:<a href="mylink\\.php\\?v=(.+?)&rang=.+?&lecteur=(.+?)" class="b" target="mesliens">)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    print results

    if results[0]:
        # on bride car trop de resultat
        aResultMax = results[1]
        if len(aResultMax) > 100:
            aResultMax = aResultMax[:100]
        total = len(aResultMax)
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in aResultMax:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            # 1 er cas
            host = str(entry[2])
            url = entry[0]

            # 2 eme cas
            if entry[3]:
                host = str(entry[4])
                url = 'http://www.protect-stream.com/PS_DL_' + str(entry[3])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', str(title))

            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                '[COLOR red][' + host + '][/COLOR] ' + title,
                '',
                thumbnail,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)  # dialog

        gui.setEndOfDirectory()  # ferme l'affichage


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # on decrypte le seul lien present
    cConfig().showInfo('Decryptage', 'Please wait 10s')
    results = _DecryptProtectStream(url)

    if (results):

        hoster_url = str(results)

        hoster = HosterGui().checkHoster(hoster_url)
        if (hoster):
            hoster.setDisplayName(movie_title)
            hoster.setFileName(movie_title)
            HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()
