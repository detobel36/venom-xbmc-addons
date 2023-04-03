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
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_NEWS[1],
        'Vidéos (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', NETS_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        NETS_GENRES[1],
        'Vidéos (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + search_text
        showMovies(url)
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
    for title, url in liste:
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()

    if search:
        url = search.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace('<span class="likeThis">', '')

    pattern = 'id="(post-[0-9]+)".+?src="([^"]+?)".+?href="([^"]+?)" rel="bookmark" title="([^"]+?)".+?title="([^"]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            sPoster = entry[1]
            sUrlp = entry[2]
            title = entry[3]

            # categorie video
            cat = entry[4]

            # vire lien categorie image
            if (cat != 'Image'):

                output_parameter_handler.addParameter('site_url', sUrlp)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', sPoster)

                if (SPION_CENSURE):
                    if (cat == 'NSFW') or (cat == 'Trash'):
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

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            number = re.search('/page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + number,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = '<div class="nav-previous"><a href="([^"<>]+/[0-9]/?[^"]+)" class="nq_previous">'
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    html_content = html_content.replace(
        '<iframe src="//www.facebook.com/',
        '') .replace(
        '<iframe src=\'http://creative.rev2pub.com',
        '') .replace(
            'dai.ly',
            'www.dailymotion.com/video') .replace(
                'youtu.be/',
        'www.youtube.com/watch?v=')
    parser = Parser()

    # prise en compte lien direct mp4
    pattern = '<iframe.+?src="(.+?)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        pattern = '<div class="video_tabs"><a href="([^"]+)'
        results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry
            # Certains URL "dailymotion" sont écrits: //www.dailymotion.com
            if hoster_url[:4] != 'http':
                hoster_url = 'http:' + hoster_url

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
