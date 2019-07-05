# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_oss_licenses():
    bintray = Bintray()
    licenses = bintray.get_oss_licenses()
    copyfree = {'name': 'Copyfree', 'longname': 'Copyfree', 'url': 'http://copyfree.org/'}
    assert copyfree in licenses


def test_get_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_org_proprietary_licenses(org="jfrog")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): 403 Client Error: Forbidden for url: " \
            "https://api.bintray.com/orgs/jfrog/licenses" == error_message


def test_get_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_user_proprietary_licenses(user="uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): 400 Client Error: Bad Request for url: " \
            "https://api.bintray.com/users/uilianries/licenses" == error_message


def test_bad_credentials_for_get_oss_licenses():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_oss_licenses()
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
            "https://api.bintray.com/licenses/oss_licenses" == error_message


def test_create_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_org_proprietary_license(org="jfrog", license=[{}])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): 403 Client Error: Forbidden for url: " \
            "https://api.bintray.com/orgs/jfrog/licenses" == error_message


def test_create_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_user_proprietary_license(user="uilianries", license=[{}])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): 400 Client Error: Bad Request for url: " \
            "https://api.bintray.com/users/uilianries/licenses" == error_message
