#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Python Wrapper for Bintray API

    https://bintray.com/docs/api
"""
import os
import logging
import requests
from requests.auth import HTTPBasicAuth


__version__ = "0.1.0"
__author__ = "Uilian Ries <uilianries@gmail.com>"
__license__ = "MIT"


class Bintray(object):
    """ Python Wrapper for Bintray API

    """

    # Bintray API URL
    BINTRAY_URL = "https://api.bintray.com"

    def __init__(self, username=None, api_key=None):
        """ Initialize arguments for login

        :param username: Bintray username
        :param api_key: Bintray API Key
        """
        self._username = username or os.getenv("BINTRAY_USERNAME")
        self._password = api_key or os.getenv("BINTRAY_API_KEY")

        self._logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

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
        json_data = response.json()
        if isinstance(json_data, list):
            json_data.append({"statusCode": response.status_code, "error": not response.ok})
        else:
            json_data.update({"statusCode": response.status_code, "error": not response.ok})
        return json_data


    def _bool_to_number(self, value):
        """ Convert boolean result into numeric string

        :param value: Any boolean value
        :return: "1" when True. Otherwise, "0"
        """
        return "1" if value else "0"

    def _raise_error(self, message, response):
        try:
            response.raise_for_status()
        except Exception as error:
            raise Exception("{} ({}): {}".format(message, response.status_code, str(error)))

    # Files

    def get_package_files(self, subject, repo, package, include_unpublished=False):
        """ Get all files in a given package.

            When called by a user with publishing rights on the package,
            includes unpublished files in the list. By default only published files are shown.
        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param include_unpublished: Show not published files
        :return: List with all files
        """
        parameters = {"include_unpublished": self._bool_to_number(include_unpublished)}
        url = "{}/packages/{}/{}/{}/files?include_unpublished={}".format(Bintray.BINTRAY_URL,
                                                                subject,
                                                                repo,
                                                                package,
                                                                include_unpublished)
        response = requests.get(url, auth=self._get_authentication(), params=parameters)
        if not response.ok:
            self._raise_error("Could not list package files", response)
        return self._add_status_code(response)

    # Content Uploading & Publishing

    def upload_content(self, subject, repo, package, version, remote_file_path, local_file_path,
                       publish=True, override=False, explode=False):
        """
        Upload content to the specified repository path, with package and version information (both required).

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param remote_file_path: file name to be used on Bintray
        :param local_file_path: file path to be uploaded
        :param publish: publish after uploading
        :param override: override remote file
        :param explode: explode remote file
        :return:
        """
        url = "{}/content/{}/{}/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                 version, remote_file_path)
        parameters = {"publish": self._bool_to_number(publish),
                      "override": self._bool_to_number(override),
                      "explode": self._bool_to_number(explode)}

        with open(local_file_path, 'rb') as file_content:
            response = requests.put(url, auth=self._get_authentication(), params=parameters,
                                    data=file_content)
            if response.status_code != 201:
                self._raise_error("Could not upload", response)
        self._logger.info("Upload successfully: {}".format(url))
        return self._add_status_code(response)

    # Content Downloading

    def download_content(self, subject, repo, remote_file_path, local_file_path):
        """ Download content from the specified repository path.

        :param subject: username or organization
        :param repo: repository name
        :param remote_file_path: file name to be downloaded from Bintray
        :param local_file_path: file name to be stored in local storage
        """
        download_base_url = "https://dl.bintray.com"
        url = "{}/{}/{}/{}".format(download_base_url, subject, repo, remote_file_path)
        response = requests.get(url, auth=self._get_authentication())
        if not response.ok:
            self._raise_error("Could not download file content", response)
        with open(local_file_path, 'wb') as local_fd:
            local_fd.write(response.content)
        self._logger.info("Download successfully: {}".format(url))
        return self._add_status_code(response)
