# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from __future__ import annotations

from typing import Dict
from bs4 import BeautifulSoup
from requests import Session, Request, RequestException, ConnectionError, Response
from resources.sites.generic.token_object import TokenObject


class RequestHelper:

    def __init__(self, is_matrix: bool):
        self._is_matrix = is_matrix
        self._session = Session()
        self._timeout = 30
        self._redirects = True
        self._verify = True
        self._user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
        self._headers = {
            'User-Agent': self._user_agent,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self._list_data = {}

    def _add_token_to_header(self, token: TokenObject):
        request_response = self.request(token.getUrl(), request_type="GET", request_token_if_needed=False)
        response_data: str = self._decode_response(request_response)

        if token.isHtmlTokenInput():
            soup = BeautifulSoup(response_data, 'html.parser')
            token_input = soup.select_one(token.getHtmlTokenInput())
            if token_input is None:
                print("[ERROR] Token not found. Try to found", token.getHtmlTokenInput(), "on website",
                      token.getUrl())
                return
            if 'value' in token_input.attrs:
                token_value = token_input.attrs['value']
            else:
                token_value = ''

            self._list_data[token.getDataKey()] = token_value

        str_cookies = ''
        for cookie in request_response.cookies:
            str_cookies += cookie.name + '=' + cookie.value + '; '
        self._headers['Cookie'] = str_cookies

    def request(self, url: str, request_type: str, token_object: TokenObject = None, list_data: Dict[str, str]=None) -> Response:
        result = None
        if token_object is not None:
            self._add_token_to_header(token_object)

        if list_data is not None:
            self._list_data.update(list_data)

        method = request_type
        try:
            self._headers['Referer'] = url
            if method == 'GET':
                url = self._add_data_to_url(url)
            request = Request(method, url, headers=self._headers)
            if method == 'POST':
                request.data = self._data_to_url()

            prepped = request.prepare()

            result = self._session.send(prepped, timeout=self._timeout, allow_redirects=self._redirects,
                                        verify=self._verify)
        except ConnectionError as e:
            # TODO
            pass
        except RequestException as e:
            # TODO
            pass
        self._list_data = {}
        return result

    def _add_data_to_url(self, url: str) -> str:
        if len(self._list_data):
            if '?' in url:
                url += '&' + self._data_to_url()
            else:
                url += '?' + self._data_to_url()
        return url

    def _data_to_url(self) -> str:
        if len(self._list_data):
            return '&'.join([f"{key}={value}" for key, value in self._list_data.items()])
        return ''

    def _decode_response(self, response: Response, json_decode=False):
        if json_decode:
            content = response.json()
        else:
            content = response.content
            # Nécessaire pour Python 3
            if self._is_matrix and 'youtube' not in response.url:
                try:
                    content = content.decode()
                except:
                    # Décodage minimum obligatoire.
                    try:
                        content = content.decode('unicode-escape')
                    except:
                        pass
        return content
