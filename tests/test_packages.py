from bintray.bintray import Bintray


def test_get_packages():
    bintray = Bintray()
    response = bintray.get_packages("uilianries", "conan")
    assert {'error': False, 'statusCode': 200} in response
