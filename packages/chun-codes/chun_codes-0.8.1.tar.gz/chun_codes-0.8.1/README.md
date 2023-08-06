# chun_codes
Set of Python 2.7 and 3.xx codes used in astrochun's codes

[![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/astrochun/chun_codes/Python%20package/master?color=blue&label=build%20%28master%29&logo=github)](https://github.com/astrochun/chun_codes/actions?query=workflow%3A%22Python+package%22+branch%3Amaster)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/astrochun/chun_codes/Python%20package?color=blue&label=build%20%28latest%29&logo=github)](https://github.com/astrochun/chun_codes/actions?query=workflow%3A%22Python+package%22)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chun-codes)
[![PyPI](https://img.shields.io/pypi/v/chun-codes?color=blue)](https://pypi.org/project/chun-codes)
![License](https://img.shields.io/github/license/astrochun/chun_codes?color=blue)


## Installation

For Python 3.7+, use PyPI!

```
$ (sudo) pip install chun-codes
```

For Python 2.7, at the moment it is not built and available on PyPI, so
please clone and install:

```
$ git clone https://github.com/astrochun/chun_codes.git
$ cd chun_codes
$ (sudo) python setup.py develop
```

Notes:
 1. No CI build test for 2.7
 2. Some dependencies (e.g., `pdfmerge`) are only compatible with python 2.7.
    This requires migrating to a better solution that works for python 3.7+