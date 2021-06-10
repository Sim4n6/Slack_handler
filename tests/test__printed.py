from pathlib import Path
import pytest
import subprocess
import csv
import sys
import re

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("src")
 
# appending a SRC_DIR path for importing utils module
sys.path.append(str(SRC_DIR))
import utils


@pytest.mark.parametrize(
    "disk_image, disk_image_type, in_stdoutput",
    [
        ("di1.raw", "raw", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235"),
        ("di3.e01", "ewf", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235"),
        ("di2_100f.raw", "raw", b"3, b'NTFS / exFAT (0x07)', 10240s(5242880) 8192")
    ],
)
def test__cli_print_partition_table(disk_image, disk_image_type, in_stdoutput):
    """ check partition details display for a specific disk img """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", disk_image_type, TEST_DATA_DIR.joinpath(disk_image)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    assert b"addr, desc, starts(start*512) len" in stdoutput
    assert in_stdoutput in stdoutput

