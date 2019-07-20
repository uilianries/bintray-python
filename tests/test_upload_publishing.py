import tempfile

from bintray.bintray import Bintray


def test_upload_content():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt",
                                      temp_path, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_bad_credentials_for_upload_content():
    bintray = Bintray("foobar", "85abc6aece02515e8bd87b9754a18af697527d88")
    error_message = ""
    try:
        _, temp_path = tempfile.mkstemp()
        bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt", temp_path)
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/content/uilianries/generic/statistics/test/test.txt?" \
           "publish=1&override=0&explode=0" == error_message


def test_maven_upload():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    error_message = ""
    try:
        bintray.maven_upload("uilianries", "generic", "statistics", "pom.xml",
                             temp_path, publish=True)
    except Exception as error:
        error_message = str(error)
    assert "Could not PUT (400): 400 Client Error: Bad Request for url:" \
           " https://api.bintray.com/maven/uilianries/generic/statistics/pom.xml" \
           "?publish=1" == error_message


def test_debian_upload():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.debian_upload("uilianries", "generic", "statistics", "test", "test.deb",
                                     temp_path, deb_distribution="wheezy", deb_component="main",
                                     deb_architecture="i386,amd64", publish=True, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response


def test_publish_uploaded_content():
    bintray = Bintray()
    response = bintray.publish_uploaded_content("uilianries", "generic", "statistics", "test")
    assert {'error': False, 'files': 0, 'statusCode': 200} == response


def test_discard_uploaded_content():
    bintray = Bintray()
    response = bintray.discard_uploaded_content("uilianries", "generic", "statistics", "test")
    assert {'error': False, 'files': 0, 'statusCode': 200} == response


def test_delete_content():
    bintray = Bintray()
    _, temp_path = tempfile.mkstemp()
    response = bintray.upload_content("uilianries", "generic", "statistics", "test", "test.txt",
                                      temp_path, override=True)
    assert {'error': False, 'message': 'success', 'statusCode': 201} == response

    response = bintray.delete_content("uilianries", "generic", "test.txt")
    assert {'error': False, 'message': 'success', 'statusCode': 200} == response
