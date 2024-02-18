import unittest
import tempfile
import shutil
class TestItemHandler(unittest.TestCase):
    def setUp(self):
        self.temp_source = tempfile.mkdtemp()
        self.temp_replica = tempfile.mkdtemp()
        self.synchronizer = ItemSynchronizer(self.temp_source, self.temp_replica, "../temp_log.txt", 1)

    def tearDown(self):
        shutil.rmtree(self.temp_source)
        shutil.rmtree(self.temp_replica)
    def test_new_file_creation(self):
        test_file = os.path.join(self.temp_source, "test.txt")
        with open(test_file, "w") as f:
            f.write("Sample content")

        self.synchronizer.synchronize()

        replica_file = os.path.join(self.temp_replica, "test.txt")
        self.assertTrue(os.path.exists(replica_file))
