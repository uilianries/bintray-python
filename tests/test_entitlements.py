from bintray.bintray import Bintray


def test_get_entitlements():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_entitlements("uilianries", "generic", "statistics", "test")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message

    try:
        bintray.get_entitlements("jfrog", product="xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): forbidden" == error_message


def test_create_entitlement():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_entitlement("uilianries", "foobar", "generic", "statistics", "test")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): This resource is only available for subjects with entitlement " \
           "management." == error_message

    try:
        bintray.create_entitlement("jfrog", "foobar", product="xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): forbidden" == error_message


def test_delete_entitlement():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_entitlement("uilianries", "foobar", "generic", "statistics", "test")
    except Exception as error:
        error_message = str(error)

    assert "Could not DELETE (403): This resource is only available for subjects with entitlement "\
           "management." == error_message

    try:
        bintray.delete_entitlement("jfrog", "foobar", product="xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not DELETE (403): forbidden" == error_message


