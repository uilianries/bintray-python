# -*- coding: utf-8 -*-

import random
import pytest
from bintray.bintray import Bintray

TEMPORARY_REPO = None


@pytest.fixture()
def create_repo():
    global TEMPORARY_REPO
    bintray = Bintray()
    TEMPORARY_REPO = "test_{}".format(random.randint(1, 100000))
    response = bintray.create_repository("uilianries", TEMPORARY_REPO, "generic", "only for test",
                                         labels=["foo", "bar"], business_unit="foobar")
    return response


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


def test_create_repo(create_repo):
    assert "created" in create_repo.keys()
    assert create_repo.get("error") == False
    assert create_repo.get("name") == TEMPORARY_REPO


def test_update_repo(create_repo):
    bintray = Bintray()
    response = bintray.update_repository("uilianries", TEMPORARY_REPO,
                                         description="only for update",
                                         labels=["papa", "tango"], business_unit="foobar",
                                         gpg_sign_metadata=False, gpg_sign_files=False,
                                         gpg_use_owner_key=False)
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_update_repo_empty(create_repo):
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_repository("uilianries", TEMPORARY_REPO)
    except ValueError as error:
        error_message = str(error)
    assert "At lease one parameter must be filled." == error_message


def test_delete_repo(create_repo):
    bintray = Bintray()
    response = bintray.delete_repository("uilianries", TEMPORARY_REPO)
    assert {'error': False, 'statusCode': 200, 'message': 'success'} == response


def test_search_repository():
    bintray = Bintray()
    response = bintray.search_repository("conan-center")
    assert response[0].get("name") == "conan-center"
    assert response[0].get("owner") == "conan"


def test_search_repository_empty():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.search_repository()
    except ValueError as error:
        error_message = str(error)
    assert "At lease one parameter must be filled." == error_message