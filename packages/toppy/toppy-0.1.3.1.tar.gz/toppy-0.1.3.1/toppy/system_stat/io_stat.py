import re
import time
from collections import namedtuple

import psutil

device_iostats = namedtuple('device_iostats', 'read_time write_time busy_time')

def make_device_iostats(old_stats, new_stats, timediff):
    read_time = (new_stats.read_time - old_stats.read_time) * 100 / timediff
    write_time = (new_stats.write_time - old_stats.write_time) * 100 / timediff
    try:
        busy_time = (new_stats.busy_time - old_stats.busy_time) * 100 / timediff
    except:
        busy_time = read_time + write_time
    return device_iostats(read_time, write_time, busy_time)

def is_valid_name(name: str) -> bool:
    return re.fullmatch(r"nvme\dn\d|sd\w|disk\d", name)

class IOStat:
    def __init__(self):
        self._stats = {}
        self._time = None

        self.keys = []
        self.stats = {}


    def setup(self):
        self._update()
        self.keys = self._stats.keys()

    def update(self):
        old_stats, old_time = self._stats, self._time
        self._update()
        new_stats, new_time = self._stats, self._time
        timediff_ms = (new_time - old_time) * 1000

        keys = set(old_stats.keys()) & set(new_stats.keys())
        self.stats = {
            key: make_device_iostats(old_stats[key], new_stats[key], timediff_ms) for key in keys
        }

    def _update(self):
        self._stats = {k: v for k, v in psutil.disk_io_counters(True).items() if is_valid_name(k)}
        self._time = time.time()
