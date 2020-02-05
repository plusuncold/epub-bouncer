# EPUB Bouncer

Correct misspellings from EPUB files - with a simple, intuitive interface.

Often EPUB files from OCR'ed sources contain misspellings, such as random insertions or one character being read as two characters.

## Usage

To correct a EPUB file for the EPUB file `book.epub`:
```
   python3 bouncer.py --epub-name book.epub
```

To use a different temp folder name (default is `temp`):
```
   python3 bouncer.py --epub-name book.epub --temp-folder temp_folder
```
## Currect restrictions

The program is currently only compatible with EPUB 2 files.

At the moment, only the 'en-US' dictionary is supported (American English)

## Roadmap

Checkout the [roadmap](https://github.com/plusuncold/ebook-cleanup/wiki/Roadmap).
