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

    oRequestHandler = RequestHandler(
        "http://www.protect-stream.com/w.php?u=" + videoId[0])
    sHtmlContent = oRequestHandler.request()

    cheap = re.findall('var k=\"([^<>\"]*?)\";', sHtmlContent)

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
    # sortis du parametres siteUrl oublier pas la Majuscule
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Liste Series',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Liste Animes',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Liste Films',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()  # ferme l'affichage


def showSearch():
    gui = Gui()

    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        showMovies(str(sSearchText))
        gui.setEndOfDirectory()
        return


def showAlpha(sLettre=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
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
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sLettre', title)
            output_parameter_handler.addParameter('siteUrl', sUrl)
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

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'font-size:10px;font-weight:bold;" href="([^<]+)" class="b">(' + str(
            sLettre) + '.*?)<\\/a>'

        oParser = Parser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)

            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break

                title = aEntry[1]

                # Unicode convertion
                title = unicode(title, 'iso-8859-1')
                title = unicodedata.normalize(
                    'NFD', title).encode(
                    'ascii', 'ignore')
                title = unescape(title)

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'siteUrl', str(URL_MAIN) + '/' + str(aEntry[0]))
                output_parameter_handler.addParameter('sMovieTitle', title)
                gui.addTV(SITE_IDENTIFIER, 'showEpisode', title,
                          '', '', '', output_parameter_handler)

    cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()

    if sSearch:
        # on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)

        sDisp = input_parameter_handler.getValue('disp')
        # print sSearch

        if (sDisp == 'search3'):  # anime
            url = 'http://www.cacastream.com/rechercher-un-manga.html'
            query_args = {'searchm': str(sSearch)}
        elif (sDisp == 'search2'):  # serie
            url = 'http://www.cacastream.com/rechercher-une-serie.html'
            query_args = {'searchs': str(sSearch)}
        else:
            url = 'http://www.cacastream.com/rechercher-un-film.html'
            query_args = {'searchf': str(sSearch)}

        data = urllib.urlencode(query_args)
        headers = {'User-Agent': 'Mozilla 5.10'}

        request = urllib2.Request(url, data, headers)

        try:
            reponse = urllib2.urlopen(request)
        except URLError as e:
            print e.read()
            print e.reason

        sHtmlContent = reponse.read()

        sPattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?<i>(.+?)<.i>(?:.|\n)+?<a href="([^<]+)" class='
        # sPattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?Synopsis : <.b> <i>(.+?)<.i>(.|\n)+?<a href="([^<]+)" class='

    else:

        sUrl = input_parameter_handler.getValue('siteUrl')

        oRequestHandler = RequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'Tip\\(\'<center><b>(.+?)<.b>.+?Synopsis : <.b> <i>(.+?)<.i>(?:.|\n)+?<a href="(.+?)"><img src="(.+?)" alt'

    # fh = open('c:\\serie.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if sSearch:
                title = aEntry[1]
                sThumb = str(aEntry[0])
                sCom = aEntry[2]
                sUrl2 = str(URL_MAIN) + '/' + str(aEntry[3])
            else:
                title = aEntry[0]
                sThumb = str(aEntry[3])
                sCom = aEntry[1]
                sUrl2 = str(URL_MAIN) + '/' + str(aEntry[2])

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
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', str(title))
            output_parameter_handler.addParameter('thumbnail', sThumb)

            if ('-episode-' in sUrl2):
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    sCom,
                    output_parameter_handler)
            else:
                gui.addTV(SITE_IDENTIFIER, 'showListHosters', title,
                          '', sThumb, sCom, output_parameter_handler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            # print sNextPage
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter(
                'siteUrl', str(URL_MAIN) + sNextPage)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                'next.png',
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<td width="124" class="page_tab"><a href="(.+?)" class="b">Page Suivante<.a><.td>'
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showEpisode():
    gui = Gui()  # ouvre l'affichage

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # print sUrl

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # fh = open('c:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    oParser = Parser()

    # image
    sPattern = '<div class="tvshow_image">.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        thumbnail = aResult[1][0]
    else:
        thumbnail = ''

    # commentaire
    sPattern = '<span class="infos01">Synopsis : <\\/span>(.+?)<\\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sCom = aResult[1][0]
        # Nettoyage commentaires
        sCom = unicode(sCom, 'iso-8859-1')  # converti en unicode
        sCom = unicodedata.normalize('NFD', sCom).encode(
            'ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
        sCom = unescape(sCom)  # decode html
        sCom = re.sub('<.*?>', '', sCom)  # remove html tags

    else:
        sCom = ''

    # liens par saisons
    sPattern = '(?:<a name="s[0-9]+" >(Saison.+?)<\\/a>)|(?:<a class="e" href="(.+?)">(.+?)<\\/a>)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # si pas trouvé par episode
    if not aResult[0]:
        sPattern = '(ABXY)*<a (class)="e" href="(.+?episode.+?html)">(.+?)<\\/a>'
        aResult = oParser.parse(sHtmlContent, sPattern)

    # print aResult

    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            title = aEntry[2]

            # Nettoyage titre
            title = unicode(title, errors='replace')
            title = title.encode('ascii', 'ignore').decode('ascii')

            if aEntry[0]:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', sUrl)
                output_parameter_handler.addParameter(
                    'sMovieTitle', str(title))

                gui.addTV(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    '[COLOR red]' +
                    aEntry[0] +
                    '[/COLOR]',
                    '',
                    thumbnail,
                    '',
                    output_parameter_handler)
            else:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'siteUrl', str(URL_MAIN) + '/' + aEntry[1])
                output_parameter_handler.addParameter(
                    'sMovieTitle', str(title))
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
    sUrl = input_parameter_handler.getValue('siteUrl')
    title = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    print sUrl

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # fh = open('c:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    sPattern = '(?:<a href="(http:..www.protect-stream.com.+?)" target="_blank" class="b"><b><span class="(.+?)">(.+?)<\\/span>)|(?:<a href="mylink\\.php\\?v=(.+?)&rang=.+?&lecteur=(.+?)" class="b" target="mesliens">)'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult

    if aResult[0]:
        # on bride car trop de resultat
        aResultMax = aResult[1]
        if len(aResultMax) > 100:
            aResultMax = aResultMax[:100]
        total = len(aResultMax)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResultMax:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            # 1 er cas
            sHost = str(aEntry[2])
            sUrl = aEntry[0]

            # 2 eme cas
            if aEntry[3]:
                sHost = str(aEntry[4])
                sUrl = 'http://www.protect-stream.com/PS_DL_' + str(aEntry[3])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', str(title))

            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                '[COLOR red][' + sHost + '][/COLOR] ' + title,
                '',
                thumbnail,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)  # dialog

        gui.setEndOfDirectory()  # ferme l'affichage


def showHosters():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    # on decrypte le seul lien present
    cConfig().showInfo('Decryptage', 'Please wait 10s')
    aResult = _DecryptProtectStream(sUrl)

    if (aResult):

        sHosterUrl = str(aResult)

        oHoster = HosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            HosterGui().showHoster(gui, oHoster, sHosterUrl, thumbnail)

    gui.setEndOfDirectory()
