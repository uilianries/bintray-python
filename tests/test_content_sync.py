from bintray.bintray import Bintray


def test_sync_version_artifacts_to_maven_central():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.sync_version_artifacts_to_maven_central("uilianries", "generic", "statistics",
                                                        "test", "username", "password")
    except Exception as error:
        error_message = str(error)

    assert "Could not POST (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/maven_central_sync/uilianries/generic/statistics/versions/test"\
           == error_message
