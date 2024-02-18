import unittest
import tempfile
import shutil
import os
from FolderSync import ItemSynchronizer


class TestItemSynchronizer(unittest.TestCase):
    def setUp(self):
        self.temp_source = tempfile.mkdtemp()
        self.temp_replica = tempfile.mkdtemp()
        self.temp_log = tempfile.NamedTemporaryFile(delete=False)
        self.synchronizer = ItemSynchronizer(
            self.temp_source,
            self.temp_replica,
            self.temp_log.name,
            1
        )

    def tearDown(self):
        shutil.rmtree(self.temp_source)
        shutil.rmtree(self.temp_replica)
        self.temp_log.close()  # Close and delete
        os.unlink(self.temp_log.name)

    def test_new_file_sync(self):
        source_file = os.path.join(self.temp_source, 'test.txt')
        with open(source_file, 'w') as f:
            f.write("Some content")

        self.synchronizer.synchronize()

        replica_file = os.path.join(self.temp_replica, 'test.txt')
        self.assertTrue(os.path.exists(replica_file))

