# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_webhooks():
    bintray = Bintray()
    response = bintray.get_webhooks("uilianries", "generic")
    assert {'error': False, 'statusCode': 200} in response


def test_register_webhook():
    bintray = Bintray()
    response = bintray.register_webhook("uilianries", "generic", "statistics",
                                        "https://example.com/", "get")
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_test_webhook():
    bintray = Bintray()
    response = bintray.test_webhook("uilianries", "generic", "statistics", "tests",
                                    "https://example.com/", "get")
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_delete_webhook():
    bintray = Bintray()
    response = bintray.delete_webhook("uilianries", "generic", "statistics")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response
