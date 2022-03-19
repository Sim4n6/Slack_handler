from pathlib import Path
import pytest
import subprocess

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("tests").joinpath("test_data")
SRC_DIR = CWD.joinpath("slack_handler")

def test__module():
    """check partition details display for a specific disk img"""

    # TODO call the installed version of the program.    
    proc = subprocess.Popen(
        [
            "slack_handler",
            "--version",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, stderror = proc.communicate()

    assert b"v" in stdoutput

    
def test__cli_unfound_disk_img():
    """check std output in case of an unfound disk image"""

    proc = subprocess.Popen(
        ["slack_handler", "--type", "raw", "unfound_disk.img"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutput, stderror = proc.communicate()
    assert b"unfound_disk.img" in stderror
    assert b"not found" in stderror