from bintray.bintray import Bintray


def _create_package():
    bintray = Bintray()
    response = bintray.create_package("uilianries", "generic", "qux", ["MIT"],
                                      "https://github.com/uilianries/bintray-python", None, "foo",
                                      ["test", "jfrog", "couse"], "http://example.com",
                                      "https://github.com/uilianries/bintray-python/issues",
                                      "uilianries/bintray-python", None, True)
    return response


def test_get_packages():
    bintray = Bintray()
    response = bintray.get_packages("uilianries", "conan")
    assert {'error': False, 'statusCode': 200} in response


def test_get_package():
    bintray = Bintray()
    response = bintray.get_package("uilianries", "generic", "statistics")
    assert response["name"] == "statistics"


def test_create_package():
    bintray = Bintray()
    try:
        bintray.get_package("uilianries", "generic", "qux")
        bintray.delete_package("uilianries", "generic", "qux")
    except:
        pass

    response = _create_package()

    assert response["name"] == "qux"
    assert response["error"] == False


def test_delete_package():
    bintray = Bintray()
    try:
        _create_package()
    except:
        pass

    response = bintray.delete_package("uilianries", "generic", "qux")

    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_update_package():
    bintray = Bintray()
    try:
        _create_package()
    except:
        pass

    response = bintray.update_package("uilianries", "generic", "qux", ["MIT"],
                                      "https://github.com/uilianries/bintray-python", None, "foo",
                                      ["test", "jfrog", "couse"], "http://example.com",
                                      "https://github.com/uilianries/bintray-python/issues",
                                      "uilianries/bintray-python", None, True)
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response


def test_search_package():
    bintray = Bintray()
    try:
        _create_package()
    except:
        pass

    response = bintray.search_package("qux", "foo", "uilianries", "generic")
    assert {'error': False, 'statusCode': 200} in response


def test_get_package_for_file():
    bintray = Bintray()
    response = bintray.get_package_for_file("uilianries", "generic", "packages.json")

    assert response["name"] == "statistics"
    assert response["repo"] == "generic"


def test_search_maven_package():
    bintray = Bintray()
    response = bintray.search_maven_package("com.jfrog.bintray.gradle", "*bintray*", None, "jfrog",
                                            "jfrog-jars")

    assert [{'error': False, 'statusCode': 200}] == response
