# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_version():
    bintray = Bintray()
    response = bintray.get_version("uilianries", "generic", "statistics", version="_latest")
    assert response.get("error") == False
    assert response.get("name") == "test"
    assert response.get("statusCode") == 200
