Slack_handler [![Build & Test](https://github.com/Sim4n6/Slack_handler/actions/workflows/build-n-test.yml/badge.svg)](https://github.com/Sim4n6/Slack_handler/actions/workflows/build-n-test.yml)
=============

Slack_handler is a python tool for extracting File slacks in raw format and writing their details to a CSV file. 

The File slacks considered are both RAM and DISK file slacks which represent the data between the none multiple size of the file and the allocated size in clusters. No volume slack is considered.

 - A presentation is available on [Youtube](https://www.youtube.com/watch?v=NRSIjeiStxE) (~17min).
 - A description article is [available](https://doi.org/10.1109/CyberSA52016.2021.9478197) on IEEE Xplore.

## Features

Implemented so far:
- [x] extract all file slacks from raw or ewf disk image to a directory.
- [x] display file slacks in LATIN-1 or Hex encoding to the console/terminal.
- [x] pretty print all found file slack data in the provided disk image.
- [x] Write-out File slacks details to a CSV file including: the original file, the file slack size, the parent directories, MD5 and SHA1 hashes, etc.
- [x] Support for 'RAW' disk images. 
- [x] Support for 'EWF' disk images. 
- [x] Add CI using Github action. 
- [x] Add a helper function for MD5_calc and SHA1_calc in 'utils' module for factoring the code.
- [x] Add EWF disk image to test_data.
- [x] add more tests 'test__file_slack_nbr' and computed MD5 hashs.
- [ ] fix shenanigans of compressed files.
- [ ] add more tests 'test__file_slack_content' (inspection at binary level).
- [ ] add a test case for no_file_slack file.
- [ ] Add relative/absolute location details to CSV report file.
- [x] cache and optimize Github actions.
- [ ] Add support for disk images in AFF formats.
- [ ] Optimize the way it locates the File slack space.
- [ ] Simulate user behaviors in test disk images using a Bash script.
- [ ] Generate more disk images for validation.
- [ ] add XML description file of each disk image using fiwalk or fls.
- [x] package everything.

## Installation on a Debian/GNU Linux for developers

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

## Installation from Pypi (In progress ... )


The tool is hosted on [Pypi](https://pypi.org/project/slack-handler/)
 - `pip3 install slack-handler`
 - `slack_handler --version`

## Usage

To dump all File slacks to 'slacks/' folder and extract all the information to CSV format file named 'report.csv' from a raw image 'USB-NTFS.dd' :

```slack_handler --type raw --dump slacks/ --csv report.csv images/USB-NTFS.dd```

Help: 

```
usage: slack_handler [-h] [-e ENCODING] -t TYPE [-p] [-d DUMP] [-c CSV] [-v] [--version] disk image

Extract the file slack spaces.

positional arguments:
  disk image

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Display slack space in LATIN-1 or Hex. Supported options 'latin-1', 'hex'.
  -t TYPE, --type TYPE  Type of the disk image. Currently supported options 'raw' and 'ewf'.
  -p, --pprint          Pretty print all found file slack spaces.
  -d DUMP, --dump DUMP  Dump file slack spaces of each file in raw format to a directory if specified, by default temporary dir.
  -c CSV, --csv CSV     Write file slacks information to a CSV file.
  -v, --verbose         Control the verbosity of the output.
  --version             show program's version number and exit
```

## LICENSE

Feel free to read the file **[LICENSE](https://github.com/Sim4n6/Slack_handler/blob/master/LICENSE)**.

## History

- Original version Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>
- Current updated version: 0.1 since 25/10/2020 by ALJI Mohamed <sim4n6@gmail.com>

## Special Thanks fly to 

- [Joachim Metz](https://twitter.com/joachimmetz) for providing an initial feedback on the little tool related to the different types of disk slack space and the licensing.
- [David Cowen](https://www.hecfblog.com/2015/02/automating-dfir-how-to-series-on.html) for the awesome serie of "How-to on programming using libtsk and python".
- Any feedback is a welcome via Github [issues](https://github.com/Sim4n6/Slack_handler/issues) or reach out via [The Open Source DFIR Slack community](https://open-source-dfir.slack.com) using the registration [link](https://github.com/open-source-dfir/slack).
