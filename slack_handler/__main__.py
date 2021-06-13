"""
**************************************************************************************.
Original version: 1.0 Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>.
Current updated version: 1.1 Date 15/10/2020 by ALJI Mohamed <sim4n6@gmail.com>.

    Copyright (C) 2020 - 2021 ALJI Mohamed <sim4n6@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
**************************************************************************************.
"""

import csv
import pprint
from pathlib import Path
from argparse import ArgumentParser
import sys
import tempfile

from slack_handler import slack

try:
    import pyewf
    import pytsk3

    from slack_handler import ewf
except ModuleNotFoundError as e:
    print("A module is not installed.", e, file=sys.stderr)
    sys.exit(1)


def is_fs_directory(f):
    """Check if an inode/addr is a filesystem directory."""

    try:
        return f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR
    except AttributeError:
        return False


def is_fs_regfile(f):
    """Check if an inode/addr is a regular file."""

    try:
        return f.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG
    except AttributeError:
        return False


def processing(partition, directory, queue, parent_names):
    """Iterate over all files recursively in a all directories and get
    the slack on each file (only regular files and not filesystem metadata
    file)."""

    queue.append(directory)

    for f in directory:
        # exclude none directories, current_dir, parent_dir and NTFS system dirs (such as $Extend)
        if f.info.name.name in [b".", b".."]:
            continue
        elif f.info.name.name[0:1] == b"$":
            continue
        elif is_fs_directory(f):
            if arguments.verbose:
                print(f"Current dir: {f.info.name.name}")
            parent_names.append(f.info.name.name.decode("UTF-8"))

            d = f.as_directory()
            # no recurse, to avoid circular loops:
            if d not in queue:
                processing(partition, d, queue, parent_names)

        elif is_fs_regfile(f):
            if arguments.verbose:
                print(f"Getting file slack from: {f.info.name.name.decode('UTF-8')}")
            s = get_slack(partition, f)
            if s is not None:
                s.set_s_dirs(parent_names)
                all_slacks.append(s)

        else:
            continue

    queue.pop(-1)
    parent_names.pop(-1)


def print_partition_table(partition_table):
    """Print the partition table."""

    print("\naddr, desc, starts(start*512) len")
    for partition in partition_table:
        # partition.addr : Represents the partition number
        # parition.desc: NTFS (0x07)- Reprents the partition description including the type flag for NTFS
        # partition.start: 128s - Represnts the starting sector of the partition
        # partition.start*512: (65536) - Represents the offset by multiplying the sector number  where the partition starts by 512 bytes to calculate the absolute position within the image where the partition begins.
        # partition.len: 1042432 - Represents the length in sectors that makes up this partition. If you where to again multiply this number by 512 you would get 533,725,184 which is 509 MegaBytes (divide 533,725,184 by 1024 once to get kilobytes, twice to get megabytes) and is the size of the partition found within the image.
        # http://www.sleuthkit.org/sleuthkit/docs/api-docs/4.9.0/structTSK__VS__PART__INFO.html
        # FIXME not all time 512 !
        print(
            f"{partition.addr}, {partition.desc}, {partition.start}s({partition.start*512}) {partition.len}"
        )
    print()


def get_slack(partition, f):
    """Return the file slack space of a single file."""

    # walk all clusteres allocated by this file as in NTFS filesystem
    # each file has several attributes which can allocate multiple clusters.
    l_block = 0
    for attr in f:
        for run in attr:
            #  https://flatcap.org/linux-ntfs/ntfs/concepts/clusters.html
            # l_block : last block of the file
            l_block = run.addr + run.len - blocksize

    # file size (in bytes)
    size = f.info.meta.size

    # actual file data in the last block
    l_d_size = size % blocksize

    #  multiple just clusters (no slack)
    if l_d_size == 0:
        # TODO a dedicated test case to be added.
        return None
    else:
        # slack space size
        s_size = blocksize - l_d_size

        # force reading the slack of the file by providing the FLAG_SLACK
        # print(l_block, s_size, file=sys.stderr)
        data = f.read_random(
            l_block,
            s_size,
            pytsk3.TSK_FS_ATTR_TYPE_DEFAULT,
            -1,
            pytsk3.TSK_FS_FILE_READ_FLAG_SLACK,
        )

        # construct a slack object
        s = slack.slack(
            s_size=s_size,
            s_bytes=data,
            s_partition_addr=partition.addr,
            s_name=f.info.name.name,
        )
        return s


