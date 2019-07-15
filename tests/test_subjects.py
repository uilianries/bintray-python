# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_regenerate_subject_url_signing_key():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.regenerate_subject_url_signing_key("uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/subjects/uilianries/keypair" == error_message
