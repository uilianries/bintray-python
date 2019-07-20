from bintray.bintray import Bintray


def test_get_products():
    bintray = Bintray()
    response = bintray.get_products("jfrog")
    assert {'error': False, 'statusCode': 200} in response


def test_get_product():
    bintray = Bintray()
    response = bintray.get_product("jfrog", "xray")
    assert response["name"] == "xray"
