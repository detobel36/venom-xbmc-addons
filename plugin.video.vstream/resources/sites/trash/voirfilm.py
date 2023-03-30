# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre nom ou pseudo
# Site avec que openload et souvent sans aucun lien.
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False

SITE_IDENTIFIER = 'voirfilm'
SITE_NAME = 'Voir Film'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'http://www.voirfilm.bz/'

URL_SEARCH = (URL_MAIN + 'engine/ajax/search.php', 'showMoviesSearch')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMoviesSearch'

MOVIE_NEWS = (URL_MAIN + 'films-a-laffiche/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'url', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_YEARS = (True, 'showMovieYears')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')


def load():
    oGui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MOVIE_YEARS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_YEARS[1], 'Films (Par Années)', 'annees.png', output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = Gui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        showMoviesSearch(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Animation', URL_MAIN + 'films-animation/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Crime', URL_MAIN + 'crime/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'])
    liste.append(['Famille', URL_MAIN + 'famille/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Historique', URL_MAIN + 'films-historique/'])
    liste.append(['Musical', URL_MAIN + 'musique/'])
    liste.append(['Mystère', URL_MAIN + 'mystere/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Sport', URL_MAIN + 'sport/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])

    for sTitle, sUrl in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = Gui()

    for i in reversed(xrange(1913, 2019)):
        Year = str(i)
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + '/xfsearch/year/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    oGui.setEndOfDirectory()


def showMoviesSearch(sSearch):
    oGui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(URL_MAIN)
    oRequestHandler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addHeaderEntry('User-Agent',
                                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0')
    oRequestHandler.addParameters('do', 'search')
    oRequestHandler.addParameters('subaction', 'search')
    oRequestHandler.addParameters('story', sSearch)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="mov-i img-box">\\s*<img src="([^"]+)" title="([^"]+)".+?data-link="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[2]
            sThumb = URL_MAIN[:-1] + aEntry[0]

            sTitle = sTitle.replace(' voirfilm streaming', '')

            sDisplayTitle = sTitle

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if 'Saison' in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = Gui()
    if sSearch:
        sUrl = sSearch
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'series/' in sUrl:
        sPattern = '<div class="mov clearfix">\\s*<div class="mov-i img-box">\\s*<img src="(.+?)" title="(.+?)voirfilm streaming.+?>\\s*<div class="mov-mask flex-col ps-link" data-link="(.+?)"><span class="fa fa-play"></span></div>\\s*<div class="mov-m"><b><a href=".+?">(.+?)</a> - <a href=".+?">(.+?)</a> - <a href=".+?">(.+?)</a></b></div>'
    else:
        sPattern = '<div class="mov clearfix">\\s*<div class="mov-i img-box">\\s*<img src="(.+?)" title="(.+?)voirfilm streaming.+?>\\s*<div class="mov-mask flex-col ps-link" data-link="(.+?)"><span class="fa fa-play"></span></div>\\s*<div class="mov-m"><b><a href=".+?">(.+?)</a> - <a href=".+?">(.+?)</a></b></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = str(aEntry[0])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            if 'series' in sUrl:
                sLang = str(aEntry[4])
                sQual = str(aEntry[5])
                sUrl2 = str(aEntry[2])
                sTitle = str(aEntry[1]) + str(aEntry[3])
            else:
                sLang = str(aEntry[3])
                sQual = str(aEntry[4])
                sUrl2 = str(aEntry[2])
                sTitle = str(aEntry[1])
            sDesc = ''

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', sTitle)
            output_parameter_handler.addParameter('sThumb', sThumb)

            if 'Saison' in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, output_parameter_handler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', output_parameter_handler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="navigation"><span>.+?</span> <a href="(.+?)">.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def seriesHosters():
    i = 0
    oGui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            i = i + 1
            sHosterUrl = str(aEntry)
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle + 'Episode' + str(i))
                oHoster.setFileName(sMovieTitle + 'Episode' + str(i))
                HosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
