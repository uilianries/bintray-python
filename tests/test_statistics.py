from bintray.bintray import Bintray


def test_get_daily_downloads():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_daily_downloads("uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): This resource is only available for premium packages." \
           == error_message


def test_get_total_downloads():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_total_downloads("uilianries", "generic", "statistics")
    except Exception as error:
        error_message = str(error)
    assert "Could not POST (403): This resource is only available for premium packages." \
           == error_message
