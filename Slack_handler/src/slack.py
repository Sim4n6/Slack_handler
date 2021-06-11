"""
**************************************************************************************.
 Original version: 1.0 Date: 13/06/2012 by Sokratis Vidros <sokratis.vidros@gmail.com>.
 Current updated version: 1.1 Date 15/10/2020 by ALJI Mohamed <sim4n6@gmail.com>.
**************************************************************************************.
"""

import utils


class slack:
    """A slack class for details about RAM slack and DISK slack of a single file."""

    def __init__(self, **kwargs):

        # the slack size
        if "s_size" in kwargs:
            self.s_size = kwargs["s_size"]

        # the slack bytes
        if "s_bytes" in kwargs:
            self.set_s_bytes(kwargs["s_bytes"])

        # the slack partition address
        if "s_partition_addr" in kwargs:
            self.s_partition_addr = kwargs["s_partition_addr"]

        # the slack parent directories
        if "s_dirs" in kwargs:
            self.s_dirs = kwargs["s_dirs"]

        #  the filename of the file associated with file slack
        if "s_name" in kwargs:
            self.s_name = kwargs["s_name"].decode("utf-8")

    def __repr__(self):
        """Return a simple string to represent the slack file details."""
        return f"* slack size: {self.s_size} (in bytes)\n partition address: {self.s_partition_addr}\n parent directories:{self.s_dirs}"

    def calc_hash_values(self):
        """Calculate the hash values (MD5/SHA1) depending on slack bytes."""
        # if not empty
        if self.s_bytes is not None:
            self.s_md5 = utils.MD5_calc(self.s_bytes)
            self.s_sha1 = utils.SHA1_calc(self.s_bytes)
        else:
            self.s_md5 = 0  # FIXME should it be zero or something else !
            self.s_sha1 = 0

    def print_hash_values(self):
        """Print the MD5 and SHA1 hash values."""
        print("MD5 hash:", self.s_md5)
        print("SHA1 hash:", self.s_sha1)

    def get_s_md5(self):
        """Return the slack MD5 hash value."""
        return self.s_md5

    def get_s_sha1(self):
        """Return the slack SHA1 hash value."""
        return self.s_sha1

    def get_s_name(self):
        """Get the slack filename as "slack--filename.dd"."""
        return f"slack--{self.s_name}.dd"

    def get_s_size(self):
        """Return the slack file size."""
        return self.s_size

    def set_s_size(self, s_size):
        """Set the slack file size."""
        self.s_size = s_size

    def get_s_bytes(self):
        """Return the slack data in bytes."""
        return self.s_bytes

    def set_s_bytes(self, s_bytes):
        """Set the slack data in bytes."""
        self.s_bytes = s_bytes
        self.calc_hash_values()

    def get_s_partition_addr(self):
        """Get the slack partition address."""
        return self.s_partition_addr

    def set_s_partition_addr(self, s_partition_addr):
        """Set the slack partition address."""
        self.s_partition_addr = s_partition_addr

    def get_s_dirs(self):
        """Return the current slack file parent directories."""
        return self.s_dirs

    def set_s_dirs(self, s_dirs):
        """Set the slack file parent directories."""
        self.s_dirs = "/".join([dir_name for dir_name in s_dirs])
