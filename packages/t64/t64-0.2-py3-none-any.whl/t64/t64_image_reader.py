import codecs
import logging
import math
import mmap
import struct

from pathlib import Path

from .dir_entry import DirEntry


log = logging.getLogger(__name__)


class T64ImageReader:
    def __init__(self, filepath):
        self.filepath = Path(filepath) if isinstance(filepath, str) else filepath
        self.fileh = None
        self.map = None

    def open(self):
        self.fileh = self.filepath.open('rb')
        self.map = mmap.mmap(self.fileh.fileno(), 0, mmap.MAP_PRIVATE, mmap.ACCESS_READ)
        if self.map[:3] != b'C64':
            raise ValueError("Invalid file format, "+str(self.map[:32]))

        self.version, self.max_entries, self.used_entries = struct.unpack('<HHH', self.map[0x20:0x26])
        self.tape_name = self.map[0x28:0x40]
        if self.max_entries == 0:
            raise ValueError("Invalid max entries, 0")
        if self.used_entries == 0:
            raise ValueError("Invalid used entries, 0")

        self.entries = []
        for eidx in range(0, self.max_entries):
            estart = 0x40 + (eidx * 0x20)
            ftype, disk_type, start, end, _, img_start = struct.unpack('<BBHHHI', self.map[estart:estart+12])
            if ftype == 1:
                if end == 0xc3c6 or end <= start:
                    raise ValueError("Invalid entry end address, 0x{:x}".format(end))
                file_name = self.map[estart+0x10:estart+0x20].rstrip(b' ')
                dir_entry = DirEntry(self, file_name, ftype, disk_type, start, end, img_start)
                self.entries.append(dir_entry)
            elif ftype != 0:
                log.warning("Unsupported file type, "+str(ftype))

    def close(self):
        if self.map:
            self.map.close()
        if self.fileh:
            self.fileh.close()

    def directory(self, encoding='petscii-c64en-uc', drive=0):
        try:
            _ = codecs.lookup(encoding)
        except LookupError:
            log.warning("PETSCII codecs not available, using ASCII")
            encoding = 'ascii'

        yield '{} "{:24}"'.format(drive, self.tape_name.decode(encoding))

        for entry in self.entries:
            size_blocks = math.ceil((entry.end_addr-entry.start_addr) / 254)
            closed_ch = ' ' if entry.closed else '*'
            disk_type = entry.disk_type
            if entry.protected:
                disk_type += '<'
            name = '"'+entry.name.decode(encoding)+'"'
            yield '{!s:5}{:18}{}{}'.format(size_blocks, name, closed_ch, disk_type)

    def iterdir(self):
        yield from self.entries

    def entry(self, name):
        entry_list = [e for e in self.entries if e.name == name]
        if entry_list:
            return entry_list[0]
        return None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __str__(self):
        return "<{}: {!s}>".format(type(self).__name__, self.filepath)
