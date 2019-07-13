# -*- coding: utf-8 -*-

import datetime
import pytest
from bintray.bintray import Bintray


PACKAGE_VERSION = None

@pytest.fixture
def create_version():
    global PACKAGE_VERSION
    bintray = Bintray()
    now = datetime.datetime.now()
    PACKAGE_VERSION = now.strftime("%Y%m%d%H%M%S%f")
    released = now.strftime("%Y-%m-%d")

    return bintray.create_version("uilianries", "generic", "statistics", version=PACKAGE_VERSION,
                                  released=released, vcs_tag="0.1.0")


def test_get_version():
    bintray = Bintray()
    response = bintray.get_version("uilianries", "generic", "statistics", version="_latest")
    assert response.get("error") == False
    assert response.get("name") == "test"
    assert response.get("statusCode") == 200


def test_create_version(create_version):
    assert create_version.get("error") == False
    assert create_version.get("name") == PACKAGE_VERSION
    assert create_version.get("statusCode") == 201


def test_delete_version(create_version):
    bintray = Bintray()
    response = bintray.delete_version("uilianries", "generic", "statistics",
                                      version=PACKAGE_VERSION)
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_update_version(create_version):
    bintray = Bintray()
    response = bintray.update_version("uilianries", "generic", "statistics",
                                      version=PACKAGE_VERSION, description="foobar",
                                      vcs_tag="0.1.1")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response
