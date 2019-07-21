""" Python Wrapper for Bintray API

    https://bintray.com/docs/api
"""
import os

from bintray.requester import Requester
from bintray.logger import Logger
from bintray.utils import bool_to_number


__version__ = "0.8.0"
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

    def search_file_by_name(self, name, subject=None, repo=None, start_pos=None,
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

    def search_file_by_checksum(self, sha1, subject=None, repo=None, start_pos=None,
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

    # Readme

    def get_readme(self, subject, repo, package):
        """ Returns the readme for the specified package by subject.
            Either Bintray readme or GitHub readme.

            Security: Authenticated user with 'read' permission for private repositories,
                      or package read entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/readme".format(Bintray.BINTRAY_URL, subject, repo, package)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_readme(self, subject, repo, package, github=None, bintray_syntax=None,
                      bintray_content=None):
        """ Creates a new readme for the specified package by subject.

            "content" has to be passed to the command if using "bintray", or will be retrieved from
            a GitHub repository, when using "github". GitHub repository name has to be provided.

            Security: Authenticated user with 'publish' permission,
                      or package read/write entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param github: Github URL with README
        :param bintray_syntax: Readme syntax e.g. [markdown/asciidoc/plain_text default markdown]
        :param bintray_content: Readme content
        :return: request response
        """
        if github and (bintray_syntax or bintray_content):
            raise ValueError("Only accept github or bintray")

        url = "{}/packages/{}/{}/{}/readme".format(Bintray.BINTRAY_URL, subject, repo, package)
        json_data = {}
        if isinstance(github, str):
            json_data["github"] = {
                "github_repo": github
            }
        if isinstance(bintray_syntax, str) and isinstance(bintray_content, str):
            json_data = {"bintray": {
                    "syntax": bintray_syntax,
                    "content": bintray_content
                }
            }

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.post(url, json_data)
        self._logger.info("Create successfully")
        return response

    def create_product_readme(self, subject, product, github=None, bintray_syntax=None,
                              bintray_content=None):
        """ Sets the readme for all of a product’s underlying packages.

            "content" has to be passed to the command if using "bintray", or will be retrieved from
            a GitHub repository, when using "github". GitHub repository name has to be provided.

            Security: Authenticated user with 'publish' permission,
                      or package read/write entitlement.

        :param subject: repository owner
        :param product: product name
        :param github: Github URL with README
        :param bintray_syntax: Readme syntax e.g. [markdown/asciidoc/plain_text default markdown]
        :param bintray_content: Readme content
        :return: request response
        """
        if github and (bintray_syntax or bintray_content):
            raise ValueError("Only accept github or bintray")

        url = "{}/products/{}/{}/readme".format(Bintray.BINTRAY_URL, subject, product)
        json_data = {}
        if isinstance(github, str):
            json_data["github"] = {
                "github_repo": github
            }
        if isinstance(bintray_syntax, str) and isinstance(bintray_content, str):
            json_data = {"bintray": {
                    "syntax": bintray_syntax,
                    "content": bintray_content
                }
            }

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.post(url, json_data)
        self._logger.info("Create successfully")
        return response

    def delete_product_readme(self, subject, product):
        """ Deletes the readme for all of a product’s underlying packages.

            Security: Authenticated user with 'publish' permission.

        :param subject: repository owner
        :param product: product name
        :return: request response
        """
        url = "{}/products/{}/{}/readme".format(Bintray.BINTRAY_URL, subject, product)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    # Users & Organizations

    def get_user(self, user):
        """ Get information about a specified user

            Security: Get information about a specified user

        :param user: user name
        :return: user information
        """
        url = "{}/users/{}".format(Bintray.BINTRAY_URL, user)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_organization(self, organization):
        """ Get information about a specified organization.

            "type" inside the "members" list is available only to organization admins
            "teams" list is available only to Premium organization admins

            Security: Authenticated user is required

        :param organization: organization name to be searched
        :return: organization information
        """
        url = "{}/orgs/{}".format(Bintray.BINTRAY_URL, organization)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_followers(self, user, start_pos=None):
        """ Get followers of the specified repository owner

            Security: Authenticated user is required

        :param user: user name to be searched
        :param start_pos: initial index position
        :return: follower list
        """
        url = "{}/users/{}/followers".format(Bintray.BINTRAY_URL, user)
        params = None

        if isinstance(start_pos, int):
            params = {"start_pos": start_pos}

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def search_user(self, name):
        """ Search for a user.

            Security: Authenticated user is required

        :param name: name to be searched
        :return: Returns an array of results, where elements are similar to the result of getting a
                 single user.
        """
        url = "{}/search/users".format(Bintray.BINTRAY_URL)
        params = {"name": name}

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    # Webhooks

    def get_webhooks(self, subject, repo=None):
        """ Get all the webhooks registered for the specified subject, optionally for a specific
            repository.

            failure_count is the number of times a callback has failed.
            A callback will be auto-deactivated after 7 subsequent failures.
            A successful callback resets the count.

        :param subject: repository owner
        :param repo: repository name
        :return: list with web hooks
        """
        url = "{}/webhooks/{}".format(Bintray.BINTRAY_URL, subject)
        if isinstance(repo, str):
            url += '/' + repo

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def register_webhook(self, subject, repo, package, url, method):
        """ Register a webhook for receiving notifications on a new package release.

            By default a user can register up to 10 webhook callbacks.
            The callback URL may contain the %r and %p tokens for repo and package name,
            respectively. method is the callback request method: can be in post, put or get.
            If not specified, post is used.

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param url: URL for callback
        :param method: HTTP method for callback e.g. "post"
        :return: request response
        """
        request_url = "{}/webhooks/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        json_data = {
            "url": url,
            "method": method
        }

        response = self._requester.post(request_url, json=json_data)
        self._logger.info("Register successfully")
        return response

    def test_webhook(self, subject, repo, package, version, url, method):
        """ Test a webhook callback for the specified package release.

            A webhook post request is authenticated with an HMAC-SHA256 authentication header of the
            package name keyed by the registering subject’s API key, and base64-encoded.

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repositoy owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param url: URL for callback
        :param method: HTTP method for callback
        :return: request response
        """
        url_requrest = "{}/webhooks/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                     version)
        json_data = {
            "url": url,
            "method": method
        }

        response = self._requester.post(url_requrest, json=json_data)
        self._logger.info("Get successfully")
        return response

    def delete_webhook(self, subject, repo, package):
        """ Delete a user’s webhook associated with the specified package.

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: request response
        """
        url = "{}/webhooks/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    # Teams

    def get_org_teams(self, org):
        """ Get a list of teams associated with an organization

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :return: team list
        """
        url = "{}/orgs/{}/teams".format(Bintray.BINTRAY_URL, org)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_user_teams(self, user):
        """ Get a list of teams associated with an user

            This resource is only available to Bintray Premium users.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :return: team list
        """
        url = "{}/users/{}/teams".format(Bintray.BINTRAY_URL, user)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_org_team(self, org, team):
        """ Get details of a team associated with an organization


            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param team: team name
        :return: team details
        """
        url = "{}/orgs/{}/teams/{}".format(Bintray.BINTRAY_URL, org, team)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_user_team(self, user, team):
        """ Get details of a team associated with an user

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param team: team name
        :return: team details
        """
        url = "{}/users/{}/teams/{}".format(Bintray.BINTRAY_URL, user, team)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_org_team(self, org, name, members, allow_repo_creation=True, business_unit=None):
        """ Create a new team for an organization

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param name: team name
        :param members: list of members to be associated to the team
        :param allow_repo_creation: team members are allowed to create and update repositories.
        :param business_unit: a default business unit can be associated to a team and will be the
                              default business unit for all repositories that are created by this
                              team. A business unit can only be associated with a team if its
                              members are allowed to create repositories.
        :return: request response
        """
        url = "{}/orgs/{}/teams".format(Bintray.BINTRAY_URL, org)
        json_data = {
            'name': name,
            'members': members,
            'allow_repo_creation': allow_repo_creation
        }
        if isinstance(business_unit, str):
            json_data['business_unit'] = business_unit

        response = self._requester.post(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def create_user_team(self, user, name, members, allow_repo_creation=True, business_unit=None):
        """ Create a new team for an user

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param name: team name
        :param members: list of members to be associated to the team
        :param allow_repo_creation: team members are allowed to create and update repositories.
        :param business_unit: a default business unit can be associated to a team and will be the
                              default business unit for all repositories that are created by this
                              team. A business unit can only be associated with a team if its
                              members are allowed to create repositories.
        :return: request response
        """
        url = "{}/users/{}/teams".format(Bintray.BINTRAY_URL, user)
        json_data = {
            'name': name,
            'members': members,
            'allow_repo_creation': allow_repo_creation
        }
        if isinstance(business_unit, str):
            json_data['business_unit'] = business_unit

        response = self._requester.post(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def update_org_team(self, org, team, members=None, allow_repo_creation=None, business_unit=None):
        """ Update a team associated with an organization

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param team: team name
        :param members: list of members to be associated to the team
        :param allow_repo_creation: team members are allowed to create and update repositories.
        :param business_unit: a default business unit can be associated to a team and will be the
                              default business unit for all repositories that are created by this
                              team. A business unit can only be associated with a team if its
                              members are allowed to create repositories.
        :return: request response
        """
        url = "{}/orgs/{}/teams/{}".format(Bintray.BINTRAY_URL, org, team)
        json_data = {}
        if isinstance(members, list):
            json_data['members'] = members
        if isinstance(allow_repo_creation, bool):
            json_data['allow_repo_creation'] = allow_repo_creation
        if isinstance(business_unit, str):
            json_data['business_unit'] = business_unit
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Update successfully")
        return response

    def update_user_team(self, user, team, members=None, allow_repo_creation=None,
                         business_unit=None):
        """ Update a team associated with an user

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param team: team name
        :param members: list of members to be associated to the team
        :param allow_repo_creation: team members are allowed to create and update repositories.
        :param business_unit: a default business unit can be associated to a team and will be the
                              default business unit for all repositories that are created by this
                              team. A business unit can only be associated with a team if its
                              members are allowed to create repositories.
        :return: request response
        """
        url = "{}/users/{}/teams/{}".format(Bintray.BINTRAY_URL, user, team)
        json_data = {}
        if isinstance(members, list):
            json_data['members'] = members
        if isinstance(allow_repo_creation, bool):
            json_data['allow_repo_creation'] = allow_repo_creation
        if isinstance(business_unit, str):
            json_data['business_unit'] = business_unit
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Update successfully")
        return response

    def delete_org_team(self, org, team):
        """ Delete a team associated with an organization

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param team: team name
        :return: request response
        """
        url = "{}/orgs/{}/teams/{}".format(Bintray.BINTRAY_URL, org, team)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def delete_user_team(self, user, team):
        """ Delete a team associated with an user

            This resource is only available to Bintray Premium users.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param team: team name
        :return: request response
        """
        url = "{}/users/{}/teams/{}".format(Bintray.BINTRAY_URL, user, team)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def get_all_team_permissions(self, subject, repo):
        """ Get the permissions defined for teams on the specified repository

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :return: request response
        """
        url = "{}/repos/{}/{}/permissions".format(Bintray.BINTRAY_URL, subject, repo)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_team_permissions(self, subject, repo, team):
        """ Get the permissions defined for a team on the specified repository

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param team: team name
        :return: request response
        """
        url = "{}/repos/{}/{}/permissions/{}".format(Bintray.BINTRAY_URL, subject, repo, team)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def set_team_permissions(self, subject, repo, team, permission):
        """ Set the permissions defined for a team on the specified repository.


            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param team: team name
        :param permission: permission type e.g. "read", "write"
        :return: request response
        """
        url = "{}/repos/{}/{}/permissions".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {"team": team, "permission": permission}

        response = self._requester.put(url, json=json_data)
        self._logger.info("Set successfully")
        return response

    def delete_team_permission(self, subject, repo, team):
        """ Delete the permission defined for a team on the specified repository

            This resource is only available to Bintray Premium users.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param team: team name
        :return: request response
        """
        url = "{}/repos/{}/{}/permissions/{}".format(Bintray.BINTRAY_URL, subject, repo, team)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    # EULAs (This resource is only available to Bintray Enterprise users.)

    def get_eulas(self, subject, product):
        """ Get a list of EULAs for the specified product.

            This resource is only available to Bintray Enterprise users.

            Security: Authenticated user with 'read' permission for private repositories, or
                      repository read entitlement.

        :param subject: repository owner
        :param product: product name
        :return: List of EULAs
        """
        url = "{}/products/{}/{}/eulas".format(Bintray.BINTRAY_URL, subject, product)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_eula(self, subject, product, eula):
        """ Returns the specified product EULA.

            This resource is only available to Bintray Enterprise users.

            Security: Authenticated user with 'read' permission for private repositories, or
                      repository read entitlement.

        :param subject: repository owner
        :param product: product name
        :param eula: EULA name
        :return: Dictionary with EULA details
        """
        url = "{}/products/{}/{}/eulas/{}".format(Bintray.BINTRAY_URL, subject, product, eula)

        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_eula(self, subject, product, name, syntax, content, versions, default=False):
        """ Create a EULA for the given subject, with the given product.

            A new EULA will apply to all new versions if the 'default' parameter is specified.

            This resource is only available to Bintray Enterprise users.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param product: product name
        :param name: EULA name
        :param syntax: EULA syntax [markdown/asciidoc/plain_text default markdown]
        :param content: EULA content
        :param versions: product versions to use this new EULA
        :param default: True if all product versions should use same EULA.
        :return: request response
        """
        url = "{}/products/{}/{}/eulas".format(Bintray.BINTRAY_URL, subject, product)
        json_data = {
            "name": name,
            "syntax": syntax,
            "content": content,
            "default": default
        }
        if isinstance(versions, list):
            json_data["versions"] = versions

        response = self._requester.post(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def update_eula(self, subject, product, eula, syntax, content, versions, default=False):
        """ Update a EULA under a specified subject and product.

            A new EULA will apply to all new versions if the 'default' parameter is specified.

            This resource is only available to Bintray Enterprise users.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param product: product name
        :param eula: EULA name
        :param syntax: EULA syntax [markdown/asciidoc/plain_text default markdown]
        :param content: EULA content
        :param versions: product versions to use this new EULA
        :param default: True if all product versions should use same EULA.
        :return: request response
        """
        url = "{}/products/{}/{}/eulas/{}".format(Bintray.BINTRAY_URL, subject, product, eula)
        json_data = {}
        if isinstance(syntax, str):
            json_data["syntax"] = syntax
        if isinstance(content, str):
            json_data["content"] = content
        if isinstance(default, bool):
            json_data["default"] = default
        if isinstance(versions, list):
            json_data["versions"] = versions
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def delete_eula(self, subject, product, eula):
        """ Delete the specified EULA under the specified subject and product.

            This resource is only available to Bintray Enterprise users.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param product: product name
        :param eula: eula name to be removed
        :return: request response
        """
        url = "{}/products/{}/{}/eulas/{}".format(Bintray.BINTRAY_URL, subject, product, eula)

        response = self._requester.delete(url)
        self._logger.info("Delete successfully")

    # Subjects (This resource is only available to Bintray Premium users.)

    def regenerate_subject_url_signing_key(self, subject):
        """ Re-generates Subject key for URL Signing.

            This resource is only available to Bintray Premium users.
            For organization, caller must be an admin of the organization.

            Note: regenerating the URL signing key will revoke all active signed URLs.

        :param subject: repository owner
        :return: request response
        """
        url = "{}/subjects/{}/keypair".format(Bintray.BINTRAY_URL, subject)

        response = self._requester.post(url)
        self._logger.info("Generate successfully")
        return response

    # Attributes

    def get_attributes(self, subject, repo, package, version=None, attributes=None):
        """ Get attributes associated with the specified package or version.

            If no attribute names are specified, return all attributes.

            Note: Dates are defined in ISO8601 format.

            Security: Authenticated user with 'read' permission for private repositories,
                      or version/package read entitlement for the corresponding calls.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (optional)
        :param attributes: attributes to be listed
        :return: a list of attributes
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        if version:
            url += "/versions/{}".format(version)
        url += "/attributes"

        params = None
        if attributes:
            params = {"names": ",".join(attributes)}

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def set_attributes(self, subject, repo, package, version=None, attributes=None):
        """ Associate attributes with the specified package or version, overriding all previous
            attributes.

            Optionally, specify an attribute type. Otherwise, type will be inferred from the
            attribute’s value. If a type cannot be inferred, string type will be used.
            Non-homogeneous arrays are not accepted. Attributes names beginning with an underscore
            ("_") will only be visible for users with publish rights. Attribute types can be one of
            the following: string, date, number, boolean, version version currently behaves like
            string. This will change with future Bintray versions.

            Security: Authenticated user with 'publish' permission for private repositories, or
                      version/package read/write entitlement for the corresponding calls.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (optional)
        :param attributes: attributes to be configured [{"name":"att1", "values":["val1"],
                                                         "type": "string"}]
        :return: request response
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        if version:
            url += "/versions/{}".format(version)
        url += "/attributes"

        response = self._requester.post(url, json=attributes)
        self._logger.info("Set successfully")
        return response

    def update_attributes(self, subject, repo, package, version=None, attributes=None):
        """ Update attributes associated with the specified package or version.

            Attributes may have a null value. Optionally, specify an attribute type. Otherwise,
            type will be inferred from the attribute’s value. If a type cannot be inferred, string
            type will be used. Non-homogeneous arrays are not accepted. Attribute types can be one
            of the following: string, date, number, boolean, version version currently behaves like
            string. This will change with future Bintray versions.

            Security: Authenticated user with 'publish' permission for private repositories, or
                      version/package read/write entitlement for the corresponding calls.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (optional)
        :param attributes: attributes to be configured [{"name":"att1", "values":["val1"],
                                                         "type": "string"}]
        :return: request response
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        if version:
            url += "/versions/{}".format(version)
        url += "/attributes"

        response = self._requester.patch(url, json=attributes)
        self._logger.info("Update successfully")
        return response

    def delete_attributes(self, subject, repo, package, version=None, attributes=None):
        """ Delete attributes associated with the specified repo, package or version.

            If no attribute names are specified, delete all attributes.

            Security: Authenticated user with 'publish' permission for private repositories, or
                      version/package read/write entitlement for the corresponding calls.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (optional)
        :param attributes: attributes to be deleted [{"name":"att1", "values":["val1"],
                                                         "type": "string"}]
        :return: request response
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        if version:
            url += "/versions/{}".format(version)
        url += "/attributes"

        params = {"names": ",".join(attributes)}

        response = self._requester.delete(url, params=params)
        self._logger.info("Delete successfully")
        return response

    def search_attributes(self, subject, repo, package=None, attributes=None,
                          attribute_values=True):
        """ Search for packages/versions inside a given repository matching a set of attributes.

            The AND operator will be used when using multiple query clauses, for example attribute
            A equals X and attribute B is greater than Z When an array value is used, if the
            existing attribute value is a scalar match against one of the array values; if the
            existing attribute value is an array check that the existing array contains the query
            array.

            Note: The values range is defined by the brackets direction and the comma position.

            Security: Authenticated user with 'publish' permission for private repositories, or
                      version/package read/write entitlement for the corresponding calls.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (optional)
        :param attributes: attributes to be searched
        :param attribute_values: True to search attribute values
        :return: Returns an array of results
        """
        url = "{}/search/attributes/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        if package:
            url += "/{}/versions".format(package)

        params = {"attribute_values": bool_to_number(attribute_values)}

        response = self._requester.post(url, params=params, json=attributes)
        self._logger.info("Search successfully")
        return response

    def get_file_attributes(self, subject, repo, file_path):
        """ Returns all the attributes related to Artifact.

            This resource can be consumed by both authenticated and anonymous users.

            Security: Authenticated user with 'read' permission, or repository read entitlement for
                      repository path.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: file to be checked
        :return: a list of attributes
        """
        url = "{}/files/{}/{}/{}/attributes".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def set_file_attributes(self, subject, repo, file_path, attributes):
        """ Set attributes associated with the specified Artifact.

            Overriding all previous attributes.

            Security: Authenticated user with 'publish' permission, or write entitlement for
                      repository path.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: file to be checked
        :param attributes: attributes to be configured
        :return: request response
        """
        url = "{}/files/{}/{}/{}/attributes".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.post(url, json=attributes)
        self._logger.info("Set successfully")
        return response

    def update_file_attributes(self, subject, repo, file_path, attributes):
        """ Update the Artifact with new attributes without removing the older Artifact’s attributes

            Security: Authenticated user with 'publish' permission, or write entitlement for
                      repository path.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: file to be checked
        :param attributes: attributes to be configured
        :return: request response
        """
        url = "{}/files/{}/{}/{}/attributes".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.patch(url, json=attributes)
        self._logger.info("Set successfully")
        return response

    def delete_file_attributes(self, subject, repo, file_path, attributes):
        """ Remove attributes associated with the specified Artifact.

            By default, delete all attributes related to the specified Artifact.
            The ‘names’ parameter is optional, and is used to remove specific attributes only.

            Security: Authenticated user with 'publish' permission, or write entitlement for
                      repository path.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: file to be checked
        :param attributes: attributes to be deleted
        :return: request response
        """
        url = "{}/files/{}/{}/{}/attributes".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        params = {"names": ",".join(attributes)}
        response = self._requester.delete(url, params=params)
        self._logger.info("Set successfully")
        return response

    def search_file_attributes(self, subject, repo, attributes):
        """ Returns all artifacts in the specified repository that at least one of their attributes
            correspond to names and values specified in the JSON payload.

            Note: The values range is defined by the brackets direction and the comma position.

            Security: Authenticated user with 'read' permission, or repository read
                      entitlement for repository path.

        :param subject: repository owner
        :param repo: repository name
        :param attributes: attributes to be searched
        :return: request response
        """
        url = "{}/files/{}/{}/search/attributes".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.post(url, json=attributes)
        self._logger.info("Search successfully")
        return response

    # EULA Tracking

    def get_product_signed_eulas(self, subject, product, from_date=None, to_date=None,
                                 username=None, eula_name=None):
        """ Get a list of users who signed eula per product with sign date, version signed and eula.

        :param subject: repository owner
        :param product: product name
        :param from_date: date to filter by, ISO8601 format (yyyy-MM-dd’T’HH:mm:ss.SSSZ)
        :param to_date: date to filter by, ISO8601 format (yyyy-MM-dd’T’HH:mm:ss.SSSZ)
        :param username: filter by username
        :param eula_name: filter by Eula name
        :return: A list of EULAs
        """
        url = "{}/products/{}/{}/signed_eulas".format(Bintray.BINTRAY_URL, subject, product)
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if username:
            params["username"] = username
        if eula_name:
            params["eula_name"] = eula_name
        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def get_all_products_signed_eulas(self, subject, from_date=None, to_date=None, username=None,
                                      eula_name=None):
        """ Get a list of users who signed eula with sign date, version signed and eula name for
            each product owned by the given subject.

        :param subject: repository owner
        :param from_date: date to filter by, ISO8601 format (yyyy-MM-dd’T’HH:mm:ss.SSSZ)
        :param to_date: date to filter by, ISO8601 format (yyyy-MM-dd’T’HH:mm:ss.SSSZ)
        :param username: filter by username
        :param eula_name: filter by Eula name
        :return: a list of EULAs
        """
        url = "{}/products/{}/_all/signed_eulas".format(Bintray.BINTRAY_URL, subject)
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if username:
            params["username"] = username
        if eula_name:
            params["eula_name"] = eula_name
        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    # Release Notes

    def get_package_release_notes(self, subject, repo, package):
        """ Get the release notes for a specific package by subject; Either Bintray
            release notes or GitHub release notes.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: returns the release notes for a specific package by subject
        """
        url = "{}/packages/{}/{}/{}/release_notes".format(Bintray.BINTRAY_URL, subject, repo,
                                                          package)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_package_release_notes_github(self, subject, repo, package, github_repo,
                                            github_release_notes_file):
        """ Create release notes for a package by subject

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param github_repo: GitHub repository name
        :param github_release_notes_file: GitHub release notes file path
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/release_notes".format(Bintray.BINTRAY_URL, subject, repo,
                                                          package)
        json_data = {"github": {
                        "github_repo": github_repo,
                        "github_release_notes_file": github_release_notes_file
                    }}
        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def create_package_release_notes_bintray(self, subject, repo, package, syntax, content):
        """ Create release notes for a package by subject

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param syntax: content syntax
        :param content: release notes content
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/release_notes".format(Bintray.BINTRAY_URL, subject, repo,
                                                          package)
        json_data = {"package": package,
                     "repo": repo,
                     "owner": subject,
                     "bintray": {
                        "syntax": syntax,
                        "content": content
                     }}
        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def delete_package_release_notes(self, subject, repo, package):
        """ Deletes release notes for a specific package by subject.

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: response request
        """
        url = "{}/packages/{}/{}/{}/release_notes".format(Bintray.BINTRAY_URL, subject, repo,
                                                          package)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def get_version_release_notes(self, subject, repo, package, version):
        """ Get release notes for a specific version by subject

            Security: Authenticated user with 'read' permission for private repositories, or version
                      read entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :return: release notes
        """
        url = "{}/packages/{}/{}/{}/versions/{}/release_notes".format(Bintray.BINTRAY_URL, subject,
                                                                      repo, package, version)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_version_release_notes_github(self, subject, repo, package, version, github_repo,
                                            github_release_notes_file):
        """ Create release notes for a specific version by subject. Release notes "content"
            will be copied from the provided GitHub release notes if using "github".

            Security: Authenticated user with 'publish' permission, or version read/write
                      entitlement.


        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param github_repo: GitHub repository name
        :param github_release_notes_file: GitHub release notes file path
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/versions/{}/release_notes".format(Bintray.BINTRAY_URL, subject,
                                                                      repo, package, version)
        json_data = {"github": {
                        "github_repo": github_repo,
                        "github_release_notes_file": github_release_notes_file
                    }}
        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def create_version_release_notes_bintray(self, subject, repo, package, version, syntax,
                                             content):
        """ Create release notes for a package by subject.
            Release notes "content" has to be passed to the command

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param syntax: content syntax
        :param content: release notes content
        :return: request response
        """
        url = "{}/packages/{}/{}/{}/versions/{}/release_notes".format(Bintray.BINTRAY_URL, subject,
                                                                      repo, package, version)
        json_data = {"bintray": {
                        "syntax": syntax,
                        "content": content
                     }}
        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    # Logs (This resource is only available to Bintray Premium users.)

    def get_list_package_download_log_files(self, subject, repo, package):
        """ Retrieve a list of available download log files for a package

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: response request
        """
        url = "{}/packages/{}/{}/{}/logs".format(Bintray.BINTRAY_URL, subject, repo, package)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def download_package_download_log_file(self, subject, repo, package, remote_log_name,
                                           local_log_name):
        """ Download the package download log file specified by log_name

            Security: Authenticated user with 'publish' permission, or package read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param remote_log_name: log to be downloaded
        :param local_log_name: log to be saved in local storage
        :return: response request
        """
        url = "{}/packages/{}/{}/{}/logs/{}".format(Bintray.BINTRAY_URL, subject, repo, package,
                                                    remote_log_name)
        content = self._requester.download(url, add_status_code=False)
        with open(local_log_name, 'wb') as local_fd:
            local_fd.write(content)
        self._logger.info("Download successfully")

    # Stream API (Events Firehose)

    def get_stream_api(self, subject):
        """ Get a stream of events generated by activity for the specified subject.

            Security: Authenticated subject admin.

        :param subject: repository owner
        :return: response request
        """
        url = "{}/stream/{}".format(Bintray.BINTRAY_URL, subject)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    # Product (This resource is only available to Bintray Enterprise Edition users.)

    def get_products(self, subject):
        """ Get a list of products for the specified subject.

            Security: Authenticated user with 'read' permission for private repositories, or
                      repository read entitlement.

        :param subject: repository owner
        :return: a list of products associated to the subject
        """
        url = "{}/products/{}".format(Bintray.BINTRAY_URL, subject)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_product(self, subject, product):
        """ Get details for the specified product.

            Security: Authenticated user with 'read' permission for private repositories, or
                      repository read entitlement.

        :param subject: repository owner
        :param product: product name
        :return: details of a product
        """
        url = "{}/products/{}/{}".format(Bintray.BINTRAY_URL, subject, product)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_product(self, subject, name, display_name, desc, website, vcs, packages,
                       sign_url_expiry=10):
        """ Create a product for the given subject.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param name: product name
        :param display_name: product name to be displayed
        :param desc: product description
        :param website: product website url
        :param vcs: product VCS url
        :param packages: list of packages associated to the product
        :param sign_url_expiry: expiration time
        :return: request response
        """
        url = "{}/products/{}".format(Bintray.BINTRAY_URL, subject)
        json_data = {}
        if name:
            json_data["name"] = name
        if display_name:
            json_data["display_name"] = display_name
        if desc:
            json_data["desc"] = desc
        if website:
            json_data["website_url"] = website
        if vcs:
            json_data["vcs_url"] = vcs
        if packages:
            json_data["packages"] = packages
        if sign_url_expiry:
            json_data["sign_url_expiry"] = sign_url_expiry

        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def update_product(self, subject, product, display_name=None, desc=None, website=None, vcs=None,
                       packages=None):
        """ Update an existing product.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param product: product name
        :param display_name: product name to be displayed
        :param desc: product description
        :param website: product website url
        :param vcs: product VCS url
        :param packages: list of packages associated to the product
        :return: request response
        """
        url = "{}/products/{}/{}".format(Bintray.BINTRAY_URL, subject, product)
        json_data = {}
        if display_name:
            json_data["display_name"] = display_name
        if desc:
            json_data["desc"] = desc
        if website:
            json_data["website_url"] = website
        if vcs:
            json_data["vcs_url"] = vcs
        if packages:
            json_data["packages"] = packages

        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Patch successfully")
        return response

    def delete_product(self, subject, product):
        """ Delete the specified product and all its sub-elements (such as EULAs).

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param product: product name
        :return: request response
        """
        url = "{}/products/{}/{}".format(Bintray.BINTRAY_URL, subject, product)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    # Usage Thresholds (This resource is only available for Bintray Enterprise accounts.)

    def get_usage_threshold_org(self, org):
        """ Get organization usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :return: request response
        """
        url = "{}/usage_threshold/organization/{}".format(Bintray.BINTRAY_URL, org)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_usage_threshold_repository(self, org, repo):
        """ Get repository organization usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param repo: repo name
        :return: request response
        """
        url = "{}/usage_threshold/repo/{}/{}".format(Bintray.BINTRAY_URL, org, repo)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_usage_threshold_business_unit(self, org, business_unit):
        """ Get business unit usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param business_unit: business unit name
        :return: request response
        """
        url = "{}/usage_threshold/business_unit/{}/{}".format(Bintray.BINTRAY_URL, org,
                                                              business_unit)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_usage_threshold_org(self, org, monthly_storage=None, monthly_download=None,
                                   daily_download=None, alert_to_emails=None, alert_to_admins=True):
        """ Create organization usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/organization/{}".format(Bintray.BINTRAY_URL, org)

        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.post(url, json=json_data)

        self._logger.info("Post successfully")
        return response

    def create_usage_threshold_repository(self, org, repo, monthly_storage=None,
                                          monthly_download=None, daily_download=None,
                                          alert_to_emails=None, alert_to_admins=True):
        """ Create repository usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param repo: repository name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/repo/{}/{}".format(Bintray.BINTRAY_URL, org, repo)

        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.post(url, json=json_data)

        self._logger.info("Post successfully")
        return response

    def create_usage_threshold_business_unit(self, org, business_unit, monthly_storage=None,
                                             monthly_download=None, daily_download=None,
                                             alert_to_emails=None, alert_to_admins=True):
        """ Create usage threshold for business unit

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param business_unit: business unit name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/business_unit/{}/{}".format(Bintray.BINTRAY_URL, org,
                                                              business_unit)

        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.post(url, json=json_data)

        self._logger.info("Post successfully")
        return response

    def update_usage_threshold_org(self, org, monthly_storage=None, monthly_download=None,
                                   daily_download=None, alert_to_emails=None, alert_to_admins=None):
        """ Update organization usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/organization/{}".format(Bintray.BINTRAY_URL, org)

        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        if alert_to_admins is not None:
            json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.patch(url, json=json_data)

        self._logger.info("Patch successfully")
        return response

    def update_usage_threshold_repository(self, org, repo, monthly_storage=None,
                                          monthly_download=None, daily_download=None,
                                          alert_to_emails=None, alert_to_admins=None):
        """ Update repository usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param repo: repository name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/repo/{}/{}".format(Bintray.BINTRAY_URL, org, repo)

        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        if alert_to_admins is not None:
            json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.patch(url, json=json_data)

        self._logger.info("Patch successfully")
        return response

    def update_usage_threshold_business_unit(self, org, business_unit, monthly_storage=None,
                                             monthly_download=None, daily_download=None,
                                             alert_to_emails=None, alert_to_admins=None):
        """ Update usage threshold for business unit

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param business_unit: business unit name
        :param monthly_storage: monthly storage in bytes
        :param monthly_download: monthly download in bytes
        :param daily_download: daily download in bytes
        :param alert_to_emails: list of emails to receive alerts
        :param alert_to_admins: send alerts to admins.
        :return: request response
        """
        url = "{}/usage_threshold/business_unit/{}/{}".format(Bintray.BINTRAY_URL, org,
                                                              business_unit)
        json_data = {}
        if monthly_storage:
            json_data["monthly_storage_bytes"] = monthly_storage
        if monthly_download:
            json_data["monthly_download_bytes"] = monthly_download
        if daily_download:
            json_data["daily_download_bytes"] = daily_download
        if alert_to_emails:
            json_data["alert_to_emails"] = alert_to_emails
        if alert_to_admins is not None:
            json_data["alert_to_admins"] = alert_to_admins

        response = self._requester.patch(url, json=json_data)

        self._logger.info("Patch successfully")
        return response

    def delete_usage_threshold_org(self, org):
        """ Delete organization usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :return: request response
        """
        url = "{}/usage_threshold/organization/{}".format(Bintray.BINTRAY_URL, org)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def delete_usage_threshold_repository(self, org, repo):
        """ Delete repository usage threshold

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param repo: repository name
        :return: request response
        """
        url = "{}/usage_threshold/repo/{}/{}".format(Bintray.BINTRAY_URL, org, repo)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def delete_usage_threshold_business_unit(self, org, business_unit):
        """ Delete usage threshold for business unit

            Security: Authenticated user with organization ‘admin’ permission.

        :param org: organization name
        :param business_unit: business unit name
        :return: request response
        """
        url = "{}/usage_threshold/business_unit/{}/{}".format(Bintray.BINTRAY_URL, org,
                                                              business_unit)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    # Packages

    def get_packages(self, subject, repo, start_pos=None, start_name=None):
        """ Get a list of packages in the specified repository.

            Security: Authenticated user with 'read' permission, or repository read entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param start_pos: starting position filter
        :param start_name: name prefix filter
        :return: list of packages
        """
        url = "{}/repos/{}/{}/packages".format(Bintray.BINTRAY_URL, subject, repo)
        params = {}
        if start_pos:
            params["start_pos"] = start_pos
        if start_name:
            params["start_name"] = start_name
        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def get_package(self, subject, repo, package, attribute_values=True):
        """ Get general information about a specified package with package name.

            Security: Non-authenticated user.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param attribute_values: show attribute values
        :return: package details
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        params = {"attribute_values": bool_to_number(attribute_values)}
        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def get_package_for_file(self, subject, repo, file_path):
        """ Get general information about the package a repository file is associated with.

            Security: Non-authenticated user.

        :param subject: repository owner
        :param repo: repository name
        :param file_path: file path to be searched
        :return: package details
        """
        url = "{}/file_package/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, file_path)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def search_maven_package(self, group_id=None, artifact_id=None, query=None, subject=None,
                             repo=None):
        """ Search for a Maven package using Maven groupId and artifactId

            Security: Non-authenticated user.

        :param group_id: maven group id
        :param artifact_id: maven artifact id
        :param query: wildcard query
        :param subject: repository owner
        :param repo: repository name
        :return: package details
        """
        url = "{}/search/packages/maven".format(Bintray.BINTRAY_URL)
        params = {}
        if group_id:
            params["g"] = group_id
        if artifact_id:
            params["a"] = group_id
        if query:
            params["q"] = query
        if subject:
            params["subject"] = subject
        if repo:
            params["repo"] = repo

        if not params:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def create_package(self, subject, repo, package, licenses=None, vcs_url=None,
                       custom_licenses=None, desc=None, labels=None, website_url=None,
                       issue_tracker_url=None, github_repo=None, github_release_notes_file=None,
                       public_download_numbers=None, public_stats=None):
        """ Creates a new package in the specified repo (user has to be an owner of the repo)

            Security: Authenticated user with 'publish' permission, or repository read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param desc: package description
        :param labels: package lables (tags)
        :param licenses: list of licenses (mandatory for OSS packages)
        :param custom_licenses: custom licenses (available only for Premium accounts)
        :param vcs_url: VCS url (mandatory for OSS packages)
        :param website_url: website url
        :param issue_tracker_url: issue tracker url
        :param github_repo: Github repository
        :param github_release_notes_file: release notes on Github
        :param public_download_numbers: display download number
        :param public_stats: stats are public (available only for Premium accounts)
        :return: request response
        """
        url = "{}/packages/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {"name": package}
        if desc:
            json_data["desc"] = desc
        if labels:
            json_data["labels"] = labels
        if licenses:
            json_data["licenses"] = licenses
        if custom_licenses:
            json_data["custom_licenses"] = custom_licenses
        if vcs_url:
            json_data["vcs_url"] = vcs_url
        if website_url:
            json_data["website_url"] = website_url
        if issue_tracker_url:
            json_data["issue_tracker_url"] = issue_tracker_url
        if github_repo:
            json_data["github_repo"] = github_repo
        if github_release_notes_file:
            json_data["github_release_notes_file"] = github_release_notes_file
        if public_download_numbers is not None:
            json_data["public_download_numbers"] = public_download_numbers
        if public_stats is not None:
            json_data["public_stats"] = public_stats

        response = self._requester.post(url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def delete_package(self, subject, repo, package):
        """ Delete the specified package

            Security: Authenticated user with 'publish' permission, or repository
                      ead/write entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :return: request response
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def update_package(self, subject, repo, package, licenses=None, vcs_url=None,
                       custom_licenses=None, desc=None, labels=None, website_url=None,
                       issue_tracker_url=None, github_repo=None, github_release_notes_file=None,
                       public_download_numbers=None, public_stats=None):
        """ Update the information of the specified package.

            Security: Authenticated user with 'publish' permission, or repository read/write
                      entitlement.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param desc: package description
        :param labels: package lables (tags)
        :param licenses: list of licenses (mandatory for OSS packages)
        :param custom_licenses: custom licenses (available only for Premium accounts)
        :param vcs_url: VCS url (mandatory for OSS packages)
        :param website_url: website url
        :param issue_tracker_url: issue tracker url
        :param github_repo: Github repository
        :param github_release_notes_file: release notes on Github
        :param public_download_numbers: display download number
        :param public_stats: stats are public (available only for Premium accounts)
        :return: request response
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        json_data = {}
        if desc:
            json_data["desc"] = desc
        if labels:
            json_data["labels"] = labels
        if licenses:
            json_data["licenses"] = licenses
        if custom_licenses:
            json_data["custom_licenses"] = custom_licenses
        if vcs_url:
            json_data["vcs_url"] = vcs_url
        if website_url:
            json_data["website_url"] = website_url
        if issue_tracker_url:
            json_data["issue_tracker_url"] = issue_tracker_url
        if github_repo:
            json_data["github_repo"] = github_repo
        if github_release_notes_file:
            json_data["github_release_notes_file"] = github_release_notes_file
        if public_download_numbers is not None:
            json_data["public_download_numbers"] = public_download_numbers
        if public_stats is not None:
            json_data["public_stats"] = public_stats
        if not json_data:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Update successfully")
        return response

    def search_package(self, package=None, desc=None, subject=None, repo=None):
        """ Search for a package.

            Security: Non-authenticated user.

        :param subject: repository owner to filter
        :param repo: repository name to filter
        :param package: package name to filter
        :param desc: desc name to filter
        :return: an array of results
        """
        url = "{}/search/packages".format(Bintray.BINTRAY_URL)
        params = {}
        if package:
            params["name"] = package
        if desc:
            params["desc"] = desc
        if subject:
            params["subject"] = subject
        if repo:
            params["repo"] = repo
        if not params:
            raise ValueError("At lease one parameter must be filled.")

        response = self._requester.get(url, params=params)
        self._logger.info("Search successfully")
        return response

    # Statistics & Usage Report (This resource is only available for Bintray Premium accounts.)

    def _get_custom_downloads(self, subject, repo, package, suffix, version=None,
                              from_date=None,
                              to_date=None):
        """ Get number of downloads, for the passed time range, per package or per version.
            Security: Authenticated user with 'publish' permission for private repositories,
                      or package read/write entitlement.
        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param suffix: suffix name
        :param version: package version (Optional)
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        url = "{}/packages/{}/{}/{}".format(Bintray.BINTRAY_URL, subject, repo, package)
        if version:
            url += "/versions/{}/stats/{}".format(version, suffix)
        else:
            url += "/stats/{}".format(suffix)
        json_data = {}
        if from_date:
            json_data["from"] = from_date
        if to_date:
            json_data["to"] = to_date

        response = self._requester.post(url, json=json_data)
        self._logger.info("Search successfully")
        return response

    def get_daily_downloads(self, subject, repo, package, version=None, from_date=None,
                            to_date=None):
        """ Get number of downloads per day, for the passed time range, per package or per version.
            Security: Authenticated user with 'publish' permission for private repositories,
                      or package read/write entitlement.
        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (Optional)
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        return self._get_custom_downloads(subject, repo, package, "time_range_downloads",
                                          version,
                                          from_date, to_date)

    def get_total_downloads(self, subject, repo, package, version=None, from_date=None,
                            to_date=None):
        """ Get total number of downloads, for the passed time range, per package or per version.
            Security: Authenticated user with 'publish' permission for private repositories,
                      or package read/write entitlement.
        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (Optional)
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        return self._get_custom_downloads(subject, repo, package, "total_downloads", version,
                                          from_date, to_date)

    def get_downloads_by_country(self, subject, repo, package, version=None, from_date=None,
                                 to_date=None):
        """ Get total number of downloads, for the passed time range, per package or per version.
            Security: Authenticated user with 'publish' permission for private repositories,
                      or package read/write entitlement.
        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version (Optional)
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        return self._get_custom_downloads(subject, repo, package, "country_downloads", version,
                                          from_date, to_date)

    def get_usage_report_for_subject(self, subject, from_date=None, to_date=None):
        """ Get monthly download and storage usage report, according to the specified date range
            for a subject.
            Security: Authenticated user with 'admin' permission.
        :param subject: repository owner
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        url = "{}/usage/{}".format(Bintray.BINTRAY_URL, subject)
        json_data = {}
        if from_date:
            json_data["from"] = from_date
        if to_date:
            json_data["to"] = to_date

        response = self._requester.post(url, json=json_data)
        self._logger.info("Search successfully")
        return response

    def get_usage_report_for_repository(self, subject, repo, from_date=None, to_date=None):
        """ Get monthly download and storage usage report, according to the specified date range
            for a specific subject repository.
            Security: Authenticated user with 'admin' permission.
        :param subject: repository owner
        :param repo: repository name
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        url = "{}/usage/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        json_data = {}
        if from_date:
            json_data["from"] = from_date
        if to_date:
            json_data["to"] = to_date

        response = self._requester.post(url, json=json_data)
        self._logger.info("Search successfully")
        return response

    def get_usage_report_for_package(self, subject, repo, package=None, start_pos=50,
                                     from_date=None, to_date=None):
        """ Get current storage usage report. Report can be requested for the specified repository,
            optionally for a specific package.
            Security: Authenticated user with 'admin' permission for repo, or 'publish' permission
                      for specific package.
        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param start_pos: index position
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        url = "{}/usage/package_usage/{}/{}".format(Bintray.BINTRAY_URL, subject, repo)
        if package:
            url += "/{}".format(package)
        params = {"start_pos": start_pos}
        json_data = {}
        if from_date:
            json_data["from"] = from_date
        if to_date:
            json_data["to"] = to_date

        response = self._requester.post(url, json=json_data, params=params)
        self._logger.info("Search successfully")
        return response

    def get_usage_report_grouped_by_business_unit(self, subject, business_unit=None,
                                                  from_date=None,
                                                  to_date=None):
        """ Get monthly download and storage usage report, according to the specified date range
            and grouped by business unit. Report can be requested for a subject or for a specific
            subject business unit.
            Security: Authenticated user with 'admin' permission.
        :param subject: repository owner
        :param business_unit: business unit name
        :param from_date: initial date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :param to_date: end date range ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)
        :return: download details
        """
        url = "{}/usage/business_unit_usage/{}".format(Bintray.BINTRAY_URL, subject)
        if business_unit:
            url += "/{}".format(business_unit)
        json_data = {}
        if from_date:
            json_data["from"] = from_date
        if to_date:
            json_data["to"] = to_date

        response = self._requester.post(url, json=json_data)
        self._logger.info("Search successfully")
        return response

    # Entitlements (This resource is only available to Bintray Pro and Enterprise users)

    def get_access_keys_org(self, org):
        """ Get a list of access keys associated with an organization

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :return: list of keys
        """
        url = "{}/orgs/{}/access_keys".format(Bintray.BINTRAY_URL, org)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_access_keys_user(self, user):
        """ Get a list of access keys associated with an user

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :return: list of keys
        """
        url = "{}/users/{}/access_keys".format(Bintray.BINTRAY_URL, user)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_access_key_org(self, org, access_key_id):
        """ Get an access key associated with an organization, by its id.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param access_key_id: access key id
        :return: list of keys
        """
        url = "{}/orgs/{}/access_keys/{}".format(Bintray.BINTRAY_URL, org, access_key_id)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_access_key_user(self, user, access_key_id):
        """ Get an access key associated with an user, by its id.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param access_key_id: access key id
        :return: list of keys
        """
        url = "{}/users/{}/access_keys/{}".format(Bintray.BINTRAY_URL, user, access_key_id)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def _create_access_key(self, request_url, id, url=None, cache_for_secs=None, expiry=None,
                           white_cidrs=None, black_cidrs=None, api_only=False):
        """ Create a new access key identified by an access key id

             An access key password will be auto-generated if not specified.

        :param request_url: base_url
        :param id: access key id
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :param api_only: allow access keys access to Bintray UI as well as to the API
        :return: request response
        """
        json_data = {}
        if id:
            json_data["id"] = id
        if expiry:
            json_data["expiry"] = expiry
        if url or cache_for_secs:
            json_data["existence_check"] = {}
            if url:
                json_data["existence_check"]["url"] = url
            if cache_for_secs:
                json_data["existence_check"]["cache_for_secs"] = cache_for_secs
        if white_cidrs:
            json_data["white_cidrs"] = white_cidrs
        if black_cidrs:
            json_data["black_cidrs"] = black_cidrs
        if api_only is not None:
            json_data["api_only"] = api_only

        response = self._requester.post(request_url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def create_access_key_org(self, org, id, url=None, cache_for_secs=None, expiry=None,
                              white_cidrs=None, black_cidrs=None, api_only=False):
        """ Create a new access key identified by an access key id, for an organization.

             An access key password will be auto-generated if not specified.

        :param org: organization name
        :param id: access key id
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :param api_only: allow access keys access to Bintray UI as well as to the API
        :return: request response
        """
        request_url = "{}/orgs/{}/access_keys".format(Bintray.BINTRAY_URL, org)
        return self._create_access_key(request_url, id, url, cache_for_secs, expiry, white_cidrs,
                                       black_cidrs, api_only)

    def create_access_key_user(self, user, id, url=None, cache_for_secs=None, expiry=None,
                               white_cidrs=None, black_cidrs=None, api_only=False):
        """ Create a new access key identified by an access key id, for an user.

             An access key password will be auto-generated if not specified.

        :param user: user name
        :param id: access key id
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :param api_only: allow access keys access to Bintray UI as well as to the API
        :return: request response
        """
        request_url = "{}/users/{}/access_keys".format(Bintray.BINTRAY_URL, user)
        return self._create_access_key(request_url, id, url, cache_for_secs, expiry, white_cidrs,
                                       black_cidrs, api_only)

    def delete_access_key_org(self, org, access_key_id):
        """ Delete an access key associated with an organization.

            Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param access_key_id: access key id
        :return: request response
        """
        url = "{}/orgs/{}/access_keys/{}".format(Bintray.BINTRAY_URL, org, access_key_id)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def delete_access_key_user(self, user, access_key_id):
        """ Delete an access key associated with an user.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param access_key_id: access key id
        :return: request response
        """
        url = "{}/users/{}/access_keys/{}".format(Bintray.BINTRAY_URL, user, access_key_id)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def _update_access_key(self, request_url, url=None, cache_for_secs=None, expiry=None,
                           white_cidrs=None, black_cidrs=None):
        """ Update an existing access key identified by an access key id

            Security: Authenticated user with 'admin' permission.

        :param request_url: base_url
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :return: request response
        """
        json_data = {}
        if expiry:
            json_data["expiry"] = expiry
        if url or cache_for_secs:
            json_data["existence_check"] = {}
            if url:
                json_data["existence_check"]["url"] = url
            if cache_for_secs:
                json_data["existence_check"]["cache_for_secs"] = cache_for_secs
        if white_cidrs:
            json_data["white_cidrs"] = white_cidrs
        if black_cidrs:
            json_data["black_cidrs"] = black_cidrs

        response = self._requester.patch(request_url, json=json_data)
        self._logger.info("Post successfully")
        return response

    def update_access_key_org(self, org, access_key_id, url=None, cache_for_secs=None, expiry=None,
                           white_cidrs=None, black_cidrs=None):
        """ Update an existing access key identified by an access key id, for an organization.

             Security: Authenticated user with 'admin' permission.

        :param org: organization name
        :param access_key_id: access key to be updated
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :return: request response
        """
        request_url = "{}/orgs/{}/access_keys/{}".format(Bintray.BINTRAY_URL, org, access_key_id)
        return self._update_access_key(request_url, url, cache_for_secs, expiry, white_cidrs,
                                       black_cidrs)

    def update_access_key_user(self, user, access_key_id, url=None, cache_for_secs=None,
                               expiry=None, white_cidrs=None, black_cidrs=None):
        """ Update an existing access key identified by an access key id, for an user.

            Security: Authenticated user with 'admin' permission.

        :param user: user name
        :param access_key_id: access key to be updated
        :param expiry: after that will be automatically revoked. (Unix epoch time in milliseconds)
        :param url: URL for existence_check (callback)
        :param cache_for_secs: specified period for caching result. minimum is 60 seconds.
        :param white_cidrs: will allow access only for those IPs that exist in that address range
        :param black_cidrs: will block access for all IPs that exist in the specified range.
        :return: request response
        """
        request_url = "{}/users/{}/access_keys/{}".format(Bintray.BINTRAY_URL, user, access_key_id)
        return self._update_access_key(request_url, url, cache_for_secs, expiry, white_cidrs,
                                       black_cidrs)

    def get_entitlements(self, subject, repo=None, package=None, version=None, product=None):
        """ Get the entitlements defined on the specified product, repository, package or version.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param product: product name (only for Enterprise Account)
        :return: entitlements list
        """
        if product:
            url = "{}/products/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, product)
        else:
            if version:
                url = "{}/packages/{}/{}/{}/versions/{}/entitlements".format(Bintray.BINTRAY_URL,
                                                                             subject, repo,
                                                                             package, version)
            elif package:
                url = "{}/packages/{}/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, repo,
                                                                 package)
            else:
                url = "{}/packages/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, repo)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def get_entitlement(self, subject, entitlement_id, repo=None, package=None, version=None,
                        product=None):
        """ Get an entitlement by its id and scope. Scope can be a product, a repository, a package
            or a version.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param entitlement_id: entitlement to be acquired
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param product: product name (only for Enterprise Account)
        :return: entitlements list
        """
        if product:
            url = "{}/products/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, product,
                                                             entitlement_id)
        else:
            if version:
                url = "{}/packages/{}/{}/{}/versions/{}/entitlements/{}".format(Bintray.BINTRAY_URL,
                                                                                subject, repo,
                                                                                package, version,
                                                                                entitlement_id)
            elif package:
                url = "{}/packages/{}/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject,
                                                                    repo, package, entitlement_id)
            else:
                url = "{}/packages/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                                 entitlement_id)
        response = self._requester.get(url)
        self._logger.info("Get successfully")
        return response

    def create_entitlement(self, subject, repo=None, package=None, version=None,
                           access=None, access_keys=None, path=None, tags=None, product=None):
        """ Create an entitlement on the specified scope. Scope can be a product, a repository with
            an optional path, a package or a version.

            When specifying an optional path value for repository scope, path needs to be relative
            and refer to a directory or a file in the repository.

            Access mode can be either rw (read-write: implies download, upload and delete) or r
            (read: implies download).

            When specifying a scope with product, access mode can only be r (read: implies
            download). Tags can be added for search purposes.

            An entitlement id will be auto-generated if not specified.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param product: product name (only for Enterprise Account)
        :param access: entitlement access more (r/w)
        :param access_keys: list of access keys
        :param path: file path
        :param tags: associated tags
        :return: entitlements list
        """
        if product:
            url = "{}/products/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, product)
        else:
            if version:
                url = "{}/packages/{}/{}/{}/versions/{}/entitlements".format(Bintray.BINTRAY_URL,
                                                                             subject, repo,
                                                                             package, version)
            elif package:
                url = "{}/packages/{}/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, repo,
                                                                 package)
            else:
                url = "{}/packages/{}/{}/entitlements".format(Bintray.BINTRAY_URL, subject, repo)

        json_data = {}
        if access:
            json_data["access"] = access
        if access_keys:
            json_data["access_keys"] = access
        if path:
            json_data["path"] = path
        if tags:
            json_data["tags"] = tags

        response = self._requester.post(url, json=json_data)
        self._logger.info("Create successfully")
        return response

    def delete_entitlement(self, subject, entitlement_id, repo=None, package=None, version=None,
                           product=None):
        """ Delete an entitlement by its id and scope. Scope can be a product, a repository,
            a package or a version.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param entitlement_id: entitlement to be deleted
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param product: product name (only for Enterprise Account)
        :return: entitlements list
        """
        if product:
            url = "{}/products/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, product,
                                                             entitlement_id)
        else:
            if version:
                url = "{}/packages/{}/{}/{}/versions/{}/entitlements/{}".format(Bintray.BINTRAY_URL,
                                                                                subject, repo,
                                                                                package, version,
                                                                                entitlement_id)
            elif package:
                url = "{}/packages/{}/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject,
                                                                    repo, package, entitlement_id)
            else:
                url = "{}/packages/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                                 entitlement_id)
        response = self._requester.delete(url)
        self._logger.info("Delete successfully")
        return response

    def update_entitlement(self, subject, entitlement_id, repo=None, package=None, version=None,
                           access=None, access_keys=None, tags=None, product=None):
        """ Update the information of the specified entitlement of a specified scope. Scope can be a
            product, a repository with an optional path, a package or a version.

            When specifying an optional path value for repository scope, path needs to be relative
            and refer to a directory or a file in the repository.

            Access mode can be either rw (read-write: implies download, upload and delete) or r
            (read: implies download).

            When specifying a scope with product, access mode can only be r (read: implies
            download). Tags can be added for search purposes.

            An entitlement id will be auto-generated if not specified.

            Security: Authenticated user with 'admin' permission.

        :param subject: repository owner
        :param entitlement_id: entitlement id to be updated
        :param repo: repository name
        :param package: package name
        :param version: package version
        :param product: product name (only for Enterprise Account)
        :param access: entitlement access more (r/w)
        :param access_keys: list of access keys
        :param tags: associated tags
        :return: entitlements list
        """
        if product:
            url = "{}/products/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, product,
                                                             entitlement_id)
        else:
            if version:
                url = "{}/packages/{}/{}/{}/versions/{}/entitlements/{}".format(Bintray.BINTRAY_URL,
                                                                                subject, repo,
                                                                                package, version,
                                                                                entitlement_id)
            elif package:
                url = "{}/packages/{}/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject,
                                                                    repo, package, entitlement_id)
            else:
                url = "{}/packages/{}/{}/entitlements/{}".format(Bintray.BINTRAY_URL, subject, repo,
                                                                 entitlement_id)
        json_data = {}
        if access:
            json_data["access"] = access
        if access_keys:
            json_data["access_keys"] = access
        if tags:
            json_data["tags"] = tags

        response = self._requester.patch(url, json=json_data)
        self._logger.info("Update successfully")
        return response

    def search_entitlement_by_access_key(self, access_key=None, scope=None, product=None,
                                         deep=False):
        """ Search for entitlements for a specific access key in the specified scope.

            The minimal scope is a subject.
            You can optionally add a sub-scope of product, repo, package and version.

            If deep equals true (default is false), will return all entitlements under the given
            scope, for example, if scope is repository, existing package and version entitlements
            under the given repository will be returned.

            Security: Authenticated user with 'admin' permission.

        :param access_key: specific access key to be searched
        :param scope: specified scope to be used in the search
        :param product: products name associated to the access key
        :param deep: return all entitlements under the given scope
        :return: entitlement found
        """
        url = "{}/search/entitlements".format(Bintray.BINTRAY_URL)
        params = {"deep": bool_to_number(deep)}
        if access_key:
            params["access_key"] = access_key
        if scope:
            params["scope"] = scope
        if product:
            params["product"] = product

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response

    def search_entitlement_by_tag(self, tag=None, scope=None, product=None, deep=False):
        """ Search for entitlements for a specific tag in the specified scope.

            The minimal scope is a subject.
            You can optionally add a sub-scope of product, repo, package and version.

            If deep equals true (default is false), will return all entitlements under the given
            scope, for example, if scope is repository, existing package and version entitlements
            under the given repository will be returned.

            Security: Authenticated user with 'admin' permission.

        :param tag: specific tag to be searched
        :param scope: specified scope to be used in the search
        :param product: products name associated to the access key
        :param deep: return all entitlements under the given scope
        :return: entitlement found
        """
        url = "{}/search/entitlements".format(Bintray.BINTRAY_URL)
        params = {"deep": bool_to_number(deep)}
        if tag:
            params["tag"] = tag
        if scope:
            params["scope"] = scope
        if product:
            params["product"] = product

        response = self._requester.get(url, params=params)
        self._logger.info("Get successfully")
        return response
