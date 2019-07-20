from bintray.bintray import Bintray


def test_regenerate_subject_url_signing_key():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.regenerate_subject_url_signing_key("uilianries")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (400): This action is not allowed for none-premium subject uilianries" \
           == error_message
