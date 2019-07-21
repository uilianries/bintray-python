Installation
============

    pip install bintray-python

Usage
=====

To search repositories from a subject:

.. code-block:: python

    from bintray.bintray import Bintray

    bintray = Bintray()
    response = bintray.search_repository("conan-center")
    print(response)


Documentation
=============

Please, read the official documentation from Bintray: https://bintray.com/docs/api