# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_eulas("jfrog", "bintray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/jfrog/bintray/eulas" == error_message


def test_get_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_eula("jfrog", "bintray", "eula")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/jfrog/bintray/eulas/eula" == error_message
