import unittest
import tempfile
import shutil
import hashlib
import os
from folder_sync import ItemSynchronizer, ItemHandler


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

    def test_file_modification(self):
        test_file = os.path.join(self.temp_source, "test.txt")
        replica_file = os.path.join(self.temp_replica, "test.txt")

        with open(test_file, "w") as f:
            f.write("Initial content")
        shutil.copy(test_file, replica_file)

        with open(test_file, "w") as f:
            f.write("Updated content")

        self.synchronizer.synchronize()

        source_hash = self.synchronizer.get_item_list(self.temp_source)[0].calculate_hash()
        replica_hash = self.synchronizer.get_item_list(self.temp_replica)[0].calculate_hash()
        self.assertEqual(source_hash, replica_hash)

    def test_file_deletion(self):
        test_file = os.path.join(self.temp_source, "test.txt")
        replica_file = os.path.join(self.temp_replica, "test.txt")

        with open(test_file, "w") as f:
            f.write("Some content")
        shutil.copy(test_file, replica_file)
        os.remove(test_file)

        self.synchronizer.synchronize()

        self.assertFalse(os.path.exists(replica_file))

    def test_directory_creation(self):
        test_dir = os.path.join(self.temp_source, "new_dir")
        replica_dir = os.path.join(self.temp_replica, "new_dir")

        os.mkdir(test_dir)

        self.synchronizer.synchronize()

        self.assertTrue(os.path.exists(replica_dir))

    def test_directory_deletion(self):
        test_dir = os.path.join(self.temp_source, "new_dir")
        replica_dir = os.path.join(self.temp_replica, "new_dir")

        os.mkdir(test_dir)
        os.mkdir(replica_dir)

        shutil.rmtree(test_dir)

        self.synchronizer.synchronize()

        self.assertFalse(os.path.exists(replica_dir))
