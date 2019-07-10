# -*- coding: utf-8 -*-
""" Python Wrapper for Bintray API

    https://bintray.com/docs/api
"""
import os

from bintray.requester import Requester
from bintray.logger import Logger
from bintray.utils import bool_to_number


__version__ = "0.2.0"
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
        self._requester = Requester(self._username, self._password)
        self._logger = Logger().logger

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
        parameters = {"include_unpublished": bool_to_number(include_unpublished)}
        url = "{}/packages/{}/{}/{}/files".format(Bintray.BINTRAY_URL,
                                                  subject,
                                                  repo,
                                                  package)
        return self._requester.get(url, parameters)

    def get_version_files(self, subject, repo, package, version, include_unpublished=False):
        """ Get all files in a given version.

            Returns an array of results, where elements are similar to the result of getting
            package files.

            When called by a user with publishing rights on the package, includes unpublished
            files in the list.

            By default only published files are shown.

            Security: Authenticated user with 'read' permission for private repositories,
            or version read entitlement.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param include_unpublished: Show not published files
        :return: List with all files
        """
        parameters = {"include_unpublished": bool_to_number(include_unpublished)}
        url = "{}/packages/{}/{}/{}/versions/{}/files".format(Bintray.BINTRAY_URL,
                                                              subject,
                                                              repo,
                                                              package,
                                                              version)
        return self._requester.get(url, parameters)

    def file_search_by_name(self, name, subject=None, repo=None, start_pos=None,
                            created_after=None):
        """ Search for a file by its name. name can take the * and ? wildcard characters.

            May take an optional subject and/or repo name to search in and/or created_after
            search from the 'dateCreatedAfter' until today.
            The 'dateCreatedAfter' is defined in the following ISO8601 format (yyyy-MM-
            dd’T’HH:mm:ss.SSSZ). Returns an array of results, where elements are similar
            to the result of getting package files. Search results will not contain private files.

            Security: Authentication is not required

        :param name: File to be searched
        :param subject: File subject to filter
        :param repo: File repo filter
        :param start_pos: Start position name to filter
        :param created_after: Creation date to filter
        :return: Package found. Otherwise, error.
        """
        parameters = {"name": name}
        if subject:
            parameters["subject"] = str(subject)
        if repo:
            parameters["repo"] = str(repo)
        if start_pos:
            parameters["start_pos"] = str(start_pos)
        if created_after:
            parameters["created_after"] = str(created_after)
        url = "{}/search/file".format(Bintray.BINTRAY_URL)
        return self._requester.get(url, parameters)

    def file_search_by_checksum(self, sha1, subject=None, repo=None, start_pos=None,
                            created_after=None):
        """ Search for a file by its sha1 checksum.

            May take an optional subject and/or repo name to search in.

            Returns an array of results, where elements are similar to the result of getting
            package files. Search results will not contain private files.

            Security: Authentication is not required

        :param sha1: File SHA-1
        :param subject: File subject to filter
        :param repo: File repo filter
        :param start_pos: Start position name to filter
        :param created_after: Creation date to filter
        :return: Package found. Otherwise, error.
        """
        parameters = {"sha1": sha1}
        if subject:
            parameters["subject"] = str(subject)
        if repo:
            parameters["repo"] = str(repo)
        if start_pos:
            parameters["start_pos"] = str(start_pos)
        if created_after:
            parameters["created_after"] = str(created_after)
        url = "{}/search/file".format(Bintray.BINTRAY_URL)
        return self._requester.get(url, parameters)

    def file_in_download_list(self, subject, repo, file_path, add_or_remove):
        """ Add or remove a file from/to the 'Download List'.

            Security: Authenticated user with 'publish' permission,
                      or version read/write entitlement.

        :param subject: File subject to filter
        :param repo: File repo filter
        :param file_path: File path to be added or removed
        :param add_or_remove: True to add in Download list. False to remove.
        :return: Request response.
        """
        action = 'true' if add_or_remove else 'false'
        json_data = {'list_in_downloads': action}
        url = "{}/file_metadata/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        return self._requester.put(url, json=json_data)

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
        parameters = {"publish": bool_to_number(publish),
                      "override": bool_to_number(override),
                      "explode": bool_to_number(explode)}

        with open(local_file_path, 'rb') as file_content:
            response = self._requester.put(url, params=parameters, data=file_content)

        self._logger.info("Upload successfully: {}".format(url))
        return response

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
        response, content = self._requester.download(url)

        with open(local_file_path, 'wb') as local_fd:
            local_fd.write(content)

        self._logger.info("Download successfully: {}".format(url))
        return response

    # Licenses

    def get_org_proprietary_licenses(self, org):
        """ Get a list of custom, proprietary licenses associated with an organization

        :param org: Organization name
        :return: Licenses list
        """
        url = "{}/orgs/{}/licenses".format(Bintray.BINTRAY_URL, org)
        return self._requester.get(url)

    def get_user_proprietary_licenses(self, user):
        """ Get a list of custom, proprietary licenses associated with an user

        :param user: User name
        :return: Licenses list
        """
        url = "{}/users/{}/licenses".format(Bintray.BINTRAY_URL, user)
        return self._requester.get(url)

    def create_org_proprietary_license(self, org, license):
        """ Create a license associated with an organization.
            Caller must be an admin of the organization.

        :param org: Organization name
        :param license: JSON data with license information
        :return: request answer
        """
        url = "{}/orgs/{}/licenses".format(Bintray.BINTRAY_URL, org)
        return self._requester.post(url, json=license)

    def create_user_proprietary_license(self, user, license):
        """ Create a license associated with an user.

        :param user: User name
        :param license: JSON data with license information
        :return: request answer
        """
        url = "{}/users/{}/licenses".format(Bintray.BINTRAY_URL, user)
        return self._requester.post(url, json=license)

    def update_org_proprietary_license(self, org, custom_license_name, license):
        """ Update a license associated with an organization.
            Caller must be an admin of the organization.

        :param org: Organization name
        :param custom_license_name: License to be updated
        :param license: JSON data with license information
        :return: request answer
        """
        url = "{}/orgs/{}/licenses/{}".format(Bintray.BINTRAY_URL, org, custom_license_name)
        return self._requester.patch(url, json=license)

    def update_user_proprietary_license(self, user, custom_license_name, license):
        """ Update a license associated with an user.

        :param user: User name
        :param custom_license_name: License to be updated
        :param license: JSON data with license information
        :return: request answer
        """
        url = "{}/users/{}/licenses/{}".format(Bintray.BINTRAY_URL, user, custom_license_name)
        return self._requester.patch(url, json=license)

    def delete_org_proprietary_license(self, org, custom_license_name):
        """ Delete a license associated with an organization.
            For organization, caller must be an admin of the organization.

        :param org: Organization name
        :param custom_license_name: License name to be deleted
        :return: request answer
        """
        url = "{}/orgs/{}/licenses/{}".format(Bintray.BINTRAY_URL, org, custom_license_name)
        return self._requester.delete(url)

    def delete_user_proprietary_license(self, user, custom_license_name):
        """ Delete a license associated with an user.

        :param user: User name
        :param custom_license_name: License to be deleted
        :return: request answer
        """
        url = "{}/users/{}/licenses/{}".format(Bintray.BINTRAY_URL, user, custom_license_name)
        return self._requester.delete(url)

    def get_oss_licenses(self):
        """ Returns a list of all the OSS licenses.

        :return: List with OSS licenses
        """
        url = "{}/licenses/oss_licenses".format(Bintray.BINTRAY_URL)
        return self._requester.get(url)
