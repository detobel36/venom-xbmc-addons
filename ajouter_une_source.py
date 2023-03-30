# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.gui.hoster import HosterGui  # systeme de recherche pour l'hôte
from resources.lib.gui.gui import Gui  # systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import InputParameterHandler  # entree des parametres
from resources.lib.handler.outputParameterHandler import OutputParameterHandler  # sortie des parametres
from resources.lib.handler.requestHandler import RequestHandler  # requête url
from resources.lib.parser import Parser  # recherche de code
from resources.lib.comaddon import Progress, VSlog  # import du dialog Progress

# from resources.lib.util import cUtil # outils pouvant être utiles

# Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous KODI

SITE_IDENTIFIER = 'ajouter_une_source'  # identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'ajouter_une_source'  # nom que KODI affiche
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent' # description courte de votre source

URL_MAIN = 'http://le_site.org/'  # url de la source

# definit les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
# LA RECHERCHE GLOBAL N'UTILISE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
# recherche global films
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')  # filtre uniquement les films pour la recherche
# recherche global serie
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')  # filtre uniquement les séries pour la recherche
# recherche global manga
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')  # filtre uniquement les animes pour la recherche
# recherche global drama
URL_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')  # filtre uniquement les dramas pour la recherche
# recherche global divers
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

# menu films existant dans l'accueil (Home)
MOVIE_MOVIE = ('http://', 'showMenuMovies')  # films (sous menu)
MOVIE_NEWS = (URL_MAIN, 'showMovies')  # films (derniers ajouts = trie par date)
MOVIE_HD = (URL_MAIN + 'url', 'showMovies')  # films HD
MOVIE_VIEWS = (URL_MAIN + 'url', 'showMovies')  # films (les plus vus = populaire)
MOVIE_COMMENTS = (URL_MAIN + 'url', 'showMovies')  # films (les plus commentés) (pas afficher sur HOME)
MOVIE_NOTES = (URL_MAIN + 'url', 'showMovies')  # films (les mieux notés)
MOVIE_GENRES = (True, 'showGenres')  # films genres
MOVIE_ANNEES = (True, 'showMovieYears')  # films (par années)
# menu supplementaire non gerer par l'accueil
MOVIE_VF = (URL_MAIN + 'url', 'showMovies')  # films VF
MOVIE_VOSTFR = (URL_MAIN + 'url', 'showMovies')  # films VOSTFR

# menu serie existant dans l'accueil (Home)
SERIE_SERIES = ('http://', 'showMenuTvShows')  # séries (sous menu)
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')  # news.png ou series.png | séries (derniers ajouts = trie par date)
SERIE_VIEWS = (URL_MAIN + 'url', 'showMovies')  # views.png | series (les plus vus = populaire)
SERIE_HD = (URL_MAIN + 'series/', 'showMovies')  # hd.png | séries HD
SERIE_GENRES = (True, 'showGenres')  # séries genres
SERIE_ANNEES = (True, 'showSerieYears')  # séries (par années)
SERIE_VFS = (URL_MAIN + 'series/', 'showMovies')  # séries VF
SERIE_VOSTFRS = (URL_MAIN + 'series/', 'showMovies')  # séries Vostfr


