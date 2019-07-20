from bintray.bintray import Bintray


def test_get_access_keys_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_access_keys_org("bincrafters")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message


def test_get_access_keys_user():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_access_keys_user("uilianries")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message


def test_get_access_key_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_access_key_org("bincrafters", "foobar")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message


def test_get_access_key_user():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_access_key_user("uilianries", "foobar")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message


def test_create_access_key_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_access_key_org("bincrafters", "foobar")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): This resource is only available for subjects with entitlement " \
           "management." == error_message


def test_create_access_key_user():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_access_key_user("uilianries", "foobar")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): This resource is only available for subjects with entitlement " \
           "management." == error_message
