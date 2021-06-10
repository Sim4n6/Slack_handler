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
    "disk_image, expected_result",
    [
        ("disk_img__scenario1_1__100_files.raw", True),
        ("disk_img_ntfs-scenario6.1.raw", True),
        ("di1.raw", True),
        ("original.raw", False),
    ],
)
def test__files_presence(disk_image, expected_result):
    """ assert files presence or no """
    disk_image = TEST_DATA_DIR.joinpath(disk_image)
    assert disk_image.exists() == expected_result


def test__cli_unfound_disk_img():
    """ check std output in case of an unfound disk image """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", "raw", "unfound_disk.img"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    assert b"unfound_disk.img" in stdoutput
    assert b"not found" in stdoutput


@pytest.mark.parametrize(
    "disk_image, disk_image_type, in_stdoutput",
    [
        ("disk_img__scenario1_1__100_files.raw", "raw", b"3, b'NTFS / exFAT (0x07)', 10240s(5242880) 8192"),
        ("di1.raw", "raw", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235"),
        ("di3.e01", "ewf", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235")
    ],
)
def test__cli_print_partition_table(disk_image, disk_image_type, in_stdoutput):
    """ check partition details display for a specific disk img """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", disk_image_type, TEST_DATA_DIR.joinpath(disk_image)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    assert b"addr, desc, starts(start*512) len" in stdoutput
    assert in_stdoutput in stdoutput


@pytest.mark.parametrize(
    "disk_image, disk_image_type, nbr_reg_files",
    [
        ("di1.raw", "raw", 11),
        ("di3.e01", "ewf", 11)
    ],
)
def test__cli_csv_file(disk_image, disk_image_type, nbr_reg_files):
    """ check whether results0.csv is generated correctly with 11 rows and a header. """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", disk_image_type, "--csv", f"results-{nbr_reg_files}.csv", TEST_DATA_DIR.joinpath(disk_image)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    with open(f"results-{nbr_reg_files}.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        assert csv_reader.__next__() == ['slack filename', 'slack size', 'partition address', 'MD5', 'SHA1', 'parent dirs']
        assert len(list(csv_reader)) == nbr_reg_files


def test__files_slack_nbr():
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", "raw", "--dump", CWD.joinpath("slacks-nbr"), TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    slacks_found = [sf for sf in CWD.joinpath("slacks-nbr").iterdir() if sf.is_file()]
    assert len(slacks_found) == 11


def test__file_slack_fn():
    """ check a specific file slack filename found and format of all files dumped correspond to 'slack--XXXXXdd' """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", "raw", "--dump", CWD.joinpath("slacks-fn"), TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    slacks_found_fn = [sf.name for sf in CWD.joinpath("slacks-fn").iterdir() if sf.is_file()]    
    assert 'slack--001961.pdf.dd' in slacks_found_fn
    for slack_f in slacks_found_fn:
        assert re.match('^slack--.+dd$', slack_f)
    
    
def test__file_slack_content():
    """ Ensure all computed MD5 of the extracted file slacks are equals to the ones in the results.csv generated report. """
    proc = subprocess.Popen(["python3", SRC_DIR.joinpath("main.py"), "-t", "raw", "--dump", CWD.joinpath("slacks-cnt"), "--csv", "results.csv", TEST_DATA_DIR.joinpath("di1.raw")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutput, error = proc.communicate()
    print(stdoutput, error)
    slacks_found = [sf for sf in CWD.joinpath("slacks-cnt").iterdir() if sf.is_file()]
    
    # compute MD5 hashs
    hashs_md5 = []
    for sf in slacks_found:
        with open(sf, "rb") as f:
            md5hash = utils.MD5_calc(f.read())
            hashs_md5.append(md5hash)
        
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
