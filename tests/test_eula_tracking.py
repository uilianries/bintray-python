from bintray.bintray import Bintray


def test_get_product_signed_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_product_signed_eulas("jfrog", "xray")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): forbidden" == error_message


def test_get_all_products_signed_eulas():
    bintray = Bintray()
    error_message = ""
    try:
        bintray.get_all_products_signed_eulas("jfrog")
    except Exception as error:
        error_message = str(error)
    assert "Could not GET (403): forbidden" == error_message
