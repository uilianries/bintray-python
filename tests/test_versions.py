# -*- coding: utf-8 -*-

import datetime
from bintray.bintray import Bintray


def test_get_version():
    bintray = Bintray()
    response = bintray.get_version("uilianries", "generic", "statistics", version="_latest")
    assert response.get("error") == False
    assert response.get("name") == "test"
    assert response.get("statusCode") == 200


def test_create_version():
    bintray = Bintray()
    now = datetime.datetime.now()
    version = now.strftime("%Y%m%d%H%M%S")
    released = now.strftime("%Y-%m-%d")

    response = bintray.create_version("uilianries", "generic", "statistics", name=version,
                                      released=released, vcs_tag="0.1.0")
    assert response.get("error") == False
    assert response.get("name") == version
    assert response.get("statusCode") == 201
