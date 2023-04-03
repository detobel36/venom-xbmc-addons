# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Par jojotango

import re
import random

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager, VSlog
from resources.lib.config import GestionCookie
from resources.lib.util import Unquote

SITE_IDENTIFIER = 'neuf_docu'
SITE_NAME = '9Docu'
SITE_DESC = 'Site pour Telecharger ou Regarder des Documentaires et Emissions TV Gratuitement'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_GENRES = (True, 'showGenres')
DOC_DOCS = ('http://', 'load')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'


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

    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Nouveautés',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', DOC_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_GENRES[1],
        'Genres',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['[COLOR gold]CATEGORIES[/COLOR]', ''])
    liste.append(['Séries Documentaires', URL_MAIN +
                 'categorie/series-documentaires/'])
    liste.append(['Documentaires Exclus', URL_MAIN +
                 'categorie/documentaires-exclus/'])
    liste.append(['Documentaires Inédits', URL_MAIN +
                 'categorie/documentaires-inedits/'])
    liste.append(['Films Documentaires', URL_MAIN +
                 'categorie/films-documentaires/'])
    liste.append(['Emissions Documentaires / Replay TV',
                  URL_MAIN + 'categorie/emissions-documentaires-replay-tv/'])

    liste.append(['[COLOR gold]GENRES[/COLOR]', ''])
    liste.append(['Actualités', URL_MAIN + 'categorie/actualites/'])
    liste.append(['Animaux', URL_MAIN + 'categorie/animaux/'])
    liste.append(['Architecture', URL_MAIN + 'categorie/architecture/'])
    liste.append(['Art martiaux', URL_MAIN + 'categorie/art-martiaux/'])
    liste.append(['Arts', URL_MAIN + 'categorie/arts/'])
    liste.append(['Auto/Moto', URL_MAIN + 'categorie/auto-moto/'])
    liste.append(['Aventure', URL_MAIN + 'categorie/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'categorie/biopic/'])
    liste.append(['Cinéma/Film', URL_MAIN + 'categorie/cinema-film/'])
    liste.append(['Civilisation', URL_MAIN + 'categorie/civilisation/'])
    liste.append(['Consommation', URL_MAIN + 'categorie/consommation/'])
    liste.append(['Cuisine', URL_MAIN + 'categorie/cuisine/'])
    liste.append(['Culture/Littérature', URL_MAIN +
                 'categorie/culturelitterature/'])
    liste.append(['Divertissement', URL_MAIN + 'categorie/divertissement/'])
    liste.append(['Economie', URL_MAIN + 'categorie/economie/'])
    liste.append(['Education', URL_MAIN + 'categorie/education/'])
    liste.append(['Emission TV', URL_MAIN + 'categorie/emission/'])
    liste.append(['Emploi/Métier', URL_MAIN + 'categorie/emploi-metier/'])
    liste.append(['Enquète', URL_MAIN + 'categorie/enquete/'])
    liste.append(['Environnement', URL_MAIN + 'categorie/environnement/'])
    liste.append(['Espionnage', URL_MAIN + 'categorie/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'categorie/famille/'])
    liste.append(['Guerre', URL_MAIN + 'categorie/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'categorie/histoire/'])
    liste.append(['Humour', URL_MAIN + 'categorie/humour/'])
    liste.append(['Investigations', URL_MAIN + 'categorie/investigations/'])
    liste.append(['Jeux vidéo/TV', URL_MAIN + 'categorie/jeux-video-tv/'])
    liste.append(['Justice/Criminalité', URL_MAIN +
                 'categorie/justice-criminalite/'])
    liste.append(['Magazine', URL_MAIN + 'categorie/magazine/'])
    liste.append(['Médias', URL_MAIN + 'categorie/medias/'])
    liste.append(['Mode', URL_MAIN + 'categorie/mode/'])
    liste.append(['Musique', URL_MAIN + 'categorie/musique/'])
    liste.append(['Nature', URL_MAIN + 'categorie/nature/'])
    liste.append(['People', URL_MAIN + 'categorie/people/'])
    liste.append(['Politique', URL_MAIN + 'categorie/politique/'])
    liste.append(['Religion', URL_MAIN + 'categorie/religion/'])
    liste.append(['Reportage', URL_MAIN + 'categorie/reportage/'])
    liste.append(['Santé/Bien-etre', URL_MAIN + 'categorie/sante-bien-etre/'])
    liste.append(['Science/Technologie', URL_MAIN +
                 'categorie/science-technologie/'])
    liste.append(['Sexualité', URL_MAIN + 'categorie/sexualite/'])
    liste.append(['Société', URL_MAIN + 'categorie/societe/'])
    liste.append(['Sport/Football/Auto/Moto', URL_MAIN +
                 'categorie/sport-football-auto-moto/'])
    liste.append(['Téléréalite', URL_MAIN + 'categorie/telerealite/'])
    liste.append(['Tourisme', URL_MAIN + 'categorie/tourisme/'])
    liste.append(['Voyage/Decouverte', URL_MAIN +
                 'categorie/voyage-decouverte/'])

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
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        url = search.replace(' ', '+')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'class="attachment-medium.+?" data-src="([^"]+)".+?<a href="([^"<]+)"[^<>]+>([^<>]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[0]
            url = entry[1]
            title = entry[2]

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMisc(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'doc.png',
                thumb,
                '',
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    parser = Parser()
    pattern = 'role=\'navigation\'.+?class=\'pages\'>Page.+?sur ([^<]+).+?rel="next" href="([^"]+)">»'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        VSlog(next_page)
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a href="([^"]+)" title=".+?".+?</a>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            if "clictune" in entry:
                request_handler = RequestHandler(entry)
                html_content = request_handler.request()

                pattern = 'txt = \'<b><a href="([^"]+)"'
                results = parser.parse(html_content, pattern)[1][0]
                entry = Unquote(re.search('url=(.+?)&', results).group(1))

            if "ReviveLink" in entry:
                url2 = 'http://' + (entry.split('/')
                                    [2]).lower() + '/qcap/Qaptcha.jquery.php'
                idUrl = entry.split('/')[3]

                # Make random key
                s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@"
                RandomKey = ''.join(random.choice(s) for i in range(32))

                request_handler = RequestHandler(url2)
                request_handler.setRequestType(1)
                request_handler.addHeaderEntry('Host', 'revivelink.com')
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Accept', 'application/json, text/javascript, */*; q=0.01')
                request_handler.addHeaderEntry(
                    'Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
                request_handler.addHeaderEntry('Referer', entry)
                request_handler.addHeaderEntry(
                    'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                request_handler.addHeaderEntry(
                    'X-Requested-With', 'XMLHttpRequest')
                request_handler.addParameters('action', 'qaptcha')
                request_handler.addParameters('qaptcha_key', RandomKey)

                html_content = request_handler.request()

                cookies = request_handler.GetCookies()
                GestionCookie().SaveCookie('revivelink.com', cookies)
                # VSlog('result' + html_content)

                if '"error":false' not in html_content:
                    VSlog('Captcha rate')
                    VSlog(html_content)
                    return

                cookies = GestionCookie().Readcookie('revivelink.com')
                request_handler = RequestHandler(
                    'http://revivelink.com/slinks.php?R=' + idUrl + '&' + RandomKey)
                request_handler.addHeaderEntry('Host', 'revivelink.com')
                request_handler.addHeaderEntry('Referer', entry)
                request_handler.addHeaderEntry(
                    'Accept', 'application/json, text/javascript, */*; q=0.01')
                request_handler.addHeaderEntry('User-Agent', UA)
                request_handler.addHeaderEntry(
                    'Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
                request_handler.addHeaderEntry(
                    'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                request_handler.addHeaderEntry(
                    'X-Requested-With', 'XMLHttpRequest')
                request_handler.addHeaderEntry('Cookie', cookies)

                html_content = request_handler.request()

                result = re.findall(
                    '<td><a href="([^"]+)" title=\'([^<]+)\'>',
                    html_content)
                for url, title in result:
                    hoster_url = url
                    hoster = HosterGui().checkHoster(hoster_url)
                    if hoster:
                        hoster.setDisplayName(title)
                        hoster.setFileName(title)
                        HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                               input_parameter_handler=input_parameter_handler)
            else:

                hoster_url = entry
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
