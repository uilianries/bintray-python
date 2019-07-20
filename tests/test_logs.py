import os
from bintray.bintray import Bintray


def test_get_list_package_download_log_files():
    bintray = Bintray()
    response = bintray.get_list_package_download_log_files("conan-community", "conan",
                                                           "7z_installer:conan")
    assert {'error': False, 'statusCode': 200} in response


def test_download_package_download_log_file():
    bintray = Bintray()
    response = bintray.get_list_package_download_log_files("conan-community", "conan",
                                                           "7z_installer:conan")
    log_name = response[0]["name"]
    bintray.download_package_download_log_file("conan-community", "conan",
                                               "7z_installer:conan", log_name, log_name)
    assert os.path.isfile(log_name)
