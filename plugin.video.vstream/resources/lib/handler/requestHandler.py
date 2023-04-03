# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from requests import post, Session, Request, RequestException, ConnectionError
from resources.lib.comaddon import Addon, dialog, VSlog, VSPath, isMatrix
from resources.lib.util import urlHostName

import requests.packages.urllib3.util.connection as urllib3_cn
import socket
import string
import random


class RequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1

    def __init__(self, url):
        self.__sUrl = url
        self.__sRealUrl = ''
        self.__cType = 0
        self.__paramaters = {}
        self.__paramaters_line = ''
        self.__header_entries = {}
        self.__cookie = {}
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 30
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''
        self.BUG_SSL = False
        self.__enableDNS = False
        self.s = Session()
        self.redirects = True
        self.verify = True
        self.json = {}
        self.forceIPV4 = False
        self.reponse = None

    def statusCode(self):
        return self.reponse.status_code

    # Utile pour certains hebergeurs qui ne marche pas en ipv6.
    def disableIPV6(self):
        self.forceIPV4 = True

    def allowed_gai_family(self):
        """
         https://github.com/shazow/urllib3/blob/master/urllib3/util/connection.py
        """
        family = socket.AF_INET
        if urllib3_cn.HAS_IPV6:
            family = socket.AF_INET  # force ipv6 only if it is available
        return family

    # Desactive le ssl
    def disableSSL(self):
        self.verify = False

    # Empeche les redirections
    def disableRedirect(self):
        self.redirects = False

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    # Defini le type de requete
    # 0 : pour un requete GET
    # 1 : pour une requete POST
    def setRequestType(self, cType):
        self.__cType = cType

    # Permets de definir un timeout
    def setTimeout(self, valeur):
        self.__timeout = valeur

    # Ajouter un cookie dans le headers de la requete
    def addCookieEntry(self, header_key, header_value):
        header = {header_key: header_value}
        self.__cookie.update(header)

    # Ajouter des parametre JSON
    def addJSONEntry(self, header_key, header_value):
        header = {header_key: header_value}
        self.json.update(header)

    # Ajouter un elements dans le headers de la requete
    def addHeaderEntry(self, header_key, header_value):
        for sublist in list(self.__header_entries):
            if header_key in sublist:
                self.__header_entries.pop(sublist)

            if header_key == "Content-Length":
                header_value = str(header_value)

        header = {header_key: header_value}
        self.__header_entries.update(header)

    # Ajout un parametre dans la requete
    def addParameters(self, parameter_key, parameter_value):
        self.__paramaters[parameter_key] = parameter_value

    # Ajoute une ligne de parametre
    def addParametersLine(self, parameter_value):
        self.__paramaters_line = parameter_value

    # egg addMultipartFiled({'sess_id': s_id, 'upload_type': 'url',
    # 'srv_tmp_url': sTmp})
    def addMultipartFiled(self, fields):
        mpartdata = MPencode(fields)
        self.__paramaters_line = mpartdata[1]
        self.addHeaderEntry('Content-Type', mpartdata[0])
        self.addHeaderEntry('Content-Length', len(mpartdata[1]))

    # Je sais plus si elle gere les doublons
    def getResponseHeader(self):
        return self.__sResponseHeader

    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl

    def request(self, json_decode=False):
        # Supprimee car deconne si url contient ' ' et '+' en meme temps
        # self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest(json_decode)

    # Recupere les cookies de la requete
    def GetCookies(self):
        if not self.__sResponseHeader:
            return ''

        if 'Set-Cookie' in self.__sResponseHeader:
            import re

            c = self.__sResponseHeader.get('set-cookie')

            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,]+?);', c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
                cookies = cookies[:-1]
                return cookies
        return ''

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self, json_decode=False):
        if self.__enableDNS:
            self.save_getaddrinfo = socket.getaddrinfo
            socket.getaddrinfo = self.new_getaddrinfo

        if self.__paramaters_line:
            parameters = self.__paramaters_line
        else:
            parameters = self.__paramaters

        if self.__cType == RequestHandler.REQUEST_TYPE_GET:
            if len(parameters) > 0:
                if self.__sUrl.find('?') == -1:
                    self.__sUrl = self.__sUrl + '?' + str(parameters)
                    parameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(parameters)
                    parameters = ''

        if self.BUG_SSL:
            self.verify = False

        if self.__cType == RequestHandler.REQUEST_TYPE_GET:
            method = "GET"
        else:
            method = "POST"

        if self.forceIPV4:
            urllib3_cn.allowed_gai_family = self.allowed_gai_family

        try:
            _request = Request(method, self.__sUrl, headers=self.__header_entries)
            if method in ['POST']:
                _request.data = parameters

            if self.__cookie:
                _request.cookies = self.__cookie

            if self.json:
                _request.json = self.json

            prepped = _request.prepare()
            self.s.headers.update(self.__header_entries)

            self.reponse = self.s.send(prepped, timeout=self.__timeout, allow_redirects=self.redirects,
                                       verify=self.verify)
            self.__sResponseHeader = self.reponse.headers
            self.__sRealUrl = self.reponse.url

            if json_decode:
                content = self.reponse.json()
            else:
                content = self.reponse.content
                # Necessaire pour Python 3
                if isMatrix() and 'youtube' not in self.reponse.url:
                    try:
                        content = content.decode()
                    except BaseException:
                        # Decodage minimum obligatoire.
                        try:
                            content = content.decode('unicode-escape')
                        except BaseException:
                            pass

        except ConnectionError as e:
            # Retry with DNS only if addon is present
            if 'getaddrinfo failed' in str(e) or\
                    'Failed to establish a new connection' in str(e)and self.__enableDNS is False:
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = '%s (%s)' % (Addon().VSlang(30470), urlHostName(self.__sUrl))
                    dialog().VSerror(error_msg)
                    content = ''
            else:
                return False

        except RequestException as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e) and self.BUG_SSL is False:
                self.BUG_SSL = True
                return self.__callRequest()
            elif 'getaddrinfo failed' in str(e) and self.__enableDNS is False:
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = '%s (%s)' % (Addon().VSlang(30470), urlHostName(self.__sUrl))
            else:
                error_msg = "%s (%s),%s" % (Addon().VSlang(30205), e, self.__sUrl)

            dialog().VSerror(error_msg)
            content = ''

        if self.reponse is not None:
            if self.reponse.status_code in [503, 403]:
                if "Forbidden" not in content:
                    # Default
                    cloudproxy_endpoint = 'http://' + Addon().getSetting('ipaddress') + ':8191/v1'

                    json_response = False
                    try:
                        # On fait une requete.
                        json_response = post(cloudproxy_endpoint, headers=self.__header_entries, json={
                            'cmd': 'request.%s' % method.lower(),
                            'url': self.__sUrl
                        })
                    except BaseException:
                        dialog().VSerror("%s (%s)" %("Page protegee par Cloudflare, essayez FlareSolverr",
                                                     urlHostName(self.__sUrl)))

                    if json_response:
                        response = json_response.json()
                        if 'solution' in response:
                            if self.__sUrl != response['solution']['url']:
                                self.__sRealUrl = response['solution']['url']

                            content = response['solution']['response']

            if self.reponse and not content:
                # Ignorer ces deux codes erreurs.
                ignore_status = [200, 302]
                if self.reponse.status_code not in ignore_status:
                    dialog().VSerror(
                        "%s (%d),%s" %
                        (Addon().VSlang(30205),
                         self.reponse.status_code,
                         self.__sUrl))

        if content:
            if self.__bRemoveNewLines:
                content = content.replace("\n", "")
                content = content.replace("\r\t", "")

            if self.__bRemoveBreakLines:
                content = content.replace("&nbsp;", "")

        if self.__enableDNS:
            socket.getaddrinfo = self.save_getaddrinfo
            self.__enableDNS = False

        return content

    def new_getaddrinfo(self, *args):
        try:
            import sys
            import dns.resolver

            if isMatrix():
                path = VSPath('special://home/addons/script.module.dnspython/lib/')
            else:
                path = VSPath('special://home/addons/script.module.dnspython/lib/').decode('utf-8')

            if path not in sys.path:
                sys.path.append(path)
            host = args[0]
            port = args[1]
            # Keep the domain only: http://example.com/foo/bar => example.com
            if "//" in host:
                host = host[host.find("//"):]
            if "/" in host:
                host = host[:host.find("/")]
            resolver = dns.resolver.Resolver(configure=False)
            # Résolveurs DNS ouverts: https://www.fdn.fr/actions/dns/
            resolver.nameservers = [
                '80.67.169.12',
                '2001:910:800::12',
                '80.67.169.40',
                '2001:910:800::40']
            answer = resolver.query(host, 'a')
            host_found = str(answer[0])
            VSlog("new_getaddrinfo found host %s" % host_found)
            # Keep same return schema as socket.getaddrinfo (family, type,
            # proto, canonname, sockaddr)
            return [(2, 1, 0, '', (host_found, port)),
                    (2, 1, 0, '', (host_found, port))]
        except Exception as e:
            VSlog("new_getaddrinfo ERROR: {0}".format(e))
            return self.save_getaddrinfo(*args)


