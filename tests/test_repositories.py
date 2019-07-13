# -*- coding: utf-8 -*-

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
