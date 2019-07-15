# -*- coding: utf-8 -*-

from bintray.bintray import Bintray


def test_get_teams():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.get_user_teams("uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): 400 Client Error: Bad Request for url: " \
            "https://api.bintray.com/users/uilianries/teams" == error_message

    try:
        bintray.get_org_teams("jfrog")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/orgs/jfrog/teams" == error_message


def test_get_team():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.get_user_team("uilianries", "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/users/uilianries/teams/foobar" == error_message

    try:
        bintray.get_org_team("jfrog", "bintray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/orgs/jfrog/teams/bintray" == error_message


def test_create_team():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.create_user_team("uilianries", "foobar", ["uilianries"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/users/uilianries/teams" == error_message

    try:
        bintray.create_org_team("jfrog", "bintray", ["uilianries"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/orgs/jfrog/teams" == error_message
