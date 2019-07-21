# Bintray Python

![logo](logo.png)


[![codecov](https://codecov.io/gh/uilianries/bintray-python/branch/master/graph/badge.svg)](https://codecov.io/gh/uilianries/bintray-python)
[![Maintainability](https://api.codeclimate.com/v1/badges/eb7ea878f71e2a464172/maintainability)](https://codeclimate.com/github/uilianries/bintray-python/maintainability)
[![Build Status](https://travis-ci.com/uilianries/bintray-python.svg?branch=master)](https://travis-ci.com/uilianries/bintray-python)
[![Download Pypi](https://img.shields.io/badge/pypi-download-blue.svg)](https://pypi.org/manage/project/bincrafters-conventions)


#### About

**The Python wrapper for Bintray API**

#### Installation

    pip install bintray-python

#### Usage

To search repositories from a subject:

```python
from bintray.bintray import Bintray

bintray = Bintray()
response = bintray.search_repository("conan-center")
print(response)
```

#### Documentation

Please, read the official documentation from Bintray: https://bintray.com/docs/api

Alternatively, you can check the project reference on https://bintray-python.readthedocs.io

#### License
[MIT](LICENSE)
