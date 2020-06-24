# Changelog

### v2.2.1

Fixed README and PYPI 'long description'

### v2.2.0

* Fixed: `datetime has no attribute fromisoformat`
* `starcli` now supports 3.6
* Changed readme to rst type

### v2.1.0

Remove unneeded imports
* import argparse to just importing ArgumentParser
* removed dev-dependencies in setup.py and requirements.txt
* added requirements_dev.txt

### v2.0.0

Changed:
* migrated from click to argparse
* some other refactoring

Added:
* `--debug` option to view some debugging info

### v1.3.0

New:
* `--stars` option to specify amount of star needed

Changed:
* default amount if stars is now >=50
* stats emojis updated for list and table layout

Fixed:
* table can't display properly when language is none


### v1.2.2

github action workflow and readme updates


### v1.2.1

* format files with black
* add tests
* fix some files
* add codespell to requirements

### v1.2.0

refactor starcli

### v1.1.0
Fixed:

* Spelling mistakes (checked using codespell)
* code formatting (black)
* linting (pylint)

Added:
* github workflows
* README badges
...and more

### v1.0.0
Fmt option is now layout, with either list or table


### v0.0.1 initial release
initial release
