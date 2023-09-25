# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from requests import Session, Request, RequestException, ConnectionError, Response

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteRequest:

    def __init__(self, is_matrix: bool, site: SiteObject):
        self._site = site
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
        self._request_token = self._site.is_token_protection_enabled()

    def _add_token_to_header(self):
        site_json_token_data = self._site.get_token_json()
        request_response = self.request(site_json_token_data['url'], request_type="GET", request_token_if_needed=False)
        response_data: str = self._decode_response(request_response)

        soup = BeautifulSoup(response_data, 'html.parser')
        token_input = soup.select_one(site_json_token_data['html_token_input'])
        if 'value' in token_input.attrs:
            token_value = token_input.attrs['value']
        else:
            token_value = ''

        str_cookies = ''
        for cookie in request_response.cookies:
            str_cookies += cookie.name + '=' + cookie.value + '; '
        self._headers['Cookie'] = str_cookies

        self._list_data[site_json_token_data['data_key']] = token_value

    def request(self, url: str, request_type: str, request_token_if_needed=True, list_data=None) -> Response:
        result = None
        if self._request_token and request_token_if_needed:
            self._add_token_to_header()

        if list_data is not None:
            self._list_data.update(list_data)

        method = request_type
        try:
            self._headers['Referer'] = url
            if method == 'GET':
                url = self._add_data_to_url(url)
            # print("Request URL:", url)
            request = Request(method, url, headers=self._headers)
            if method == 'POST':
                request.data = self._data_to_url()
            # print("request.data", request.data)
            # print("Header:", self._headers)

            prepped = request.prepare()

            # print("Cookies in session:", self._session.cookies)

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
