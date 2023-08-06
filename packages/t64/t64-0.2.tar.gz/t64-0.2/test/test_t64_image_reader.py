import unittest
from unittest.mock import patch

from t64.t64_image_reader import T64ImageReader


class TestT64ImageReader(unittest.TestCase):

    def setUp(self):
        self.map = bytearray(b'C64 tape image file'.ljust(32, b'\x00'))
        self.map += b'\x01\x01\x02\x00\x01\x00\x00\x00'
        self.map += b'tape name'.ljust(24, b' ')
        self.map += b'\x00'*32
        self.image = T64ImageReader('/dev/null')

    def tearDown(self):
        self.image.map = None
        self.image.__exit__(None, None, None)

    def test_header(self):
        self.map += b'\x00'*32
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.__enter__()
        self.assertEqual(self.image.tape_name, b'tape name'.ljust(24, b' '))
        self.assertEqual(self.image.max_entries, 2)
        self.assertEqual(self.image.used_entries, 1)

    def test_entries(self):
        self.map += b'\x01\x82\x00\x10\x00\x20'.ljust(16, b'\x00')
        self.map += b'file name'.ljust(16, b' ')
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.__enter__()
        self.assertEqual(len(self.image.entries), 1)
        self.assertIsNotNone(self.image.entry(b'file name'))
        self.assertIsNone(self.image.entry(b'not found'))

    def test_directory(self):
        self.map += b'\x01\x82\x00\x10\x00\x20'.ljust(16, b'\x00')
        self.map += b'file name'.ljust(16, b' ')
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.__enter__()
        dir_list = [l for l in self.image.directory('ascii')]
        self.assertEqual(dir_list, ['0 "tape name               "', '17   "file name"        PRG'])

    def test_bad_magic(self):
        self.map[:3] = b'bad'
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            with self.assertRaises(ValueError):
                self.image.__enter__()
