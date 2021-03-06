# EPUB Bouncer ![travis_build_status](https://travis-ci.org/plusuncold/epub-bouncer.svg?branch=master)

Correct misspellings from EPUB files - with a simple interface.

Often EPUB files from OCR'ed sources contain misspellings, such as random insertions 
or one character being read as two characters. `bouncer` applies language rules to
make it easy to remove these errors from EPUB files.

## Installation

Bouncer depends on the spelling library `enchant`. This will need to be installed
prior to running bouncer. On Windows the wheel packaged with `pyenchant` contains
the needed binary. However it should be known that that this binary only provides
access to the provider `hunspell`. To use any other providers on Windows, you will
need to use WSL or another Linux emulation tool.

On Linux and MacOS, use your package manager to install `enchant`.

On Arch there seems to be a problem with the bindings `pyenchant` is using to
access `enchant`, resulting in `pip` not being able to find the library, and thus
it cannot install `pyenchant`.

Once `enchant` is installed, install the required Python packages with
`pip install -r requirements.txt`

## Development

Additional packages required for development are in `requirements-dev.txt`. Commits
are checked with Travis CI [Travis CI](https://travis-ci.org/plusuncold/epub-bouncer)
against `pytest` unit testing and `flake8` unit testing. 
Enabling [pre-commit](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/)
can help ensure that code meets these requirements before committing.


## Usage

To correct a EPUB file for the EPUB file `book.epub`:
```
   python3 bouncer/bouncer.py --epub-name book.epub
```

To use a different temp folder name (default is `temp`):
```
   python3 bouncer/bouncer.py --epub-name book.epub --temp-folder temp_folder
```
## Currect restrictions

The program is currently only compatible with EPUB 2 files.

At the moment, only the 'en-US' dictionary is supported (American English)

## Roadmap

Checkout the [roadmap](https://github.com/plusuncold/ebook-cleanup/wiki/Roadmap).
