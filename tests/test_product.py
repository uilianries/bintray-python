from bintray.bintray import Bintray


def test_get_products():
    bintray = Bintray()
    response = bintray.get_products("jfrog")
    assert {'error': False, 'statusCode': 200} in response


def test_get_product():
    bintray = Bintray()
    response = bintray.get_product("jfrog", "xray")
    assert response["name"] == "xray"


def test_create_product():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_product("uilianries", "test", "test_display", "another test product",
                               "http://www.example.com",
                               "http://github.com/uilianries/bintray-python",
                               ["generic/statistics"])
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): Package generic/statistics should be under premium repository " \
           "for owning product." == error_message
