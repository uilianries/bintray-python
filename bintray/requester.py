# -*- coding: utf-8 -*-

import requests
import json

from requests.auth import HTTPBasicAuth


class Requester(object):

    def __init__(self, username=None, api_key=None):
        """ Initialize arguments for login

        :param username: Bintray username
        :param api_key: Bintray API Key
        """
        self._username = username
        self._password = api_key

    def _get_authentication(self):
        """ Retrieve Basic HTTP Authentication based on username and API key

        :return: Basic Authentication handler
        """
        if not self._username or not self._password:
            return None
        return HTTPBasicAuth(self._username, self._password)

    def _add_status_code(self, response):
        """ Update JSON result with error and status code

        :param response: Requests response
        :return: Response JSON
        """
        try:
            json_data = response.json()
        except json.decoder.JSONDecodeError:
            json_data = {'message': response.content.decode()}
        if isinstance(json_data, list):
            json_data.append({"statusCode": response.status_code, "error": not response.ok})
        else:
            json_data.update({"statusCode": response.status_code, "error": not response.ok})
        return json_data

    def _raise_error(self, message, response):
        try:
            response.raise_for_status()
        except Exception as error:
            raise Exception("{} ({}): {}".format(message, response.status_code, str(error)))

    def get(self, url, params=None):
        """ Forward GET method

        :param url: Web address
        :param params: URL params
        :return: JSON answer
        """
        response, _ = self.download(url, params)
        return response

    def download(self, url, params=None):
        """ Just like GET method, but with content

        :param url: URL Address
        :param params: URL parameters
        :return: JSON response and content
        """
        response = requests.get(url, auth=self._get_authentication(), params=params)
        if not response.ok:
            self._raise_error("Could not GET", response)
        return self._add_status_code(response), response.content

    def put(self, url, params=None, data=None, json=None, headers=None):
        """ Forward PUT method

        :param url: URL address
        :param params: URL params
        :param data: Data content
        :param json: JSON content
        :param headers: Request headers
        :return: JSON
        """
        if data and json:
            raise Exception("Only accept 'data' or 'json'")
        if data:
            response = requests.put(url, auth=self._get_authentication(), params=params, data=data,
                                    headers=headers)
        else:
            response = requests.put(url, auth=self._get_authentication(), params=params, json=json,
                                    headers=headers)
        if not response.ok:
            self._raise_error("Could not PUT", response)
        return self._add_status_code(response)

    def post(self, url, json=None, params=None, headers=None):
        """ Forward POST method

        :param url: URL address
        :param params: URL parameters
        :param json: Data to be posted
        :param headers: Request headers
        :return: Request response
        """
        response = requests.post(url, auth=self._get_authentication(), json=json, params=params,
                                 headers=headers)
        if not response.ok:
            self._raise_error("Could not POST", response)
        return self._add_status_code(response)

    def patch(self, url, json=None, params=None):
        """ Forward PATCH method

        :param url: URL address
        :param params: URL parameters
        :param json: Data to be patched
        :return: Request response
        """
        response = requests.patch(url, auth=self._get_authentication(), json=json, params=params)
        if not response.ok:
            self._raise_error("Could not PATCH", response)
        return self._add_status_code(response)

    def delete(self, url, params=None):
        """ Forward DELETE method

        :param url: URL address
        :param params: URL parameters
        :return: Request response
        """
        response = requests.delete(url, auth=self._get_authentication(), params=params)
        if not response.ok:
            self._raise_error("Could not DELETE", response)
        return self._add_status_code(response)
