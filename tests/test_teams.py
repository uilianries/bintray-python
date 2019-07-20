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


def test_update_team():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.update_user_team("uilianries", "foobar", ["uilianries"], True, "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/users/uilianries/teams/foobar" == error_message

    try:
        bintray.update_org_team("jfrog", "bintray", ["uilianries"], True, "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/orgs/jfrog/teams/bintray" == error_message


def test_delete_team():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.delete_user_team("uilianries", "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/users/uilianries/teams/foobar" == error_message

    try:
        bintray.delete_org_team("jfrog", "bintray",)
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/orgs/jfrog/teams/bintray" == error_message


def test_get_all_team_permissions():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.get_all_team_permissions("uilianries", "generic")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/repos/uilianries/generic/permissions" == error_message


def test_get_team_permissions():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.get_team_permissions("uilianries", "generic", "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/repos/uilianries/generic/permissions/foobar" == error_message


def test_set_team_permissions():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.set_team_permissions("uilianries", "generic", "foobar", "read")
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/repos/uilianries/generic/permissions" == error_message


def test_delete_team_permission():
    bintray = Bintray()
    error_message = ""

    try:
        bintray.delete_team_permission("uilianries", "generic", "foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/repos/uilianries/generic/permissions/foobar" == error_message
