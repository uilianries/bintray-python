from bintray.bintray import Bintray


def test_get_product_signed_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_product_signed_eulas("jfrog", "bintray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (404): 404 Client Error: Not Found for url: " \
           "https://api.bintray.com/products/jfrog/bintray/signed_eulas" == error_message


def test_get_all_products_signed_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_all_products_signed_eulas("jfrog")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): 403 Client Error: Forbidden for url: " \
           "https://api.bintray.com/products/jfrog/_all/signed_eulas" == error_message
