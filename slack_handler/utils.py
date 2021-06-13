import hashlib


def MD5_calc(data):
    """compute MD5 hash"""
    md5hash = hashlib.md5()
    md5hash.update(data)
    return md5hash.hexdigest()


def SHA1_calc(data):
    """compute data SHA1"""
    sha1hash = hashlib.sha1()
    sha1hash.update(data)
    return sha1hash.hexdigest()