def main():

    # commands and arguments
    # argparse https://docs.python.org/3/library/argparse.html#module-argparse
    parser = ArgumentParser(description="Extract the file slack spaces.")
    parser.add_argument("image", metavar="disk image", nargs=1, action="store")
    parser.add_argument(
        "-e",
        "--encoding",
        default="",
        help="Display slack space in LATIN-1 or Hex. Supported options 'latin-1', 'hex'.",
    )
    parser.add_argument(
        "-t",
        "--type",
        required=True,
        help="Type of the disk image. Currently supported options 'raw' and 'ewf'.",
    )
    parser.add_argument(
        "-p",
        "--pprint",
        action="store_true",
        help="Pretty print all found file slack spaces.",
    )

    # create a temporary dir for slacks
    tmpdir = tempfile.TemporaryDirectory(prefix="slacks_")
    parser.add_argument(
        "-d",
        "--dump",
        action="store",
        default=tmpdir.name,
        help="Dump file slack spaces of each file in raw format to a directory if specified, by default temporary dir.",
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="store",
        default=None,
        help="Write file slacks information to a CSV file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Control the verbosity of the output.",
    )
    parser.add_argument("--version", action="version", version="v0.2.6")

    global arguments
    arguments = parser.parse_args()

    global all_slacks
    all_slacks = []

    if arguments.image is not None:
        CWD = Path().cwd()
        if not CWD.joinpath(arguments.image[0]).exists():
            print(
                f"The disk image '{arguments.image[0]}' is not found.",
                file=sys.stderr,
            )
            sys.exit(1)

        # print versions
    print("SleuthKit lib version:", pytsk3.TSK_VERSION_STR)
    print("Module pytsk3 version:", pytsk3.get_version())
    print("Module pyewf version:", pyewf.get_version())

    # open image
    if arguments.image is not None:
        if arguments.type == "raw":
            img_handler = pytsk3.Img_Info(arguments.image[0])
        elif arguments.type == "ewf":
            print(arguments.image)
            ewf_handle = pyewf.handle()
            filenames = pyewf.glob(arguments.image[0])
            ewf_handle.open(filenames)
            img_handler = ewf.ewf_Img_Info(ewf_handle)
        elif arguments.type == "aff":
            print("Not Supported Yet ! ", file=sys.stderr)
            sys.exit(1)
        elif arguments.type not in ["raw", "ewf"]:
            print("Not Supported Yet ! Only 'raw' and 'ewf'. ", file=sys.stderr)
            sys.exit(1)

        # open the image volume for the partitions within it
    try:
        partition_table = pytsk3.Volume_Info(img_handler)
        print_partition_table(partition_table)
    except OSError as e:
        # there is no Volume in the image.
        print(
            "Maybe there is no Volume in the provided disk image.\n",
            e,
            file=sys.stderr,
        )
    else:
        for partition in partition_table:
            if b"NTFS" in partition.desc:
                # open the filesystem with offset set to the absolute offset of
                # the beginning of the NTFS partition.
                fs = pytsk3.FS_Info(img_handler, offset=(partition.start * 512))

                #  The Cluster Size (blocksize) can be chosen when the volume is formatted.
                global blocksize
                blocksize = fs.info.block_size
                print("NTFS Cluster size: ", blocksize, "in bytes.")

                # get the sector size
                global sector
                sector = fs.info.dev_bsize
                print("NTFS Sector size: ", sector, "in bytes.\n")
                # open the directory node for recursiveness and enqueue all
                # directories in image fs from the root dir "/"
                queue_all_dirs = []
                directory = fs.open_dir(path="/")

                processing(
                    partition,
                    directory=directory,
                    queue=queue_all_dirs,
                    parent_names=["/"],
                )

        # pretty printing the all_slack files
    if arguments.pprint:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(all_slacks)

        # writing out file slack spaces into seperate files located in 'slacks' directory
    if arguments.dump:
        if arguments.verbose:
            print(f"{arguments.dump} is the temporary output dir for file slacks.")

        for s in all_slacks:
            CWD = Path().cwd()
            SLACKS_DIR = CWD.joinpath(arguments.dump)
            SLACKS_DIR.mkdir(exist_ok=True)
            file_slack_name = SLACKS_DIR.joinpath(s.get_s_name())
            file_slack_name.write_bytes(s.get_s_bytes())

        # print slack bytes with encoding 'latin-1', 'hex'.
    if arguments.encoding is not None:
        for s in all_slacks:
            s_bytes = s.get_s_bytes()
            if arguments.encoding == "latin-1":
                print(s_bytes.decode("latin-1"))
            elif arguments.encoding == "hex":
                print(s_bytes.hex())

    #  handle csv argument
    if arguments.csv is not None:
        csv_filename = arguments.csv
        if arguments.verbose:
            print(f"Writing CSV report to '{arguments.csv}'.")

        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = [
                "slack filename",
                "slack size",
                "partition address",
                "MD5",
                "SHA1",
                "parent dirs",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for s in all_slacks:
                writer.writerow(
                    {
                        "slack filename": s.get_s_name(),
                        "slack size": s.get_s_size(),
                        "partition address": s.get_s_partition_addr(),
                        "MD5": s.get_s_md5(),
                        "SHA1": s.get_s_sha1(),
                        "parent dirs": s.get_s_dirs(),
                    }
                )

    tmpdir.cleanup()


if __name__ == "__main__":
    main()
