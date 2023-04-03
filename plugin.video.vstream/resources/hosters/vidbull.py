# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://forums.tvaddons.ag/tknorris-release-repository/10792-debugging-daclips-2.html

import re

from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.GKDecrypter import GKDecrypter


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbull', 'VidBull')

    def _getMediaLinkForGuest(self, auto_play=False):
        url_stream = ''

        request = RequestHandler(self._url)
        html_content = request.request()

        parser = Parser()

        pattern = "<script type='text\\/javascript'>(eval\\(function\\(p,a,c,k,e,d.+?)<\\/script>"
        results = parser.parse(html_content, pattern)

        if results[0] is True:
            for i in results[1]:
                html_content = cPacker().unpack(i)
                # xbmc.log(html_content)

                # Premiere methode avec <embed>
                if '<embed' in html_content:
                    pass

                # deuxieme methode, lien code aes
                else:
                    EncodedLink = re.search(
                        'file:"([^"]+)"', html_content, re.DOTALL)

                    if EncodedLink:

                        Key = "a949376e37b369" + "f17bc7d3c7a04c5721"
                        x = GKDecrypter(128, 128)
                        url = x.decrypt(
                            EncodedLink.group(1),
                            Key.decode("hex"),
                            "ECB").split('\0')[0]

                        # Si utilise pyaes
                        # import resources.lib.pyaes as pyaes
                        # decryptor = pyaes.new(Key.decode("hex"), pyaes.MODE_ECB, IV = '')
                        # url = decryptor.decrypt(lt.decode("hex")).replace('\x00', '')

                        # xbmc.log('>> ' + url)

                        url_stream = url

        if url_stream:
            return True, url_stream
        else:
            return False, False

        return False, False