# menu animes existant dans l'accueil (Home)
ANIM_ANIMS = ('http://', 'showMenuAnims')  # animés (sous menu)
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')  # animés (derniers ajouts = trie par date)
ANIM_VIEWS = (URL_MAIN + 'url', 'showMovies')  # views.png #animés (les plus vus = populaire)
ANIM_GENRES = (True, 'showGenres')  # anime genres
ANIM_ANNEES = (True, 'showAnimesYears')  # anime (par années)
ANIM_VFS = (URL_MAIN + 'animes', 'showMovies')  # animés VF
ANIM_VOSTFRS = (URL_MAIN + 'animes', 'showMovies')  # animés VOSTFR
ANIM_ENFANTS = (URL_MAIN + 'animes', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')  # Documentaire
DOC_DOCS = ('http://', 'load')  # Documentaire Load
DOC_GENRES = (True, 'showGenres')  # Documentaires Genres

SPORT_SPORTS = (URL_MAIN + 'url', 'showMovies')  # sport
SPORT_LIVE = (URL_MAIN + 'live', 'showMovies')  # lien vers la page des directs
SPORT_GENRES = (URL_MAIN + 'genres', 'showGenres')  # lien vers la page des genres

REPLAYTV_REPLAYTV = ('http://', 'load')  # Replay load
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')  # Replay trie par date
REPLAYTV_GENRES = (True, 'showGenres')  # Replay Genre


def load():  # fonction chargée automatiquement par l'addon, acceuil de la source.
    gui = Gui()  # ouvre l'affichage

    output_parameter_handler = OutputParameterHandler()  # appelle la fonction pour sortir un paramètre
    output_parameter_handler.addParameter('siteUrl', 'http://venom/')  # sortie du parametres siteUrl n'oubliez pas la Majuscule
    gui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', output_parameter_handler)
    # Ajoute lien dossier (identifant, function a attendre, nom, icone, paramètre de sortie)
    # Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on veut dans le paramètre siteUrl

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)
    # ici la function showMovies a besoin d'une url ici le raccourci MOVIE_NEWS

    output_parameter_handler.addParameter('siteUrl', MOVIE_MOVIE[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)
    # showGenres n'a pas besoin d'une url pour cette méthode

    output_parameter_handler.addParameter('siteUrl', MOVIE_ANNEES[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VIEWS[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NOTES[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_SERIES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_ANNEES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF) ', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', output_parameter_handler)

    # Menu SPORTS si disponible
    output_parameter_handler.addParameter('siteUrl', SPORT_LIVE[0])
    gui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Les sports (En direct)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SPORT_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Les sports (Genres)', 'sport.png', output_parameter_handler)

    # fin des menus
    gui.setEndOfDirectory()  # ferme l'affichage


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    gui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', MOVIE_VF[0])
    gui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VFS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    gui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuAnims():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    gui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Animés ', 'search.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_NEWS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_GENRES[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'series.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VFS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', output_parameter_handler)

    output_parameter_handler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    gui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():  # fonction de recherche
    gui = Gui()

    sSearchText = gui.showKeyBoard()  # appelle le clavier xbmc
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText  # modifie l'url de recherche
        showMovies(sUrl)  # appelle la fonction qui pourra lire la page de resultats
        gui.setEndOfDirectory()
        return


def showGenres():  # affiche les genres
    gui = Gui()

    # juste à entrer les categories et les liens qui vont bien
    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Animation', URL_MAIN + 'animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Biopic', URL_MAIN + 'biopic/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', URL_MAIN + 'comedie-musicale/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'])
    liste.append(['Erotique', URL_MAIN + 'erotique'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage/'])
    liste.append(['Famille', URL_MAIN + 'famille/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Historique', URL_MAIN + 'historique/'])
    liste.append(['Musical', URL_MAIN + 'musical/'])
    liste.append(['Policier', URL_MAIN + 'policier/'])
    liste.append(['Péplum', URL_MAIN + 'peplum/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Spectacle', URL_MAIN + 'spectacle/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])
    liste.append(['Divers', URL_MAIN + 'divers/'])

    output_parameter_handler = OutputParameterHandler()
    for title, sUrl in liste:  # boucle
        output_parameter_handler.addParameter('siteUrl', sUrl) # sortie de l'url en paramètre
        gui.addDir(SITE_IDENTIFIER, 'showMovies', title, 'genres.png', output_parameter_handler)
        # ajouter un dossier vers la fonction showMovies avec le titre de chaque categorie.

    gui.setEndOfDirectory()


def showMovieYears():  # creer une liste inversée d'annees
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1913, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        gui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showSerieYears():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(1936, 2021)):
        Year = str(i)
        output_parameter_handler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        gui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(sSearch=''):
    gui = Gui()  # ouvre l'affichage

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')  # recupere l'url sortie en paramètre
    if sSearch:  # si une url et envoyer directement grace a la fonction showSearch
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = RequestHandler(sUrl)  # envoye une requête a l'url
    sHtmlContent = oRequestHandler.request()  # requête aussi

    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>', '')
    # la fonction replace est pratique pour supprimer un code du resultat

    sPattern = 'class="movie movie-block"><img src="([^"]+).+?title="([^"]+).+?onclick="window.location.href=\'([^"]+).+?style="color:#F29000">.+?<div.+?>(.+?)</div'
    """
    Pour faire simple recherche ce bout de code dans le code source de l'url
    - "([^"]+)" je veux cette partie de code qui se trouve entre guillemets mais pas de guillemets dans la chaine
    - .+? je ne veux pas cette partie et peux importe ceux qu'elle contient
    - >(.+?)< je veux cette partie de code qui se trouve entre > et < mais il peut y avoir n'inporte quoi entre les 2.
    - (https*://[^"]) je veux l'adresse qui commence par https ou http jusqu'au prochain guillemet.
    Pour tester vos Regex, vous pouvez utiliser le site https://regex101.com/ en mettant dans les modifiers "gmis"
    """
    
    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    # Le plus simple est de faire un VSlog(str(aResult)),
    # dans le fichier log de Kodi vous pourrez voir un array de ce que recupere le script
    # et modifier sPattern si besoin
    VSlog(str(aResult))  # Commenter ou supprimer cette ligne une fois fini

    # affiche une information si aucun resulat
    if not aResult[0]:
        gui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        # dialog barre de progression
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            # dialog update
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # L'array affiche vos info dans l'ordre de sPattern en commencant a 0, attention dans ce cas la on recupere 6 information
            # Mais selon votre regex il ne peut y en avoir que 2 ou 3.
            sThumb = aEntry[0]
            title = aEntry[1]
            sUrl2 = aEntry[2]
            sLang = aEntry[3]
            sQual = aEntry[4]
            sHoster = aEntry[5]
            desc = ''

            title = title.replace('En streaming', '')

            # Si vous avez des informations dans aEntry Qualitée lang organiser un peux vos titre exemple.
            # Si vous pouvez la langue et la Qualite en MAJ ".upper()" vostfr.upper() = VOSTFR
            title = ('%s [%s] (%s) [COLOR coral]%s[/COLOR]') % (title, sQual, sLang.upper(), sHoster)
            # mettre les informations de streaming entre [] et le reste entre () vStream s'occupe de la couleur automatiquement.

            # Utile si les liens recupere ne commencent pas par (http://www.nomdusite.com/)
            # sUrl2 = URL_MAIN + sUrl2

            output_parameter_handler.addParameter('siteUrl', sUrl2)  # sortie de l'url
            output_parameter_handler.addParameter('sMovieTitle', title)  # sortie du titre
            output_parameter_handler.addParameter('sThumb', sThumb)  # sortie du poster
            output_parameter_handler.addParameter('desc', desc)  # sortie de la description
            output_parameter_handler.addParameter('referer', sUrl)  # URL d'origine, parfois utile comme référence

            if '/series' in sUrl:
                gui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', title, '', sThumb, desc, output_parameter_handler)
                # addTV pour sortir les series tv (identifiant, fonction, titre, icon, poster, description, sortie paramètre)
            elif '/animes' in sUrl:
                gui.addAnime(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', title, '', sThumb, desc, output_parameter_handler)
                # addAnime pour sortir les series animés (mangas) (identifiant, fonction, titre, icon, poster, description, sortie paramètre)
            else:
                gui.addMovie(SITE_IDENTIFIER, 'showHosters', title, '', sThumb, desc, output_parameter_handler)
                # addMovies pour sortir les films (identifiant, fonction, titre, icon, poster, description, sortie paramètre)

            # Il existe aussi addMisc(identifiant, function, titre, icon, poster, description, sortie paramètre)
            # A utiliser pour les autres types, tels que : documentaires, spectacles, etc.
            # qui ne nécessitent pas de metadonnées (recherches de la description, de la bande annonces, des acteurs, etc.)

        progress_.VSclose(progress_)  # fin du dialog

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)  # cherche la page suivante
        if sNextPage:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            gui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sNumPage, output_parameter_handler)
            # Si pas de numero de page dans l'url du nextPage, utiliser la ligne suivante et désactiver les 2 précédentes
            # gui.addNext(SITE_IDENTIFIER, 'showMovies', Suivant, output_parameter_handler)
            # Ajoute une entree pour le lien Suivant | pas de addMisc pas de poster et de description inutile donc

        gui.setEndOfDirectory()  # ferme l'affichage


def __checkForNextPage(sHtmlContent):  # cherche la page suivante
    oParser = Parser()
    sPattern = '<div class="navigation".+? <span.+? <a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():  # recherche et affiche les hôtes
    gui = Gui()  # ouvre l'affichage
    input_parameter_handler = InputParameterHandler()  # apelle l'entree de paramètre
    sUrl = input_parameter_handler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')  # appelle le titre
    sThumb = input_parameter_handler.getValue('sThumb')  # appelle le poster
    referer = input_parameter_handler.getValue('referer')  # récupère l'URL appelante

    oRequestHandler = RequestHandler(sUrl)  # requête sur l'url
    oRequestHandler.addHeaderEntry('Referer', referer)  # paramètre pour passer l'URL appelante (n'est pas forcement necessaire)
    sHtmlContent = oRequestHandler.request()  # requête sur l'url

    oParser = Parser()
    sPattern = '<iframe.+?src="([^"]+)"'
    # ici, nous cherchons toutes les sources iframe

    aResult = oParser.parse(sHtmlContent, sPattern)
    # pensez a faire un VSlog(str(aResult)) pour verifier

    # si un lien ne s'affiche pas, peut-être que l'hôte n'est pas supporté par l'addon
    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = HosterGui().checkHoster(sHosterUrl)  # recherche l'hôte dans l'addon
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)  # nom affiche
                oHoster.setFileName(sMovieTitle)  # idem
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)
                # affiche le lien (gui, oHoster, url du lien, poster)

    gui.setEndOfDirectory()  # fin


# Pour les series, il y a généralement une étape en plus pour la selection des episodes ou saisons.
def ShowSerieSaisonEpisodes():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sThumb = input_parameter_handler.getValue('sThumb')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    desc = input_parameter_handler.getValue('desc')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Pattern servant à retrouver les éléments dans la page
    sPattern = '?????????????????????'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = Progress().VScreate(SITE_NAME)

        output_parameter_handler = OutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            title = sMovieTitle + aEntry[0]
            sUrl2 = aEntry[1]

            output_parameter_handler.addParameter('siteUrl', sUrl2)
            output_parameter_handler.addParameter('sMovieTitle', title)
            output_parameter_handler.addParameter('sThumb', sThumb)

            gui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', title, 'series.png', sThumb, desc, output_parameter_handler)
            # il y a aussi addAnime pour les mangas
            # gui.addAnime(SITE_IDENTIFIER, 'seriesHosters', title, 'animes.png', sThumb, desc, output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def seriesHosters():  # cherche les episodes de series
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    sUrl = input_parameter_handler.getValue('siteUrl')
    sMovieTitle = input_parameter_handler.getValue('sMovieTitle')
    sThumb = input_parameter_handler.getValue('sThumb')

    oRequestHandler = RequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Exemple de pattern à changer
    sPattern = '<dd><a href="([^<]+)" class="zoombox.+?" title="(.+?)"><button class="btn">.+?</button></a></dd>'

    oParser = Parser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            oHoster = HosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(aEntry[1])
                HosterGui().showHoster(gui, oHoster, sHosterUrl, sThumb)

    gui.setEndOfDirectory()

# n'hesitez pas à poser vos questions et même à partager vos sources.
