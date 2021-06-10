Slack_handler [![Build & Test](https://github.com/Sim4n6/Slack_handler/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Sim4n6/Slack_handler/actions/workflows/main.yml)
=============

Slack_handler is a python tool for extracting File slacks in raw format and writing their details to a CSV file. 

The File slacks considered are both RAM and DISK file slacks which represent the data between the none multiple size of the file and the allocated size in clusters.No volume slack is considered.

## Features

Implemented so far:
- [x] extract all file slacks in the raw disk image to a directory.
- [x] display File slacks in LATIN-1 or Hex encoding to the console/terminal.
- [x] pretty print all found file slack data in the provided raw disk image.
- [x] Write-out File slacks details to a CSV file including: the original file, the file slack size, the parent directories, MD5 and SHA1 hashes, etc.
- [x] Support for 'RAW' disk images. 
- [x] Add CI using Github action. 
- [x] Make a function helper for MD5_calc and SHA1_calc in 'utils' module for factoring the code.
- [ ] EWF disk image format (in progress...).
- [x] add more tests 'test__file_slack_nbr' and computed MD5 hashs.
- [ ] add more tests 'test__file_slack_content' (inspection at binary level).
- [ ] Add relative/absolute location details to CSV report file.
- [x] cache and optimize Github actions (cached mentioned Pipfile modules but not pytsk nor libewf).
- [ ] Add support for disk images in AFF formats.
- [ ] Optimize the way it locates the File slack space.
- [ ] Simulate user behaviors in test disk images using a Bash script.
- [ ] Generate more disk images for validation.

## Installation on a Debian/GNU Linux

- Create a Virtual environment
- Download the [latest release](https://github.com/Sim4n6/Slack_handler/releases/latest) 
- Clone pytsk [repository](https://github.com/py4n6/pytsk)
- update the repo (get libtsk) ``python setup.py update``
- build (libtsk) ``python setup.py build`` 
- install (which will install pytsk bindings) ``python setup.py ìnstall``
- ``pip list`` now you should see pytsk installed if everything is ok! 
- clone pyewf [repository](https://github.com/libyal/libewf) 
- ``./synclibs.sh`` : Script that synchronizes the local library dependencies
- ``./autogen.sh`` 
- ``./configure --enable-python``
- ``python setup.py build``
- ``python setup.py install`` 

For further details, please check the steps of the job [Build](https://github.com/Sim4n6/Slack_handler/actions) used in Github actions process.

## Usage

To dump all File slacks to 'slacks/' folder and extract all the information to CSV format file named 'report.csv' from a raw image 'USB-NTFS.dd' :

```python main.py -t raw --dump slacks/ --csv report.csv images/USB-NTFS.dd```

Help: 

```
usage: main.py [-h] [-e ENCODING] [-t TYPE] [-p] [-d /DUMP/] [-c CSV] [-v] disk_image

Handle the file slack spaces.

positional arguments:
  disk_image

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING Display slack space in LATIN-1 or Hex. Supported options 'latin-1', 'hex'.
  -t TYPE, --type TYPE  Type of image. Currently supported options 'raw', 'ewf'.
  -p, --pprint          Pretty printing of all file slack spaces found.
  -d, --dump            Dump file slack spaces of each file in raw format to '/DUMP/' directory.
  -c CSV, --csv CSV     Write file slacks information to a CSV file.
  -v, --version         show program's version number and exit
```

## LICENSE

Feel free to read the file **[LICENSE](https://github.com/Sim4n6/Slack_handler/blob/master/LICENSE)**.

## History

- Original version Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>
- Current updated version: 0.1 since date 25/10/2020 by ALJI Mohamed <sim4n6@gmail.com>

## Special Thanks fly to 

- [Joachim Metz](https://twitter.com/joachimmetz) for providing an initial [feedback](https://open-source-dfir.slack.com/archives/CBG3B0Y82/p1603636784070600) on the little tool.
- [David Cowen](https://www.hecfblog.com/2015/02/automating-dfir-how-to-series-on.html) for the awesome serie of "How-to on programming using libtsk and python".
