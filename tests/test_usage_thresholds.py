from bintray.bintray import Bintray


def test_get_usage_threshold_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_usage_threshold_org("bincrafters")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): Usage thresholds are only available for organizations on an " \
           "Enterprise plan." == error_message


def test_get_usage_threshold_repository():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_usage_threshold_repository("bincrafters", "public-conan")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): Usage thresholds are only available for organizations on an " \
           "Enterprise plan." == error_message


def test_get_usage_threshold_business_unit():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_usage_threshold_business_unit("jfrog", "conan")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): BusinessUnit 'conan' was not found" == error_message


def test_create_usage_threshold_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_usage_threshold_org("jfrog", 10000, 10000, 10000, ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): forbidden" == error_message


def test_create_usage_threshold_repository():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_usage_threshold_repository("jfrog", "xray", 10000, 10000, 10000,
                                                  ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): forbidden" == error_message


def test_create_usage_threshold_business_unit():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_usage_threshold_business_unit("jfrog", "xray", 10000, 10000, 10000,
                                                  ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (404): BusinessUnit 'xray' was not found" == error_message


def test_update_usage_threshold_org():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_usage_threshold_org("jfrog", 10000, 10000, 10000, ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (403): forbidden" == error_message


def test_update_usage_threshold_repository():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_usage_threshold_repository("jfrog", "xray", 10000, 10000, 10000,
                                                  ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (403): forbidden" == error_message


def test_update_usage_threshold_business_unit():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_usage_threshold_business_unit("jfrog", "xray", 10000, 10000, 10000,
                                                  ["user@mail.com"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (404): BusinessUnit 'xray' was not found" == error_message
