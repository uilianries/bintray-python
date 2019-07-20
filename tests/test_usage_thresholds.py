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
