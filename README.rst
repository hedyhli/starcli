|Cover image|

.. _browse-trending-repos-on-github-by-starstarsstar-from-your-command-line-computer:

Browse trending repos on Github by ⭐stars⭐ from your command line 💻
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|checks| |pr checks| |Code style: black| |PyPI version| |GitHub license|
|PRs Welcome| |made-with-python|

Prerequisites
-------------

-  Requires Python 3.7 or greater

Installation
------------

.. code:: sh

   pip install starcli

Usage
-----

.. code:: sh

   usage: starcli [-h] [-l LANG] [-d DATE] [-L {list,table}] [-s STARS] [--debug]

   Browse trending repos on GitHub by stars

   optional arguments:
     -h, --help            show this help message and exit
     -l LANG, --lang LANG  Language filter eg:python
     -d DATE, --date DATE  Specify repo creation date in ISO8601 format YYYY-MM-DD
     -L {list,table}, --layout {list,table}
                           The output format (list or table), default is list
     -s STARS, --stars STARS
                           Range of stars required, default is '>=50'
     --debug               Turn on debugging mode

Development
-----------

This project is still in its early development stage, contributions are not suggested
but issue reporting are welcome. Once everything is stable, we will update this
section and let your know how to contribute.


.. |Cover image| image:: https://github.com/hedythedev/starcli/blob/main/starcli-small-cover.png
.. |checks| image:: https://github.com/hedythedev/starcli/workflows/checks/badge.svg
.. |pr checks| image:: https://github.com/hedythedev/starcli/workflows/pr%20checks/badge.svg
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |PyPI version| image:: https://badge.fury.io/py/starcli.svg
   :target: https://badge.fury.io/py/starcli
.. |GitHub license| image:: https://img.shields.io/github/license/hedythedev/starcli.svg
   :target: https://github.com/hedythedev/starcli/blob/main/LICENSE
.. |PRs Welcome| image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: http://makeapullrequest.com
.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
