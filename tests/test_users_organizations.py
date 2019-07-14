# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_user():
    bintray = Bintray()
    response = bintray.get_user("uilianries")
    assert response.get("name") == "uilianries"
    assert response.get("error") == False
    assert response.get("statusCode") == 200


def test_get_organization():
    bintray = Bintray()
    response = bintray.get_organization("jfrog")
    assert response.get("name") == "jfrog"
    assert response.get("error") == False
    assert response.get("statusCode") == 200


def test_get_followers():
    bintray = Bintray()
    response = bintray.get_followers("uilianries")
    assert [{'name': 'solvingj'}, {'error': False, 'statusCode': 200}] == response


def test_search_user():
    bintray = Bintray()
    response = bintray.search_user("uilianries")
    assert {'error': False, 'statusCode': 200} in response
