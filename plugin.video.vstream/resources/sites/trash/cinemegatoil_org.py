# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# 07/05/20 mise en place recaptcha
from resources.lib.comaddon import Progress, dialog, VSlog
from resources.lib.recaptcha import ResolveCaptcha
from resources.lib.config import GestionCookie
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
import xbmcgui
import xbmc
import re
return False  # 07/03/2021


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'cinemegatoil_org'
SITE_NAME = 'CineMegaToil'
SITE_DESC = 'Films - Films HD'

URL_MAIN = 'https://www.cinemegatoil.org/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')
URL_SEARCH_MOVIES = (
    URL_MAIN +
    '?do=search&mode=advanced&subaction=search&titleonly=3&story=',
    'showMovies')


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

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if (search_text):
        url = search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action'])
    liste.append(['Animation', URL_MAIN + 'animation'])
    liste.append(['Arts-martiaux', URL_MAIN + 'arts-martiaux'])
    liste.append(['Aventure', URL_MAIN + 'aventure'])
    liste.append(['Biopic', URL_MAIN + 'biopic'])
    liste.append(['Comédie', URL_MAIN + 'comedie'])
    # l'url sur le site n'est pas bonne
    liste.append(['Comédie musicale', URL_MAIN + 'comedie-musicale'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire'])
    liste.append(['Drame', URL_MAIN + 'drame'])
    liste.append(['Epouvante-horreur', URL_MAIN + 'epouvante-horreur'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage'])
    liste.append(['Exclu', URL_MAIN + 'exclu'])
    liste.append(['Famille', URL_MAIN + 'famille'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique'])
    liste.append(['Guerre', URL_MAIN + 'guerre'])
    liste.append(['Historique', URL_MAIN + 'historique'])
    liste.append(['Musical', URL_MAIN + 'musical'])
    liste.append(['Policier', URL_MAIN + 'policier'])
    liste.append(['Romance', URL_MAIN + 'romance'])
    liste.append(['Science-fiction', URL_MAIN + 'science-fiction'])
    liste.append(['Thriller', URL_MAIN + 'thriller'])
    liste.append(['Vieux Film', URL_MAIN + 'vieux-film'])
    liste.append(['Western', URL_MAIN + 'western'])

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


def showYears():
    gui = Gui()
    output_parameter_handler = OutputParameterHandler()
    for i in reversed(range(2005, 2023)):
        Year = str(i)
        output_parameter_handler.addParameter(
            'site_url', URL_MAIN + 'index.php?do=xfsearch&xf=' + Year)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            Year,
            'annees.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()

    if search:
        if URL_SEARCH[0] in search:
            url = search
        else:
            url = URL_SEARCH[0] + search
        url = url.replace(' ', '+')
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'class="poster.+?img src="([^"]+)".+?class="quality">([^<]+)</div>.+?class="title"><a href="([^"]+)".+?title="([^"]+)".+?class="label">Ann.+?<a href.+?>([^<]+)</a>.+?class="shortStory">([^<]+)</div>'
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

            url2 = entry[2]
            thumb = entry[0]
            if thumb.startswith('//'):
                thumb = 'http:' + thumb

            title = entry[3]
            qual = entry[1]
            year = entry[4]
            desc = entry[5]
            display_title = ('%s [%s]') % (title, qual)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)
            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                display_title,
                'films.png',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            sNumPage = re.search('page/([0-9]+)', next_page).group(1)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + sNumPage,
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<div id=\'dle-content\'>.+?<span class="prev-next"> <a href="([^"]+)">'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    year = input_parameter_handler.getValue('year')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    # Vire les bandes annonces
    html_content = html_content.replace('src="https://www.youtube.com/', '')

    pattern = '<div class="tabs_header">.+?<a.+?>([^<]+)</b><tr>|(?:<a class="" rel="noreferrer" href="([^"]+)".+?<img src="/templates/Flymix/images/(.+?).png" /> *</a>|<a href="([^"]+)" >([^"]+)</a>)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        gui.addText(SITE_IDENTIFIER, movie_title)

        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if entry[0]:
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR red]' +
                    entry[0].replace(
                        "&nbsp",
                        "") +
                    '[/COLOR]')
            else:
                if entry[3]:
                    try:
                        host, title = entry[4].split('-', 1)
                        host = '[COLOR coral]' + host + '[/COLOR]'
                        url = entry[3]
                    except ValueError:
                        host = '[COLOR coral]' + \
                            entry[4].capitalize() + '[/COLOR]'
                        host = re.sub('\\.\\w+', '', host)
                        url = entry[3]
                else:
                    host = '[COLOR coral]' + \
                        entry[2].capitalize() + '[/COLOR]'
                    host = re.sub('\\.\\w+', '', host)
                    url = entry[1]

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter(
                    'movie_title', movie_title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                output_parameter_handler.addParameter('year', year)
                gui.addLink(
                    SITE_IDENTIFIER,
                    'Display_protected_link',
                    host,
                    thumb,
                    desc,
                    output_parameter_handler)

        progress_.VSclose(progress_)

    gui.setEndOfDirectory()


def Display_protected_link():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    movie_title = input_parameter_handler.getValue('movie_title')
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')

    if 'ouo' in url:
        hoster_url = DecryptOuo(url)
        if hoster_url:
            title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        gui.setEndOfDirectory()

    # Est ce un lien dl-protect ?
    if '/l.k.s/' in url:
        html_content = DecryptddlProtect(url)

        if html_content:
            # Si redirection
            if html_content.startswith('http'):
                aResult_dlprotect = (True, [html_content])
            else:
                sPattern_dlprotect = '<p><a href="(.+?)">.+?</a></p>'
                aResult_dlprotect = parser.parse(
                    html_content, sPattern_dlprotect)

        else:
            oDialog = dialog().VSok(
                'Désolé, problème de captcha.\n Veuillez en rentrer un directement sur le site, le temps de réparer')
            aResult_dlprotect = (False, False)

    elif 'keeplinks' in url:
        hoster_url = DecryptKeeplinks(url)
        if hoster_url:
            title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        gui.setEndOfDirectory()
    # Si lien normal
    else:
        if not url.startswith('http'):
            url = 'http://' + url
        aResult_dlprotect = (True, [url])

    if (aResult_dlprotect[0]):
        for entry in aResult_dlprotect[1]:
            hoster_url = entry

            title = movie_title

            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

    gui.setEndOfDirectory()


def DecryptddlProtect(url):
    # VSlog 'entering DecryptddlProtect'
    if not url:
        return ''

    # Get host
    tmp = url.split('/')
    host = tmp[0] + '//' + tmp[2] + '/' + tmp[3] + '/'
    host1 = tmp[2]

    cookies = ''
    dialogs = dialog()
    # try to get previous cookie
    cookies = GestionCookie().Readcookie('cinemegatoil_org')

    request_handler = RequestHandler(url)
    if cookies:
        request_handler.addHeaderEntry('Cookie', cookies)
    html_content = request_handler.request()

    # A partir de la on a les bon cookies pr la protection cloudflare

    # Si ca demande le captcha
    if 'Vérification Captcha:' in html_content:
        if cookies:
            GestionCookie().DeleteCookie('cinemegatoil_org')
            request_handler = RequestHandler(url)
            html_content = request_handler.request()

        s = re.findall('<img src="([^<>"]+?)" /><br />', html_content)
        if host in s[0]:
            image = s[0]
        else:
            image = host + s[0]

        captcha, cookies2 = get_response(image, cookies)
        cookies = cookies2.replace(';', '')

        request_handler = RequestHandler(url)
        request_handler.setRequestType(1)
        request_handler.addHeaderEntry('Host', host1)
        request_handler.addHeaderEntry('User-Agent', UA)
        request_handler.addHeaderEntry(
            'Accept-Language',
            'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        request_handler.addHeaderEntry(
            'Accept',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request_handler.addHeaderEntry('Cookie', cookies)
        request_handler.addHeaderEntry('Referer', url)

        request_handler.addParameters('submit1', 'Submit')
        request_handler.addParameters('security_code', captcha)

        html_content = request_handler.request()

        if 'Code de securite incorrect' in html_content:
            dialogs.VSinfo("Mauvais Captcha")
            return 'rate'

        if 'Veuillez recopier le captcha ci-dessus' in html_content:
            dialogs.VSinfo("Rattage")
            return 'rate'

        # si captcha reussi
        # save cookies
        GestionCookie().SaveCookie('cinemegatoil_org', cookies)

    return html_content


def get_response(img, cookie):
    # on telecharge l'image
    import xbmcvfs

    dialogs = dialog()

    filename = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"
    # PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
    # filename  = os.path.join(PathCache, 'Captcha.raw')

    hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', img)
    host = re.sub(r'https*:\/\/', '', hostComplet)
    url = img

    request_handler = RequestHandler(url)
    request_handler.addHeaderEntry('User-Agent', UA)
    # request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry('Cookie', cookie)

    htmlcontent = request_handler.request()

    NewCookie = request_handler.GetCookies()

    downloaded_image = xbmcvfs.File(filename, 'wb')
    # downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

    # on affiche le dialogue
    solution = ''

    if True:
        # nouveau captcha
        try:
            # affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                # """
                # Dialog class for captcha
                # """
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    # image background captcha
                    self.getControl(1).setImage(
                        filename.encode("utf-8"), False)
                    # image petit captcha memory fail
                    self.getControl(2).setImage(
                        filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    # Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        # button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty('captcha', solution)
                        self.close()
                        return

                    elif controlId == 30:
                        # button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        # button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(
                            self.getControl(5000).getLabel(), '', False)
                        kb.doModal()

                        if (kb.isConfirmed()):
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    # touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream"
            # path = cConfig().getAddonPath().decode("utf-8")
            wd = XMLDialog('DialogCaptcha.xml', path, 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        # ancien Captcha
        try:
            img = xbmcgui.ControlImage(
                450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            # xbmc.sleep(3000)
            kb = xbmc.Keyboard(
                '', 'Tapez les Lettres/chiffres de l\'image', False)
            kb.doModal()
            if kb.isConfirmed():
                solution = kb.getText()
                if solution == '':
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution, NewCookie


def DecryptKeeplinks(url):
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    Cookie = request_handler.GetCookies()

    key = re.search(
        '<div class="g-recaptcha" data-sitekey="(.+?)"></div>',
        str(html_content)).group(1)
    hiddenAction = re.search(
        '<input type="hidden" name=".+?" id="hiddenaction" value="([^"]+)"/>',
        str(html_content)).group(1)

    gToken = ResolveCaptcha(key, url)

    data = "myhiddenpwd=&hiddenaction=" + hiddenAction + \
        "+&captchatype=Re&hiddencaptcha=1&hiddenpwd=&g-recaptcha-response=" + gToken
    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Referer', url)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', len(str(data)))
    request_handler.addHeaderEntry(
        'Cookie', 'flag[' + url.split('/')[4] + ']=1;')
    request_handler.addParametersLine(data)
    html_content = request_handler.request()

    url = re.search(
        'class="selecttext live">([^<]+)</a>',
        str(html_content)).group(1)
    return url


def DecryptOuo(url):
    urlOuo = url
    if '/fbc/' not in urlOuo:
        urlOuo = urlOuo.replace(
            'io/', 'io/fbc/').replace('press/', 'press/fbc/')

    request_handler = RequestHandler(urlOuo)
    html_content = request_handler.request()
    Cookie = request_handler.GetCookies()

    key = re.search('sitekey: "(.+?)"', str(html_content)).group(1)
    OuoToken = re.search(
        '<input name="_token" type="hidden" value="(.+?)">.+?<input id="v-token" name="v-token" type="hidden" value="(.+?)"',
        str(html_content),
        re.MULTILINE | re.DOTALL)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + \
        OuoToken.group(1) + '&g-recaptcha-response=' + gToken + "&v-token=" + OuoToken.group(2)

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Referer', urlOuo)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', str(len(params)))
    request_handler.addHeaderEntry('Cookie', Cookie)
    request_handler.addParametersLine(params)
    html_content = request_handler.request()

    final = re.search(
        '<form method="POST" action="(.+?)" accept-charset=.+?<input name="_token" type="hidden" value="(.+?)">',
        str(html_content))

    url = final.group(1)
    params = '_token=' + final.group(2) + '&x-token=' + ""

    request_handler = RequestHandler(url)
    request_handler.setRequestType(1)
    request_handler.addHeaderEntry('User-Agent', UA)
    request_handler.addHeaderEntry(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry(
        'Accept-Language',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request_handler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    request_handler.addHeaderEntry('Referer', urlOuo)
    request_handler.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request_handler.addHeaderEntry('Content-Length', str(len(params)))
    request_handler.addHeaderEntry('Cookie', Cookie)
    request_handler.addParametersLine(params)
    html_content = request_handler.request()

    return request_handler.getRealUrl()
