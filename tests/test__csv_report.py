from pathlib import Path
import pytest
import subprocess
import csv
import sys

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("src")

# appending a SRC_DIR path for importing utils module
sys.path.append(str(SRC_DIR))
import utils


@pytest.mark.parametrize(
    "disk_img, disk_img_type, nbr_reg_files",
    [
        # TODO check me again because nbr regular files may be not correct.
        # fls -F -r -o di | grep -v '\$' | wc -l
        ("di1.raw", "raw", 11),
        ("di3.e01", "ewf", 11),
        ("disk_img_ntfs-scenario6.1.raw", "raw", 22),
    ],
)
def test__cli_csv_file(tmpdir, disk_img, disk_img_type, nbr_reg_files):
    """check whether CSV_REPORT is generated correctly with enough rows and a header for each disk img"""

    REPORT_DIR = tmpdir.mkdir("report")
    CSV_REPORT = REPORT_DIR.join(f"results-{disk_img}.csv")
    proc = subprocess.Popen(
        [
            "python3",
            SRC_DIR.joinpath("main.py"),
            "--type",
            disk_img_type,
            "--csv",
            CSV_REPORT,
            TEST_DATA_DIR.joinpath(disk_img),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, error = proc.communicate()

    with open(CSV_REPORT, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        assert csv_reader.__next__() == [
            "slack filename",
            "slack size",
            "partition address",
            "MD5",
            "SHA1",
            "parent dirs",
        ]
        assert len(list(csv_reader)) == nbr_reg_files
