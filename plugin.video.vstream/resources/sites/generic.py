# Ce fichier permet de parser les informations contenue dans n'importe quel site.
# Le but est de pouvoir écrire dans une configuration tous ce qu'il faut pour parser un site web.

from resources.lib.gui.gui import cGui
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler

from resources.sites.generic.generic import Generic

SITE_IDENTIFIER = 'generic'
SITE_NAME = 'Source générique'  # nom que KODI affiche
SITE_DESC = 'Regroupement de plusieurs sites.'

# Fausse URL
URL_MAIN = 'http://google.com/'
# Ici l'URL n'est pas important. C'est ce fichier qui va directement gérer les appels sur base d'un fichier
# de configuration. Seul l'appel aux bonnes fonction compte

# Fall back URL lorsqu'aucune recherche spécifique n'est disponible
URL_SEARCH = ('', 'search')

# Call lorsque l'on fait: Streaming > Movies > Search (Movie)
# Call lorsque l'on fait: Streaming > Search > Search (Movie)
URL_SEARCH_MOVIES = ('', 'searchMovies')
URL_SEARCH_SERIES = ('', 'searchSeries')

FUNCTION_SEARCH = 'search'

generic = Generic()


def load():
    """
    Affiche le menu lorsque l'on charge cette source.

    A priori pour l'instant rien n'a affiché. On verra plus tard
    """
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Dans load', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def searchMovies(search=''):
    """
    Appelé lorsque l'on veut faire une recherche d'un film ou (j'ai pas trouvé l'autre usage)
    """
    list_movies = generic.search_movie()

    oGui = cGui()  # ouvre l'affichage
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('generic_url', 'https://youtube.com')
    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', 'Dans searchMovies (' + search + ')', '', 'search.png', '', oOutputParameterHandler)

def searchSeries(search=''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    """
    'sMovieTitle', 'sYear', 'sThumb'
    """
    oGui.addTV(SITE_IDENTIFIER, 'showSeason', 'Dans searchSeries (' + search + ')', 'search.png', oOutputParameterHandler)

def search(search = ''):
    """
    Appelé lorsque l'on fait une recherche générale (pas un film ou une série ou un autre type).
    Je n'ai pas réussi à trouver un scénario ou cette méthode est appelée
    """
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showHosters', 'Pas encore implémenté (code d\'erreur dans le code #1)', 'search.png', oOutputParameterHandler)

def showHosters():

    oInputParameterHandler = cInputParameterHandler()
    url = oInputParameterHandler.getValue('generic_url')

    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Dans show Hosters (url: ' + str(url) + ')', 'search.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showSeason():
    pass

def showEpisode():
    pass

def _getGenericParameters(oInputParameterHandler):
    params = oInputParameterHandler.getAllParameter()
    return {key: val for key, val in params.items() if key.startswith('generic_')}
