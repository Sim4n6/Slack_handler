from pathlib import Path
import pytest
import subprocess
import sys

# test_data directory
CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("tests").joinpath("test_data")

# appending a SRC_DIR path for importing utils module
CWD = Path().cwd()
SRC_DIR = CWD.joinpath("slack_handler")
sys.path.append(str(SRC_DIR))
import utils


@pytest.mark.parametrize(
    "disk_image, expected_result",
    [
        ("di1.raw", True),
        ("di3.e01", True),
        ("disk_img_ntfs-scenario6.1.raw", True),
        ("di4.raw", True),
        ("di5_42.raw", True),
        ("di5_42.e01", True),
        ("original.raw", False),
    ],
)
def test__files_presence(disk_image, expected_result):
    """assert files presence"""

    test_file = TEST_DATA_DIR.joinpath(disk_image)
    assert test_file.exists() == expected_result


@pytest.mark.parametrize(
    "disk_image, expected_md5",
    [
        ("di1.raw", "5adebd54cab3016cece85451c6ab72f3"),
        ("disk_img_ntfs-scenario6.1.raw", "aba388c5a770e946be56fae5eeb89b59"),
        ("di3.e01", "ec4defa196f4c1af0b8ff3e7e6bb9a46"),
        ("di4.raw", "2347783ca48e55fae05f2b8c06618bf0"),
        ("di5_42.raw", "771409a8f22acaf197700b3d844ee0fa"),
        ("di5_42.e01", "1e0cba3229d933a104f38bbfc657df68"),
    ],
)
def test__compare_hashs(disk_image, expected_md5):
    """assert files not corrupted"""
    test_file = TEST_DATA_DIR.joinpath(disk_image)
    with open(test_file, "rb") as f:
        md5_hash = utils.MD5_calc(f.read())
    assert md5_hash == expected_md5
