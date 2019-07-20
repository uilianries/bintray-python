from bintray.bintray import Bintray


def test_get_package_release_notes():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_package_release_notes("uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): No release notes found for subject 'uilianries' repo 'generic' " \
           "and pkg 'statistics' in the package level. Please check the version level release " \
           "notes" == error_message

