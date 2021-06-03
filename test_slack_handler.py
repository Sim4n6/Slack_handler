from pathlib import Path
import pytest
import subprocess
import csv

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")


@pytest.mark.parametrize(
    "disk_image, expected_result",
    [
        ("disk_img__scenario1_1__100_files.raw", True),
        ("disk_img_ntfs-scenario6.1.raw", True),
        ("di1.raw", True),
        ("original.raw", False),
    ],
)
def test__files_presence(disk_image, expected_result):

    disk_image = TEST_DATA_DIR.joinpath(disk_image)
    assert disk_image.exists() == expected_result


def test__cli_unfound_disk_img():
    proc = subprocess.Popen(["python3", "main.py", "unfound_disk.img"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    assert b"unfound_disk.img" in stdoutput
    assert b"not found" in stdoutput


def test__cli_print_partition_table():
    proc = subprocess.Popen(["python3", "main.py", "test_data/disk_img__scenario1_1__100_files.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    assert b"addr, desc, starts(start*512) len" in stdoutput
    # two partitions available
    assert b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 8192" in stdoutput
    assert b"3, b'NTFS / exFAT (0x07)', 10240s(5242880) 8192" in stdoutput
    # partition 1
    assert b"NTFS Cluster size:  4096 in bytes." in stdoutput
    assert b"NTFS Sector size:  512 in bytes." in stdoutput


def test__cli_csv_file():
    proc = subprocess.Popen(["python3", "main.py", "--csv", "results0.csv", "./test_data/di1.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    with open("results0.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        assert csv_reader.__next__() == ['slack filename', 'slack size', 'partition address', 'MD5', 'SHA1', 'parent dirs']
        assert len(list(csv_reader)) == 11


if __name__ == "__main__":
    test__cli_csv_file()
