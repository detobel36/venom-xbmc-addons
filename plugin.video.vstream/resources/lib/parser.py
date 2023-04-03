# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from operator import itemgetter
import re


class Parser:

    def sorted_nicely(self, l, key):
        """ Sort the given iterable in the way that humans expect."""
        def convert(text): return int(text) if text.isdigit() else text
        def alphanum_key(item): return [convert(c)
                                        for c in re.split('([0-9]+)', key(item))]
        return sorted(l, key=alphanum_key)

    def parseSingleResult(self, html_content, pattern):
        aMatches = re.compile(pattern).findall(html_content)
        if len(aMatches) == 1:
            aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
            return True, aMatches[0]
        return False, aMatches

    def __replaceSpecialCharacters(self, sString):
        """ /!\\ pas les mêmes tirets, tiret moyen et cadratin."""
        return sString.replace('\r', '').replace('\n', '').replace('\t', '').replace('\\/', '/').replace('&amp;', '&')\
                      .replace('&#039;', "'").replace('&#8211;', '-').replace('&#8212;', '-').replace('&eacute;', 'é')\
                      .replace('&acirc;', 'â').replace('&ecirc;', 'ê').replace('&icirc;', 'î').replace('&ocirc;', 'ô')\
                      .replace('&hellip;', '...').replace('&quot;', '"').replace('&gt;', '>').replace('&egrave;', 'è')\
                      .replace('&ccedil;', 'ç').replace('&laquo;', '<<').replace('&raquo;', '>>').replace('\xc9', 'E')\
                      .replace('&ndash;', '-').replace('&ugrave;', 'ù').replace('&agrave;', 'à').replace('&lt;', '<')\
                      .replace('&rsquo;', "'").replace('&lsquo;', '\'').replace('&nbsp;', '').replace('&#8217;', "'")\
                      .replace('&#8230;', '...').replace('&#8242;', "'").replace('&#884;', '\'').replace('&#39;', '\'')\
                      .replace('&#038;', '&').replace('&iuml;', 'ï').replace('&#8220;', '"').replace('&#8221;', '"')\
                      .replace('–', '-').replace('—', '-').replace('&#58;', ':')

    def parse(self, html_content, pattern, iMinFoundValue=1):
        html_content = self.__replaceSpecialCharacters(str(html_content))
        aMatches = re.compile(pattern, re.IGNORECASE).findall(html_content)

        # extrait la page html après retraitement vStream
        # fh = open('c:\\test.txt', "w")
        # fh.write(html_content)
        # fh.close()

        if len(aMatches) >= iMinFoundValue:
            return True, aMatches
        return False, aMatches

    def replace(self, pattern, sReplaceString, sValue):
        return re.sub(pattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)

    def getNumberFromString(self, sValue):
        pattern = '\\d+'
        aMatches = re.findall(pattern, sValue)
        if len(aMatches) > 0:
            return aMatches[0]
        return 0

    def titleParse(self, html_content, pattern):
        html_content = self.__replaceSpecialCharacters(str(html_content))
        aMatches = re.compile(pattern, re.IGNORECASE)
        try:
            [m.groupdict() for m in aMatches.finditer(html_content)]
            return m.groupdict()
        except BaseException:
            return {'title': html_content}

    def abParse(self, html_content, start, end=None, startoffset=0):
        # usage parser.abParse(html_content, 'start', 'end')
        # startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        # la fin est recherchée forcement après le début
        # la recherche de fin n'est pas obligatoire
        # usage2 parser.abParse(html_content, 'start', 'end', 6)
        # ex youtube.py

        startIdx = html_content.find(start)
        if startIdx == -1:  # rien trouvé, on prend depuis le début
            startIdx = 0

        if end:
            endIdx = html_content[startoffset +
                                  startIdx + len(start):].find(end)
            if endIdx > 0:
                return html_content[startoffset +
                                    startIdx: startoffset +
                                    startIdx +
                                    endIdx +
                                    len(start)]
        return html_content[startoffset + startIdx:]
