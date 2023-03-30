# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto et Arias800 02/06/2019
import re

from resources.lib.comaddon import addon, isMatrix, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'animeultime'
SITE_NAME = 'Anime Ultime'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

URL_SEARCH_DRAMAS = (URL_MAIN + 'search-0-1+', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'search-0-1+', 'showSeries')

ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_ANNEES = (True, 'ShowYearsAnimes')
ANIM_GENRES = (True, 'ShowGenreAnimes')
ANIM_ALPHA = (True, 'ShowAlphaAnimes')

DRAMA_DRAMAS = (True, 'showMenuDramas')
DRAMA_ANNEES = (True, 'ShowYearsDramas')
DRAMA_GENRES = (True, 'ShowGenreDramas')
DRAMA_ALPHA = (True, 'ShowAlphaDramas')

TOKUSATSU_TOKUSATSUS = (True, 'showMenuTokusatsu')
TOKUSATSU = (URL_MAIN + 'series-0-1/tokusatsu/0---', 'showSeries')
TOKUSATSU_ALPHA = ('true', 'ShowAlphaTokusatsu')

adulteContent = addon().getSetting('contenu_adulte')


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_DRAMAS[1],
        'Dramas',
        'dramas.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', TOKUSATSU_TOKUSATSUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU_TOKUSATSUS[1],
        'Tokusatsu',
        'films.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnimes():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', ANIM_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ALPHA[1],
        'Animés  (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_GENRES[1],
        'Animés (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANNEES[1],
        'Animés (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuDramas():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', DRAMA_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_ALPHA[1],
        'Dramas (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_GENRES[1],
        'Dramas (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', DRAMA_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DRAMA_ANNEES[1],
        'Dramas (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTokusatsu():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', TOKUSATSU[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU[1],
        'Tokusatsu',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', TOKUSATSU_ALPHA[0])
    gui.addDir(
        SITE_IDENTIFIER,
        TOKUSATSU_ALPHA[1],
        'Tokusatsu (Ordre alphabétique)',
        'az.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def loadTypelist(typemovie, typelist):
    # typelist genre ou year
    # <select name="genre"
    # <select name="year"
    sUrl = URL_MAIN + 'series-0-1/' + typemovie

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = Parser()

    sPattern = '<select name="([^"]+)|<option value=\'([^\']+).*?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    list_typelist = {}

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                if aEntry[0] == typelist:
                    bfind = True
                else:
                    bfind = False

            if bfind and aEntry[1]:
                if not isMatrix():
                    title = aEntry[2].decode('iso-8859-1').encode('utf8')
                else:
                    title = aEntry[2]
                title = title.replace('e', 'E').strip()
                list_typelist[title] = aEntry[1]

    list_typelist = sorted(
        list_typelist.items(),
        key=lambda typeList: typeList[0])

    return list_typelist


def ShowGenreAnimes():
    ShowGenre('anime')


def ShowGenreDramas():
    ShowGenre('drama')


def ShowGenre(typemovie):
    gui = Gui()
    list_listgenre = loadTypelist(typemovie, 'genre')
    output_parameter_handler = OutputParameterHandler()
    for ilist in list_listgenre:
        url = URL_MAIN + 'series-0-1/' + typemovie + '/-' + ilist[1] + '---'
        title = ilist[0].title()
        output_parameter_handler.addParameter('siteUrl', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowYearsAnimes():
    ShowYears('anime')


def ShowYearsDramas():
    ShowYears('drama')


def ShowYears(typemovie):
    gui = Gui()
    list_year = loadTypelist(typemovie, 'year')
    # http://www.anime-ultime.net/series-0-1/anime/--626--    2019
    output_parameter_handler = OutputParameterHandler()
    for liste in reversed(list_year):
        url = URL_MAIN + 'series-0-1/' + typemovie + '/--' + liste[1] + '--'
        title = liste[0]
        output_parameter_handler.addParameter('siteUrl', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            title,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def ShowAlphaAnimes():
    ShowAlpha('anime')


def ShowAlphaDramas():
    ShowAlpha('drama')


def ShowAlphaTokusatsu():
    ShowAlpha('tokusatsu')


def ShowAlpha(typemovie):
    gui = Gui()

    import string
    # http://www.anime-ultime.net/series-0-1/tokusatsu/c---
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = [['#', URL_MAIN + 'series-0-1/' + typemovie + '/' + '1---']]
    for alpha in listalpha:
        liste.append([str(alpha).upper(), URL_MAIN +
                     'series-0-1/' + typemovie + '/' + alpha + '---'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            'Lettre [COLOR coral]' +
            title +
            '[/COLOR]',
            'listes.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    sSearchText = gui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showSeries(sUrl)
        gui.setEndOfDirectory()
        return


def showSeries(sSearch=''):
    gui = Gui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_DRAMAS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    if sSearch:
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=.+?img=([^>]+)\\/>.+?onMouseOut.+?>(.+?)<\\/a>.+?<td class="" align="center">([^<]+)<'
    else:
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=([^>]+)\\/>.+?alt="([^"]+).+?align="center">([^<]+)<'

    aResult = oParser.parse(sHtmlContent, sPattern)

    # Si il y a qu'un seule resultat alors le site fait une redirection.
    if not aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        if sSearch and "sultats anime" not in sHtmlContent:
            title = ''
            try:
                title = re.search('<h1>([^<]+)', sHtmlContent).group(1)
            except BaseException:
                pass
            if title:
                sUrl2 = sUrl
                sThumb = ''

                # Enleve le contenu pour adultes.
                if 'Public Averti' in title or 'Interdit' in title:
                    if adulteContent == "false":
                        gui.addText(
                            SITE_IDENTIFIER,
                            '[COLOR red]Contenu pour adultes désactivé[/COLOR]')
                        return

                output_parameter_handler.addParameter('siteUrl', sUrl2)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sThumb)

                if '/anime/' in sUrl:
                    gui.addAnime(
                        SITE_IDENTIFIER,
                        'showEpisode',
                        title,
                        '',
                        sThumb,
                        '',
                        output_parameter_handler)
                else:
                    gui.addDrama(
                        SITE_IDENTIFIER,
                        'showEpisode',
                        title,
                        '',
                        sThumb,
                        '',
                        output_parameter_handler)

            else:
                gui.addText(SITE_IDENTIFIER)
        else:
            gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry[2]
            if sSearch:
                # Enleve les balise.
                try:
                    title = re.sub('<.*?>', '', title)
                except BaseException:
                    pass

            try:
                title = title.decode('iso-8859-1').encode('utf8')
            except BaseException:
                pass

            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = aEntry[1]

            if adulteContent == "false":
                # Enleve le contenu pour adulte.
                if 'Public Averti' in title or 'Interdit' in title:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, title):
                    continue

            sType = aEntry[3].strip()
            title += ' [%s]' % sType

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if sType != 'Episode':
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            elif '/anime/' in sUrl:
                gui.addAnime(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addDrama(
                    SITE_IDENTIFIER,
                    'showEpisode',
                    title,
                    '',
                    sThumb,
                    '',
                    output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def showEpisode():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = Parser()
    desc = ''
    try:
        sPattern = 'src="images.+?(?:<br />)(.+?)(?:<span style|TITRE ORIGINAL|ANNÉE DE PRODUCTION|STUDIO|GENRES)'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            desc = aResult[1][0].replace('<br>', '').replace('<br />', '')
            desc = desc.replace(
                'Synopsis',
                '').replace(
                'synopsis',
                '').replace(
                ':',
                ' ')
            desc = ('[I][COLOR coral]%s[/COLOR][/I] %s') % ('Synopsis :', desc)

            # Enleve les balises.
            try:
                desc = re.sub('<.*?>', '', desc)
            except BaseException:
                pass
    except BaseException:
        pass

    sPattern = '<tr.+?align="left">.+?align="left">([^"]+)</td>.+?nowrap>+?<.+?</td>.+?<.+?/td>.+?<.+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry[0]
            try:
                title = title.decode('iso-8859-1').encode('utf8')
            except BaseException:
                pass

            sLang = ''
            if ' vostfr' in title:
                sLang = 'VOSTFR'
            if ' vf' in title:
                sLang = 'VF'
            title = aEntry[0].replace(
                '[',
                '').replace(
                ']',
                '').replace(
                'FHD',
                '').replace(
                'vostfr',
                '').replace(
                    'vf',
                    '').replace(
                        'HD',
                        '').replace(
                            'HQ',
                '').strip()
            if '(saison' in title:
                title = title.replace('(', '').replace(')', '')
            sEpisode = title.split(' ')[-1]
            title = title.replace(sEpisode, ' Episode ' + sEpisode).strip()
            sDisplayTtitle = title + ' [' + sLang + ']'

            sUrl2 = URL_MAIN + aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sLang', sLang)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                sDisplayTtitle,
                '',
                sThumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    oParser = Parser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="stream">Streaming <span itemprop="name">([^<]+)<.+?thumbnailUrl" content="([^\"]+)".+?contentURL" content="([^\"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            title = aEntry[0].strip()
            if ' vostfr' in title:
                sLang = 'VOSTFR'
            if ' vf' in title:
                sLang = 'VF'
            title = ('%s - [%s]') % (sMovieTitle, sLang)

            sThumb = aEntry[1]
            sHosterUrl = aEntry[2]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(title)
                oHoster.setFileName(title)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
