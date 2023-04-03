import re

from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.util import cUtil
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megavideo', 'MegaVideo.com')

    def getPattern(self):
        return ' errortext="(.+?)"'

    def setUrl(self, url):
        self._url = str(self.__modifyUrl(url))
        self._url = self._url.replace('http://www.megavideo.com/?v=', '')
        self._url = self._url.replace('http://megavideo.com/?v=', '')
        self._url = 'http://www.megavideo.com/?v=' + str(self._url)

    def __modifyUrl(self, url):
        if (url.startswith('http://www.megavideo.com/v/')):
            request_handler = RequestHandler(url)
            request_handler.request()
            sRealUrl = request_handler.getRealUrl()
            self._url = sRealUrl
            return self.__getIdFromUrl()

        return url

    def getMediaLink(self, auto_play=False):
        premium_handler = cPremiumHandler(self.getPluginIdentifier())
        if (premium_handler.isPremiumModeAvailable()):
            username = premium_handler.getUsername()
            password = premium_handler.getPassword()
            return self._getMediaLinkByPremiumUser(username, password)

        return self._getMediaLinkForGuest(auto_play)

    def __getIdFromUrl(self):
        pattern = "v=([^&]+)"
        parser = Parser()
        results = parser.parse(self._url, pattern)
        if results[0] is True:
            return results[1][0]

        return ''

    def _getMediaLinkForGuest(self, auto_play=False):
        s_id = self.__getIdFromUrl()

        self._url = 'http://www.megavideo.com/xml/videolink.php?v=' + str(s_id)

        request = RequestHandler(self.getUrl())
        request.addHeaderEntry('Referer', 'http://www.megavideo.com/')
        content = request.request()

        results = Parser().parse(content, self.getPattern())

        if results[0] is False:
            s = re.compile(' s="(.+?)"').findall(content)
            k1 = re.compile(' k1="(.+?)"').findall(content)
            k2 = re.compile(' k2="(.+?)"').findall(content)
            un = re.compile(' un="(.+?)"').findall(content)

            url = "http://www" + s[0] + ".megavideo.com/files/" + \
                self.__decrypt(un[0], k1[0], k2[0]) + "/?.flv"

            results = []
            results.append(True)
            results.append(url)
            return results

        results = []
        results.append(False)
        results.append('')
        return results

    def _getMediaLinkByPremiumUser(self, username, password):
        request_handler = RequestHandler(
            'http://www.megavideo.com/?s=account')
        request_handler.setRequestType(RequestHandler.REQUEST_TYPE_POST)
        request_handler.addParameters('login', '1')
        request_handler.addParameters('username', username)
        request_handler.addParameters('password', password)
        request_handler.request()

        header = request_handler.getResponseHeader()
        sReponseCookie = header.getheader("Set-Cookie")

        self._url = self.__getIdFromUrl()

        pattern = 'user=([^;]+);'
        parser = Parser()
        results = parser.parse(sReponseCookie, pattern)
        if results[0] is True:
            sUserId = results[1][0]
            url = 'http://www.megavideo.com/xml/player_login.php?u=' + \
                str(sUserId) + '&v=' + str(self._url)
            request_handler = RequestHandler(url)
            sXmlContent = request_handler.request()

            pattern = 'downloadurl="([^"]+)"'
            parser = Parser()
            results = parser.parse(sXmlContent, pattern)

            if results[0] is True:
                sMediaLink = cUtil().urlDecode(str(results[1][0]))
                return True, sMediaLink

        return False, ''

    def __decrypt(self, str1, key1, key2):
        __reg1 = []
        __reg3 = 0
        while (__reg3 < len(str1)):
            __reg0 = str1[__reg3]
            holder = __reg0
            if (holder == "0"):
                __reg1.append("0000")
            else:
                if (__reg0 == "1"):
                    __reg1.append("0001")
                else:
                    if (__reg0 == "2"):
                        __reg1.append("0010")
                    else:
                        if (__reg0 == "3"):
                            __reg1.append("0011")
                        else:
                            if (__reg0 == "4"):
                                __reg1.append("0100")
                            else:
                                if (__reg0 == "5"):
                                    __reg1.append("0101")
                                else:
                                    if (__reg0 == "6"):
                                        __reg1.append("0110")
                                    else:
                                        if (__reg0 == "7"):
                                            __reg1.append("0111")
                                        else:
                                            if (__reg0 == "8"):
                                                __reg1.append("1000")
                                            else:
                                                if (__reg0 == "9"):
                                                    __reg1.append("1001")
                                                else:
                                                    if (__reg0 == "a"):
                                                        __reg1.append("1010")
                                                    else:
                                                        if (__reg0 == "b"):
                                                            __reg1.append(
                                                                "1011")
                                                        else:
                                                            if (__reg0 == "c"):
                                                                __reg1.append(
                                                                    "1100")
                                                            else:
                                                                if (__reg0 == "d"):
                                                                    __reg1.append(
                                                                        "1101")
                                                                else:
                                                                    if (__reg0 == "e"):
                                                                        __reg1.append(
                                                                            "1110")
                                                                    else:
                                                                        if (__reg0 == "f"):
                                                                            __reg1.append(
                                                                                "1111")

        __reg3 = __reg3 + 1

        mtstr = self.__ajoin(__reg1)
        __reg1 = self.__asplit(mtstr)
        __reg6 = []
        __reg3 = 0
        while (__reg3 < 384):

            key1 = (int(key1) * 11 + 77213) % 81371
            key2 = (int(key2) * 17 + 92717) % 192811
            __reg6.append((int(key1) + int(key2)) % 128)
            __reg3 = __reg3 + 1

        __reg3 = 256
        while (__reg3 >= 0):

            __reg5 = __reg6[__reg3]
            __reg4 = __reg3 % 128
            __reg8 = __reg1[__reg5]
            __reg1[__reg5] = __reg1[__reg4]
            __reg1[__reg4] = __reg8
            __reg3 = __reg3 - 1

        __reg3 = 0
        while (__reg3 < 128):

            __reg1[__reg3] = int(__reg1[__reg3]) ^ int(
                __reg6[__reg3 + 256]) & 1
            __reg3 = __reg3 + 1

        __reg12 = self.__ajoin(__reg1)
        __reg7 = []
        __reg3 = 0
        while (__reg3 < len(__reg12)):

            __reg9 = __reg12[__reg3:__reg3 + 4]
            __reg7.append(__reg9)
            __reg3 = __reg3 + 4

        __reg2 = []
        __reg3 = 0
        while (__reg3 < len(__reg7)):
            __reg0 = __reg7[__reg3]
            holder2 = __reg0

            if (holder2 == "0000"):
                __reg2.append("0")
            else:
                if (__reg0 == "0001"):
                    __reg2.append("1")
                else:
                    if (__reg0 == "0010"):
                        __reg2.append("2")
                    else:
                        if (__reg0 == "0011"):
                            __reg2.append("3")
                        else:
                            if (__reg0 == "0100"):
                                __reg2.append("4")
                            else:
                                if (__reg0 == "0101"):
                                    __reg2.append("5")
                                else:
                                    if (__reg0 == "0110"):
                                        __reg2.append("6")
                                    else:
                                        if (__reg0 == "0111"):
                                            __reg2.append("7")
                                        else:
                                            if (__reg0 == "1000"):
                                                __reg2.append("8")
                                            else:
                                                if (__reg0 == "1001"):
                                                    __reg2.append("9")
                                                else:
                                                    if (__reg0 == "1010"):
                                                        __reg2.append("a")
                                                    else:
                                                        if (__reg0 == "1011"):
                                                            __reg2.append("b")
                                                        else:
                                                            if (__reg0 ==
                                                                    "1100"):
                                                                __reg2.append(
                                                                    "c")
                                                            else:
                                                                if (__reg0 ==
                                                                        "1101"):
                                                                    __reg2.append(
                                                                        "d")
                                                                else:
                                                                    if (__reg0 ==
                                                                            "1110"):
                                                                        __reg2.append(
                                                                            "e")
                                                                    else:
                                                                        if (__reg0 ==
                                                                                "1111"):
                                                                            __reg2.append(
                                                                                "f")

            __reg3 = __reg3 + 1

        endstr = self.__ajoin(__reg2)
        return endstr

    def __ajoin(self, arr):
        strtest = ''
        for num in range(len(arr)):
            strtest = strtest + str(arr[num])
        return strtest

    def __asplit(self, mystring):
        arr = []
        for num in range(len(mystring)):
            arr.append(mystring[num])
        return arr
