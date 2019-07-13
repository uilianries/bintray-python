# -*- coding: utf-8 -*-

import random
from bintray.bintray import Bintray


def test_get_repositories():
    bintray = Bintray()
    response = bintray.get_repositories("conan")
    assert {'error': False, 'statusCode': 200} in response


def test_get_repository():
    bintray = Bintray()
    response = bintray.get_repository("conan", "conan-center")
    assert response.get("error") == False
    assert response.get("statusCode") == 200
    assert response.get("owner") == "conan"


def test_create_repo():
    bintray = Bintray()
    repo = "test_{}".format(random.randint(1,100000))
    response = bintray.create_repository("uilianries", repo, "generic", "only for test",
                                         labels=["foo", "bar"], business_unit="foobar")
    assert "created" in response.keys()
    assert response.get("error") == False
    assert response.get("name") == repo
