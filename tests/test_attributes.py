# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_attributes():
    bintray = Bintray()
    response = bintray.get_attributes("uilianries", "generic", "statistics", "test")
    assert [{'error': False, 'statusCode': 200}] == response

    response = bintray.get_attributes("uilianries", "generic", "statistics", "test", ["name"])
    assert [{'error': False, 'statusCode': 200}] == response

