# -*- coding: utf-8 -*-
""" Python Wrapper for Bintray API

    https://bintray.com/docs/api
"""
import os

from bintray.requester import Requester
from bintray.logger import Logger
from bintray.utils import bool_to_number


__version__ = "0.4.0"
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
        """ Upload content to the specified repository path, with package and version information.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param remote_file_path: file name to be used on Bintray
        :param local_file_path: file path to be uploaded
        :param publish: publish after uploading
        :param override: override remote file
        :param explode: explode remote file
        :return: Request response
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

    def maven_upload(self, subject, repo, package, remote_file_path, local_file_path, publish=True,
                     passphrase=None):
        """ Upload Maven artifacts to the specified repository path, with package information.

            Version information is resolved from the path, which is expected to follow the Maven
            layout.

            You may supply a passphrase for signing uploaded files using the X-GPG-PASSPHRASE header

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param remote_file_path: file name to be used on Bintray
        :param local_file_path: file path to be uploaded
        :param publish: publish after uploading
        :param passphrase: GPG passphrase
        :return: Request response
        """
        url = "{}/maven/{}/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                            remote_file_path)
        parameters = {"publish": bool_to_number(publish)}
        headers = {"X-GPG-PASSPHRASE": passphrase} if passphrase else None

        with open(local_file_path, 'rb') as file_content:
            response = self._requester.put(url, params=parameters, data=file_content,
                                           headers=headers)

        self._logger.info("Upload successfully: {}".format(url))
        return response

    def debian_upload(self, subject, repo, package, version, remote_file_path, local_file_path,
                      deb_distribution, deb_component, deb_architecture, publish=True,
                      override=False, passphrase=None):
        """ Upload Debian artifacts to the specified repository path, with package information.

            When artifacts are uploaded to a Debian repository using the Automatic index layout,
            the Debian distribution information is required and must be specified.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param remote_file_path: file name to be used on Bintray
        :param local_file_path: file path to be uploaded
        :param deb_distribution: Debian package distribution e.g. wheezy
        :param deb_component: Debian package component e.g. main
        :param deb_architecture: Debian package architecture e.g. i386,amd64
        :param publish: publish after uploading
        :param override: override remote file
        :param passphrase: GPG passphrase
        :return: Request response
        """
        url = "{}/content/{}/{}/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                 version, remote_file_path)
        parameters = {"publish": bool_to_number(publish),
                      "override": bool_to_number(override)}
        headers = {
            "X-Bintray-Debian-Distribution": deb_distribution,
            "X-Bintray-Debian-Component": deb_component,
            "X-Bintray-Debian-Architecture": deb_architecture
        }
        if passphrase:
            headers["X-GPG-PASSPHRASE"] = passphrase

        with open(local_file_path, 'rb') as file_content:
            response = self._requester.put(url, params=parameters, data=file_content,
                                           headers=headers)

        self._logger.info("Upload successfully: {}".format(url))
        return response

    def _publish_discard_uploaded_content(self, subject, repo, package, version, discard=False,
                                          publish_wait_for_secs=-1, passphrase=None):
        """ Asynchronously publishes all unpublished content for a user’s package version. Returns
            the number of to-be-published files.

            In order to wait for publishing to finish and run this call synchronously, specify a
            "publish_wait_for_secs" timeout in seconds. To wait for the maximum timeout allowed by
            Bintray use a wait value of -1 . A wait value of 0 is the default and is the same as
            running this call asynchronously without waiting.

            Optionally, pass in a "discard" flag to discard any unpublished content, instead of
            publishing.

            Automatic Signing for Repository Metadata

            For repositories that support automatic calculation of repository metadata (such as
            Debian and YUM), you may supply signing required information.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param discard: Discard package
        :param publish_wait_for_secs: Publishing timeout
        :param passphrase: GPG passphrase
        :return: Request response
        """
        url = "{}/content/{}/{}/{}/{}/publish".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                      version)
        body = {'discard': discard,
                'publish_wait_for_secs': publish_wait_for_secs}
        headers = {"X-GPG-PASSPHRASE": passphrase} if passphrase else None

        response = self._requester.post(url, json=body, headers=headers)

        self._logger.info("Publish/Discard successfully: {}".format(url))
        return response

    def publish_uploaded_content(self, subject, repo, package, version, passphrase=None):
        """ Asynchronously publishes all unpublished content for a user’s package version.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param passphrase: GPG passphrase
        :return: the number of to-be-published files.
        """
        return self._publish_discard_uploaded_content(subject, repo, package, version,
                                                      discard=False, passphrase=passphrase)

    def discard_uploaded_content(self, subject, repo, package, version, passphrase=None):
        """ Asynchronously discard all unpublished content for a user’s package version.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param passphrase: GPG passphrase
        :return: the number of discarded files.
        """
        return self._publish_discard_uploaded_content(subject, repo, package, version,
                                                      discard=True, passphrase=passphrase)

    def delete_content(self, subject, repo, file_path):
        """ Delete content from the specified repository path,

            Currently supports only deletion of files.
            For OSS, this action is limited for 180 days from the content’s publish date.

            Security: Authenticated user with 'publish' permission, or read/write entitlement for a
            repository path

        :param subject: username or organization
        :param repo: repository name
        :param file_path: file to be deleted
        :return: request response
        """
        url = "{}/content/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.delete(url)

        self._logger.info("Delete successfully: {}".format(url))
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

    def dynamic_download(self, subject, repo, remote_file_path, local_file_path, bt_package=None):
        """ Download a file based on a dynamic file_path .

            This resource is only available for Bintray Premium repositories.

            Currently, only the $latest token is supported, which is useful for downloading the
            latest file published under a specified package.

            Package name can be supplied as a:
                The bt_package query parameter
                The bt_package matrix parameter
                The X-Bintray-Package request header

            A successful call will return a 302 redirect to a generated signed URL
            (with 15 second expiry) to the resolved file path.

        :param subject: username or organization
        :param repo: repository name
        :param remote_file_path: file name to be downloaded from Bintray
        :param local_file_path: file name to be stored in local storage
        :param bt_package: query parameter
        """

        parameters = {"bt_package": bt_package} if bt_package else None
        download_base_url = "https://dl.bintray.com"
        url = "{}/{}/{}/{}".format(download_base_url, subject, repo, remote_file_path)
        response, content = self._requester.download(url, params=parameters)

        with open(local_file_path, 'wb') as local_fd:
            local_fd.write(content)

        self._logger.info("Download successfully: {}".format(url))
        return response

    def url_signing(self, subject, repo, file_path, json_data, encrypt=False):
        """ Generates an anonymous, signed download URL with an expiry date.

            Caller must be an owner of the repository or a publisher in the organization owning
            the repository.

            Encrypted download is possible - encryption will be done using AES 256 CBC, see below
            documentation.

            This resource is only available to Bintray Premium users.

        :param subject: username or organization
        :param repo: repository name
        :param file_path: signed path
        :param json_data: URL data
        :param encrypt: encrypted download
        """

        parameters = {"encrypt": str(encrypt).lower()}
        url = "{}/signed_url/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.post(url, json=json_data, params=parameters)
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
