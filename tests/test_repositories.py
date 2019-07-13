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


def test_link_package():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.link_package("uilianries", "statistics", "uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (403): 403 Client Error: Forbidden for url: " \
            "https://api.bintray.com/repository/uilianries/statistics/links/" \
            "uilianries/generic/statistics" == error_message


def test_unlink_package():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.unlink_package("uilianries", "statistics", "uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (404): 404 Client Error: Not Found for url: " \
            "https://api.bintray.com/repository/uilianries/statistics/links/" \
            "uilianries/generic/statistics" == error_message


def test_schedule_metadata_calculation():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.schedule_metadata_calculation("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/calc_metadata/uilianries/generic" == error_message


def test_get_geo_restrictions():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_geo_restrictions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/geo_restrictions" == error_message


def test_update_geo_restrictions():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_geo_restrictions("uilianries", "generic", white_list=["US", "CA"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/geo_restrictions" == error_message

    try:
        bintray.update_geo_restrictions("uilianries", "generic", black_list=["US", "CA"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/geo_restrictions" == error_message

    try:
        bintray.update_geo_restrictions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "At lease one parameter must be filled." == error_message

    try:
        bintray.update_geo_restrictions("uilianries", "generic", black_list=["US", "CA"],
                                        white_list=["CH", "RU"])
    except Exception as error:
        error_message = str(error)
    assert "The update can be done on one list only." == error_message


def test_delete_geo_restrictions():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_geo_restrictions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/geo_restrictions" == error_message


def test_get_ip_restrictions():
    bintray = Bintray()
    response = bintray.get_ip_restrictions("uilianries", "generic")
    assert {'black_cidrs': [],
            'error': False,
            'hasWritePermission': None,
            'statusCode': 200,
            'white_cidrs': []} == response


def test_set_ip_restrictions():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.set_ip_restrictions("uilianries", "generic", white_cidrs=["10.0.0.1/32"],
                                    black_cidrs=["192.168.0.1/32"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/ip_restrictions" == error_message

    try:
        bintray.set_ip_restrictions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "At lease one parameter must be filled." == error_message


def test_update_ip_restrictions():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_ip_restrictions("uilianries", "generic", add_white_cidrs=["10.0.0.1/32"],
                                       rm_white_cidrs=["10.0.0.2/32"],
                                       add_black_cidrs=["192.168.0.1/32"],
                                       rm_black_cidrs=["192.168.0.2/32"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/repos/uilianries/generic/ip_restrictions" == error_message

    try:
        bintray.update_ip_restrictions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "At lease one parameter must be filled." == error_message
