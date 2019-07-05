# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_oss_licenses():
    bintray = Bintray()
    licenses = bintray.get_oss_licenses()
    copyfree = {'name': 'Copyfree', 'longname': 'Copyfree', 'url': 'http://copyfree.org/'}
    assert copyfree in licenses


def test_bad_credentials_for_get_oss_licenses():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_oss_licenses()
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
            "https://api.bintray.com/licenses/oss_licenses" == error_message
