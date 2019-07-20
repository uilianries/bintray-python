from bintray.bintray import Bintray


def test_get_eulas():
    bintray = Bintray()
    response = bintray.get_eulas("jfrog", "xray")
    assert response[0]["name"] == "XRAY_License_Agreement"


def test_get_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_eula("jfrog", "xray", "eula")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): forbidden" == error_message


def test_create_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_eula("uilianries", "generic", "eula", "foobar", "plain_text", "nothing",
                            ["1.0"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (404): Product 'generic' was not found" == error_message


def test_update_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_eula("uilianries", "generic", "eula", "foobar", "plain_text", "nothing",
                            ["1.0"])
    except Exception as error:
        error_message = str(error)
    assert "Could not PATCH (404): Product 'generic' was not found" == error_message


def test_delete_eula():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_eula("uilianries", "generic", "eula")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (404): Product 'generic' was not found" == error_message
