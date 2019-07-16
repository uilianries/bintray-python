# -*- coding: utf-8 -*-

import pytest
from bintray.bintray import Bintray


@pytest.fixture()
def create_attributes():
    bintray = Bintray()
    attributes = [{"name": "att1", "values": ["val1"], "type": "string"}]
    response = bintray.set_attributes("uilianries", "generic", "statistics", "test", attributes)
    return response


def test_get_attributes(create_attributes):
    bintray = Bintray()
    response = bintray.get_attributes("uilianries", "generic", "statistics", "test")
    assert [{'name': 'att1', 'type': 'string', 'values': ['val1']},
            {'error': False, 'statusCode': 200}] == response

    response = bintray.get_attributes("uilianries", "generic", "statistics", "test", ["att1"])
    assert [{'name': 'att1', 'type': 'string', 'values': ['val1']},
            {'error': False, 'statusCode': 200}] == response


def test_set_attributes(create_attributes):
    assert [{'name': 'att1', 'type': 'string', 'values': ['val1']},
            {'error': False, 'statusCode': 200}] == create_attributes


def test_update_attributes(create_attributes):
    bintray = Bintray()
    attributes = [{"name": "att1", "values": ["val2"], "type": "string"}]
    response = bintray.update_attributes("uilianries", "generic", "statistics", "test", attributes)
    assert [{'name': 'att1', 'type': 'string', 'values': ['val2']},
            {'error': False, 'statusCode': 200}] == response


def test_delete_attributes(create_attributes):
    bintray = Bintray()
    attributes = ["att1"]
    response = bintray.delete_attributes("uilianries", "generic", "statistics", "test", attributes)
    assert {'error': False, 'statusCode': 200} == response
