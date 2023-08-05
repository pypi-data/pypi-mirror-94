# Sands Python Functions

<p align="center">
<a href="https://github.com/ldsands/SandsPythonFunctions/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://github.com/ldsands/SandsPythonFunctions/blob/master/LICENSE"><img src="https://img.shields.io/github/license/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<img src="https://img.shields.io/github/repo-size/ldsands/SandsPythonFunctions?style=flat-square"></img>
<img src="https://img.shields.io/github/languages/count/ldsands/SandsPythonFunctions?style=flat-square"></img>
<a href=""><img src="https://img.shields.io/github/languages/top/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://github.com/ldsands/SandsPythonFunctions/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://github.com/ldsands/SandsPythonFunctions/commits/master"><img src="https://img.shields.io/github/last-commit/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://github.com/ldsands/SandsPythonFunctions/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues-raw/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://github.com/ldsands/SandsPythonFunctions/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/ldsands/SandsPythonFunctions?style=flat-square"></img></a>
<a href="https://pepy.tech/project/sandspythonfunctions"><img src="https://img.shields.io/pypi/dm/sandspythonfunctions?style=flat-square"></img></a>
<!-- <a href="https://lgtm.com/projects/g/ldsands/SandsPythonFunctions"><img src="https://img.shields.io/lgtm/grade/python/g/ldsands/SandsPythonFunctions.svg?logo=lgtm&logoWidth=18&style=flat-square"></img></a> -->
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>
<p>

<!-- <img src="_static/cache/matplotlib_pypi_downloads_badge.svg"/> -->
<!-- https://img.shields.io/lgtm/grade/python/g/ldsands/SandsPythonFunctions.svg?logo=lgtm&logoWidth=18&style=flat-square -->
<!-- https://img.shields.io/pypi/dm/sandspythonfunctions?style=flat-square -->

Some functions I find useful regularly and I put them all into one package for easy access

I created this using [Poetry](https://python-poetry.org/).

## Instructions

- To build this you must first install poetry see instructions [here](https://python-poetry.org/docs/#installation)
- However to make it easy to access this is all of the code you'll need on linux to make this run (note that I use zsh not bash for my shell)
    - First you must navigate to the folder containing these files `CHANGELOG.md   LICENSE  'README reference.md'   README.md   dist   poetry.lock   pyproject.toml   src`
    - You then to make sure that you have the python environment that you want activated
    - You can then enter the code below

```sh
poetry build
poetry install
```

## Basic Usage Example

TODO:

## Included Packages

### Functions from EmailFunctions

- 

### Functions from MultiprocessingFunctions

- 

### Functions from ParquetFunctions

- 

### Functions from PrintFunctions

- 

### Functions from TimerFunctions

- 

## CI/CD

See [this repo](https://github.com/speg03/shishakai/blob/971261e6f73ee8b9dcc83837b6c1a5f809c985f8/.github/workflows/upload-python-package.yml) for an example of someone using poetry with they're python project to upload to PyPI on push to master.

## Other Notes About This Code

I use "TESTCODE:" to designate code used in testing functions and scripts. I try to make sure to comment or delete those lines in the release versions of the package
