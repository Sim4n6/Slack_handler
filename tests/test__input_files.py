from pathlib import Path
import pytest
import subprocess
import sys

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
SRC_DIR = CWD.joinpath("src")

# appending a SRC_DIR path for importing utils module
sys.path.append(str(SRC_DIR))
import utils


@pytest.mark.parametrize(
    "disk_image, expected_result",
    [
        ("di1.raw", True),
        ("di3.e01", True),
        ("disk_img_ntfs-scenario6.1.raw", True),
        ("di2_100f.raw", True),
        ("original.raw", False),
    ],
)
def test__files_presence(disk_image, expected_result):
    """assert files presence """

    test_file = TEST_DATA_DIR.joinpath(disk_image)
    assert test_file.exists() == expected_result


@pytest.mark.parametrize(
    "disk_image, expected_md5",
    [
        ("di1.raw", "5adebd54cab3016cece85451c6ab72f3"),
        ("disk_img_ntfs-scenario6.1.raw", "aba388c5a770e946be56fae5eeb89b59"),
        ("di3.e01", "ec4defa196f4c1af0b8ff3e7e6bb9a46"),
        ("di2_100f.raw", "0816c0a8e5bf4891cc7dd25dabf2e771"),
    ],
)
def test__compare_hashs(disk_image, expected_md5):
    """assert files not corrupted"""
    test_file = TEST_DATA_DIR.joinpath(disk_image)
    with open(test_file, "rb") as f:
        md5_hash = utils.MD5_calc(f.read())
    assert md5_hash == expected_md5


def test__cli_unfound_disk_img():
    """check std output in case of an unfound disk image"""

    proc = subprocess.Popen(
        ["python3", SRC_DIR.joinpath("main.py"), "--type", "raw", "unfound_disk.img"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, stderror = proc.communicate()
    assert b"unfound_disk.img" in stderror
    assert b"not found" in stderror
