from pathlib import Path
import pytest
import subprocess
import csv
import sys
import re

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("src")

# FIXME styling ?
# appending a SRC_DIR path for importing utils module
sys.path.append(str(SRC_DIR))
import utils

@pytest.mark.parametrize("disk_img, disk_img_type, nbr_file_slacks", [("di1.raw", "raw", 11), ("di3.e01", "ewf", 11)])
def test__files_slack_nbr(tmpdir, disk_img, disk_img_type, nbr_file_slacks):
    """assert a correct number of file slacks per each disk img"""

    SLACKS_DIR = tmpdir.mkdir("slacks")

    proc = subprocess.Popen(
        [
            "python3",
            SRC_DIR.joinpath("main.py"),
            "--type",
            disk_img_type,
            "--dump",
            SLACKS_DIR,
            TEST_DATA_DIR.joinpath(disk_img),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, error = proc.communicate()

    files_found = [sf for sf in SLACKS_DIR.listdir() if sf.check(file=True)]
    assert len(files_found) == nbr_file_slacks


@pytest.mark.parametrize("disk_img, disk_img_type", [("di1.raw", "raw"), ("di3.e01", "ewf")])
def test__file_slack_fn(tmpdir, disk_img, disk_img_type):
    """check a specific file slack filename found and format of all files dumped correspond to 'slack--XXXXXdd'"""

    SLACKS_DIR = tmpdir.mkdir("slacks")
    proc = subprocess.Popen(
        [
            "python3",
            SRC_DIR.joinpath("main.py"),
            "--type",
            disk_img_type,
            "--dump",
            SLACKS_DIR,
            TEST_DATA_DIR.joinpath(disk_img),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, error = proc.communicate()

    files_found_fn = [sf.basename for sf in SLACKS_DIR.listdir() if sf.check(file=True)]
    assert "slack--001961.pdf.dd" in files_found_fn
    for slack_f in files_found_fn:
        assert re.match("^slack--.+dd$", slack_f)

@pytest.mark.parametrize("disk_img, disk_img_type", [("di1.raw", "raw"), ("di3.e01", "ewf")])
def test__file_slack_content(tmpdir, disk_img, disk_img_type):
    """Ensure all computed MD5 of the extracted file slacks are equals to the ones in the results.csv generated report."""

    SLACKS_DIR = tmpdir.mkdir("slacks")
    REPORT_DIR = tmpdir.mkdir("report")
    CSV_REPORT = REPORT_DIR.join("results.csv")
    proc = subprocess.Popen(
        [
            "python3",
            SRC_DIR.joinpath("main.py"),
            "--type",
            disk_img_type,
            "--dump",
            SLACKS_DIR,
            "--csv",
            CSV_REPORT,
            TEST_DATA_DIR.joinpath(disk_img),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, error = proc.communicate()

    files_found = [sf for sf in SLACKS_DIR.listdir() if sf.check(file=True)]

    # compute MD5 hashs
    hashs_md5 = []
    for sf in files_found:
        with open(sf, "rb") as f:
            md5hash = utils.MD5_calc(f.read())
            hashs_md5.append(md5hash)

    # retrieve stored MD5 hashs
    stored_md5 = []
    with open(CSV_REPORT, newline="") as csvfile:
        results_reader = csv.DictReader(csvfile)
        for row in results_reader:
            stored_md5.append(row["MD5"])

    hashs_md5.sort()
    stored_md5.sort()
    assert hashs_md5 == stored_md5
