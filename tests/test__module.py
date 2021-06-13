from pathlib import Path
import pytest
import subprocess

CWD = Path().cwd()
TEST_DATA_DIR = CWD.joinpath("test_data")
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
