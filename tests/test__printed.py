from pathlib import Path
import pytest
import subprocess

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("slack_handler")


@pytest.mark.parametrize(
    "disk_img, disk_img_type, in_stdoutput",
    [
        ("di1.raw", "raw", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235"),
        ("di3.e01", "ewf", b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 12235"),
        ("di4.raw", "raw", b"2, b'NTFS / exFAT (0x07)', 128s(65536) 8192"),
        ("di5_42.raw", "raw", b"2, b'NTFS / exFAT (0x07)', 128s(65536) 45056"),
        ("di5_42.e01", "ewf", b"2, b'NTFS / exFAT (0x07)', 128s(65536) 45056"),
    ],
)
def test__cli_print_partition_table(disk_img, disk_img_type, in_stdoutput):
    """check partition details display for a specific disk img"""
    proc = subprocess.Popen(
        [
            "slack_handler",
            "--type",
            disk_img_type,
            TEST_DATA_DIR.joinpath(disk_img),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, error = proc.communicate()

    assert b"addr, desc, starts(start*512) len" in stdoutput
    assert in_stdoutput in stdoutput
