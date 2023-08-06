# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2021-02-13
### Fixed
- Plot functions did remove figures, leaving documentation without example diagrams.

### Removed
- Deprecated alpha note from README.md

## [1.0.0rc1] - 2021-02-13
### Added
- .coveragerc, .travis.yml, makefile, tox.ini, tests/load_test.py, tests/plot_test.py

### Changed
- CreatesCurves inherits from abc.ABC
- setup.py to setup.cfg

### Removed
- Deprecated functions create, load

## [0.5a0.post1] - 2021-01-08
### Fixed
- Missing requirements for installation via pip.

## [0.5a0] - 2021-01-02
### Added
- New families of curves *VerticalLinear0*, *VerticalLinear1*, *VerticalLinear2* and
  *VerticalLinear3*.

## [0.4a0] - 2020-12-27
### Added
- New families of curves *DiagonalLinear0*, *DiagonalLinear1*, *DiagonalLinear2* and
  *DiagonalLinear3*.

### Changed
- The necessity of sub classes of static linear families of curves was removed, changing
  the creation and documentation layout. In this case all subclasses were removed, since
  they wasn't meant to be used directly anyway.

## [0.3a0] - 2020-12-17
### Added
- New families of curves *HorizontalLinear1*, *HorizontalLinear2* and
 *HorizontalLinear3*.

## [0.2a1] - 2020-12-17
### Fixed
- Missing parameter leading to broken installation.
- Missing requirement 'dicthandling'

## [0.2a0] - 2020-12-15
### Added
- A normal distributed linear family of curves with *LinearHorizontal0*.
- Support for loading curve creation parameters from json files.
- *resources* subpackage for parameter files.

### Changed
- Turned module `examplecurves.py` into a `examplecurves` package.
- Shifted project to *setuptools_scm*; updated setup.py

### Removed
- Constant \_\_version\_\_ is removed; package version is now managed solely by git
  tags.

## [0.1a0] - 2020-12-05
### Changed
- added class `Static` to distinguish static curves from random curves, which
  are on the way.

### deprecated
- Method `create` will be moved to `Static` in the next release.

## [0.0a1] - 2020-12-05
- First code release of examplecurves