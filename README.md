slack handler
=============

A Sleuthkit tool to check the slack space at the end of each file in a filesystem.  For more information: http://www.sleuthkit.org

The project is based on pytsk which is a python binding for the sleuthkit. For more information: https://github.com/py4n6/pytsk

## Features

- display file slacks in LATIN-1 or Hex encoding.
- pretty print all found file slacks in a raw image.
- dump all file slacks in the raw image to a directory 'slacks/'.
- write file slacks information to a CSV file. 
- support 'raw' images (EWF format in progress)

## Installation

- create virtualenv 
- clone pytsk repository
- update the repo (get libtsk)
- build (libtsk)
- install (which will install pytsk bindings) 
- clone pyewf repository
- /synclibs.sh & ./autogen.sh 
- ./configure --enable-python
- python setup.py build
- python setup.py install 
- check the installed modules `pip list`


## How to use


To use the script type: 

```
usage: main.py [-h] [-e ENCODING] [-t TYPE] [-p] [-d] [-c CSV] [-v] image

Handle the file slack spaces.

positional arguments:
  image

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING Display slack space in LATIN-1 or Hex. Supported options 'latin-1', 'hex'.
  -t TYPE, --type TYPE  Type of image. Currently supported options 'raw', 'ewf'.
  -p, --pprint          Pretty printing of all file slack spaces found.
  -d, --dump            Dump file slack spaces of each file in raw format.
  -c CSV, --csv CSV     Write file slacks information to a CSV file.
  -v, --version         show program's version number and exit
```

## History 

- Original version: 1.0 Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>
- Current updated version: 1.1 Date 25/10/2020 by ALJI Mohamed <sim4n6@gmail.com>