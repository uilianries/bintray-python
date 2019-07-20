import os
from bintray.bintray import Bintray


def test_download_content():
    json_file = "packages.json"
    bintray = Bintray()
    response = bintray.download_content("uilianries", "generic", json_file, json_file)
    assert os.path.exists(json_file)
    assert False == response["error"]


def test_bad_credentials_for_download_content():
    json_file = "packages.json"
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.download_content("uilianries", "generic", json_file, json_file)
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: "\
           "https://dl.bintray.com/uilianries/generic/packages.json" == error_message


def test_dynamic_download():
    json_file = "packages.json"
    bintray = Bintray()
    response = bintray.dynamic_download("uilianries", "generic", json_file, json_file)
    assert os.path.exists(json_file)
    assert False == response["error"]


def test_bad_credentials_for_dynamic_download():
    json_file = "packages.json"
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.dynamic_download("uilianries", "generic", json_file, json_file)
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: "\
           "https://dl.bintray.com/uilianries/generic/packages.json" == error_message


def test_url_signing():
    json_file = "packages.json"
    bintray = Bintray()
    error_message = ""
    try:
        bintray.url_signing("uilianries", "generic", json_file, {})
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/signed_url/uilianries/generic/packages.json" \
           "?encrypt=false" == error_message
