from bintray.bintray import Bintray


def test_get_readme():
    bintray = Bintray()
    response = bintray.get_readme("bincrafters", "public-conan", "Catch%3Abincrafters")
    assert {'error': False,
            'github': {'github_repo': 'bincrafters/conan-catch'},
            'owner': 'bincrafters',
            'package': 'Catch:bincrafters',
            'repo': 'public-conan',
            'statusCode': 200} == response


def test_create_readme():
    bintray = Bintray()
    response = bintray.create_readme("uilianries", "generic", "statistics",
                                  github="uilianries/bintray-python")
    assert {'error': False,
            'github': {'github_repo': 'uilianries/bintray-python'},
            'owner': 'uilianries',
            'package': 'statistics',
            'repo': 'generic',
            'statusCode': 200} == response


def test_create_product_readme():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_product_readme("jfrog", "xray",
                                      github="uilianries/bintray-python")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): forbidden" == error_message


def test_delete_product_readme():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_product_readme("jfrog", "xray")
    except Exception as error:
        error_message = str(error)

    assert "Could not DELETE (403): forbidden" == error_message
