from pathlib import Path
import pytest
import subprocess
import csv
import sys

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("src")
SLACKS_DIR = CWD.joinpath("slacks")
 
# appending a SRC_DIR path for importing utils module
sys.path.insert(0, str(SRC_DIR))
print(sys.path)
import utils

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
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "unfound_disk.img"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    assert b"unfound_disk.img" in stdoutput
    assert b"not found" in stdoutput


def test__cli_print_partition_table():
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), TEST_DATA_DIR.joinpath("disk_img__scenario1_1__100_files.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    assert b"addr, desc, starts(start*512) len" in stdoutput
    # two partitions available
    assert b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 8192" in stdoutput
    assert b"3, b'NTFS / exFAT (0x07)', 10240s(5242880) 8192" in stdoutput
    # partition 1
    assert b"NTFS Cluster size:  4096 in bytes." in stdoutput
    assert b"NTFS Sector size:  512 in bytes." in stdoutput


def test__cli_csv_file():
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "--csv", "results0.csv", TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    with open("results0.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        assert csv_reader.__next__() == ['slack filename', 'slack size', 'partition address', 'MD5', 'SHA1', 'parent dirs']
        assert len(list(csv_reader)) == 11

def test__files_slack_nbr():
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "--dump", SLACKS_DIR, TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    slacks_found = [sf for sf in SLACKS_DIR.iterdir() if sf.is_file()]
    assert len(slacks_found) == 11
    
    
def test__file_slack_content():
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "--dump", SLACKS_DIR, "--csv", "results.csv", TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    slacks_found = [sf for sf in SLACKS_DIR.iterdir() if sf.is_file()]
    
    #compute MD5 hashs
    hashs_md5 = []
    for sf in slacks_found:
        with open(sf, "rb") as f:
            md5hash = utils.MD5_calc(f.read())
        
    # retrieve stored MD5 hashs
    stored_md5 = []
    with open('results.csv', newline='') as csvfile:
        results_reader = csv.DictReader(csvfile)
        for row in results_reader:
            stored_md5.append(row['MD5'])
     
    hashs_md5.sort()
    stored_md5.sort()
    assert hashs_md5 == stored_md5
    
        

if __name__ == "__main__":
    test__cli_csv_file()
