# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_org_gpg_public_key():
    bintray = Bintray()
    response = bintray.get_org_gpg_public_key("jfrog")
    assert response.get("error") == False
    assert response.get("statusCode") == 200
    assert "BEGIN PGP PUBLIC KEY BLOCK" in response.get("message")


def test_get_user_gpg_public_key():
    bintray = Bintray()
    response = bintray.get_user_gpg_public_key("bintray")
    assert response.get("error") == False
    assert response.get("statusCode") == 200
    assert "BEGIN PGP PUBLIC KEY BLOCK" in response.get("message")


def test_gpg_sign_version():
    bintray = Bintray()
    response = bintray.gpg_sign_version("uilianries", "generic", "statistics", "test")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response or \
           {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_gpg_sign_file():
    bintray = Bintray()
    response = bintray.gpg_sign_file("uilianries", "generic", "packages.json")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response or \
           {'error': False, 'message': 'success', 'statusCode': 201} == response
