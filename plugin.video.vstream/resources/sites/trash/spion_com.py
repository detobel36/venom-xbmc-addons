# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Par jojotango
from resources.lib.comaddon import dialog
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False


SITE_IDENTIFIER = 'spion_com'
SITE_NAME = 'Spi0n'
SITE_DESC = 'Insolite du web'

URL_MAIN = "https://www.spi0n.com/"

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN + 'page/1/', 'showMovies')
NETS_GENRES = (True, 'showGenres')

# True : Contenu Censuré | False : Contenu Non Censuré
SPION_CENSURE = True

# logo censure -18ans
LOGO_CSA = 'http://a398.idata.over-blog.com/1/40/34/11/archives/0/16588469.jpg'


def showCensure():

    content = 'Pour activer le contenu (+18) mettre: \n[COLOR coral]SPION_CENSURE = False[/COLOR]\ndans le fichier:\n[COLOR coral]plugin.video.vstream/resources/sites/spion_com.py[/COLOR]'
    dialog().VSok(content)


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    sSearchText = gui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Actualité', URL_MAIN + 'category/actualite/'])
    liste.append(['Animaux', URL_MAIN + 'category/animaux/'])
    liste.append(['Art', URL_MAIN + 'category/art-technique/'])
    liste.append(['Danse', URL_MAIN + 'category/danse/'])
    liste.append(['Expérience', URL_MAIN + 'category/experiences/'])
    liste.append(['Fake', URL_MAIN + 'category/fake-trucage/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre-militaire/'])
    liste.append(['Humour', URL_MAIN + 'category/humour-comedie/'])
    liste.append(['Internet', URL_MAIN + 'category/siteweb-internet/'])
    liste.append(['Jeux Vidéo', URL_MAIN + 'category/jeuxvideo-consoles/'])
    liste.append(['Musique', URL_MAIN + 'category/musique/'])
    liste.append(['Non Classé', URL_MAIN + 'category/non-classe/'])
    liste.append(['Owned', URL_MAIN + 'category/owned/'])
    liste.append(['Pub', URL_MAIN + 'category/publicite-marque/'])
    liste.append(['Rewind', URL_MAIN + 'category/rewind/'])
    liste.append(['Santé', URL_MAIN + 'category/sante-corps/'])
    liste.append(['Sport', URL_MAIN + 'category/sport/'])
    liste.append(['Technologie', URL_MAIN +
                  'category/technologie-innovations/'])
    liste.append(['Transport', URL_MAIN + 'category/auto-transport/'])
    liste.append(['TV & Cinéma', URL_MAIN + 'category/tv-cinema/'])
    liste.append(['WTF?!', URL_MAIN + 'category/wtf/'])
    liste.append(['Zapping', URL_MAIN + 'category/zapping-web/'])

    if (SPION_CENSURE == False):
        liste.append(['NSFW (+18)', URL_MAIN + 'nsfw/'])
        liste.append(['Trash (+18)', URL_MAIN + 'category/trash-gore/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:
        output_parameter_handler.addParameter('siteUrl', sUrl)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        sUrl = input_parameter_handler.getValue('siteUrl')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')

    sPattern = 'id="(post-[0-9]+)".+?src="([^"]+?)".+?href="([^"]+?)" rel="bookmark" title="([^"]+?)".+?title="([^"]+)'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            sPoster = aEntry[1]
            sUrlp = aEntry[2]
            title = aEntry[3]

            # categorie video
            sCat = aEntry[4]

            # vire lien categorie image
            if (sCat != 'Image'):

                output_parameter_handler.addParameter('siteUrl', sUrlp)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('sThumb', sPoster)

                if (SPION_CENSURE):
                    if (sCat == 'NSFW') or (sCat == 'Trash'):
                        sPoster = LOGO_CSA
                        gui.addMisc(
                            SITE_IDENTIFIER,
                            'showCensure',
                            title,
                            '',
                            sPoster,
                            '',
                            output_parameter_handler)
                    else:
                        gui.addMisc(
                            SITE_IDENTIFIER,
                            'showHosters',
                            title,
                            '',
                            sPoster,
                            '',
                            output_parameter_handler)
                else:
                    gui.addMisc(
                        SITE_IDENTIFIER,
                        'showHosters',
                        title,
                        '',
                        sPoster,
                        '',
                        output_parameter_handler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

    if not sSearch:
        gui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = Parser()
    sPattern = '<div class="nav-previous"><a href="([^"<>]+/[0-9]/?[^"]+)" class="nq_previous">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace(
        '<iframe src="//www.facebook.com/',
        '') .replace(
        '<iframe src=\'http://creative.rev2pub.com',
        '') .replace(
            'dai.ly',
            'www.dailymotion.com/video') .replace(
                'youtu.be/',
        'www.youtube.com/watch?v=')
    oParser = Parser()

    # prise en compte lien direct mp4
    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        sPattern = '<div class="video_tabs"><a href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Certains URL "dailymotion" sont écrits: //www.dailymotion.com
            if sHosterUrl[:4] != 'http':
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = HosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
