import unittest

from t64.dir_entry import DirEntry


class TestDirEntry(unittest.TestCase):

    def setUp(self):
        self.entry = DirEntry(None, b'TEST', 1, 0x82, 0x1000, 0x2000, 0x3000)

    def test_file_type(self):
        self.assertEqual(self.entry.file_type, 1)

    def test_disk_type(self):
        self.assertEqual(self.entry.disk_type, 'PRG')

    def test_protected(self):
        self.assertFalse(self.entry.protected)
        self.entry._disk_type = 0xc2
        self.assertTrue(self.entry.protected)

    def test_closed(self):
        self.assertTrue(self.entry.closed)
        self.entry._disk_type = 0x02
        self.assertFalse(self.entry.closed)
