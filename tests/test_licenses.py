from bintray.bintray import Bintray


def test_get_oss_licenses():
    bintray = Bintray()
    licenses = bintray.get_oss_licenses()
    copyfree = {'name': 'Copyfree', 'longname': 'Copyfree', 'url': 'http://copyfree.org/'}
    assert copyfree in licenses


def test_get_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_org_proprietary_licenses(org="jfrog")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): 403 Client Error: Forbidden for url: " \
            "https://api.bintray.com/orgs/jfrog/licenses" == error_message


def test_get_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_user_proprietary_licenses(user="uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (400): 400 Client Error: Bad Request for url: " \
            "https://api.bintray.com/users/uilianries/licenses" == error_message


def test_bad_credentials_for_get_oss_licenses():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        bintray.get_oss_licenses()
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
            "https://api.bintray.com/licenses/oss_licenses" == error_message


def test_create_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_org_proprietary_license(org="jfrog", name='foobar', description='foo',
                                                url='https://opensource.org/licenses/MIT')
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): 403 Client Error: Forbidden for url: " \
            "https://api.bintray.com/orgs/jfrog/licenses" == error_message


def test_create_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.create_user_proprietary_license(user="uilianries", name='foobar', description='foo',
                                                url='https://opensource.org/licenses/MIT')
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/users/uilianries/licenses" == error_message


def test_update_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_org_proprietary_license(org="jfrog", custom_license_name="foobar",
                                               description="MIT license",
                                               url="https://opensource.org/licenses/MIT")
    except Exception as error:
        error_message = str(error)

    assert "Could not PATCH (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/orgs/jfrog/licenses/foobar" == error_message


def test_update_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.update_user_proprietary_license(user="uilianries",
                                                custom_license_name="foo",
                                                description="MIT license",
                                                url="https://opensource.org/licenses/MIT")
    except Exception as error:
        error_message = str(error)

    assert "Could not PATCH (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/users/uilianries/licenses/foo" == error_message


def test_delete_org_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_org_proprietary_license(org="jfrog", custom_license_name="foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/orgs/jfrog/licenses/foobar" == error_message


def test_delete_user_proprietary_licenses():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.delete_user_proprietary_license(user="uilianries", custom_license_name="foobar")
    except Exception as error:
        error_message = str(error)
    assert "Could not DELETE (400): 400 Client Error: Bad Request for url: " \
           "https://api.bintray.com/users/uilianries/licenses/foobar" == error_message
