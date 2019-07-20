from bintray.bintray import Bintray


def test_get_stream_api():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_stream_api("uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): Forbidden" == error_message
