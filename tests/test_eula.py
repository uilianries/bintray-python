from bintray.bintray import Bintray


def test_get_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_eulas("jfrog", "bintray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/jfrog/bintray/eulas" == error_message


def test_get_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_eula("jfrog", "bintray", "eula")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/jfrog/bintray/eulas/eula" == error_message


def test_create_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_eula("uilianries", "generic", "eula", "foobar", "plain_text", "nothing",
                            ["1.0"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/uilianries/generic/eulas" == error_message


def test_update_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_eula("uilianries", "generic", "eula", "foobar", "plain_text", "nothing",
                            ["1.0"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/uilianries/generic/eulas/eula" == error_message


def test_delete_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_eula("uilianries", "generic", "eula")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/uilianries/generic/eulas/eula" == error_message
