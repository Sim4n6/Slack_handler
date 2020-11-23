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
        ("original.raw", False),
    ],
)
def test__files_presence(disk_image, expected_result):

    disk_image = TEST_DATA_DIR.joinpath(disk_image)
    assert disk_image.exists() == expected_result


def test__cli_unfound_disk_img():
    completedProcess = subprocess.run(["python", "main.py", "unfound_disk.img"], capture_output=True)
    assert b"unfound_disk.img" in completedProcess.stdout
    assert b"not found" in completedProcess.stdout


def test__cli_print_partition_table():
    completedProcess = subprocess.run(["python", "main.py", "test_data/disk_img__scenario1_1__100_files.raw"], capture_output=True)
    assert b"addr, desc, starts(start*512) len" in completedProcess.stdout
    # two partitions available
    assert b"2, b'NTFS / exFAT (0x07)', 2048s(1048576) 8192" in completedProcess.stdout
    assert b"3, b'NTFS / exFAT (0x07)', 10240s(5242880) 8192" in completedProcess.stdout
    # partition 1
    assert b"NTFS Cluster size:  4096 in bytes." in completedProcess.stdout
    assert b"NTFS Sector size:  512 in bytes." in completedProcess.stdout


def test__cli_csv_file():
    subprocess.run(["python", "main.py", "-c", "results.csv", "test_data/disk_img__scenario1_1__100_files.raw"], capture_output=True)
    with open("results.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        assert csv_reader.__next__() == ['slack filename', 'slack size', 'partition address', 'MD5', 'SHA1', 'parent dirs']
        with pytest.raises(StopIteration):
            csv_reader.__next__()


if __name__ == "__main__":
    test__cli_csv_file()