# ******************************************************************************
# from https://github.com/eliellis/mpart.py
# ******************************************************************************
def MPencode(fields):
    import mimetypes
    random_boundary = __randy_boundary()
    content_type = "multipart/form-data, boundary=%s" % random_boundary

    form_data = []

    if fields:
        try:
            data = fields.iteritems()
        except BaseException:
            data = fields.items()

        for (key, value) in data:
            if not hasattr(value, 'read'):
                item_str = '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % \
                          (random_boundary, key, value)
                form_data.append(item_str)
            elif hasattr(value, 'read'):
                with value:
                    file_mimetype = mimetypes.guess_type(
                        value.name)[0] if mimetypes.guess_type(
                        value.name)[0] else 'application/octet-stream'

                    item_str = ('--%s\r\nContent-Disposition: form-data; name="%s"; ' % (random_boundary, key))
                    item_str += ('filename="%s"\r\nContent-Type: %s\r\n\r\n' % (value.name, file_mimetype))
                    item_str += ('%s\r\n' % value.read())
                form_data.append(item_str)
            else:
                raise Exception(value, 'Field is neither a file handle or any other decodable type.')
    else:
        pass

    form_data.append('--%s--\r\n' % random_boundary)

    return content_type, ''.join(form_data)


def __randy_boundary(length=10, reshuffle=False):
    if isMatrix():
        character_string = string.ascii_letters + string.digits
    else:
        character_string = string.letters + string.digits

    boundary_string = []
    for i in range(0, length):
        rand_index = random.randint(0, len(character_string) - 1)
        boundary_string.append(character_string[rand_index])
    if reshuffle:
        random.shuffle(boundary_string)
    else:
        pass
    return ''.join(boundary_string)
