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
        bintray.create_entitlement("uilianries", "generic", "statistics", "test", "rw",
                                   ["key1", "key2"], "a/b/c", ["tag1", "tag2"])
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): This resource is only available for subjects with entitlement " \
           "management." == error_message

    try:
        bintray.create_entitlement("jfrog", access="rw", access_keys=["key1", "key2"], path="a/b/c",
                                   tags=["tag1", "tag2"], product="xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): forbidden" == error_message


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


def test_update_entitlement():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_entitlement("uilianries", "foobar", "generic", "statistics", "test", "rw",
                                   ["key1", "key2"], ["tag1", "tag2"])
    except Exception as error:
        error_message = str(error)

    assert "Could not PATCH (403): This resource is only available for subjects with entitlement " \
           "management." == error_message

    try:
        bintray.update_entitlement("jfrog", "foobar", access="rw", access_keys=["key1", "key2"],
                                   tags=["tag1", "tag2"], product="xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not PATCH (403): forbidden" == error_message


def test_search_entitlement_by_access_key():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.search_entitlement_by_access_key("uilianries", "foobar", "generic/statistics/test")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): Forbidden" == error_message


def test_search_entitlement_by_tag():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.search_entitlement_by_tag("tag1", "jfrog/test-repo")
    except Exception as error:
        error_message = str(error)

    assert "Could not GET (403): Forbidden" == error_message
