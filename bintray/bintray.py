# -*- coding: utf-8 -*-
""" Python Wrapper for Bintray API

    https://bintray.com/docs/api
"""
import os

from bintray.requester import Requester
from bintray.logger import Logger
from bintray.utils import bool_to_number


__version__ = "0.7.0"
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

    def create_org_proprietary_license(self, org, name, description, url):
        """ Create a license associated with an organization.
            Caller must be an admin of the organization.

        :param org: Organization name
        :param name: license name
        :param description: license description
        :param url: license url
        :return: request answer
        """
        url_request = "{}/orgs/{}/licenses".format(Bintray.BINTRAY_URL, org)
        json_data = {
            'name': name,
            'description': description,
            'url': url
        }
        return self._requester.post(url_request, json=json_data)

    def create_user_proprietary_license(self, user, name, description, url):
        """ Create a license associated with an user.

        :param user: User name
        :param name: license name
        :param description: license description
        :param url: license url
        :return: request response
        """
        url_request = "{}/users/{}/licenses".format(Bintray.BINTRAY_URL, user)
        json_data = {
            'name': name,
            'description': description,
            'url': url
        }
        return self._requester.post(url_request, json=json_data)

    def update_org_proprietary_license(self, org, custom_license_name, description=None, url=None):
        """ Update a license associated with an organization.
            Caller must be an admin of the organization.

        :param org: Organization name
        :param custom_license_name: License to be updated
        :param description: license description
        :param url: license url
        :return: request answer
        """
        request_url = "{}/orgs/{}/licenses/{}".format(Bintray.BINTRAY_URL, org, custom_license_name)
        json_data = {}
        if isinstance(description, str):
            json_data["description"] = description
        if isinstance(url, str):
            json_data["url"] = url
        return self._requester.patch(request_url, json=json_data)

    def update_user_proprietary_license(self, user, custom_license_name, description=None,
                                        url=None):
        """ Update a license associated with an user.

        :param user: User name
        :param custom_license_name: License to be updated
        :param description: license description
        :param url: license url
        :return: request answer
        """
        request_url = "{}/users/{}/licenses/{}".format(Bintray.BINTRAY_URL, user,
                                                       custom_license_name)
        json_data = {}
        if isinstance(description, str):
            json_data["description"] = description
        if isinstance(url, str):
            json_data["url"] = url

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        return self._requester.patch(request_url, json=json_data)

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

    # Content Signing

    def get_org_gpg_public_key(self, org):
        """ Get the organization GPG public key.

            The response Content-Type format is 'application/pgp-keys'.

        :param org: Organization name
        :return: response Content-Type format as 'application/pgp-keys'.
        """
        url = "{}/orgs/{}/keys/gpg/public.key".format(Bintray.BINTRAY_URL, org)
        return self._requester.get(url)

    def get_user_gpg_public_key(self, user):
        """ Get the subject GPG public key.

            The response Content-Type format is 'application/pgp-keys'.

        :param org: Organization name
        :return: response Content-Type format as 'application/pgp-keys'.
        """
        url = "{}/users/{}/keys/gpg/public.key".format(Bintray.BINTRAY_URL, user)
        return self._requester.get(url)

    def gpg_sign_version(self, subject, repo, package, version, key_subject=None, passphrase=None,
                         key_path=None):
        """ GPG sign all files associated with the specified version.

            GPG signing information may be needed

            Security: Authenticated user with 'publish' permission.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param key_subject: Alternative Bintray subject for the GPG public key
        :param passphrase: Optional private key passphrase, if required
        :param key_path: Optional private key, if not stored in Bintray
        :return: request response
        """
        url = "{}/gpg/{}/{}/{}/versions/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                   version)
        body = {}
        if subject:
            body['subject'] = key_subject
        if passphrase:
            body['passphrase'] = passphrase
        if key_path:
            with open(key_path, 'r') as fd:
                body['private_key'] = fd.read()
        body = None if body == {} else body
        headers = None
        if "passphrase" in body and len(body.keys()) == 1:
            headers = {"X-GPG-PASSPHRASE": passphrase}
            body = None

        response = self._requester.post(url, json=body, headers=headers)

        self._logger.info("Sign successfully: {}".format(url))
        return response

    def gpg_sign_file(self, subject, repo, file_path, key_subject=None, passphrase=None,
                      key_path=None):
        """ GPG sign the specified repository file.

            GPG signing information may be needed

        :param subject: username or organization
        :param repo: repository name
        :param file_path: file path to be signed
        :param key_subject: Alternative Bintray subject for the GPG public key
        :param passphrase: Optional private key passphrase, if required
        :param key_path: Optional private key, if not stored in Bintray
        :return: request response
        """
        url = "{}/gpg/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        body = {}
        if subject:
            body['subject'] = key_subject
        if passphrase:
            body['passphrase'] = passphrase
        if key_path:
            with open(key_path, 'r') as fd:
                body['private_key'] = fd.read()
        body = None if body == {} else body
        headers = None
        if "passphrase" in body and len(body.keys()) == 1:
            headers = {"X-GPG-PASSPHRASE": passphrase}
            body = None

        response = self._requester.post(url, json=body, headers=headers)

        self._logger.info("Sign successfully: {}".format(url))
        return response

    # Content Sync

    def sync_version_artifacts_to_maven_central(self, subject, repo, package, version, username,
                                                password, close="1"):
        """ Sync version files to a oss.sonatype.org staging repository to publish these files to
            Maven Central.

            Once Sonatype oss credentials have been set in subject "Accounts" tab, user can send
            this rest call without specifying username and password (or use different
            username/password by specifying them in JSON body)

            By default the staging repository is closed and artifacts are released to Maven Central.
            You can optionally turn this behaviour off and release the version manually.
            This is achieved by passing 0 in the 'close' field of the JSON passed to the call.

            Security: Authenticated user with 'publish' permission.

        :param subject: username or organization
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param username: Sonatype OSS user token
        :param password: Sonatype OSS user password
        :param close: staging repository mode
        :return: request response
        """
        url = "{}/maven_central_sync/{}/{}/{}/versions/{}".format(Bintray.BINTRAY_URL, subject,
                                                                  repo, package, version)
        body = {
            'username': username,
            'password': password,
            'close': close
        }

        return self._requester.post(url, json=body)

    # Repositories

    def get_repositories(self, subject):
        """ Get a list of repos writable by subject (personal or organizational)

            Security: Authenticated user with 'read' permission for private repositories,
                      or repository read entitlement.

        :param subject: subject name
        :return: A list of repositories
        """
        url = "{}/repos/{}".format(Bintray.BINTRAY_URL, subject)
        return self._requester.get(url)

    def get_repository(self, subject, repo):
        """ Get general information about a repository of the specified user

            Security: Authenticated user with 'read' permission for private repositories,
                      or repository read entitlement.

        :param subject: Subject name
        :param repo: Repository name
        :return: Repository information
        """
        url = "{}/repos/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        return self._requester.get(url)

    def create_repository(self, subject, repo, type, description, private=False, labels=None,
                          gpg_sign_metadata=False, gpg_sign_files=False, gpg_use_owner_key=False,
                          business_unit=None, version_update_max_days=None):
        """ Create a repository under to the specified subject.

            The possible types for a repository are: maven, debian, conan, rpm, docker, npm, opkg,
            nuget, vagrant and generic (default).

            GPG auto sign flags - they let you specify whether GPG signing should be applied to this
            repo. auto signing with gpg is disabled by default.

        :param subject: repository owner
        :param repo: repository name
        :param type: repository type
        :param private: True to private repository (premium account). Otherwise, False.
        :param description: repository description
        :param labels: repository labels (tags)
        :param gpg_sign_metadata:  if set to true then the repo’s metadata will be automatically
                                   signed with Bintray GPG key.
        :param gpg_sign_files: if set to true then the repo’s files will be automatically signed
                               with Bintray GPG key.
        :param gpg_use_owner_key: if set to true then the repo’s metadata and files will be signed
                                  automatically with the owner’s GPG key. this flag cannot be set
                                  true simultaneously with either of the bintray key falgs (files or
                                  metadata). this flag can be set true only if the repo’s owner
                                  supplied a private (and public) GPG key on his bintray profile.
        :param business_unit:  can be associated to repositories allowing you to monitor overall
                               usage per business unit.
        :param version_update_max_days: Number of days after the version is published in which an
                                        organization member can upload, override or delete files in
                                        the version, delete the version or its package. After this
                                        period these actions are not available to the member.
                                        This does not apply to the Admin of the repository who can
                                        make changes to the version at any time after it is published
        :return: Request response
        """
        assert isinstance(private, bool), "private must be a boolean value [True, False]"
        url = "{}/repos/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {
            'name': repo,
            'type': type,
            'private': private,
            'desc': description,
            'gpg_sign_metadata': gpg_sign_metadata,
            'gpg_sign_files': gpg_sign_files,
            'gpg_use_owner_key': gpg_use_owner_key
        }
        if labels:
            assert isinstance(labels, list), "labels must be a list e.g. ['label1', 'label2']"
            json_data['labels'] = labels
        if business_unit:
            json_data['business_unit'] = business_unit
        if isinstance(version_update_max_days, int) or version_update_max_days:
            json_data['version_update_max_days'] = int(version_update_max_days)

        response = self._requester.post(url, json=json_data)
        self._logger.info("Repository {} created successfully".format(repo))
        return response

    def update_repository(self, subject, repo, business_unit=None, description=None, labels=None,
                          gpg_sign_metadata=None, gpg_sign_files=None, gpg_use_owner_key=None,
                          version_update_max_days=None):
        """ Update a repository under the specified subject


        :param subject: repository owner
        :param repo: repository name
        :param description: repository description
        :param labels: repository labels (tags)
        :param gpg_sign_metadata:  if set to true then the repo’s metadata will be automatically
                                   signed with Bintray GPG key.
        :param gpg_sign_files: if set to true then the repo’s files will be automatically signed
                               with Bintray GPG key.
        :param gpg_use_owner_key: if set to true then the repo’s metadata and files will be signed
                                  automatically with the owner’s GPG key. this flag cannot be set
                                  true simultaneously with either of the bintray key falgs (files or
                                  metadata). this flag can be set true only if the repo’s owner
                                  supplied a private (and public) GPG key on his bintray profile.
        :param business_unit:  can be associated to repositories allowing you to monitor overall
                               usage per business unit.
        :param version_update_max_days: Number of days after the version is published in which an
                                        organization member can upload, override or delete files in
                                        the version, delete the version or its package. After this
                                        period these actions are not available to the member.
                                        This does not apply to the Admin of the repository who can
                                        make changes to the version at any time after it is published
        :return: Request response
        """
        url = "{}/repos/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {}

        if isinstance(business_unit, str):
            json_data["business_unit"] = business_unit
        if isinstance(description, str):
            json_data["desc"] = description
        if isinstance(labels, list):
            json_data["labels"] = labels
        if isinstance(gpg_sign_metadata, bool):
            json_data["gpg_sign_metadata"] = gpg_sign_metadata
        if isinstance(gpg_sign_files, bool):
            json_data["gpg_sign_files"] = gpg_sign_files
        if isinstance(gpg_use_owner_key, bool):
            json_data["gpg_use_owner_key"] = gpg_use_owner_key
        if isinstance(version_update_max_days, int):
            json_data["version_update_max_days"] = version_update_max_days

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Repository {} updated successfully".format(repo))
        return response

    def delete_repository(self, subject, repo):
        """ Delete the specified repository under the specified subject

        :param subject: subject name
        :param repo: repo name
        :return: request response
        """
        url = "{}/repos/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.delete(url)
        self._logger.info("Repository {} deleted successfully".format(repo))
        return response

    def search_repository(self, name=None, description=None):
        """ Search for a repository.

            At least one of the name and desc search fields need to be specified.

            Returns an array of results, where elements are similar to the result of getting a
            single repository.

            Search results will not contain private repositories.

            Security: Authenticated user is required

        :param name: repository name
        :param description: repository name
        :return: request response
        """
        url = "{}/search/repos".format(Bintray.BINTRAY_URL)
        params = {}
        if name:
            params["name"] = name
        if description:
            params["desc"] = description

        if not params:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.get(url, params=params)
        self._logger.info("Repository {} searched successfully".format(params))
        return response

    def link_package(self, subject, repo, source_subject, source_repo, source_package,
                     path_prefix=None):
        """ Link the package source_package into the repo repository.

            Caller must be an admin of the organization owning the repository.

        :param subject: target subject name
        :param repo: target subject repository
        :param source_subject: source subject
        :param source_repo: source repository
        :param source_package: source package name
        :param path_prefix: path to include the files from
        :return: request response
        """
        url = "{}/repository/{}/{}/links/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                          source_subject, source_repo,
                                                          source_package)
        json_data = {"path_prefix": path_prefix} if path_prefix else None

        response = self._requester.put(url, json=json_data)
        self._logger.info("Link package successfully")
        return response

    def unlink_package(self, subject, repo, source_subject, source_repo, source_package):
        """ Unlink the package source_package from the repo repository.

            Caller must be an admin of the organization owning the repository.

        :param subject: target subject name
        :param repo: target subject repository
        :param source_subject: source subject
        :param source_repo: source repository
        :param source_package: source package name
        :return: request response
        """
        url = "{}/repository/{}/{}/links/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                          source_subject, source_repo,
                                                          source_package)
        response = self._requester.delete(url)
        self._logger.info("Unlink package successfully")
        return response

    def schedule_metadata_calculation(self, subject, repo, path=None):
        """ Schedule metadata (index) calculation for the specified repository.

            For a Maven repository you need to specify the path in the repository for which the
            metadata should be calculated. For an RPM repository, you need to specify the path
            according to the repository 'YUM Metadata Folder Depth' field, if different from zero.
            For other repository types the path is ignored.

            Security: Authenticated user with 'publish' permission, or repository read/write
            entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param path: path in the repository
        :return: request response
        """
        url = "{}/calc_metadata/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        if path:
            url += '/' + path

        response = self._requester.post(url)
        self._logger.info("Schedule metadata successfully")
        return response

    def get_geo_restrictions(self, subject, repo):
        """ Get the list of countries which are defined in the 'black_list' or in the 'white_list'.

            This feature is limited to users with Enterprise account.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :return: request response
        """
        url = "{}/repos/{}/{}/geo_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def update_geo_restrictions(self, subject, repo, white_list=[], black_list=[]):
        """ Update the 'black_list' or 'white_list' with the related countries code.

            This feature is limited to users with Enterprise account.

            The update can be done on one list only.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param white_list: Countries in white list e.g. ["US", "CA"]
        :param black_list: Countries in black list e.g. ["RU", "BR"]
        :return: request response
        """
        url = "{}/repos/{}/{}/geo_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {}
        if white_list and black_list:
            raise ValueError("The update can be done on one list only.")
        if white_list:
            json_data["white_list"] = white_list
        if black_list:
            json_data["black_list"] = black_list
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")
        response = self._requester.put(url, json=json_data)
        self._logger.put("Update successfully")
        return response

    def delete_geo_restrictions(self, subject, repo):
        """ Remove all the countries from the 'white_list' and 'black_list'.

            This feature is limited to users with Enterprise account.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :return: request response
        """
        url = "{}/repos/{}/{}/geo_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.delete(url)
        self._logger.put("Delete successfully")
        return response

    def get_ip_restrictions(self, subject, repo):
        """ Gets whitelisted and blacklisted CIDRs.

        :param subject: repository owner
        :param repo: repository name
        :return: request response
        """
        url = "{}/repos/{}/{}/ip_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def set_ip_restrictions(self, subject, repo, white_cidrs=None, black_cidrs=None):
        """ Update ip restrictions with the given white list and black list of CIDRs.

        :param subject: repository owner
        :param repo: repository name
        :param white_cidrs: white list for CIDRs
        :param black_cidrs: black list for CIDRs
        :return: request response
        """
        url = "{}/repos/{}/{}/ip_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {}
        if isinstance(white_cidrs, list):
            json_data["white_cidrs"] = white_cidrs
        if isinstance(black_cidrs, list):
            json_data["black_cidrs"] = black_cidrs
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.put(url, json=json_data)
        self._logger.info("Set successfully")
        return response

    def update_ip_restrictions(self, subject, repo, add_white_cidrs=None, rm_white_cidrs=None,
                               add_black_cidrs=None, rm_black_cidrs=None):
        """ Add or remove CIDRs from black/white list restrictions.

        :param subject: repository owner
        :param repo: repository name
        :param add_white_cidrs: CIDRs to be added in the white list
        :param rm_white_cidrs: CIDRs to be removed from the white list
        :param add_black_cidrs: CIDRs to be added in the black list
        :param rm_black_cidrs: CIDRs to be removed from the black list
        :return: request response
        """
        url = "{}/repos/{}/{}/ip_restrictions".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {}
        if isinstance(add_white_cidrs, list):
            json_data["add"] = {"white_cidrs": add_white_cidrs}
        if isinstance(add_black_cidrs, list):
            json_data["add"] = {"black_cidrs": add_black_cidrs}

        if isinstance(rm_white_cidrs, list):
            json_data["remove"] = {"white_cidrs": rm_white_cidrs}
        if isinstance(rm_black_cidrs, list):
            json_data["remove"] = {"black_cidrs": rm_black_cidrs}

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Update successfully")
        return response

    def delete_ip_restrictions(self, subject, repo):
        """ Removes all restrictions, black and white.

        :param subject: repository owner
        :param repo: repository name
        :return: request response
        """
        url = "{}/repos/{}/{}/ip_restrictions".format(Bintray.BINTRAY_URL, subject, repo)

        response = self._requester.delete(url)
        self._logger.info("Update successfully")
        return response

    # Versions

    def get_version(self, subject, repo, package, version="_latest", attribute_values=True):
        """ Get general information about a specified version, or query for the latest version that
            has at least one file published to it.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param attribute_values: show attributes
        :return: request response + package version information
        """
        url = "{}/packages/{}/{}/{}/versions/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                        package, version)
        params = {"attribute_values": bool_to_number(attribute_values)}
        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def create_version(self, subject, repo, package, version, description=None,
                       released=None, github_release_notes_file=None,
                       github_use_tag_release_notes=None, vcs_tag=None):
        """ Creates a new version in the specified package (user has to be owner of the package)

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: version name
        :param description: version description
        :param released: release date ISO8601
        :param github_release_notes_file: file path for release notes e.g. RELEASE.txt
        :param github_use_tag_release_notes: True when contain release notes file
        :param vcs_tag: tag name in VCS
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/versions".format(Bintray.BINTRAY_URL, subject, repo, package)
        json_data = {'name': version}
        if isinstance(description, str):
            json_data["desc"] = description
        if isinstance(released, str):
            json_data["released"] = released
        if isinstance(github_release_notes_file, str):
            json_data["github_release_notes_file"] = github_release_notes_file
        if isinstance(github_use_tag_release_notes, bool):
            json_data["github_use_tag_release_notes"] = github_use_tag_release_notes
        if isinstance(vcs_tag, str):
            json_data["vcs_tag"] = vcs_tag

        response = self._requester.post(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def delete_version(self, subject, repo, package, version):
        """ Delete the specified version

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: version to be deleted
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/versions/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                        version)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def update_version(self, subject, repo, package, version, description=None,
                        github_release_notes_file=None, github_use_tag_release_notes=None,
                        vcs_tag=None):
        """ Update the information of the specified version

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: version name to be updated
        :param description: version description
        :param github_release_notes_file: file path for release notes e.g. RELEASE.txt
        :param github_use_tag_release_notes: True when contain release notes file
        :param vcs_tag: tag name in VCS
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/versions/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                        package, version)
        json_data = {}
        if isinstance(description, str):
            json_data["desc"] = description
        if isinstance(github_release_notes_file, str):
            json_data["github_release_notes_file"] = github_release_notes_file
        if isinstance(github_use_tag_release_notes, bool):
            json_data["github_use_tag_release_notes"] = github_use_tag_release_notes
        if isinstance(vcs_tag, str):
            json_data["vcs_tag"] = vcs_tag

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def version_for_file(self, subject, repo, file_path):
        """ Get general information about the version a repository file is associated with.

            Security: Non-authenticated user.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: associated file path
        :return: request response
        """
        url = "{}/file_version/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response
