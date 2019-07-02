#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from bintray.bintray import Bintray


def test_download_content():
    json_file = "packages.json"
    bintray = Bintray()
    response = bintray.download_content("uilianries", "generic", json_file, json_file)
    assert os.path.exists(json_file)
    assert False == response["error"]


def test_get_package_files():
    bintray = Bintray()
    response = bintray.get_package_files("uilianries", "generic", "statistics")
    assert {'error': False, 'statusCode': 200} in response
    assert {'created': '2019-07-01T20:51:42.879Z',
            'name': 'packages.json',
            'owner': 'uilianries',
            'package': 'statistics',
            'path': 'packages.json',
            'repo': 'generic',
            'sha1': '85abc6aece02515e8bd87b9754a18af697527d88',
            'sha256': '9537027db06c520b6eeb3b8317cef5c994ab93e5ad4b17fac3567fba7089b165',
            'size': 1967,
            'version': '20190701'} in response


def test_upload_content():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt",
                                      temp_path, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_bad_credentials_for_download_content():
    json_file = "packages.json"
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.download_content("uilianries", "generic", json_file, json_file)
    except Exception as error:
        error_message = str(error)
    assert "Could not download file content (401): 401 Client Error: Unauthorized for url: "\
           "https://dl.bintray.com/uilianries/generic/packages.json" == error_message


def test_bad_credentials_for_get_package_files():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_package_files("uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not list package files (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/packages/uilianries/generic/statistics/files?" \
           "include_unpublished=False&include_unpublished=0" == error_message


def test_bad_credentials_for_upload_content():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        _, temp_path = tempfile.mkstemp()
        bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt", temp_path)
    except Exception as error:
        error_message = str(error)
    assert "Could not upload (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/content/uilianries/generic/statistics/test/test.txt?" \
           "publish=1&override=0&explode=0" == error_message
