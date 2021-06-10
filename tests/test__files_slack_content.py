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
    # FIXME too much random dirs !
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
