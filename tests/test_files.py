# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


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


def test_bad_credentials_for_get_package_files():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_package_files("uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/packages/uilianries/generic/statistics/files?" \
           "include_unpublished=0" == error_message


def test_get_version_files():
    bintray = Bintray()
    response = bintray.get_version_files("uilianries", "generic", "statistics", "20190701")
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


def test_bad_credentials_for_get_version_files():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_version_files("uilianries", "generic", "statistics", "20190701")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/packages/uilianries/generic/statistics/versions" \
           "/20190701/files?include_unpublished=0" == error_message


def test_file_search_by_name():
    bintray = Bintray()
    response = bintray.file_search_by_name("packages.json", subject="uilianries", repo="generic")
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


def test_bad_credentials_file_search_by_name():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.file_search_by_name("packages.json", subject="uilianries", repo="generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/search/file" \
           "?name=packages.json&subject=uilianries&repo=generic" == error_message


def test_file_search_by_checksum():
    bintray = Bintray()
    response = bintray.file_search_by_checksum("85abc6aece02515e8bd87b9754a18af697527d88",
                                               subject="uilianries", repo="generic",
                                               created_after="2019-07-01")
    assert {'error': False, 'statusCode': 200} in response


def test_bad_credentials_file_search_by_checksum():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.file_search_by_checksum(
            "85abc6aece02515e8bd87b9754a18af697527d88",
            subject="uilianries", repo="generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/search/file" \
           "?sha1=85abc6aece02515e8bd87b9754a18af697527d88" \
           "&subject=uilianries&repo=generic" == error_message


def test_file_in_download_list():
    bintray = Bintray()
    response = bintray.file_in_download_list("uilianries", "generic", "packages.json", True)
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response

