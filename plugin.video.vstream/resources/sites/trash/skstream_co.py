# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# le 04/03/20
from resources.lib.comaddon import progress  # ,VSlog
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False


SITE_IDENTIFIER = 'skstream_co'
SITE_NAME = 'Skstream'
SITE_DESC = 'Films & Séries'

URL_MAIN = 'https://www.skstream.to/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = ('http://films', 'showMenuMovies')
MOVIE_GENRES = (URL_MAIN + 'film/', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'film/date-', 'showYears')
MOVIE_PAYS = (URL_MAIN + 'film/', 'showPays')

SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')
SERIE_SERIES = ('http://series', 'showMenuSeries')
SERIE_GENRES = (URL_MAIN + 'serie/', 'showGenres')
SERIE_ANNEES = (URL_MAIN + 'serie/date-', 'showYears')
SERIE_PAYS = (URL_MAIN + 'serie/', 'showPays')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'search?Search=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'lang.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Séries (Par Pays)', 'lang.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')  # + '&_token=5Z4MWpyCQOERtMOYGRVUKwr8LzQvH1ktwVeAVqpi'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'genre-Action'])
    liste.append(['Animation', sUrl + 'genre-Animation'])
    liste.append(['Arts Martiaux', sUrl + 'genre-Art_Martiaux'])
    liste.append(['Aventure', sUrl + 'genre-Aventure'])
    liste.append(['Biopic', sUrl + 'genre-Biopic'])
    liste.append(['Comédie', sUrl + 'genre-Comedie'])
    liste.append(['Comédie Dramatique', sUrl + 'genre-Comedie_Dramatique'])
    liste.append(['Documentaire', sUrl + 'genre-Documentaire'])
    liste.append(['Drame', sUrl + 'genre-Drame'])
    liste.append(['Epouvante Horreur', sUrl + 'genre-Epouvante-Horreur'])
    liste.append(['Espionnage', sUrl + 'genre-Espionnage'])
    liste.append(['Famille', sUrl + 'genre-famille'])
    liste.append(['Fantastique', sUrl + 'genre-Fantastique'])
    liste.append(['Guerre', sUrl + 'genre-guerre'])
    liste.append(['Policier', sUrl + 'genre-Policier'])
    liste.append(['Romance', sUrl + 'genre-Romance'])
    liste.append(['Science Fiction', sUrl + 'genre-Science_Fiction'])
    liste.append(['Thriller', sUrl + 'genre-Thriller'])
    liste.append(['Western', sUrl + 'genre-Western'])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showPays():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    liste = []
    if 'film' in sUrl:  # films
        liste.append(['Américain', sUrl + 'nat-u.s.a'])
        liste.append(['Allemand', sUrl + 'nat-allemagne'])
        liste.append(['Belgique', sUrl + 'nat-belgique'])
        liste.append(['Bulgarie', sUrl + 'nat-bulgarie'])
        liste.append(['Britanique', sUrl + 'nat-u.k'])
        liste.append(['Canada', sUrl + 'nat-canada'])
        liste.append(['Chine', sUrl + 'nat-chine'])
        liste.append(['Danemark', sUrl + 'nat-danemark'])
        liste.append(['Français', sUrl + 'nat-france'])
        liste.append(['Japon', sUrl + 'nat-japan'])
        liste.append(['Norvégien', sUrl + 'nat-norvaege'])
        liste.append(['Russie', sUrl + 'nat-russie'])
    else:  # séries
        liste.append(['Américain', sUrl + 'nat-U.S.A'])
        liste.append(['Australie', sUrl + 'nat-Australie'])
        liste.append(['Britanique', sUrl + 'nat-Grande-Bretagne'])
        liste.append(['Espagne', sUrl + 'nat-Espagne'])
        liste.append(['Français', sUrl + 'nat-France'])
        liste.append(['Canada', sUrl + 'nat-Canada'])
        liste.append(['Russie', sUrl + 'nat-Russie'])
        liste.append(['Korean', sUrl + 'nat-KOREAN'])
        liste.append(['Allemagne', sUrl + 'nat-Allemagne'])
        liste.append(['Japon', sUrl + 'nat-Japon'])
        liste.append(['Turquie', sUrl + 'nat-Turquie'])
        # liste.append( ['Brésil', sUrl + 'nat-Br%C3%83%C2%A9sil'] )
        liste.append(['Belgique', sUrl + 'nat-belgique'])
        liste.append(['Danemark', sUrl + 'nat-danemark'])
        liste.append(['Norvégien', sUrl + 'nat-norvaege'])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    for i in reversed(range(1980, 2020)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', ('%s%s') % (sUrl, Year))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        sPattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)"[^<>]+ alt="([^"]+)"'

    elif '/film' in sUrl:
        sPattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)" title="([^"]+)".+?class="qual".+?<span>([^<]+)<.+?class="lang_img_poster".+?alt="([^"]+)"'
    else:
        sPattern = 'href="([^"]+)" class="hvr-shutter-out-horizontal".+?<img src="([^"]+)" title="([^"]+)"'

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sTitle = aEntry[2]
            sQual = ''
            sLang = ''
            if len(aEntry) > 3:
                sQual = aEntry[3]
                sLang = aEntry[4].upper()

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', output_parameter_handler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)" rel="next" aria-label="Next »"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSaisons():
    oGui = Gui()
    oParser = cParser()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = '<div class="details text-muted">([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('Ã©', 'é').replace('Â', 'â').replace('Ã', 'à')
    except BaseException:
        pass

    sPattern = 'w3l-movie-gride-agile">.+?<img src="([^"]+)".+?<h6><a href="([^"]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:

            sThumb = URL_MAIN[:-1] + aEntry[0]
            sUrl = aEntry[1]
            sTitle = sMovieTitle + ' ' + aEntry[2]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            output_parameter_handler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, output_parameter_handler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = Gui()
    oParser = cParser()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')
    sDesc = input_parameter_handler.getValue('sDesc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^"]+)" class="epi_box".+?<span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1].replace('Ep', 'episode') + sMovieTitle

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    if sUrl.endswith(' '):
        sUrl = sUrl[:-1]

    oRequest = RequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = "href='([^']+)' (?:|target=\"_blank\" )class=\"a_server"

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for sHosterUrl in aResult[1]:
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
