from bintray.bintray import Bintray


def test_get_list_package_download_log_files():
    bintray = Bintray()
    response = bintray.get_list_package_download_log_files("conan-community", "conan",
                                                           "7z_installer:conan")
    assert {'error': False, 'statusCode': 200} in response



