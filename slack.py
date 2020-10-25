import hashlib


class slack:
    """ a slack class """

    def __init__(self, **kwargs):

        # the slack size
        if 's_size' in kwargs:
            self.s_size = kwargs['s_size']

        # the slack bytes
        if 's_bytes' in kwargs:
            self.set_s_bytes(kwargs['s_bytes'])

        # the slack partition address
        if 's_partition_addr' in kwargs:
            self.s_partition_addr = kwargs['s_partition_addr']

        # the slack parent directories
        if 's_dirs' in kwargs:
            self.s_dirs = kwargs['s_dirs']

        # the filename of the file associated with file slack
        if 's_name' in kwargs:
            self.s_name = kwargs['s_name'].decode('utf-8')

    def __repr__(self):
        return f"* slack size: {self.s_size} (in bytes)\n partition address: {self.s_partition_addr}\n parent directories:{self.s_dirs}"

    def calc_hash_values(self):
        # if not empty
        if self.s_bytes is not None:
            md5hash = hashlib.md5()
            md5hash.update(self.s_bytes)
            self.s_md5 = md5hash.hexdigest()

            sha1hash = hashlib.sha1()
            sha1hash.update(self.s_bytes)
            self.s_sha1 = sha1hash.hexdigest()
        else:
            self.s_md5 = 0
            self.s_sha1 = 0

    def print_hash_values(self):
        print("MD5 hash:", self.s_md5)
        print("SHA1 hash:", self.s_sha1)

    def get_s_md5(self):
        return self.s_md5

    def get_s_sha1(self):
        return self.s_sha1

    def get_s_name(self):
        """ get slack name """
        return f"slack--{self.s_name}.dd"

    def get_s_size(self):
        return self.s_size

    def set_s_size(self, s_size):
        self.s_size = s_size

    def get_s_bytes(self):
        return self.s_bytes

    def set_s_bytes(self, s_bytes):
        self.s_bytes = s_bytes
        self.calc_hash_values()

    def get_s_partition_addr(self):
        return self.s_partition_addr

    def set_s_partition_addr(self, s_partition_addr):
        self.s_partition_addr = s_partition_addr

    def get_s_dirs(self):
        return self.s_dirs

    def set_s_dirs(self, s_dirs):
        self.s_dirs = "/".join([dir_name for dir_name in s_dirs])
