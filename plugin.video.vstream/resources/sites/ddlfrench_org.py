#-*- coding: utf-8 -*-
#Zombi.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'ddlfrench_org'
SITE_NAME = 'ddlfrench.org'
SITE_DESC = 'TOP REPLAY TV'

URL_MAIN = 'http://ddlfrench.org/'

REPLAYTV_NEWS = ('http://ddlfrench.org/', 'showMovies')

REPLAYTV_REPLAYTV = ('http://', 'load')

REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = ('http://ddlfrench.org/index.php?story={)', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'REPLAY TV', 'films.png', oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'REPLAY TV par chaine', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://ddlfrench.org/index.php?story={'+sSearchText+'}&do=search&subaction=search'  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["TF1","http://ddlfrench.org/tf1"] )
    liste.append( ["France2","http://ddlfrench.org/france2"] )
    liste.append( ["France3","http://ddlfrench.org/france3"] )
    liste.append( ["France4","http://ddlfrench.org/france4"] )
    liste.append( ["France5","http://ddlfrench.org/france5"] )
    liste.append( ["FranceO","http://ddlfrench.org/franceo"] )
    liste.append( ["ARTE","http://ddlfrench.org/arte"] )
    liste.append( ["M6","http://ddlfrench.org/m6"] )
    liste.append( ["CANAL+","http://ddlfrench.org/canal-plus"] )
    liste.append( ["D8","http://ddlfrench.org/d8"] )
    liste.append( ["W9","http://ddlfrench.org/w9"] )
    liste.append( ["TMC","http://ddlfrench.org/tmc"] )
    liste.append( ["NT1","http://ddlfrench.org/nt1"] )
    liste.append( ["NRJ12","http://ddlfrench.org/nrj12"] )
    liste.append( ["RMC DECOUVERTE","http://ddlfrench.org/rmc-decouverte"] )
    liste.append( ["TNT CANALSAT","http://ddlfrench.org/tnt-canalsat"] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
   
    oParser = cParser()
    #sPattern = "<div class='mediathumb'>.*?<a href='([^<]+)' title='([^<]+)'>.*?<img src='([^<]+)' alt='(.+?)'>.*?</a>"
    sPattern = '<article class="shortstory cf"> <a href="([^<]+)" class="short_post post_img"> <img src="([^<]+)"> </a> <div class="short_post_content"> <h2 class="short_title"><a href=".*?" title="([^<]+)">.*?</a></h2> <div class="short_views">([^<]+)</div> </div></article>'
    sPattern = sPattern + '|' + 'class="hblock cf"> <h4>([^<]+)</h4>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    Saison = '0'

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[4]:
               Saison = 'Top Replay Tv'
               oOutputParameterHandler = cOutputParameterHandler()
               oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
               oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
               oGui.addMisc(SITE_IDENTIFIER, 'showHosters', '[COLOR red]'+ Saison + '[/COLOR]', 'series.png', '', aEntry[2], oOutputParameterHandler)

            else:
                sTitle = aEntry[2]
                sUrl= str(aEntry[1])
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
                oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'doc.png', aEntry[1], aEntry[3], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'class="next"><a href="(.+?)">SUIVANT</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
    oParser = cParser()
               
        
    sPattern = '<b>(.+?)2016<br/><a' 
    sPattern = sPattern + '|' + '>E(.+?)<br'
    sPattern = sPattern + '|' + 'target="_blank">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]'+ aEntry[0] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)
                        
            elif aEntry[1]:
                 oOutputParameterHandler = cOutputParameterHandler()
                 oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]E'+ aEntry[1] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)

            elif aEntry[2]:
                 sHosterUrl = str(aEntry[2])
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle)
                     oHoster.setFileName(sMovieTitle)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    
