import pytest
from bintray.bintray import Bintray


@pytest.fixture()
def create_attributes():
    bintray = Bintray()
    attributes = [{"name": "att1", "values": ["val1"], "type": "string"}]
    return bintray.set_attributes("uilianries", "generic", "statistics", "test", attributes)


@pytest.fixture()
def create_file_attributes():
    bintray = Bintray()
    attributes = [{"name": "att1", "values": ["val1"], "type": "string"}]
    response = bintray.set_file_attributes("uilianries", "generic", "packages.json", attributes)
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
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_search_attributes(create_attributes):
    bintray = Bintray()
    attributes = [{'att1': ["val1", "val2"]}]
    response = bintray.search_attributes("uilianries", "generic", "statistics", attributes)
    assert {'error': False, 'statusCode': 200} in response


def test_get_files_attributes(create_file_attributes):
    assert [{'name': 'att1', 'type': 'STRING', 'values': ['val1']},
            {'error': False, 'statusCode': 200}] == create_file_attributes


def test_set_files_attributes():
    bintray = Bintray()
    attributes = [{'name': 'att1', 'values': ['val2'], 'type': "string"}]
    response = bintray.set_file_attributes("uilianries", "generic", "packages.json", attributes)
    assert [{'name': 'att1', 'type': 'STRING', 'values': ['val2']},
            {'error': False, 'statusCode': 200}] == response


def test_update_files_attributes():
    bintray = Bintray()
    attributes = [{"name": "att1", "values": ["val3"], "type": "string"}]
    response = bintray.update_file_attributes("uilianries", "generic", "packages.json", attributes)
    assert [{'name': 'att1', 'type': 'STRING', 'values': ['val3']},
            {'error': False, 'statusCode': 200}] == response


def test_delete_file_attributes(create_file_attributes):
    bintray = Bintray()
    attributes = ["att1"]
    response = bintray.delete_file_attributes("uilianries", "generic", "packages.json", attributes)
    assert {'error': False,
            'message': 'Attributes were deleted successfully from the following file path: '
                       'packages.json',
            'statusCode': 200} == response


def test_search_file_attributes(create_file_attributes):
    bintray = Bintray()
    attributes = [{'att1': ["val1"]}]
    response = bintray.search_file_attributes("uilianries", "generic", attributes)
    assert "packages.json" == response[0]["name"]

