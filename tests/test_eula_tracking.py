from bintray.bintray import Bintray


def test_get_product_signed_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_product_signed_eulas("jfrog", "bintray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (401): 401 Client Error: Unauthorized for url: " \
           "https://api.bintray.com/products/jfrog/bintray/signed_eulas" == error_message
