
class DirEntry:
    DTYPE_STR = ('DEL', 'SEQ', 'PRG', 'USR', 'REL', '???', '???', '???')

    def __init__(self, image, name, file_type, disk_type, start_addr, end_addr, img_start):
        self.image = image
        self.name = name
        self.file_type = file_type
        self._disk_type = disk_type
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.img_start = img_start

    @property
    def disk_type(self):
        return self.DTYPE_STR[self._disk_type & 7]

    @property
    def protected(self):
        return bool(self._disk_type & 0x40)

    @property
    def closed(self):
        return bool(self._disk_type & 0x80)

    def contents(self):
        img_end = self.img_start+self.end_addr-self.start_addr
        return self.image.map[self.img_start:img_end]
