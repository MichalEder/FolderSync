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
