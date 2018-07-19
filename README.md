# PDFSlides
by Sam Ehrenstein (sie3@case.edu)

## Overview
This program is designed to display PDF files in a looped slideshow, although it can display
any PNG images. For PDFs, it is also able to convert PDF files to PNG images.

## Requirements
This program requires Python 3.2.x or greater, as well as the external libraries `wand` and `PIL`. Both can
be installed from PIP.

## Usage
### Image directory structure
All images must be in a directory called `images`, a subdirectory of the directory containing
`viewer.py`. As of now, the directories will be displayed in sorted order, as determined by
Python.

Within each directory are PNG files named in the form `#.png`, where `# is a number. They will be
displayed in numeric order.

### With PDFs
Any PDF in the same directory as `viewer.py` will be converted to PNG images, numbered by page. They
will be located in `images/<filename minus extension>`.

### With other images
If you wish to use other images files, simply create a directory in `images` with the files named
as described above. Non-numeric characters in file names will crash the program.

### Displaying the slideshow
When `viewer.py` is run, it will convert (if necessary) any PDFs in the same directory.
Once this is done, it will start the slideshow. The delay can be controlled by changing the `delay`
variable. The slideshow can be ended by pressing `Ctrl+Shift+R`.

### Command line options
If `viewer.py` is run through the command line, the delay between slides (in milliseconds) can be
specified with the `--delay` or `-d` option.