# -*- coding: utf-8 -*-

import tempfile

from bintray.bintray import Bintray


def test_upload_content():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt",
                                      temp_path, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_bad_credentials_for_upload_content():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        _, temp_path = tempfile.mkstemp()
        bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt", temp_path)
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/content/uilianries/generic/statistics/test/test.txt?" \
           "publish=1&override=0&explode=0" == error_message
