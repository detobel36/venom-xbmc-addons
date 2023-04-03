# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import HosterGui  # systeme de recherche pour l'hote
from resources.lib.gui.gui import Gui  # systeme d'affichage pour xbmc
# entree des parametres
from resources.lib.handler.inputParameterHandler import InputParameterHandler
# sortie des parametres
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler  # requete url
from resources.lib.parser import Parser  # recherche de code
from resources.lib.comaddon import Progress  # , VSlog
# from resources.lib.util import cUtil #outils pouvant etre utiles


# 11/12/17 le site fonctionne mais pas regarder.

# identifant (nom de votre fichier) remplacez les espaces et les . par _
# AUCUN CARACTERE SPECIAL
SITE_IDENTIFIER = 'otakufr_com'
SITE_NAME = 'otakufr.com'  # nom que xbmc affiche
# description courte de votre source
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite'

URL_MAIN = 'http://otakufr.com/'  # url de votre source

# definis les url pour les catégories principale, ceci est automatique, si
# la definition est présente elle seras affichee.
URL_SEARCH = ('http://www.otakufr.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


ANIM_NEWS = (URL_MAIN + 'latest-episodes/', 'showMovies')  # anime nouveautés
ANIM_ANIMS = (URL_MAIN + 'anime-list-all/', 'showMovies2')  # anime vrac


def load():  # fonction chargee automatiquement par l'addon l'index de votre navigation.
    gui = Gui()  # ouvre l'affichage

    # apelle la function pour sortir un parametre
    output_parameter_handler = OutputParameterHandler()
    # sortie du parametres site_url n'oubliez pas la Majuscule
    output_parameter_handler.addParameter('site_url', 'site_url')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)
    # Ajoute lien dossier (identifant, function a attendre, nom, icon, parametre de sortie)
    # Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on
    # veut dans le parametre site_url

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_NEWS[1],
        'Animes Nouveautés',
        'news.png',
        output_parameter_handler)
    # ici la function showMovies a besoin d'une url ici le racourci MOVIE_NEWS

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ANIMS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ANIMS[1],
        'Animes liste complete',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()  # ferme l'affichage


def showSearch():  # function de recherche
    gui = Gui()

    search_text = gui.showKeyBoard()  # apelle le clavier xbmx
    if (search_text):
        url = URL_SEARCH[0] + search_text  # modifi l'url de recherche
        # apelle la function qui pouras lire la page de resultats
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()  # ouvre l'affichage
    if search:  # si une url et envoyer directement grace a la function showSearch
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue(
            'site_url')  # recupere l'url sortie en parametre

    request_handler = RequestHandler(url)  # envoye une requete a l'url
    html_content = request_handler.request()  # requete aussi

    html_content = html_content.replace(
        '<span class="likeThis">', '').replace(
        '</span>', '')
    # la function replace et pratique pour supprimer un code du resultat

    pattern = '<a href="([^"]+)" class="anm" title="([^"]+)">[^<]+<\\/a>.+?<img src="([^"]+)"'
    # pour faire simple recherche ce bout de code dans le code source de l'url
    # - ([^<]+) je veut cette partie de code mais y a une suite
    # - .+? je ne veut pas cette partis et peux importe ceux qu'elle contient
    # - (.+?) je veut cette partis et c'est la fin

    parser = Parser()
    results = parser.parse(html_content, pattern)
    # le plus simple et de faire un print results
    # dans le fichier log d'xbmc vous pourez voir un array de ce que recupere le script
    # et modifier pattern si besoin

    # xbmc.log(str(results)) #Commenter ou supprimer cette ligne une foix fini

    if results[0]:
        total = len(results[1])
        # dialog barre de progression
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # L'array affiche vos info dans l'orde de pattern en commencant a
            # 0
            title = entry[1]
            url = entry[0]
            Sthumb = entry[2]

            Sthumb = 'http:' + Sthumb

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter(
                'site_url', url)  # sortie de l'url
            output_parameter_handler.addParameter(
                'movie_title', title)  # sortie du titre
            output_parameter_handler.addParameter(
                'thumbnail', Sthumb)  # sortie du poster

            gui.addTV(
                SITE_IDENTIFIER,
                'seriesListEpisodes',
                title,
                '',
                Sthumb,
                '',
                output_parameter_handler)

            # il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            # la difference et pour les metadonner serie, films ou sans

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(
            html_content)  # cherche la page suivante
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                'next.png',
                output_parameter_handler)
            # Ajoute une entree pour le lien Next | pas de addMisc pas de
            # poster et de description inutile donc

    if not search:
        gui.setEndOfDirectory()  # ferme l'affichage


def showMovies2(search=''):
    gui = Gui()
    if search:
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = '<li><a href="([^<]+)" title="([^<]+)" rel="([^<]+)" class="anm_det_pop">([^<]+)</a></li>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', str(entry[0]))
            output_parameter_handler.addParameter(
                'movie_title', str(entry[1]))
            if 'type2=1' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    entry[1],
                    'series.png',
                    '',
                    '',
                    output_parameter_handler)
            else:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'seriesHosters',
                    entry[1],
                    'animes.png',
                    '',
                    '',
                    output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):  # cherche la page suivante
    parser = Parser()
    pattern = '<li><a href="([^<]+)">Suivant</a></li>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        return results[1][0]

    return False


def showHosters():  # recherche et affiche les hotes
    gui = Gui()  # ouvre l'affichage
    input_parameter_handler = InputParameterHandler()  # apelle l'entree de paramettre
    url = input_parameter_handler.getValue('site_url')  # apelle site_url
    movie_title = input_parameter_handler.getValue(
        'movie_title')  # apelle le titre
    thumbnail = input_parameter_handler.getValue(
        'thumbnail')  # apelle le poster

    request_handler = RequestHandler(url)  # requete sur l'url
    html_content = request_handler.request()  # requete sur l'url
    html_content = html_content.replace(
        '<iframe src="//www.facebook.com/',
        '').replace(
        '<iframe src=\'http://creative.rev2pub.com',
        '')
    # supprimer a l'aide de replace toute les entrer qui corresponde a votre
    # recherche mais ne doivent pas etre pris en compte

    parser = Parser()
    pattern = '<iframe.+?src="(.+?)"'
    # ici nous cherchont toute les sources iframe
    results = parser.parse(html_content, pattern)
    # penser a faire un print results pour verifier

    # si un lien ne s'affiche pas peux etre que l'hote n'est pas supporte par
    # l'addon
    if results[0]:
        for entry in results[1]:

            hoster_url = str(entry[0])
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(entry[1])
                hoster.setFileName(entry[1])
                HosterGui().showHoster(gui, hoster, hoster_url, thumbnail)

    gui.setEndOfDirectory()  # fin


def seriesListEpisodes():  # cherche les episode de series
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumbnail = input_parameter_handler.getValue('thumbnail')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # pattern = '<option value="([0-9]+)">([^<]+)<\/option>'
    pattern = '<a class="lst" href="([^"]+)" title="([^"]+)"><b class="val">'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    # fh = open('c:\\test.txt', "w")
    # fh.write(html_content)
    # fh.close()

    # VSlog(str(results))

    if results[0]:
        for entry in results[1]:

            title = entry[1]
            url2 = entry[0]

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                'series.png',
                '',
                '',
                output_parameter_handler)

    gui.setEndOfDirectory()
