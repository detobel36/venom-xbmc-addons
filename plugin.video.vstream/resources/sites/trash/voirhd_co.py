# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# S09 update 02/11/2020
from resources.lib.comaddon import Progress
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import re
return False  # 0212020 Site HS depuis plus de 1 moi

SITE_IDENTIFIER = 'voirhd_co'
SITE_NAME = 'Voir HD'
SITE_DESC = 'Films et Series en streaming hd'

URL_MAIN = 'https://voirhd.co/'
# use -1.html instead of .html
MOVIE_MOVIE = (URL_MAIN + 'films-1.html', 'showMovies')

# add tags in URL_MAIN       : Home page site :
tbox = '#box'                # Film Box Office
tmoviestend = '#moviestend'  # Tendance Films
tlastmovie = '#lastmovie'    # Dernier Films ajoutés
tseriestend = '#seriestend'  # Tendance Series
tlastvf = '#lastvf'          # Derniers episodes vf Ajouté # épisode pas de desc : normal
tlastvost = '#lastvost'      # Derniers episodes VOSTFR Ajoute  #
# recherche : key pour différencier le type de recherche
key_search_movies = '#search_movies_#'
key_search_series = '#search_series_#'
# recherche globale
URL_SEARCH = (URL_MAIN + 'rechercher-', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')
# recherche interne
MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')
# genre : movies et series (pas de difference) on indique film ou serie
# dans le resultat
MOVIE_GENRES = (True, 'showGenres')

MOVIE_TOP = (URL_MAIN + tbox, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + tmoviestend, 'showMovies')
MOVIE_NEWS = (URL_MAIN + tlastmovie, 'showMovies')

SERIE_VIEWS = (URL_MAIN + tseriestend, 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-1.html',
                'showMovies')  # or https://voirhd.co/serie
SERIE_NEWS_EPISODE_VF = (URL_MAIN + tlastvf, 'showMovies')
SERIE_NEWS_EPISODE_VOST = (URL_MAIN + tlastvost, 'showMovies')

URL_IMAGE_VF = 'https://voirhd.co/image/vf.png'
URL_IMAGE_VOST = 'https://voirhd.co/image/vostfr.png'


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

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films & Series (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMoviesMenu',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSeriesMenu',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMoviesMenu():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_MOVIES[1],
        'Recherche Films ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_TOP[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_TOP[1],
        'Films (Box Office)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_VIEWS[1],
        'Films (Les plus populaires)',
        'films.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesMenu():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MY_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MY_SEARCH_SERIES[1],
        'Recherche Series ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VIEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VIEWS[1],
        'Séries (Les plus populaires)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS_EPISODE_VF[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_EPISODE_VF[1],
        'Séries (Derniers Episodes VF)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', SERIE_NEWS_EPISODE_VOST[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS_EPISODE_VOST[1],
        'Séries (Derniers Episodes VOST)',
        'series.png',
        output_parameter_handler)
    gui.setEndOfDirectory()


def MyshowSearchSerie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        # search_text.replace(' ', '-') recherche plus précise mais plus
        # risquée
        url = URL_SEARCH[0] + key_search_series + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + key_search_movies + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


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
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    # bug sur le site:les options genres ne marchent pas
    # on fait une recheche par mot clef genre  pour la recherche
    # URL_MAIN+'recherche-'+ mot_saisie_ds_recherche_site + '-0.html'
    # ** url2g :'-0' pour valider la premiere requete  RequestHandlerGenre
    # result RequestHandlerGenre : '-1' neccessaire apres pour le next page

    liste = []
    listegenre = [
        'Action',
        'Animation',
        'aventure',
        'Biopic',
        'Comedie',
        'Comedie-musicale',
        'Documentaire',
        'Drame',
        'Epouvante-horreur',
        'Famille',
        'Fantastique',
        'Guerre',
        'Policier',
        'Romance',
        'Science-fiction',
        'Thriller']

    url1g = URL_MAIN + 'recherche-'
    url2g = '-0.html'  # **

    for igenre in listegenre:
        liste.append([igenre, url1g + igenre + url2g])

    for title, url in liste:
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def RequestHandlerSearch(searchs):
    parser = Parser()
    pattern = 'voirhd.co.rechercher-([^ ]*)'
    results = parser.parse(searchs, pattern)
    html_content = ''
    if results[0]:
        ssearch = results[1][0]
    else:
        return False, html_content, 'Erreur'

    sCookies = 'PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'
    request_handler = RequestHandler(req2)
    request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    request_handler.addParameters('Search', ssearch)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Cookie', sCookies)
    html_content = request_handler.request()

    if not html_content:
        return False, html_content, 'Erreur de requete'

    if ssearch in html_content:  # on degrossi en  gros pour eviter de parser des resultats
        return True, html_content, ' Requete ok'
    else:
        return False, html_content, 'Recherche : Aucun resultat'


def RequestHandlerGenre(searchs):

    parser = Parser()
    pattern = 'recherche-([^-]*)'
    results = parser.parse(searchs, pattern)

    if results[0]:
        ssearch = results[1][0]
    else:
        return False, 'none'

    sCookies = 'PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'
    request_handler = RequestHandler(req2)
    request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
    request_handler.addParameters('Search', ssearch)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Cookie', sCookies)
    html_content = request_handler.request()
    return True, html_content


def showMovies(search=''):
    gui = Gui()

    bSearchMovie = False
    bSearchSerie = False
    if search:
        url = search
        if key_search_movies in url:
            url = str(url).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in url:
            url = str(url).replace(key_search_series, '')
            bSearchSerie = True
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    pattern = 'class="short-images-link".+?img src="([^"]+)".+?short-link"><a href="([^"]+)".+?>([^<]+)</a>'
    # pattern home page
    # 2 etapes /ou utiliser s=s[s.find(start):s.find(end))
    if url == URL_MAIN + tbox:  # etape 1/2
        pattern = 'Film Box Office.*?Tendance Films'  # < 5ms regex101
    if url == URL_MAIN + tmoviestend:  # etape 1/2
        pattern = 'Tendance Films.+?Dernier Films ajout'
    if url == URL_MAIN + tseriestend:  # etape 1/2
        pattern = 'Tendance Series.+?start jaded serie'
    # normale ; 1 etape
    if url == URL_MAIN + tlastmovie:  # url  thumb title
        pattern = '<li class="TPostMv">.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]+)'
    if url == URL_MAIN + \
            tlastvf:  # url title ex 'max s1s2'  thumb flag https://voirhd.co/image/vf.png
        pattern = '<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vf.png'
    if url == URL_MAIN + tlastvost:
        pattern = '<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vostfr.png'
    # else home page
    if URL_MAIN + 'films' in url:
        # url quality  lang  thumb  title.replace('  ', '')
        pattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?Langhds.([^"]*).+?src="([^"]*).+?alt="([^"]*)'
    if URL_MAIN + 'serie' in url:
        # url   nbredesaison thumb title
        pattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'
    if URL_MAIN + 'recherche' in url:  # meme que serie mais a tester
        # url   nbredesaison thumb title
        pattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'

    if search:
        sbool, html_content, mes = RequestHandlerSearch(url)
        if not sbool:
            gui.addText(SITE_IDENTIFIER, mes)
            return

    elif URL_MAIN + 'recherche' in url:  # 1 seule RequestHandlerGenre() if  genre-0.html
        surl = str(url).replace('.html', '')
        snumber = re.search('([0-9]+)$', surl).group(1)
        if snumber == '0':
            sbool, html_content = RequestHandlerGenre(url)
            # genre-0.html / genre-1.html l : '-1' need for next page
            url = surl.replace('0', '1.html')
        else:
            request_handler = RequestHandler(url)
            html_content = request_handler.request()
    else:
        request_handler = RequestHandler(url)
        html_content = request_handler.request()

    parser = Parser()
    results = parser.parse(html_content, pattern)
    if not results[0]:
        if (URL_MAIN + 'rechercher' in url) and '<div class="divrecher">' in html_content:
            gui.addText(SITE_IDENTIFIER, 'Recherche : Aucun resultat')
        # erreur interne qui peu etre cause par mauvais liens du site mais
        # aussi le programme
        elif '<title>404 Not Found</title>' in html_content:
            gui.addText(SITE_IDENTIFIER, ' request failed : ')
        else:
            gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        progress_1 = Progress().VScreate(SITE_NAME)
        bclosedprogress_1 = False

        for entry in results[1]:
            progress_1.VSupdate(progress_1, total)
            if progress_1.iscanceled():
                break

            qual = ''
            lang = ''
            url2 = ''
            title = ''
            thumb = ''
            # parse home page
            # etape 2/2
            if url == URL_MAIN + tbox or url == URL_MAIN + \
                    tmoviestend or url == URL_MAIN + tseriestend:
                progress_1.VSclose(progress_1)
                bclosedprogress_1 = True
                shtml = str(entry)
                # url2 thumb title
                sPattern1 = '<div class=.item.>.+?ref=.([^"]*).+?src=.([^"]*).+?alt=.([^"]+)'
                oParser2 = Parser()
                aResult2 = oParser2.parse(shtml, sPattern1)
                if (aResult2[0] == False):
                    gui.addText(SITE_IDENTIFIER)

                if (aResult2[0]):
                    total = len(aResult2[1])
                    progress_2 = Progress().VScreate(SITE_NAME)

                    for entry in aResult2[1]:
                        progress_2.VSupdate(progress_2, total)
                        if progress_2.iscanceled():
                            break

                        url2 = entry[0]
                        thumb = entry[1]
                        title = entry[2]
                        if thumb.startswith('poster'):
                            thumb = URL_MAIN + thumb

                        output_parameter_handler = OutputParameterHandler()
                        output_parameter_handler.addParameter('site_url', url2)
                        output_parameter_handler.addParameter(
                            'movie_title', title)
                        output_parameter_handler.addParameter('thumb', thumb)
                        output_parameter_handler.addParameter('lang', lang)
                        output_parameter_handler.addParameter('qual', qual)
                        if URL_MAIN + 'serie' in url2:
                            gui.addTV(
                                SITE_IDENTIFIER,
                                'showSaisons',
                                title,
                                'series.png',
                                thumb,
                                '',
                                output_parameter_handler)
                        else:
                            gui.addMovie(
                                SITE_IDENTIFIER,
                                'showLink',
                                title,
                                'films.png',
                                thumb,
                                '',
                                output_parameter_handler)

                    progress_2.VSclose(progress_2)

                gui.setEndOfDirectory()
                return

            if url == URL_MAIN + tlastmovie:  # url  thumb title
                url2 = entry[0]
                thumb = entry[1]
                title = entry[2]
                display_title = title

            if url == URL_MAIN + \
                    tlastvf:  # url title ex 'the lost S1E1'  thumb flag https://voirhd.co/image/vf.png
                url2 = entry[0]
                thumb = URL_IMAGE_VF
                title = str(entry[1]).replace('  ', '') + ' (VF)'
                display_title = title

            if url == URL_MAIN + tlastvost:
                url2 = entry[0]
                thumb = URL_IMAGE_VOST
                title = str(entry[1]).replace('  ', '') + ' (VOST)'
                display_title = title

            # else no home page
            if URL_MAIN + \
                    'films' in url:  # url quality  lang  thumb  title.replace('  ', '')
                url2 = entry[0]
                title = str(entry[4]).replace('  ', '')
                thumb = entry[3]
                qual = entry[1]
                lang = entry[2]
                display_title = title

            if URL_MAIN + 'serie' in url:  # url   nbredesaison thumb title
                tagsaison = entry[1]
                if '1' in tagsaison:
                    tagsaison = tagsaison.replace('Saisons', 'Saison')
                url2 = entry[0]
                title = entry[3]
                thumb = entry[2]
                display_title = title + ' [' + tagsaison + ']'

            if URL_MAIN + 'recherche' in url:  # url   qualit thumb title
                url2 = entry[0]
                title = entry[3]
                thumb = entry[2]
                # display_title = title + ' [' + entry[1] + ']' non use
                if 'serie' in url2:
                    display_title = title + \
                        ' : Serie ' + '[' + entry[1] + ']'
                else:
                    display_title = title + ' : Film ' + '[' + entry[1] + ']'

            if bSearchMovie:
                if 'serie' in url2:
                    continue
                else:
                    display_title = display_title.replace(': Film ', '')

            if bSearchSerie:
                if 'films' in url2:
                    continue
                else:
                    display_title = display_title.replace(': Serie ', '')

            thumb = thumb.replace(' ', '%20')
            if thumb.startswith('poster'):
                thumb = URL_MAIN + thumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('lang', lang)
            output_parameter_handler.addParameter('qual', qual)

            if (URL_MAIN + 'serie' in url2) and url != URL_MAIN + \
                    tlastvf and url != URL_MAIN + tlastvost:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            elif url == URL_MAIN + tlastvf or url == URL_MAIN + tlastvost:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    'serie.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLink',
                    display_title,
                    'films.png',
                    thumb,
                    '',
                    output_parameter_handler)

        if not bclosedprogress_1:
            progress_1.VSclose(progress_1)

    if not search:
        bNextPage, urlnext, number, numbermax = __checkForNextPage(
            html_content, url)
        if (bNextPage):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', urlnext)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Page ' +
                number +
                '/' +
                numbermax +
                ' >>>[/COLOR]',
                output_parameter_handler)
        gui.setEndOfDirectory()


def __checkForNextPage(html_content, url):

    inumbermax = 0
    if URL_MAIN + 'films' in url:
        pattern = 'voirhd.co.films-([\\d]*).html'
    elif URL_MAIN + 'serie' in url:
        pattern = 'voirhd.co.serie-([\\d]*).html'
    elif URL_MAIN + 'recherche' in url:
        pattern = 'voirhd.co.recherche-.+?-([\\d]*).html'
    elif '#' in url:
        # normal url == URL_MAIN+ #tag pas besoin de page suivante
        return False, 'none', 'none', 'none'
    else:
        return False, 'none', 'none', 'none'

    parser = Parser()
    results = parser.parse(html_content, pattern)
    if not results[0]:
        return False, 'none', 'none', 'none'
    if results[0]:
        for entry in results[1]:
            snumber = str(entry)
            try:
                intnumber = int(snumber)
                if intnumber > inumbermax:
                    inumbermax = intnumber
            except BaseException:
                pass
        snumbermax = str(inumbermax)

    surl = str(url).replace('.html', '')
    snumber = re.search('([0-9]+)$', surl).group(1)

    if snumber != '0':
        inumber = int(snumber)
        inewnumber = inumber + 1
        if inewnumber > inumbermax:
            return False, 'none', 'none', 'none'
        snewnumber = str(inewnumber)
        snewnumber_html = snewnumber + '.html'
        # genre-0.html / genre-1.html l : same result req need for next page
        sUrlnext = surl.replace(snumber, snewnumber_html)
        return True, sUrlnext, snewnumber, snumbermax

    return False, 'none', 'none', 'none'


def showSaisons():

    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    desc = ''
    qual = ''
    year = ''
    desc, qual, year = GetHtmlInfo(desc, qual, year, html_content)

    # url  saisontitle ex   href="serie + (-Norsemen-saison-3-1598.html)
    # (Norsemen saison 3)
    pattern = 'div class="col-sm-3.+?href="serie([^"]*).+?<div class="serietitre">.*?<span>([^<]*)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in reversed(results[1]):
            url2 = URL_MAIN + 'serie' + entry[0]
            # c'est tjrs le meme titre
            title = entry[1]
            sTitleDisplay = title

            if qual:
                sTitleDisplay = sTitleDisplay + ' [' + qual + ']'
            if year and year not in title:  # doublon (2020)
                sTitleDisplay = sTitleDisplay + ' (' + year + ')'

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)
            output_parameter_handler.addParameter('year', year)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'ShowEpisodes',
                sTitleDisplay,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def ShowEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    desc = input_parameter_handler.getValue('desc')
    thumb = input_parameter_handler.getValue('thumb')
    qual = input_parameter_handler.getValue('qual')
    year = input_parameter_handler.getValue('year')
    movie_title = input_parameter_handler.getValue(
        'movie_title')  # contient num saison

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # url numeroEpisode
    pattern = 'streaming" href=".([^"]*).*?right"><.span>([^<]*)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:
            url2 = entry[0]
            sTitleDisplay = movie_title + ' Episode' + \
                entry[1]  # saison en odre drecroissant
            if qual:
                sTitleDisplay = sTitleDisplay + ' [' + qual + ']'
            if year and year not in movie_title:
                sTitleDisplay = sTitleDisplay + ' (' + year + ')'
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('qual', qual)
            output_parameter_handler.addParameter('year', year)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLink',
                sTitleDisplay,
                '',
                thumb,
                desc,
                output_parameter_handler)
    gui.setEndOfDirectory()


def showLink():

    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')
    lang = input_parameter_handler.getValue('lang')
    qual = input_parameter_handler.getValue('qual')
    year = input_parameter_handler.getValue('year')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    if (thumb):
        if thumb == URL_IMAGE_VF or thumb == URL_IMAGE_VOST:
            try:
                thumb = URL_MAIN + \
                    re.search('class="postere.+?.+?src="([^"]*)', html_content).group(1)
            except BaseException:
                pass

    desc, qual, year = GetHtmlInfo(desc, qual, year, html_content)

    b_ADD_MENU_VF = True
    b_ADD_MENU_VOSTFR = True
    b_ADD_MENU_DL = True

    iposVF = str(html_content).find('class="typevf">VF </h3>')
    if iposVF > 0:
        b_ADD_MENU_VF = False

    iposVOSTFR = str(html_content).find('class="typevf">VOSTFR')
    if iposVOSTFR > 0:
        b_ADD_MENU_VOSTFR = False

    iposDL = str(html_content).find('liens telechargement</a>')
    if iposDL > 0:
        b_ADD_MENU_DL = False

    pattern = '<button.+?lectt.+?src="([^"]*)"style="'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        if '<title>404 Not Found</title>' in html_content:  # erreur interne du site sur lien donnée par hd.co
            gui.addText(
                SITE_IDENTIFIER,
                ' request failed : voirhd.co no update is database')
        elif iposVF == -1 or iposVOSTFR == -1:  # index DL tjrs trouvé
            gui.addText(
                SITE_IDENTIFIER,
                'Aucun lien trouvé pour ' +
                movie_title)
        else:
            gui.addText(SITE_IDENTIFIER)

    if results[0]:
        for entry in results[1]:
            url = str(entry)

            if 'rapidgator.net' in url or 'filerio' in url:  # pas de hoster premium
                continue

            url2 = url.replace('.html.html', '.html')
            shosturl = url2.replace('www.', '')  # https://www.flashx.pw/
            try:  # http and https
                host = re.search('http.*?\\/\\/([^.]*)', shosturl).group(1)
                host = host.upper()
            except BaseException:
                host = url2
                pass

            sTitleDisplay = movie_title
            if qual:
                sTitleDisplay = sTitleDisplay + ' [' + qual + ']'
            if lang:
                sTitleDisplay = sTitleDisplay + ' (' + lang.upper() + ')'
            if year and year not in movie_title:
                sTitleDisplay = sTitleDisplay + ' (' + year + ')'
            sTitleDisplay = '%s  [COLOR coral]%s[/COLOR]' % (
                sTitleDisplay, host)

            iposurl = str(html_content).find(url2 .replace('.html', ''))
            if iposurl == -1:
                pass
            if not b_ADD_MENU_VF:
                if iposurl > iposVF:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR skyblue]STREAMING VF : [/COLOR]')
                    b_ADD_MENU_VF = True
            if not b_ADD_MENU_VOSTFR:
                if iposurl > iposVOSTFR:
                    gui.addText(SITE_IDENTIFIER,
                                '[COLOR skyblue]STREAMING VOSTFR : [/COLOR]')
                    b_ADD_MENU_VOSTFR = True
            if not b_ADD_MENU_DL:
                if iposurl > iposDL:
                    gui.addText(
                        SITE_IDENTIFIER,
                        '[COLOR skyblue]LIENS DE TELECHARGEMENT : [/COLOR]')
                    b_ADD_MENU_DL = True

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('refUrl', url)
            output_parameter_handler.addParameter('url', url2)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addLink(
                SITE_IDENTIFIER,
                'showHosters',
                sTitleDisplay,
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    hoster = HosterGui().checkHoster(url)
    if (hoster):
        hoster.setDisplayName(movie_title)
        hoster.setFileName(movie_title)
        HosterGui().showHoster(gui, hoster, url, thumb)
    # else:
        # gui.addText(SITE_IDENTIFIER, 'Host inconnu ' + url)
    gui.setEndOfDirectory()


def GetHtmlInfo(desc, qual, year, html_content):
    parser = Parser()

    if (not desc):
        desc = ''  # ne sert a rien ? mais on est sure pas d'erreur return
        pattern = 'fsynopsis.+?<p>([^<]*)<.p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = str(results[1][0]).replace('  ', '')
    if (not qual):
        qual = ''
        pattern = 'finfo-title">Qualité.*?title.+?streaming">([^<]*)<.a'
        results = parser.parse(html_content, pattern)
        if results[0]:
            qual = str(results[1][0])
    if (not year):
        year = ''
        pattern = 'Année.+?voirhd.co.recherche-([\\d]*)'
        results = parser.parse(html_content, pattern)
        if results[0]:
            year = str(results[1][0])

    return desc, qual, year
