# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_webhooks():
    bintray = Bintray()
    response = bintray.get_webhooks("uilianries", "generic")
    assert {'error': False, 'statusCode': 200} in response


