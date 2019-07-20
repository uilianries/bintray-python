import pytest
from bintray.bintray import Bintray


@pytest.fixture()
def create_release_notes():
    bintray = Bintray()
    return bintray.create_package_release_notes_bintray("uilianries", "generic", "statistics",
                                                        "markdown", "test")


@pytest.fixture()
def create_version_release_notes():
    bintray = Bintray()
    return bintray.create_version_release_notes_bintray("uilianries", "generic", "statistics",
                                                        "test", "markdown", "test")


def test_get_package_release_notes(create_release_notes):
    bintray = Bintray()
    response = bintray.get_package_release_notes("uilianries", "generic", "statistics")
    assert {'bintray': {'content': 'test', 'syntax': 'MARKDOWN'},
            'error': False,
            'owner': 'uilianries',
            'package': 'statistics',
            'repo': 'generic',
            'statusCode': 200} == response


def test_create_package_release_notes_github():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_package_release_notes_github("uilianries", "generic", "statistics",
                                                    "uilanries/bintray-python", "0.7.0/README.md")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): Failed to set release notes files for subject 'uilianries' repo "\
           "'generic' and pkg 'statistics', Please check your github details" == error_message


def test_create_package_release_notes_bintray(create_release_notes):
    assert {'bintray': {'content': 'test', 'syntax': 'MARKDOWN'},
            'error': False,
            'owner': 'uilianries',
            'package': 'statistics',
            'repo': 'generic',
            'statusCode': 200} == create_release_notes


def test_delete_package_release_notes(create_version_release_notes):
    bintray = Bintray()
    response = bintray.delete_package_release_notes("uilianries", "generic", "statistics")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_get_version_release_notes(create_version_release_notes):
    bintray = Bintray()
    response = bintray.get_version_release_notes("uilianries", "generic", "statistics", "test")
    assert {'bintray': {'content': 'test', 'syntax': 'MARKDOWN'},
            'error': False,
            'owner': 'uilianries',
            'package': 'statistics',
            'repo': 'generic',
            'statusCode': 200,
            'version': 'test'} == response


def test_create_version_release_notes_bintray(create_version_release_notes):
    assert {'bintray': {'content': 'test', 'syntax': 'MARKDOWN'},
            'error': False,
            'owner': 'uilianries',
            'package': 'statistics',
            'repo': 'generic',
            'statusCode': 200,
            'version': 'test'} == create_version_release_notes


def test_create_version_release_notes_github():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_version_release_notes_github("uilianries", "generic", "statistics",
                                                           "test", "uilanries/bintray-python",
                                                           "0.7.0/README.md")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (400): Failed to set release notes files for subject 'uilianries' repo "\
           "'generic' pkg 'statistics and version 'test', Please check your github details and " \
           "make sure the package of this version has the github repo configured" == error_message
