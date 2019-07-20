import pytest
from bintray.bintray import Bintray


@pytest.fixture()
def create_release_notes():
    bintray = Bintray()
    return bintray.create_package_release_notes_bintray("uilianries", "generic", "statistics",
                                                        "markdown", "test")


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
