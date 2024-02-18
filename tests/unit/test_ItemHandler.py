import unittest
import tempfile
import shutil
import os
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
    def test_calculate_hash(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"This is some test data")
        temp_file.close()

        item = ItemHandler("test_file.txt", temp_file.name)

        with open(temp_file.name, 'rb') as f:
            data = f.read()
            expected_hash = hashlib.md5(data).hexdigest()

        calculated_hash = item.calculate_hash()

        self.assertEqual(calculated_hash, expected_hash)

        os.unlink(temp_file.name)
