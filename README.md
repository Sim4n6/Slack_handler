Slack_handler
=============

Slack_handler is a tool to dump file slacks in raw format and to extract file slack information to CSV format. 

A Sleuthkit tool to check the slack space at the end of each file in a filesystem.  For more information: http://www.sleuthkit.org
The project is based on pytsk which is a python binding for the sleuthkit. For more information: https://github.com/py4n6/pytsk

## History

- Original version: 1.0 Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>
- Current updated version: 1.1 Date 25/10/2020 by ALJI Mohamed <sim4n6@gmail.com>
- Working on the suggestions from Joackim Metz: [conversation](https://open-source-dfir.slack.com/archives/CBG3B0Y82/p1603636784070600) ....

## Features

Implemented so far:
- display file slacks in LATIN-1 or Hex encoding.
- pretty print all found file slack data in the provided raw disk image.
- dump all file slacks in the raw disk image to a directory.
- write file slacks details to a CSV file. 
- support 'raw' images (EWF format in progress...)

## Installation process for Debian/GNU

- create virtualenv 
- clone pytsk [repository](https://github.com/py4n6/pytsk)
- update the repo (get libtsk) ``python setup.py update``
- build (libtsk) ``python setup.py build`` 
- install (which will install pytsk bindings) ``python setup.py ìnstall``
- ``pip list`` now you should see pytsk installed if everything is ok 
- clone pyewf [repository](https://github.com/libyal/libewf) 
- ``./synclibs.sh`` : Script that synchronizes the local library dependencies


- ``./autogen.sh`` 
- ``./configure --enable-python``
- ``python setup.py build``
- ``python setup.py install`` 
- check the installed modules `pip list`


## How to use


To use the script type: 

```
usage: main.py [-h] [-e ENCODING] [-t TYPE] [-p] [-d /DUMP/] [-c CSV] [-v] image

Handle the file slack spaces.

positional arguments:
  image

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING Display slack space in LATIN-1 or Hex. Supported options 'latin-1', 'hex'.
  -t TYPE, --type TYPE  Type of image. Currently supported options 'raw', 'ewf'.
  -p, --pprint          Pretty printing of all file slack spaces found.
  -d, --dump            Dump file slack spaces of each file in raw format to '/DUMP/' directory.
  -c CSV, --csv CSV     Write file slacks information to a CSV file.
  -v, --version         show program's version number and exit
```

For instance, to dump all file slacks to 'slacks/' folder and extract all the information to CSV format file from a raw image:
```python main.py -t raw --dump SLACKS_dir --csv slack_info.csv images/USB-NTFS.dd```

## TODOs 

- [ ] add images for testing [ntfs-specimens](https://github.com/dfirlabs/ntfs-specimens) or [dfvfs-test-data](https://github.com/log2timeline/dfvfs/tree/master/test_data)
- [ ] add license for the testing image
- [ ] add tests <---- (working on this...)
- [ ] specify more informations about the slack being extracted (btw allocated size file and last cluster)
- [ ] document ram slack and disk slack (mention no volume slack yet)
- [ ] check again this [conversation](https://open-source-dfir.slack.com/archives/CBG3B0Y82/p1603636784070600)

## Special Thanks fly to 

- [Joachim Metz](https://twitter.com/joachimmetz) for providing an initial feedback on the little tool.
- [David Cowen](https://www.hecfblog.com/2015/02/automating-dfir-how-to-series-on.html) for the awesome serie of "How-to on programming using libtsk and python".
- Anyone starring the github repository :) 
