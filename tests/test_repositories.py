# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_repositories():
    bintray = Bintray()
    response = bintray.get_repositories("conan")
    assert {'error': False, 'statusCode': 200} in response
