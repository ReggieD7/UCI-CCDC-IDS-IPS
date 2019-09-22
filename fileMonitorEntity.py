from pathlib import *
from hashlib import *



class FileMonitorEntity:
    """
       The Class is responsible for storing relevant data to a file
    """

    def compute_file_hash(self, file):
        """
            Computes a hash for a file
        """
        block_size = 65536
        hashed = md5();
        with file.open(mode="rb") as binary_file:
            buf = binary_file.read(block_size)
            while len(buf) > 0:
                hashed.update(buf)
                buf = binary_file.read(block_size)
        print(hashed.hexdigest())
        return hashed.hexdigest()

    def __init__(self, path=""):

        if path.exists():
            self._path = path
            meta_data = self._path.stat()
            self.recent_date_modified = meta_data.st_mtime
            self.recent_date_of_access = meta_data.st_atime
            self.creation_time = meta_data.st_ctime
            self.owner_id = meta_data.st_uid
            self.size = meta_data.st_size
            self.group_id = meta_data.st_gid
            self.device = meta_data.st_dev
            self.file_hash = self.compute_file_hash(self._path)